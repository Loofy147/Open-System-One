# Failure Ledger

Failures are durable evidence. They prevent the project from repeating dead paths.

## Execution environment

### F1 — local pretrained inference unavailable

Observed:
- PyTorch available.
- transformers unavailable.
- ONNX Runtime unavailable.
- sentence-transformers unavailable.
- tokenizers unavailable.
- no cached pretrained checkpoint.
- outbound DNS/network resolution failed for package/model downloads.

Disposition:
UNKNOWN about local pretrained execution quality.
Do not interpret environment failure as model failure.

### F2 — Hugging Face Jobs unavailable

Observed:
HF Jobs returned HTTP/API status 402 Payment Required.

Disposition:
Remote compute path unavailable in the tested session.
No benchmark result is claimed from that path.

### F3 — AppDeploy backend transformer bundle failed

Observed:
Bundling Hugging Face Transformers into the backend repeatedly failed.

Disposition:
Backend model runtime path killed for this lab.
Browser-side Transformers.js with ONNX/WASM/WebGPU became the execution path.

## Measurement bugs

### F4 — non-finite probability leakage

An earlier package allowed NaN/Inf to propagate into result probabilities.

Fixed:
validation rejects non-finite scores/probabilities.

### F5 — conformal NaN validation bug

An earlier conformal validation path did not reject NaN in a nonnegative-value check.

Fixed:
explicit finite-value validation.

### F6 — invalid permutation flip metric

The first browser diagnostic attempted to infer a reverse result from a nonexistent reverse row identifier.

Fixed:
compare actual normal and reversed predictions and align probabilities by candidate identity.

### F7 — escaped-newline benchmark bug

An intermediate benchmark constructed a literal escaped separator instead of the intended newline.

Fixed:
prompt construction now uses the intended newline.

### F8 — benchmark handler shadowing

The UI handler and benchmark function temporarily used the same name, creating self-recursion.

Fixed:
UI handler renamed.

## Statistical debt

### F9 — mixed-K Brier baseline approximation

A single baseline computed from mean K is not equal to the average of exact per-case uniform baselines.

Disposition:
do not use mixed-K skill-vs-uniform from the current browser pilot.
Correct per-K or per-case baseline before interpretation.

### F10 — prototype sampling

The current browser BANKING77 pilot uses up to the first five training examples for each intent.

Disposition:
deterministic but potentially presentation-sensitive.
Future revision should use a documented deterministic spread/sampling rule before final benchmark claims.

### F11 — user-supplied receipts

Browser benchmark JSONs were pasted by the user and not independently re-executed inside this review.

Disposition:
stored as USER_REPORTED / CONVERSATION-ONLY evidence.
They cannot upgrade a claim to independently verified evidence by repetition.
