from __future__ import annotations
import torch

def cosine_shortlist(query:torch.Tensor,candidates:torch.Tensor,k:int)->torch.Tensor:
    if query.ndim!=2 or candidates.ndim!=3 or query.shape[0]!=candidates.shape[0] or query.shape[1]!=candidates.shape[2]:
        raise ValueError("query [B,D], candidates [B,N,D] required")
    n=candidates.shape[1]
    if isinstance(k,bool) or not isinstance(k,int) or not 1<=k<=n:
        raise ValueError("k must be an integer in [1,N]")
    q=torch.nn.functional.normalize(query.float(),dim=-1); c=torch.nn.functional.normalize(candidates.float(),dim=-1)
    return torch.einsum("bd,bnd->bn",q,c).topk(k,dim=-1,largest=True,sorted=True).indices

def recall_at_k(indices:torch.Tensor,target:torch.Tensor)->float:
    if indices.ndim!=2 or target.ndim!=2 or indices.shape[0]!=target.shape[0]:
        raise ValueError("indices and target must both be [B,*]")
    hit=(indices[:,:,None]==target[:,None,:]).any(-1)
    return float(hit.any(-1).float().mean())
