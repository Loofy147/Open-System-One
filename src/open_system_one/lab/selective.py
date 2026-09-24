from __future__ import annotations
from dataclasses import dataclass
import torch

@dataclass(frozen=True)
class ConformalCalibration:
    alpha:float
    qhat:float
    n:int

def fit_temperature(logits:torch.Tensor,labels:torch.Tensor)->float:
    logits=logits.detach().float(); labels=labels.detach().long()
    if logits.ndim!=2 or labels.ndim!=1 or logits.shape[0]!=labels.shape[0] or logits.shape[0]<2:
        raise ValueError("logits must be [N,K] and labels [N] with N>=2")
    if not torch.isfinite(logits).all(): raise ValueError("logits must be finite")
    raw=torch.tensor(1.0,dtype=logits.dtype,requires_grad=True)
    opt=torch.optim.LBFGS([raw],max_iter=50,line_search_fn="strong_wolfe")
    def closure():
        opt.zero_grad(); t=raw.clamp_min(0.05)
        loss=torch.nn.functional.cross_entropy(logits/t,labels); loss.backward(); return loss
    opt.step(closure); return float(raw.detach().clamp(0.05,20.0))

def _conformal_quantile(values:torch.Tensor,alpha:float)->float:
    if not 0<alpha<1: raise ValueError("alpha must be in (0,1)")
    x=torch.sort(values.detach().float()).values; n=x.numel()
    if n==0: raise ValueError("at least one calibration value required")
    rank=min(n-1,max(0,int(torch.ceil(torch.tensor((n+1)*(1-alpha))).item())-1))
    return float(x[rank])

def fit_split_conformal(probs:torch.Tensor,labels:torch.Tensor,alpha:float=0.1)->ConformalCalibration:
    probs=probs.detach().float(); labels=labels.detach().long()
    if probs.ndim!=2 or labels.ndim!=1 or probs.shape[0]!=labels.shape[0]: raise ValueError("probs must be [N,K] and labels [N]")
    if not torch.isfinite(probs).all() or (probs<0).any() or (probs.sum(-1)<=0).any(): raise ValueError("invalid probability input")
    p=probs/probs.sum(-1,keepdim=True)
    if labels.min()<0 or labels.max()>=p.shape[1]: raise ValueError("label outside probability support")
    nonconformity=1.0-p[torch.arange(p.shape[0]),labels]
    return ConformalCalibration(alpha,_conformal_quantile(nonconformity,alpha),p.shape[0])

def predict_set(probs:torch.Tensor,cal:ConformalCalibration)->torch.Tensor:
    probs=probs.detach().float()
    if probs.ndim!=2: raise ValueError("probs must be [N,K]")
    return probs >= (1.0-cal.qhat)

def coverage(set_mask:torch.Tensor,labels:torch.Tensor)->float:
    labels=labels.long()
    if set_mask.ndim!=2 or labels.ndim!=1 or set_mask.shape[0]!=labels.shape[0]: raise ValueError("set_mask must be [N,K] and labels [N]")
    return float(set_mask[torch.arange(labels.shape[0]),labels].float().mean())

def mean_set_size(set_mask:torch.Tensor)->float: return float(set_mask.float().sum(-1).mean())

def abstain_rate(set_mask:torch.Tensor)->float:
    sizes=set_mask.sum(-1)
    return float((sizes!=1).float().mean())
