from __future__ import annotations
from dataclasses import dataclass
import torch

@dataclass
class Batch:
    query: torch.Tensor
    candidates: torch.Tensor
    target: torch.Tensor
    mask: torch.Tensor

def make_dataset(n:int,k:int,dim:int,seed:int,interaction:float=1.25)->Batch:
    g=torch.Generator().manual_seed(seed)
    query=torch.randn(n,dim,generator=g)
    candidates=torch.randn(n,k,dim,generator=g)
    base=(query[:,None,:]*candidates).sum(-1)/dim**0.5
    centroid=candidates.mean(1)
    context=(candidates*centroid[:,None,:]).sum(-1)/dim**0.5
    logits=base+interaction*context
    target=torch.softmax(logits,dim=-1)
    mask=torch.ones(n,k,dtype=torch.bool)
    return Batch(query,candidates,target,mask)

def permute(batch:Batch,seed:int)->Batch:
    g=torch.Generator().manual_seed(seed)
    perm=torch.randperm(batch.candidates.shape[1],generator=g)
    return Batch(batch.query,batch.candidates[:,perm],batch.target[:,perm],batch.mask[:,perm])
