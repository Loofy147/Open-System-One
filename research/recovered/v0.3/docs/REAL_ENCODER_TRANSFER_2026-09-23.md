# Real-Encoder Transfer Stage — 2026-09-23

## Status

EXPERIMENTALLY_SUPPORTED / OPEN

This stage tests whether the scorer comparison survives after a learned bidirectional text encoder rather than direct latent vectors.

## External solution scan
- `answerdotai/ModernBERT-base`: 149.7M parameters, Apache-2.0, English, ONNX-compatible.
- `sentence-transformers/all-MiniLM-L6-v2`: ONNX exports exist, including a 23 MB ARM64 quantized file.
- `laya-mlx`: production-like Laya decision runtime with ModernBERT-large and mmBERT-base checkpoints; actual full-checkpoint benchmarking requires Apple Silicon.

## Local execution constraint
The current execution environment has PyTorch but no `transformers`, no ONNX Runtime, and no cached pretrained checkpoint. Network access for package/model download is unavailable. Therefore this stage uses a learned 24D bidirectional Transformer encoder trained jointly on the synthetic decision task as a transfer surrogate.

This is NOT evidence that the same ranking will hold on pretrained ModernBERT/MiniLM.

## Experiment
Shared learned encoder:
- 1 Transformer encoder layer
- hidden size 24
- 4 attention heads
- frozen architecture across scorers

Scorers:
- pairwise
- marker/shared-context
- set-aware
- conditional mixture

Training:
- 120 AdamW steps
- batch 16
- same synthetic generator for all scorers
- same parameter budget order

Evaluation:
- interaction = 0.0 and 1.25
- K = 4, 8, 16
- seeds = 11, 12, 13
- 64 held-out examples per seed
- metrics: accuracy, Brier

## Results

| interaction | K | scorer | accuracy | Brier |
|---:|---:|---|---:|---:|
| 0.00 | 4 | pairwise | 0.4740 | 0.1750 |
| 0.00 | 4 | marker | 0.4688 | 0.1745 |
| 0.00 | 4 | set-aware | 0.4740 | 0.1861 |
| 0.00 | 4 | conditional | 0.5104 | 0.1550 |
| 0.00 | 8 | pairwise | 0.2500 | 0.1211 |
| 0.00 | 8 | marker | 0.2656 | 0.1203 |
| 0.00 | 8 | set-aware | 0.2604 | 0.1242 |
| 0.00 | 8 | conditional | 0.2708 | 0.1153 |
| 0.00 | 16 | pairwise | 0.0938 | 0.0667 |
| 0.00 | 16 | marker | 0.1250 | 0.0664 |
| 0.00 | 16 | set-aware | 0.1042 | 0.0676 |
| 0.00 | 16 | conditional | 0.0938 | 0.0650 |
| 1.25 | 4 | pairwise | 0.6302 | 0.1052 |
| 1.25 | 4 | marker | 0.5677 | 0.1364 |
| 1.25 | 4 | set-aware | 0.6510 | 0.1076 |
| 1.25 | 4 | conditional | 0.6458 | 0.1011 |
| 1.25 | 8 | pairwise | 0.5521 | 0.0581 |
| 1.25 | 8 | marker | 0.5417 | 0.0629 |
| 1.25 | 8 | set-aware | 0.5833 | 0.0564 |
| 1.25 | 8 | conditional | 0.5521 | 0.0595 |
| 1.25 | 16 | pairwise | 0.3698 | 0.0382 |
| 1.25 | 16 | marker | 0.3906 | 0.0390 |
| 1.25 | 16 | set-aware | 0.3698 | 0.0377 |
| 1.25 | 16 | conditional | 0.3698 | 0.0389 |

## Interpretation
1. The scorer comparison remains meaningful after introducing a learned encoder.
2. Marker/shared-context is not universally superior.
3. Set-aware retains a signal on the interaction task, especially at K=8.
4. Conditional mixture is competitive and often has the best Brier in the current small run.
5. At K=16 all methods approach the random-guess accuracy regime; this is primarily a capacity/training-budget limitation of the tiny surrogate, not evidence about pretrained encoders.

## Kill constraints
The following claims remain OPEN:
- superiority of any scorer on real NLP data;
- superiority after pretrained ModernBERT/MiniLM initialization;
- stability across domains/languages;
- scalability to large K;
- calibration ranking after proper temperature fitting;
- benefit of candidate interaction over a strong independent baseline.

## Next controlled transfer
Run exactly the same matrix with one real pretrained encoder:
1. MiniLM ONNX as the CPU/mobile baseline;
2. ModernBERT-base as the higher-capacity encoder;
3. Laya's actual decision head as a reference implementation.

Do not change the decision contract or scorer metrics between runs.
