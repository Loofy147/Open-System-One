# Browser Runtime

The current reference lab runs all-MiniLM-L6-v2-ONNX in the browser through Hugging Face Transformers.js.

Execution policy:

- prefer WebGPU when available
- otherwise use browser ONNX/WASM
- preserve the decision contract
- report runtime metadata
- never turn confidence into execution authority

The AppDeploy lab is an execution harness, not the canonical repository contract.

Current lab:
https://open-system-one-encoder-lab-ac3965.v2.appdeploy.ai/

Current experiments:

- real encoder single decision
- synthetic scorer benchmark
- BANKING77 pilot
- permutation checks
- candidate-set interventions
