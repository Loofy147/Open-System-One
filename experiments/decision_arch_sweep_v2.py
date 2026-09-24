from __future__ import annotations
import json, math, torch
from open_system_one.lab.architectures_ext import ARCHITECTURES_EXT, ExtConfig

def masked_softmax(logits,mask):
    return torch.softmax(logits.masked_fill(~mask,torch.finfo(logits.dtype).min),-1)

def make_batch(n,k,dim,seed,task,interaction=0.0):
    g=torch.Generator().manual_seed(seed); q=torch.randn(n,dim,generator=g); c=torch.randn(n,k,dim,generator=g)
    base=(q[:,None]*c).sum(-1)/math.sqrt(dim); centroid=c.mean(1)
    if task=="independent": logits=base
    elif task=="global":
        ctx=(c*centroid[:,None]).sum(-1)/math.sqrt(dim); logits=base+interaction*ctx
    elif task=="competitive":
        sims=torch.matmul(c,c.transpose(1,2))/math.sqrt(dim); eye=torch.eye(k,dtype=torch.bool)[None]
        competition=sims.masked_fill(eye,-1e9).max(-1).values; logits=base-interaction*competition
    elif task=="contrastive":
        other=(c.sum(1,keepdim=True)-c)/max(k-1,1); contrast=(c*(q[:,None]-other)).sum(-1)/math.sqrt(dim); logits=base+interaction*contrast
    else: raise ValueError(task)
    return q,c,torch.softmax(logits,-1)

def ece(p,target,bins=10):
    conf,pred=p.max(-1); true=target.argmax(-1); correct=(pred==true).float(); total=0.0
    for i in range(bins):
        lo,hi=i/bins,(i+1)/bins; sel=(conf>lo)&(conf<=hi)
        if sel.any(): total+=float(sel.float().mean())*abs(float(conf[sel].mean())-float(correct[sel].mean()))
    return total

def train_one(name,task,k,interaction,seed,steps=50,n_train=256,n_test=128):
    torch.manual_seed(seed); m=ARCHITECTURES_EXT[name](ExtConfig()); opt=torch.optim.AdamW(m.parameters(),lr=3e-3,weight_decay=1e-4)
    tq=make_batch(n_train,k,m.cfg.dim if hasattr(m,"cfg") else 12,seed+1000,task,interaction); te=make_batch(n_test,k,12,seed+3000,task,interaction)
    m.train()
    for _ in range(steps):
        q,c,target=tq; mask=torch.ones(target.shape,dtype=torch.bool); p=masked_softmax(m(q,c,mask),mask)
        loss=-(target*p.clamp_min(1e-8).log()).sum(-1).mean(); opt.zero_grad(); loss.backward(); opt.step()
    m.eval()
    with torch.no_grad():
        q,c,target=te; mask=torch.ones(target.shape,dtype=torch.bool); p=masked_softmax(m(q,c,mask),mask)
        return {"model":name,"task":task,"k":k,"interaction":interaction,"seed":seed,"accuracy":float((p.argmax(-1)==target.argmax(-1)).float().mean()),"nll":float(-(target*p.clamp_min(1e-8).log()).sum(-1).mean()),"brier":float(((p-target)**2).sum(-1).mean()),"ece":ece(p,target),"params":sum(x.numel() for x in m.parameters())}

if __name__=="__main__":
    rows=[]
    for task,interaction in [("independent",0.0),("global",1.0),("global",2.0),("competitive",1.0),("contrastive",1.0)]:
        for k in (2,8,16):
            for seed in (1,2,3):
                for name in ARCHITECTURES_EXT: rows.append(train_one(name,task,k,interaction,seed))
    print(json.dumps(rows,indent=2))
