from __future__ import annotations
from dataclasses import dataclass
import torch
from torch import nn

@dataclass(frozen=True)
class ExtConfig:
    dim:int=12
    hidden:int=32
    heads:int=3
    layers:int=1

class Pairwise(nn.Module):
    sees_others=False
    order_equivariant=True
    def __init__(self,cfg):
        super().__init__()
        self.net=nn.Sequential(nn.Linear(cfg.dim*3,cfg.hidden),nn.GELU(),nn.Linear(cfg.hidden,1))
    def forward(self,q,c,mask=None):
        qx=q[:,None,:].expand_as(c)
        return self.net(torch.cat([qx,c,qx*c],-1)).squeeze(-1)

class DeepSets(nn.Module):
    sees_others=True
    order_equivariant=True
    def __init__(self,cfg):
        super().__init__()
        self.phi=nn.Sequential(nn.Linear(cfg.dim,cfg.hidden),nn.GELU(),nn.Linear(cfg.hidden,cfg.dim))
        self.rho=nn.Sequential(nn.Linear(cfg.dim*3,cfg.hidden),nn.GELU(),nn.Linear(cfg.hidden,cfg.dim))
        self.score=nn.Sequential(nn.Linear(cfg.dim*4,cfg.hidden),nn.GELU(),nn.Linear(cfg.hidden,1))
    def forward(self,q,c,mask=None):
        if mask is None: mask=torch.ones(c.shape[:2],dtype=torch.bool,device=c.device)
        h=self.phi(c); cnt=mask.sum(1,keepdim=True).clamp_min(1).to(h.dtype)
        pooled=h.masked_fill(~mask[...,None],0).sum(1)/cnt
        summary=self.rho(torch.cat([pooled,q,pooled*q],-1))
        qq=q[:,None,:].expand_as(h); ss=summary[:,None,:].expand_as(h)
        return self.score(torch.cat([qq,c,h,ss],-1)).squeeze(-1)

class SetTransformer(nn.Module):
    sees_others=True
    order_equivariant=True
    def __init__(self,cfg):
        super().__init__()
        layer=nn.TransformerEncoderLayer(d_model=cfg.dim,nhead=cfg.heads,dim_feedforward=cfg.hidden*2,dropout=0.0,batch_first=True,norm_first=True,activation="gelu")
        self.enc=nn.TransformerEncoder(layer,cfg.layers,enable_nested_tensor=False)
        self.score=nn.Sequential(nn.Linear(cfg.dim*4,cfg.hidden),nn.GELU(),nn.Linear(cfg.hidden,1))
        self.q_proj=nn.Linear(cfg.dim,cfg.dim)
    def forward(self,q,c,mask=None):
        if mask is None: mask=torch.ones(c.shape[:2],dtype=torch.bool,device=c.device)
        h=self.enc(c+self.q_proj(q)[:,None,:],src_key_padding_mask=~mask.bool())
        cnt=mask.sum(1,keepdim=True).clamp_min(1).to(h.dtype)
        pooled=h.masked_fill(~mask[...,None],0).sum(1)/cnt
        qq=self.q_proj(q)[:,None,:].expand_as(h); pp=pooled[:,None,:].expand_as(h)
        return self.score(torch.cat([qq,c,h,pp],-1)).squeeze(-1)

class Relational(nn.Module):
    sees_others=True
    order_equivariant=True
    def __init__(self,cfg):
        super().__init__()
        self.q=nn.Linear(cfg.dim,cfg.dim,bias=False); self.k=nn.Linear(cfg.dim,cfg.dim,bias=False)
        self.v=nn.Linear(cfg.dim,cfg.dim,bias=False); self.out=nn.Linear(cfg.dim,cfg.dim)
        self.score=nn.Sequential(nn.Linear(cfg.dim*4,cfg.hidden),nn.GELU(),nn.Linear(cfg.hidden,1))
    def forward(self,q,c,mask=None):
        if mask is None: mask=torch.ones(c.shape[:2],dtype=torch.bool,device=c.device)
        Q,K,V=self.q(c),self.k(c),self.v(c)
        att=torch.matmul(Q,K.transpose(-1,-2))/(c.shape[-1]**0.5)
        att=att.masked_fill(~mask[:,None,:],torch.finfo(att.dtype).min)
        ctx=self.out(torch.matmul(torch.softmax(att,-1),V))
        qq=q[:,None,:].expand_as(c)
        return self.score(torch.cat([qq,c,ctx,c*ctx],-1)).squeeze(-1)

class ConditionalMixture(nn.Module):
    sees_others=True
    order_equivariant=True
    def __init__(self,cfg):
        super().__init__()
        self.base=nn.Sequential(nn.Linear(cfg.dim*3,cfg.hidden),nn.GELU(),nn.Linear(cfg.hidden,1))
        self.phi=nn.Sequential(nn.Linear(cfg.dim,cfg.hidden),nn.GELU(),nn.Linear(cfg.hidden,cfg.dim))
        self.rel=nn.Sequential(nn.Linear(cfg.dim*4,cfg.hidden),nn.GELU(),nn.Linear(cfg.hidden,1))
        self.gate=nn.Sequential(nn.Linear(cfg.dim*2,cfg.hidden),nn.GELU(),nn.Linear(cfg.hidden,1),nn.Sigmoid())
    def forward(self,q,c,mask=None):
        if mask is None: mask=torch.ones(c.shape[:2],dtype=torch.bool,device=c.device)
        qx=q[:,None,:].expand_as(c)
        base=self.base(torch.cat([qx,c,qx*c],-1)).squeeze(-1)
        h=self.phi(c); cnt=mask.sum(1,keepdim=True).clamp_min(1).to(h.dtype)
        pooled=h.masked_fill(~mask[...,None],0).sum(1)/cnt; pp=pooled[:,None,:].expand_as(h)
        rel=self.rel(torch.cat([qx,c,h,pp],-1)).squeeze(-1)
        gate=self.gate(torch.cat([q,pooled],-1)).expand_as(base)
        return (1-gate)*base+gate*rel

ARCHITECTURES_EXT={"pairwise":Pairwise,"deepsets":DeepSets,"set_transformer":SetTransformer,"relational":Relational,"conditional_mixture":ConditionalMixture}
