import torch
from open_system_one.lab.architectures import ARCHITECTURES,ArchConfig,masked_softmax
from open_system_one.lab.synthetic import make_dataset,permute

def test_all_architectures_produce_closed_distributions():
    b=make_dataset(8,5,12,1)
    for name,cls in ARCHITECTURES.items():
        torch.manual_seed(2); p=masked_softmax(cls(ArchConfig())(b.query,b.candidates,b.mask),b.mask)
        assert p.shape==(8,5) and torch.isfinite(p).all() and torch.allclose(p.sum(-1),torch.ones(8),atol=1e-6)

def test_candidate_permutation_is_semantically_equivariant():
    b=make_dataset(8,5,12,3); pb=permute(b,4)
    for name,cls in ARCHITECTURES.items():
        torch.manual_seed(5); m=cls(ArchConfig()); p=masked_softmax(m(b.query,b.candidates,b.mask),b.mask); pp=masked_softmax(m(pb.query,pb.candidates,pb.mask),pb.mask)
        for i in range(8):
            for j in range(5):
                idx=(pb.candidates[i]==b.candidates[i,j]).all(-1).nonzero().item()
                assert torch.allclose(pp[i,idx],p[i,j],atol=1e-5)

def test_pairwise_cannot_see_candidate_context():
    m=ARCHITECTURES["pairwise"](ArchConfig()); q=torch.randn(1,12); c=torch.randn(1,4,12); base=m(q,c); c2=c.clone(); c2[:,0]+=0.5; changed=m(q,c2); assert torch.allclose(base[:,1:],changed[:,1:])

def test_shared_context_models_can_see_candidate_context():
    q=torch.randn(1,12); c=torch.randn(1,4,12); c2=c.clone(); c2[:,0]+=0.5
    for name in ("marker_shared","set_aware"):
        torch.manual_seed(11); m=ARCHITECTURES[name](ArchConfig()); assert not torch.allclose(m(q,c)[:,1:],m(q,c2)[:,1:])

def test_masked_extra_candidates_do_not_change_valid_scores():
    torch.manual_seed(23); q=torch.randn(2,12); c=torch.randn(2,3,12); mask=torch.ones(2,3,dtype=torch.bool)
    cp=torch.cat([c,torch.randn(2,2,12)],1); mp=torch.tensor([[True,True,True,False,False],[True,True,True,False,False]])
    for name,cls in ARCHITECTURES.items():
        torch.manual_seed(24); m=cls(ArchConfig()); assert torch.allclose(m(q,c,mask),m(q,cp,mp)[:,:3],atol=1e-5)
