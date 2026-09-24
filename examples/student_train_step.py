"""Minimal teacher -> student training step.

Teacher probabilities can come from any calibrated decision backend. The student
never learns to emit JSON or prose; it learns the probability vector directly.
"""
import torch

from open_system_one.student import DecisionStudent, distillation_loss, pack_question

student = DecisionStudent("answerdotai/ModernBERT-base")
packed = pack_question(
    "The customer was charged twice.",
    "team",
    "Which team should handle this?",
    [
        ("billing", "payments, charges, refunds"),
        ("shipping", "delivery problems"),
        ("account", "login and profile problems"),
    ],
)
optimizer = torch.optim.AdamW(student.parameters(), lr=2e-5)

student_probs = [student.question_probabilities(packed)]
teacher_probs = [torch.tensor([0.92, 0.05, 0.03], device=student.device)]
loss = distillation_loss(student_probs, teacher_probs)
optimizer.zero_grad()
loss.backward()
optimizer.step()
print({"loss": float(loss.detach().cpu())})
