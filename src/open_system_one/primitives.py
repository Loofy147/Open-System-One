from __future__ import annotations
from dataclasses import dataclass, field
from functools import wraps
import hashlib, json, threading
from typing import Any, Callable, Generic, Iterable, Mapping, TypeVar

T=TypeVar("T"); U=TypeVar("U")

@dataclass(frozen=True)
class ReifiedContinuation(Generic[T,U]):
    value:T
    resume:Callable[[T],U]
    def continue_(self,value:T)->U: return self.resume(value)

def reify(value:T,resume:Callable[[T],U])->ReifiedContinuation[T,U]:
    return ReifiedContinuation(value=value,resume=resume)

def compose(*steps:Callable[[Any],Any])->Callable[[Any],Any]:
    if not steps: return lambda x:x
    def run(value:Any)->Any:
        for step in steps: value=step(value)
        return value
    return run

class UnificationError(ValueError): pass

def unify(left:Any,right:Any,env:Mapping[str,Any]|None=None)->dict[str,Any]:
    out=dict(env or {})
    def walk(term):
        while isinstance(term,str) and term.startswith("?") and term in out and out[term]!=term: term=out[term]
        return term
    def occurs(var,term):
        term=walk(term)
        if term==var: return True
        if isinstance(term,(list,tuple)): return any(occurs(var,x) for x in term)
        if isinstance(term,dict): return any(occurs(var,v) for v in term.values())
        return False
    def go(a,b):
        a,b=walk(a),walk(b)
        if a==b:return
        if isinstance(a,str) and a.startswith("?"):
            if occurs(a,b): raise UnificationError(f"occurs check failed for {a}")
            out[a]=b; return
        if isinstance(b,str) and b.startswith("?"):
            if occurs(b,a): raise UnificationError(f"occurs check failed for {b}")
            out[b]=a; return
        if isinstance(a,(list,tuple)) and isinstance(b,(list,tuple)) and len(a)==len(b):
            for x,y in zip(a,b): go(x,y)
            return
        if isinstance(a,dict) and isinstance(b,dict) and set(a)==set(b):
            for key in a: go(a[key],b[key])
            return
        raise UnificationError(f"cannot unify {a!r} with {b!r}")
    go(left,right); return out

@dataclass(frozen=True)
class Continuation:
    fn:Callable[[Any],Any]
    def invoke(self,value:Any)->Any:return self.fn(value)

@dataclass
class ControlState:
    value:Any
    continuation:Continuation|None=None
    done:bool=False
    def step(self)->Any:
        if self.done or self.continuation is None: self.done=True; return self.value
        cont=self.continuation; self.continuation=None; self.value=cont.invoke(self.value); self.done=True; return self.value

def memoize(fn:Callable[...,T])->Callable[...,T]:
    cache:dict[str,T]={}; lock=threading.RLock()
    @wraps(fn)
    def wrapped(*args,**kwargs):
        key=content_id((args,kwargs))
        with lock:
            if key in cache:return cache[key]
        value=fn(*args,**kwargs)
        with lock:
            cache.setdefault(key,value); return cache[key]
    wrapped.cache=cache
    return wrapped

@dataclass
class BloomPrefilter:
    size:int=256
    hashes:int=3
    bits:int=0
    def _positions(self,value:Any)->list[int]:
        raw=canonical_bytes(value)
        return [int.from_bytes(hashlib.sha256(bytes([i])+raw).digest()[:8],"big")%self.size for i in range(self.hashes)]
    def add(self,value:Any)->None:
        for pos in self._positions(value): self.bits|=1<<pos
    def maybe_contains(self,value:Any)->bool:
        return all((self.bits>>pos)&1 for pos in self._positions(value))

def fold_monoid(values:Iterable[T],combine:Callable[[T,T],T],identity:T)->T:
    result=identity
    for value in values: result=combine(result,value)
    return result

@dataclass
class LamportClock:
    value:int=0
    def tick(self)->int:self.value+=1;return self.value
    def receive(self,remote:int)->int:
        if remote<0:raise ValueError("remote clock cannot be negative")
        self.value=max(self.value,int(remote))+1;return self.value

def canonical_bytes(value:Any)->bytes:
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(",",":"),default=str).encode("utf-8")

def content_id(value:Any,algorithm:str="sha256")->str:
    if algorithm!="sha256":raise ValueError("only sha256 is currently supported")
    return hashlib.sha256(canonical_bytes(value)).hexdigest()

@dataclass(frozen=True)
class Capability:
    subject:str
    operation:str
    resource:str
    nonce:str

@dataclass
class CapabilityIssuer:
    secret:bytes
    def issue(self,subject:str,operation:str,resource:str)->Capability:
        unsigned={"subject":subject,"operation":operation,"resource":resource}
        nonce=hashlib.sha256(self.secret+canonical_bytes(unsigned)).hexdigest()[:24]
        return Capability(subject,operation,resource,nonce)
    def verify(self,capability:Capability,subject:str,operation:str,resource:str)->bool:
        return capability==self.issue(subject,operation,resource)

@dataclass(frozen=True)
class GSet(Generic[T]):
    values:frozenset[T]=frozenset()
    def add(self,value:T)->"GSet[T]":return GSet(self.values|{value})
    def merge(self,other:"GSet[T]")->"GSet[T]":return GSet(self.values|other.values)

def candidate_scores(query:Iterable[float],candidates:Mapping[str,Iterable[float]])->dict[str,float]:
    q=[float(x) for x in query]; qn=sum(x*x for x in q)**0.5
    if qn==0:return {name:0.0 for name in candidates}
    out={}
    for name,vector in candidates.items():
        v=[float(x) for x in vector]
        if len(v)!=len(q):raise ValueError(f"candidate {name!r} dimension mismatch")
        vn=sum(x*x for x in v)**0.5
        out[name]=0.0 if vn==0 else sum(a*b for a,b in zip(q,v))/(qn*vn)
    return out

@dataclass(frozen=True)
class PrimitiveSpec:
    name:str
    relation:str
    implementation:str
    failure_mode:str

PRIMITIVES=(
PrimitiveSpec("reification","computation -> data","ReifiedContinuation","stale/invalid continuation"),
PrimitiveSpec("composition","stage -> stage","compose","non-total stage"),
PrimitiveSpec("unification","structure -> compatible substitution","unify","conflict/occurs-check"),
PrimitiveSpec("explicit_control","state -> next state","Continuation/ControlState","non-terminating continuation"),
PrimitiveSpec("memoization","input -> reusable result","memoize","stale/non-deterministic cache"),
PrimitiveSpec("approximate_prefilter","query -> candidate gate","BloomPrefilter","false positive"),
PrimitiveSpec("associative_accumulation","items -> aggregate","fold_monoid","non-associative combine"),
PrimitiveSpec("causal_order","event -> logical order","LamportClock","clock misuse"),
PrimitiveSpec("content_identity","artifact -> stable identity","content_id","canonicalization drift"),
PrimitiveSpec("capability","authority -> action","CapabilityIssuer","forged/stale authority"),
PrimitiveSpec("convergent_merge","state + state -> converged state","GSet","non-monotone mutation"),
PrimitiveSpec("dynamic_scoring","query + candidates -> scores","candidate_scores","candidate representation mismatch"),
)
