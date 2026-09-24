from __future__ import annotations
import json, statistics, torch
from open_system_one.lab.architectures import ARCHITECTURES, ArchConfig, masked_softmax
from open_system_one.lab.synthetic import make_dataset

def run_one(name,k,interaction,seed,steps=80):
    torch.manual_seed(seed)
    train=make_dataset(1024,k,12,1000+seed,interaction)
    test=make_dataset(256,k,12,3000+seed,interaction)
    model=ARCHITECTURES[name](ArchConfig())
    opt=torch.optim.AdamW(model.parameters(),lr=3e-3,weight_decay=1e-4)
    for _ in range(steps):
        p=masked_softmax(model(train.query,train.candidates,train.mask),train.mask)
        loss=-(train.target*torch.log(p.clamp_min(1e-8))).sum(-1).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    with torch.no_grad():
        p=masked_softmax(model(test.query,test.candidates,test.mask),test.mask)
        return {"accuracy":float((p.argmax(-1)==test.target.argmax(-1)).float().mean()),"brier":float(((p-test.target)**2).sum(-1).mean()),"nll":float(-(test.target*torch.log(p.clamp_min(1e-8))).sum(-1).mean()),"params":sum(x.numel() for x in model.parameters())}

def main():
    rows=[]
    for interaction in (0.0,1.25):
        for k in (2,8,16):
            for name in ARCHITECTURES:
                vals=[run_one(name,k,interaction,seed) for seed in (7,)]
                rows.append({"model":name,"k":k,"interaction":interaction,"accuracy_mean":statistics.mean(v["accuracy"] for v in vals),"accuracy_sd":0.0,"brier_mean":statistics.mean(v["brier"] for v in vals),"nll_mean":statistics.mean(v["nll"] for v in vals),"params":vals[0]["params"]})
    print(json.dumps(rows,indent=2))

if __name__=="__main__": main()
