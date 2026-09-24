# External Sources and Boundaries

## TypeSafe

Official introduction:
https://typesafe.ai/blog/introducing-system-one-models-and-jev

Jev overview:
https://www.typesafeai.org/jev

Choice, Score, Noul guide:
https://www.typesafeai.org/guides/choice-score-noul

Use these sources for the externally published System One/Jev terminology and public contract.

Boundary: public contract does not disclose or establish hidden model internals.

## Laya

Open implementation:
https://github.com/NandhaKishorM/laya

Laya checkpoint family:
https://github.com/he-jev/laya

Use for inspection of an open typed-decision implementation and for project-reported architecture/training claims.

Boundary: Laya benchmarks remain project-reported unless independently reproduced.

## BANKING77

Hugging Face:
https://huggingface.co/datasets/PolyAI/banking77

Original source repository:
https://github.com/PolyAI-LDN/task-specific-datasets

Pinned source commit used by the browser pilot:
57ec275d8078af65b7731c2a98be812d844a6d6b

The Hugging Face dataset metadata currently lists 13,083 examples and 77 intents.

## MiniLM ONNX

https://huggingface.co/onnx-community/all-MiniLM-L6-v2-ONNX

Use: browser feature-extraction target.

Boundary: the pretrained embedding encoder is a generic representation layer in our experiment, not a native typed-decision model.

## Other mechanisms

Research references investigated include:
- Deep Sets
- Set Transformer
- proper scoring rules
- temperature scaling
- conformal/selective prediction
- dynamic-label candidate classification
- diffusion read slots
- probabilistic circuit composition

Each mechanism remains subject to the repository experiment and kill-test protocol.
