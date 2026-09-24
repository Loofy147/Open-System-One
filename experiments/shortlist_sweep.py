import json, torch
from open_system_one.lab.shortlist import cosine_shortlist

def run(seed,n=256,N=128,dim=32,ks=(4,8,16,32)):
    g=torch.Generator().manual_seed(seed); q=torch.randn(n,dim,generator=g); c=torch.randn(n,N,dim,generator=g)
    oracle=(q[:,None]*c).sum(-1); true=oracle.argmax(-1); rows=[]
    for k in ks:
        idx=cosine_shortlist(q,c,k); hit=(idx==true[:,None]).any(-1)
        rows.append({"k":k,"recall_top1":float(hit.float().mean()),"candidate_fraction":k/N})
    rows.append({"k":N,"recall_top1":1.0,"candidate_fraction":1.0})
    return {"seed":seed,"N":N,"dim":dim,"rows":rows}

if __name__=="__main__": print(json.dumps([run(s) for s in (1,2,3)],indent=2))
