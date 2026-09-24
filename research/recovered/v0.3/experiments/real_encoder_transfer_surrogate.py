
import math, random, json, time
from dataclasses import dataclass
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

SEED=7
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
DEVICE='cpu'

# -------- text world: latent task encoded in natural-ish token strings --------
VOCAB = ['PAD','CLS','state','alpha','beta','gamma','delta','red','blue','green','high','low','pair','single','option','x','y','z']
V={t:i for i,t in enumerate(VOCAB)}

def enc_text(tokens, L=24):
    ids=[V['CLS']]+[V.get(t,V['x']) for t in tokens][:L-1]
    ids += [V['PAD']]*(L-len(ids))
    return ids, [1 if x!=V['PAD'] else 0 for x in ids]

# Interaction target: best option is NOT determined by candidate independently.
# option utilities contain a pair-interaction bonus when option colors match.
COLORS=['red','blue','green']

def make_example(k=8, interaction=1.25):
    state_color=random.choice(COLORS)
    opts=[]
    for i in range(k):
        color=random.choice(COLORS)
        base=random.uniform(-1,1)
        opts.append((color,base))
    vals=[]
    for color,base in opts:
        vals.append(base + (interaction if color==state_color else 0.0))
    y=int(np.argmax(vals))
    return state_color, opts, y

# -------- learned bidirectional encoder --------
class TinyEncoder(nn.Module):
    def __init__(self, d=48, layers=2, heads=4, max_len=24):
        super().__init__()
        self.config=type('Cfg',(),{'hidden_size':d})()
        self.emb=nn.Embedding(len(VOCAB),d,padding_idx=V['PAD'])
        self.pos=nn.Parameter(torch.randn(max_len,d)*0.02)
        layer=nn.TransformerEncoderLayer(d, heads, 4*d, dropout=0.0, batch_first=True, norm_first=True)
        self.tr=nn.TransformerEncoder(layer,layers)
        self.norm=nn.LayerNorm(d)
    def forward(self, ids, mask):
        x=self.emb(ids)+self.pos[:ids.shape[1]]
        x=self.tr(x,src_key_padding_mask=~mask.bool())
        return self.norm(x)

class Pairwise(nn.Module):
    def __init__(self,d):
        super().__init__(); self.sc=nn.Sequential(nn.Linear(2*d,d),nn.GELU(),nn.Linear(d,1))
    def forward(self,h,state_vec,option_vec,mask):
        q=state_vec[:,None,:].expand_as(option_vec)
        z=self.sc(torch.cat([q,option_vec],-1)).squeeze(-1); z=z.masked_fill(~mask,-1e9); return z

class SetAware(nn.Module):
    def __init__(self,d):
        super().__init__(); self.node=nn.Sequential(nn.Linear(3*d,d),nn.GELU(),nn.Linear(d,1)); self.mix=nn.Linear(d,d)
    def forward(self,h,state_vec,option_vec,mask):
        q=state_vec[:,None,:].expand_as(option_vec)
        pooled=(option_vec*mask[...,None]).sum(1)/mask.sum(1,keepdim=True).clamp_min(1)
        pooled=self.mix(pooled)[:,None,:].expand_as(option_vec)
        z=self.node(torch.cat([q,option_vec,pooled],-1)).squeeze(-1); z=z.masked_fill(~mask,-1e9); return z

class Marker(nn.Module):
    def __init__(self,d):
        super().__init__(); self.ctx=nn.TransformerEncoder(nn.TransformerEncoderLayer(d,4,4*d,dropout=0.0,batch_first=True,norm_first=True),1); self.sc=nn.Sequential(nn.Linear(d,d),nn.GELU(),nn.Linear(d,1))
    def forward(self,h,state_vec,option_vec,mask):
        x=torch.cat([state_vec[:,None,:],option_vec],1)
        x=self.ctx(x)
        z=self.sc(x[:,1:]).squeeze(-1); return z.masked_fill(~mask,-1e9)

