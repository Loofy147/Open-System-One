# v0.3 Experimental Receipt

## Verification

Local command:
PYTHONPATH=src pytest -q

Recorded result:
31 passed in 2.24s

## Architecture sweep

Representative calibrated sweep, K=6 synthetic task:
- pairwise: accuracy 0.732421875, Brier 0.0251274426, ECE 0.3040713615
- marker_shared: accuracy 0.765625, Brier 0.0277419686, ECE 0.3394932724
- set_aware: accuracy 0.84375, Brier 0.0121995509, ECE 0.4103051432

Temperature fitting produced:
- pairwise temperature 1.0369725227
- marker temperature 1.0211656094
- set-aware temperature 0.9880068898

Calibration changes were small and did not monotonically improve ECE.

## Grid rerun

At interaction=0.0:
- K=8 pairwise accuracy 0.9609375 vs set-aware 0.76953125.
- K=16 pairwise accuracy 0.92578125 vs set-aware 0.71875.

At interaction=1.25:
- K=8 pairwise accuracy 0.796875 vs set-aware 0.734375.
- K=16 pairwise accuracy 0.6953125 vs set-aware 0.65234375.

This demonstrates that set-aware is not a universal improvement.

## Conditional mixture batch results

Two-seed means, K=8, interaction=1.0:

| Task | Pairwise acc | Conditional acc | Pairwise Brier | Conditional Brier |
|---|---:|---:|---:|---:|
| Contrastive | 0.8203125 | 0.83984375 | 0.0272166543 | 0.0247345008 |
| Competitive | 0.6015625 | 0.59765625 | 0.0504868291 | 0.0476488732 |
| Global | 0.7578125 | 0.75390625 | 0.0159802856 | 0.0141200593 |

At interaction=2.0, global:
- pairwise accuracy 0.609375, Brier 0.0532808477
- conditional accuracy 0.60546875, Brier 0.0454130807

Interpretation:
conditional mixture repeatedly improved probability quality measured by Brier in the tested synthetic batch family, while top-1 accuracy effects were mixed.

## Other architectures

At global, K=8, interaction=1.0:
- pairwise mean accuracy 0.7578125, Brier 0.0159803
- conditional mixture mean accuracy 0.75390625, Brier 0.0141201
- DeepSets 0.5000000, Brier 0.0568989
- relational 0.39453125, Brier 0.0685660
- Set Transformer 0.3906250, Brier 0.0683487

The structural permutation and masking tests nevertheless passed for all extended architectures.

## Learned encoder transfer surrogate

The 24D learned bidirectional encoder is a transfer surrogate, not pretrained MiniLM/ModernBERT.

At interaction=1.25, K=8:
- pairwise: accuracy 0.5520833, Brier 0.0580787
- marker: accuracy 0.5416667, Brier 0.0628578
- set-aware: accuracy 0.5833333, Brier 0.0564166
- conditional: accuracy 0.5520833, Brier 0.0595144

This preserves a candidate-interaction signal but does not prove real-NLP superiority.

## Shortlist

Oracle-vector N=128:
- K=8 retained 6.25 percent of candidates, recall@1 1.0 / 0.99609375 / 0.99609375 over seeds 1/2/3.
- K=16 retained 12.5 percent, recall@1 1.0 for all three seeds.

This is a retrieval/scalability proof of concept under oracle vectors.

## Status

- Structural suite: EXPERIMENTALLY_SUPPORTED
- Set-aware real-data benefit: OPEN
- Conditional real-data benefit: OPEN
- Conditional synthetic Brier effect: EXPERIMENTALLY_SUPPORTED in tested scope
- Real pretrained encoder comparison: OPEN
- BANKING77 reviewed receipt: OPEN
