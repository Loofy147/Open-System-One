# Real-Encoder Transfer Stage — 2026-09-23

## Status

EXPERIMENTALLY_SUPPORTED / OPEN

This stage tested whether scorer comparisons survived after replacing direct latent vectors with a learned bidirectional text encoder.

## Constraint

The local environment had PyTorch but not Transformers, ONNX Runtime, or a cached pretrained checkpoint. Network access for package/model download was unavailable.

The implemented 24D bidirectional Transformer is therefore a transfer surrogate.

It is not evidence about pretrained ModernBERT or MiniLM.

## Matrix

- encoder: learned 24D bidirectional Transformer
- scorers: pairwise, marker/shared-context, set-aware, conditional mixture
- interaction: 0.0 and 1.25
- K: 4, 8, 16
- held-out seeds: 11, 12, 13
- metrics: accuracy and Brier

## Key K=8 interaction=1.25 result

- pairwise: 0.5520833 accuracy, 0.0580787 Brier
- marker: 0.5416667 accuracy, 0.0628578 Brier
- set-aware: 0.5833333 accuracy, 0.0564166 Brier
- conditional: 0.5520833 accuracy, 0.0595144 Brier

## Interpretation

The scorer comparison remains meaningful after a learned encoder is introduced.

Set-aware and conditional mechanisms remain candidates, not winners.

At K=16, all methods approach random-guess accuracy in this tiny surrogate; this is primarily a capacity/training-budget limitation and is not evidence about pretrained encoders.

## Next real transfer

Compare:
1. MiniLM ONNX as the low-cost/mobile representation.
2. ModernBERT-base as the higher-capacity representation.
3. Laya's actual decision head as a reference implementation.

Keep contract and metrics fixed between runs.
