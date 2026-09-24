from __future__ import annotations
from dataclasses import dataclass

def _require_torch():
    try:
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        return torch,nn,F
    except ImportError as exc:
        raise RuntimeError("install open-system-one[training]") from exc

@dataclass(frozen=True)
class PackedQuestion:
    question_id: str
    labels: list[str]
    input_texts: list[str]

def pack_question(state:str,question_id:str,instructions:str,options:list[tuple[str,str]])->PackedQuestion:
    texts=[f"State:\n{state}\n\nQuestion:\n{instructions}\n\nCandidate:\n{name}\n{description or ''}" for name,description in options]
    return PackedQuestion(question_id,[x[0] for x in options],texts)

class DecisionStudent:
    def __init__(self,model_id:str="answerdotai/ModernBERT-base",device:str="auto"):
        torch,nn,F=_require_torch()
        from transformers import AutoModel,AutoTokenizer
        self.torch,self.nn,self.F=torch,nn,F
        self.tokenizer=AutoTokenizer.from_pretrained(model_id)
        self.encoder=AutoModel.from_pretrained(model_id)
        self.head=nn.Linear(self.encoder.config.hidden_size,1)
        self.device=torch.device("cuda" if device=="auto" and torch.cuda.is_available() else "cpu") if device=="auto" else torch.device(device)
        self.encoder.to(self.device); self.head.to(self.device)
    def parameters(self): yield from self.encoder.parameters(); yield from self.head.parameters()
    def _pool(self,hidden,attention_mask):
        mask=attention_mask.unsqueeze(-1).to(hidden.dtype)
        return (hidden*mask).sum(1)/mask.sum(1).clamp_min(1.0)
    def score_rows(self,texts:list[str],max_length:int=512):
        batch=self.tokenizer(texts,return_tensors="pt",padding=True,truncation=True,max_length=max_length)
        batch={k:v.to(self.device) for k,v in batch.items()}
        out=self.encoder(**batch); pooled=self._pool(out.last_hidden_state,batch["attention_mask"])
        return self.head(pooled).squeeze(-1)
    def question_probabilities(self,packed:PackedQuestion,max_length:int=512):
        return self.torch.softmax(self.score_rows(packed.input_texts,max_length),dim=0)

def group_softmax(logits,group_sizes:list[int]):
    torch,_,_=_require_torch(); outputs=[]; pos=0
    for size in group_sizes: outputs.append(torch.softmax(logits[pos:pos+size],dim=0)); pos+=size
    if pos!=logits.numel(): raise ValueError("group_sizes do not sum to logits length")
    return outputs

def distillation_loss(predictions,targets,brier_weight:float=0.5):
    torch,_,F=_require_torch()
    if len(predictions)!=len(targets) or not predictions: raise ValueError("predictions and targets must be non-empty and aligned")
    losses=[]
    for p,t in zip(predictions,targets):
        p=p.clamp_min(1e-8); t=t/t.sum().clamp_min(1e-8)
        kl=F.kl_div(p.log(),t,reduction="sum"); brier=(p-t).pow(2).sum()
        losses.append((1.0-brier_weight)*kl+brier_weight*brier)
    return torch.stack(losses).mean()
