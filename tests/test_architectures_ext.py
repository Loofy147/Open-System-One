import torch
from open_system_one.lab.architectures_ext import ARCHITECTURES_EXT,ExtConfig

def sm(m,q,c,mask): return torch.softmax(m(q,c,mask).masked_fill(~mask,torch.finfo(torch.float32).min),-1)

def test_extended_architectures_are_closed_and_finite():
    torch.manual_seed(1); q=torch.randn(4,12); c=torch.randn(4,8,12); mask=torch.ones(4,8,dtype=torch.bool)
    for name,cls in ARCHITECTURES_EXT.items():
        torch.manual_seed(2); p=sm(cls(ExtConfig()),q,c,mask); assert torch.isfinite(p).all() and torch.allclose(p.sum(-1),torch.ones(4),atol=1e-6)

def test_extended_architectures_are_permutation_equivariant():
    torch.manual_seed(3); q=torch.randn(3,8); c=torch.randn(3,7,8); mask=torch.ones(3,7,dtype=torch.bool); perm=torch.tensor([3,6,0,2,5,1,4])
    for name,cls in ARCHITECTURES_EXT.items():
        torch.manual_seed(4); m=cls(ExtConfig(dim=8,hidden=24,heads=2)); a=sm(m,q,c,mask); b=sm(m,q,c[:,perm],mask[:,perm]); inv=torch.empty_like(perm); inv[perm]=torch.arange(len(perm))
        assert torch.allclose(b[:,inv],a,atol=1e-5),name

def test_pairwise_is_context_blind_but_other_models_are_not():
    torch.manual_seed(5); q=torch.randn(1,8); c=torch.randn(1,5,8); c2=c.clone(); c2[:,0]+=0.75; mask=torch.ones(1,5,dtype=torch.bool)
    model=ARCHITECTURES_EXT["pairwise"](ExtConfig(dim=8,hidden=24)); x=model(q,c,mask); y=model(q,c2,mask); assert torch.allclose(x[:,1:],y[:,1:])
    for name in ("deepsets","set_transformer","relational","conditional_mixture"):
        model=ARCHITECTURES_EXT[name](ExtConfig(dim=8,hidden=24,heads=2)); assert not torch.allclose(model(q,c,mask)[:,1:],model(q,c2,mask)[:,1:]),name

def test_masked_candidates_do_not_change_valid_scores():
    torch.manual_seed(6); q=torch.randn(2,8); c=torch.randn(2,4,8); m=torch.ones(2,4,dtype=torch.bool); cp=torch.cat([c,torch.randn(2,3,8)],1); mp=torch.cat([m,torch.zeros(2,3,dtype=torch.bool)],1)
    for name,cls in ARCHITECTURES_EXT.items():
        model=cls(ExtConfig(dim=8,hidden=24,heads=2)); assert torch.allclose(sm(model,q,c,m),sm(model,q,cp,mp)[:,:4],atol=1e-5),name
