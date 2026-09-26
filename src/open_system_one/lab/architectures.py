from __future__ import annotations
from dataclasses import dataclass
import torch
from torch import nn

@dataclass(frozen=True)
class ArchConfig:
    dim:int=12
    hidden:int=32
    heads:int=4
    layers:int=1

class PairwiseScorer(nn.Module):
    order_invariant=True
    sees_other_candidates=False
    def __init__(self,cfg:ArchConfig):
        super().__init__()
        self.score=nn.Sequential(nn.Linear(cfg.dim*3,cfg.hidden),nn.GELU(),nn.Linear(cfg.hidden,1))
    def forward(self,query,candidates,mask=None):
        q=query[:,None,:].expand_as(candidates)
        return self.score(torch.cat([q,candidates,q*candidates],dim=-1)).squeeze(-1)

class MarkerSharedScorer(nn.Module):
    order_invariant=True
    sees_other_candidates=True
    def __init__(self,cfg:ArchConfig):
        super().__init__()
        enc=nn.TransformerEncoderLayer(d_model=cfg.dim,nhead=cfg.heads,dim_feedforward=cfg.hidden*2,dropout=0.0,batch_first=True,norm_first=True,activation="gelu")
        self.context=nn.TransformerEncoder(enc,num_layers=cfg.layers,enable_nested_tensor=False)
        self.q_proj=nn.Linear(cfg.dim,cfg.dim)
        self.score=nn.Sequential(nn.Linear(cfg.dim*3,cfg.hidden),nn.GELU(),nn.Linear(cfg.hidden,1))
    def forward(self,query,candidates,mask=None):
        if mask is None: mask=torch.ones(candidates.shape[:2],dtype=torch.bool,device=candidates.device)
        key_padding=None if mask is None else ~mask.bool()
        q_base=self.q_proj(query)
        contextual=self.context(candidates+q_base[:,None,:],src_key_padding_mask=key_padding)
        count=mask.sum(1,keepdim=True).clamp_min(1).to(contextual.dtype)
        pooled=contextual.masked_fill(~mask[...,None],0.0).sum(1)/count
        q=q_base[:,None,:].expand_as(contextual); pooled=pooled[:,None,:].expand_as(contextual)
        return self.score(torch.cat([q,contextual,pooled],dim=-1)).squeeze(-1)

class SetAwareScorer(nn.Module):
    order_invariant=True
    sees_other_candidates=True
    def __init__(self,cfg:ArchConfig):
        super().__init__()
        self.phi=nn.Sequential(nn.Linear(cfg.dim,cfg.hidden),nn.GELU(),nn.Linear(cfg.hidden,cfg.dim))
        self.score=nn.Sequential(nn.Linear(cfg.dim*4,cfg.hidden),nn.GELU(),nn.Linear(cfg.hidden,1))
    def forward(self,query,candidates,mask=None):
        if mask is None: mask=torch.ones(candidates.shape[:2],dtype=torch.bool,device=candidates.device)
        h=self.phi(candidates)
        count=mask.sum(1,keepdim=True).clamp_min(1).to(h.dtype)
        pooled=h.masked_fill(~mask[...,None],0.0).sum(1)/count
        pooled=pooled[:,None,:].expand_as(h); q=query[:,None,:].expand_as(h)
        return self.score(torch.cat([q,candidates,h,pooled],dim=-1)).squeeze(-1)

def masked_softmax(logits,mask):
    return torch.softmax(logits.masked_fill(~mask,torch.finfo(logits.dtype).min),dim=-1)

ARCHITECTURES={"pairwise":PairwiseScorer,"marker_shared":MarkerSharedScorer,"set_aware":SetAwareScorer}