class ConditionalMix(nn.Module):
    def __init__(self,d):
        super().__init__(); self.base=nn.Linear(2*d,d); self.rel=nn.Linear(2*d,d); self.out=nn.Linear(d,1)
    def forward(self,h,state_vec,option_vec,mask):
        q=state_vec[:,None,:].expand_as(option_vec)
        other=(option_vec*mask[...,None]).sum(1,keepdim=True)-option_vec
        n=(mask.sum(1,keepdim=True)-1).clamp_min(1).unsqueeze(-1)
        other=other/n
        z=torch.tanh(self.base(torch.cat([q,option_vec],-1))+self.rel(torch.cat([option_vec,other.expand_as(option_vec)],-1)))
        z=self.out(z).squeeze(-1); return z.masked_fill(~mask,-1e9)

def batch(examples):
    # state representation is first token CLS + mean of context; option vectors are
    # formed from the learned encoder using [state, option] passages, then scorer sees them.
    states=[]; options=[]; ys=[]
    for color,opts,y in examples:
        st,_=enc_text(['state',color,'option'])
        states.append(st)
        row=[]
        for c,b in opts:
            toks=['option',c,'high' if b>0 else 'low', 'pair']
            ids,_=enc_text(toks)
            row.append(ids)
        options.append(row); ys.append(y)
    ids_state=torch.tensor(states); mask_state=ids_state.ne(V['PAD'])
    ids_opt=torch.tensor(options); mask_opt=ids_opt.ne(V['PAD'])
    return ids_state,mask_state,ids_opt,mask_opt,torch.tensor(ys)

models={'pairwise':Pairwise(24),'marker':Marker(24),'set_aware':SetAware(24),'conditional':ConditionalMix(24)}
enc=TinyEncoder(d=24,layers=1,heads=4).to(DEVICE)
for m in models.values(): m.to(DEVICE)
params=list(enc.parameters())+sum([list(m.parameters()) for m in models.values()],[])
opt=torch.optim.AdamW(params,lr=3e-3)

# joint training, but each scorer has its own loss; shared encoder gradients are averaged by one summed loss.
for step in range(120):
    ex=[make_example(k=8,interaction=1.25) for _ in range(16)]
    ids_s,ms,ids_o,mo,y=batch(ex)
    hs=enc(ids_s,ms); ho=enc(ids_o.view(-1,ids_o.shape[-1]),mo.view(-1,mo.shape[-1]))
    d=hs.shape[-1]
    state_vec=hs[:,0]
    option_vec=ho[:,0].view(16,8,d)
    loss=0
    for name,m in models.items():
        z=m(None,state_vec,option_vec,torch.ones(16,8,dtype=torch.bool)); loss=loss+F.cross_entropy(z,y)
    opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(params,1.0); opt.step()

# evaluation on held-out seeds / interaction strengths
results=[]
for interaction in [0.0,1.25]:
    for k in [4,8,16]:
        rows={n:[] for n in models}
        for seed in [11,12,13]:
            random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
            ex=[make_example(k=k,interaction=interaction) for _ in range(64)]
            ids_s,ms,ids_o,mo,y=batch(ex)
            with torch.no_grad():
                hs=enc(ids_s,ms); ho=enc(ids_o.view(-1,ids_o.shape[-1]),mo.view(-1,mo.shape[-1]))
                state_vec=hs[:,0]; option_vec=ho[:,0].view(len(ex),k,-1); mask=torch.ones(len(ex),k,dtype=torch.bool)
                for n,m in models.items():
                    z=m(None,state_vec,option_vec,mask); p=z.softmax(-1); pred=p.argmax(-1); acc=(pred==y).float().mean().item(); brier=((p-F.one_hot(y,k).float())**2).mean().item()
                    rows[n].append((acc,brier))
        for n,v in rows.items():
            results.append({'interaction':interaction,'k':k,'scorer':n,'accuracy':float(np.mean([x[0] for x in v])),'brier':float(np.mean([x[1] for x in v]))})
print(json.dumps(results,indent=2))
Path='/mnt/data/open-system-one-realtransfer/results.json'
open(Path,'w').write(json.dumps(results,indent=2))
