from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from ..schema import ChoiceQuestion, NoulQuestion, ScoreQuestion

@dataclass
class CausalConfig:
    model_id:str
    device:str="auto"
    dtype:str="auto"
    max_length:int=4096

class CausalLogitBackend:
    name="causal-logit"
    def __init__(self,config:CausalConfig):
        try:
            import torch
            from transformers import AutoModelForCausalLM,AutoTokenizer
        except ImportError as exc:
            raise RuntimeError("install open-system-one[inference]") from exc
        self.torch=torch; self.cfg=config
        self.tokenizer=AutoTokenizer.from_pretrained(config.model_id,use_fast=True)
        if self.tokenizer.pad_token_id is None: self.tokenizer.pad_token=self.tokenizer.eos_token
        dtype=None if config.dtype=="auto" else getattr(torch,config.dtype)
        self.model=AutoModelForCausalLM.from_pretrained(config.model_id,torch_dtype=dtype,device_map=config.device)
        self.model.eval()
    def _choice_tokens(self,question:Any)->list[int]:
        if isinstance(question,NoulQuestion): codes=["A","B"]
        elif isinstance(question,ChoiceQuestion): codes=[chr(65+i) for i in range(len(question.criteria))]
        elif isinstance(question,ScoreQuestion): codes=[str(i) for i in range(len(question.criteria))]
        else: raise TypeError(type(question).__name__)
        ids=[]
        for code in codes:
            toks=self.tokenizer.encode(code,add_special_tokens=False)
            if len(toks)!=1: raise ValueError(f"answer code {code!r} is not a single tokenizer token")
            ids.append(toks[0])
        return ids
    def _prompt(self,state:str,question:Any)->str:
        if isinstance(question,NoulQuestion):
            options=[("A","true"),("B","false")]
        elif isinstance(question,ChoiceQuestion):
            options=[(chr(65+i),f"{k}: {v if v is not None else ''}") for i,(k,v) in enumerate(question.criteria.items())]
        elif isinstance(question,ScoreQuestion):
            options=[(str(i),text) for i,text in enumerate(question.criteria)]
        else: raise TypeError(type(question).__name__)
        lines=["State:",state,"","Question:",str(question.instructions),"","Allowed answers:"]
        lines.extend(f"{code}: {desc}" for code,desc in options); lines.append("Answer code:")
        return "\n".join(lines)
    def evaluate_batch(self,state:Any,questions:dict[str,Any])->dict[str,list[float]]:
        from ..engine import state_to_text
        state_text=state_to_text(state)
        prompts=[self._prompt(state_text,q) for q in questions.values()]
        enc=self.tokenizer(prompts,return_tensors="pt",padding=True,truncation=True,max_length=self.cfg.max_length)
        device=self.model.device; enc={k:v.to(device) for k,v in enc.items()}
        with self.torch.inference_mode(): logits=self.model(**enc).logits.float()
        lengths=enc["attention_mask"].sum(dim=1).tolist(); out={}
        for row,(qid,question) in enumerate(questions.items()):
            token_ids=self._choice_tokens(question)
            selected=logits[row,int(lengths[row])-1,token_ids]
            out[qid]=self.torch.softmax(selected,dim=-1).tolist()
        return out
