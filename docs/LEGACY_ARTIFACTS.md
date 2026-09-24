# Legacy Research Artifacts

Earlier implementations were built before the GitHub repository was initialized. They remain useful as migration sources and evidence records.

## Archives

- open-system-one-v0.1.0.zip
  - SHA-256: 099eb77688a4750cb3c6c69aa3e3cac77cdc2891fc64f7e7f9df231fece99dc3
- open-system-one-v0.1.0-killtested.zip
  - SHA-256: 1340defec682ccdcfa86f0d5f1fab2139d7a9a6bcdaea17881d57173ae9d9313
- open-system-one-foundation-v0.3-stage.zip
  - SHA-256: 2592f80ca68f3cd181a35c15b2d9cef4a80b2308f6de726fbc6366af26eda6d4
- open-system-one-foundation-v0.3-realtransfer.zip
  - SHA-256: f5f389c2a26de28f401e5d1510062059cb367a841fe23d90e4565bb8fd8ac13d
- real_encoder_transfer_results.json
  - SHA-256: 480e82dd9d345eb2d30b17f620e99af843d94b47732a750f90548664a852c2ee

## Historical modules

The earlier packages included additional modules for:
- richer schema/API layers
- legacy adapters
- calibration and selective prediction
- synthetic architecture sweeps
- primitive sweeps
- shortlist experiments
- learned bidirectional transfer surrogates
- examples and training utilities

They are not the canonical source tree. Import only with provenance and after rerunning tests against the current contract.

## Important negative evidence

- pretrained real-encoder execution was unavailable in the local container
- learned transfer surrogate is not evidence about pretrained ModernBERT or MiniLM
- oracle shortlist results are not evidence about real encoder retrieval
