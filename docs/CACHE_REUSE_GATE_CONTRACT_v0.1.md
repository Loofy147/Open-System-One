# Cache Reuse Gate Contract v0.1

**Status:** PROVISIONAL / EXPERIMENTALLY_SUPPORTED

## Rule

Cache value and cache reusability are different properties.

A cache may remain valuable historical/replay material while being refused for current reuse.

Minimum reuse gate:

1. cache status must be fresh;
2. source identity must match the current source reference;
3. if an integrity digest is available for the material being reused, the observed digest must match the recorded digest;
4. reuse policy must permit the requested operation;
5. revalidation must be completed when policy requires it.

Source drift and integrity mismatch are refusal conditions, not deletion conditions.

## Required negative cases

- source reference changes -> reusable=false, reason=source_revision_changed;
- recorded digest differs from the observed material -> reusable=false, reason=integrity_mismatch;
- status is stale/invalid/superseded/unknown -> reusable=false;
- policy is revalidate_before_use -> reusable=false until an independent revalidation occurs;
- preserved invalidated material remains readable for reconstruction, debugging, drift analysis, and replay preparation.

## Authority boundary

Passing the cache reuse gate does not make cache content Evidence, Claim, Decision, Authorization, or Semantic Authority.

An independently verified cache-backed Observation may support an Evidence record, but the cache remains an Artifact and its reuse gate remains a separate concern.

## Current evidence

M0 and UWS each implement the same minimal reuse-gate semantics in their conformance branches. Focused reconstructed checks show source drift blocks reuse, integrity mismatch blocks reuse, revalidation remains an explicit gate, and the stored cache artifact remains preserved.

Both runtimes also execute a cache-backed result through the independent Verification boundary: a reusable cached value of 55 is observed and rejected by an even-sum verifier while the cache remains a distinct Artifact.

## Remaining proof

The gate and verification chain do not establish general truth of cached content. Clean-clone CI, broader integrity handling, and capability-specific semantics remain open.
