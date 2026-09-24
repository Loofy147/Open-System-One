from __future__ import annotations
import json, torch
from open_system_one.lab.architectures import ARCHITECTURES, ArchConfig, masked_softmax
from open_system_one.lab.synthetic import make_dataset, permute

def ece(probs,target,bins=10):
    conf,pred=probs.max(-1); true=target.argmax(-1); correct=(pred==true).float(); total=0.0
    for lo in torch.linspace(0,1,bins+1)[:-1]:
        hi=lo+1/bins; sel=(conf>lo)&(conf<=hi)
        if sel.any(): total += float(sel.float().mean())*abs(float(conf[sel].mean())-float(correct[sel].mean()))
    return total

def fit_temperature(logits,target):
    t=torch.tensor(1.0,requires_grad=True)
    opt=torch.optim.LBFGS([t],max_iter=30,line_search_fn="strong_wolfe")
    def closure():
        opt.zero_grad()
        loss=-(target*torch.log_softmax(logits/t.clamp_min(0.05),-1)).sum(-1).mean()
        loss.backward(); return loss
    opt.step(closure); return float(t.detach().clamp(0.05,10.0))

def train(name,train_batch,valid_batch,test_batch,steps=250):
    torch.manual_seed(7); model=ARCHITECTURES[name](ArchConfig())
    opt=torch.optim.AdamW(model.parameters(),lr=3e-3,weight_decay=1e-4)
    for _ in range(steps):
        p=masked_softmax(model(train_batch.query,train_batch.candidates,train_batch.mask),train_batch.mask)
        loss=-(train_batch.target*torch.log(p.clamp_min(1e-8))).sum(-1).mean()
        opt.zero_grad(); loss.backward(); opt.step()
    with torch.no_grad():
        val_logits=model(valid_batch.query,valid_batch.candidates,valid_batch.mask)
        test_logits=model(test_batch.query,test_batch.candidates,test_batch.mask)
        test_p=masked_softmax(test_logits,test_batch.mask); t=fit_temperature(val_logits.detach(),valid_batch.target.detach())
        cal_p=torch.softmax(test_logits/t,-1)
        perm=permute(test_batch,19); perm_p=masked_softmax(model(perm.query,perm.candidates,perm.mask),perm.mask)
        diffs=[]
        for i in range(test_batch.candidates.shape[0]):
            for j in range(test_batch.candidates.shape[1]):
                idx=(perm.candidates[i]==test_batch.candidates[i,j]).all(-1).nonzero().item()
                diffs.append(abs(float(perm_p[i,idx]-test_p[i,j])))
        return {"model":name,"accuracy":float((test_p.argmax(-1)==test_batch.target.argmax(-1)).float().mean()),"nll":float(-(test_batch.target*torch.log(test_p.clamp_min(1e-8))).sum(-1).mean()),"brier":float(((test_p-test_batch.target)**2).sum(-1).mean()),"ece":ece(test_p,test_batch.target),"calibrated_nll":float(-(test_batch.target*torch.log(cal_p.clamp_min(1e-8))).sum(-1).mean()),"calibrated_brier":float(((cal_p-test_batch.target)**2).sum(-1).mean()),"calibrated_ece":ece(cal_p,test_batch.target),"temperature":t,"permutation_max_abs_error":max(diffs),"parameter_count":sum(p.numel() for p in model.parameters())}

def main():
    train_batch=make_dataset(2048,6,12,100); valid_batch=make_dataset(512,6,12,200); test_batch=make_dataset(512,6,12,300)
    print(json.dumps([train(name,train_batch,valid_batch,test_batch) for name in ARCHITECTURES],indent=2))

if __name__=="__main__": main()
