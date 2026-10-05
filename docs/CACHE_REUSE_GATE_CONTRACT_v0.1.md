# Cache Reuse Gate Contract v0.1

**Status:** PROVISIONAL / EXPERIMENTALLY SUPPORTED

## Rule

Cache value and cache reusability are different properties.

A cache may remain valuable historical/replay material while being refused for current reuse.

Minimum reuse gate:

1. cache status must be fresh;
2. source identity must match the current source reference;
3. reuse policy must permit the requested operation;
4. revalidation must be completed when policy requires it.

Source drift is therefore a refusal condition, not a deletion condition.

## Required negative cases

- source reference changes -> reusable=false, reason=source_revision_changed;
- status is stale/invalid/superseded/unknown -> reusable=false;
- policy is revalidate_before_use -> reusable=false until an independent revalidation occurs;
- preserved invalidated material remains readable for reconstruction, debugging, drift analysis, and replay preparation.

## Authority boundary

Passing the cache reuse gate does not make cache content Evidence, Claim, Decision, Authorization, or Semantic Authority.

## Current evidence

M0 and UWS each implement the same minimal reuse-gate semantics in their conformance branches. Focused reconstructed checks show source drift blocks reuse, revalidation remains an explicit gate, and the stored cache artifact remains preserved.

## Remaining proof

The gate does not prove the cached content itself is true. Independent Verification is still required before cache-backed material can advance epistemic state.
