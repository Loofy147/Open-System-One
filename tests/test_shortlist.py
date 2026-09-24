import torch
from open_system_one.lab.shortlist import cosine_shortlist,recall_at_k

def test_shortlist_is_deterministic_and_contains_top_candidate():
    q=torch.tensor([[1.0,0.0]]); c=torch.tensor([[[1.0,0.0],[0.2,0.9],[-1.0,0.0],[0.9,0.1]]])
    assert cosine_shortlist(q,c,2).tolist()==[[0,3]]

def test_k_equals_n_is_lossless():
    torch.manual_seed(1); q=torch.randn(3,8); c=torch.randn(3,11,8); idx=cosine_shortlist(q,c,11)
    assert torch.equal(torch.sort(idx,dim=-1).values,torch.arange(11).repeat(3,1))

def test_recall_at_k():
    idx=torch.tensor([[1,3],[0,2]]); target=torch.tensor([[3],[4]])
    assert recall_at_k(idx,target)==0.5

def test_invalid_k_fails():
    with __import__("pytest").raises(ValueError): cosine_shortlist(torch.randn(1,2),torch.randn(1,3,2),4)
