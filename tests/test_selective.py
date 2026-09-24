import torch
from open_system_one.lab.selective import abstain_rate,coverage,fit_split_conformal,fit_temperature,mean_set_size,predict_set

def test_temperature_fitting_is_finite_and_positive():
    torch.manual_seed(1); logits=torch.randn(40,4)*2; labels=logits.argmax(-1); t=fit_temperature(logits,labels); assert 0.05<=t<=20.0

def test_split_conformal_returns_valid_sets_and_metrics():
    probs=torch.tensor([[0.90,0.05,0.05],[0.80,0.10,0.10],[0.10,0.80,0.10],[0.10,0.10,0.80],[0.60,0.30,0.10],[0.55,0.35,0.10]])
    labels=torch.tensor([0,0,1,2,0,1]); cal=fit_split_conformal(probs,labels,alpha=0.2); sets=predict_set(probs,cal)
    assert sets.dtype==torch.bool and sets.shape==probs.shape
    assert 0.0<=coverage(sets,labels)<=1.0 and mean_set_size(sets)>=0.0 and 0.0<=abstain_rate(sets)<=1.0

def test_nonfinite_and_invalid_inputs_fail_loudly():
    with __import__("pytest").raises(ValueError): fit_split_conformal(torch.tensor([[0.5,float("nan")]]),torch.tensor([0]))
