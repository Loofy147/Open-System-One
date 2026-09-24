# BANKING77 Candidate-Set Intervention

## Dataset

PolyAI BANKING77.

Pinned source repository:
PolyAI-LDN/task-specific-datasets

Pinned commit:
57ec275d8078af65b7731c2a98be812d844a6d6b

The dataset has 77 fine-grained banking intents and separate train/test data.

## Pilot design

- test sample: deterministic balanced sample, 5 per intent
- candidate sizes: K=4, 8, 16, 32, 77
- candidate regimes: deterministic random and hard distractors
- representation: label-only and train-only prototype
- scorers: pairwise, set-aware, conditional mixture

## Boundary

This is a transfer benchmark for the decision substrate. It is not a trained BANKING77 classifier and not a Jev/Laya reproduction.

## Receipt

The browser lab contains the runnable pilot. The numerical receipt is added only after execution and review of:

- K-specific metrics
- candidate-set sensitivity
- permutation probability delta
- hard-negative behavior
- representation/scorer interaction

Until a reviewed receipt is committed, the result status is OPEN.
