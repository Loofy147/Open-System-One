import torch
from open_system_one.student import distillation_loss, group_softmax

def test_group_softmax_preserves_independent_question_boundaries():
    logits=torch.tensor([1.0,3.0,2.0,0.0,0.0])
    groups=group_softmax(logits,[2,3])
    assert len(groups)==2
    assert torch.allclose(groups[0].sum(),torch.tensor(1.0))
    assert torch.allclose(groups[1].sum(),torch.tensor(1.0))
    assert groups[0][1]>groups[0][0]

def test_distillation_loss_is_finite():
    predictions=[torch.tensor([0.8,0.2]),torch.tensor([0.1,0.2,0.7])]
    targets=[torch.tensor([0.7,0.3]),torch.tensor([0.2,0.3,0.5])]
    loss=distillation_loss(predictions,targets)
    assert torch.isfinite(loss)
    assert loss.item()>=0.0
