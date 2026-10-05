# Cache Artifact Contract v0.1

## Semantic status

**Status:** PROVISIONAL / CONFORMANCE TARGET

A cache is a **valuable reusable Artifact**: a materialized value retained because recomputation, reacquisition, or re-fetch has operational cost or dependency risk.

A cache is not automatically:
- evidence;
- truth;
- authorization;
- execution authority;
- semantic authority.

Its value is preserved by provenance, integrity, freshness state, and explicit reuse policy.

## Required properties

Every cross-system cache representation should identify:

- stable cache identity;
- what kind of value is cached;
- the source/reference from which it was derived;
- the source/run/artifact identities it depends on;
- an integrity digest;
- freshness/status;
- reuse policy;
- invalidation conditions;
- creation/update timestamps.

## Safety boundary

`status=fresh` means only that the cache satisfies its declared freshness/integrity conditions. It does not promote the cached content to a Claim or Evidence.

`reuse_policy=revalidate_before_use` requires a discriminating validation before the cache can participate in an authoritative decision.

A stale or invalid cache remains a recorded artifact. It is not silently deleted because it may be useful for:
- debugging;
- historical reconstruction;
- drift analysis;
- differential testing;
- replay preparation;
- cost avoidance where revalidation is still possible.

## Relationship to durable state

A cache is distinct from authoritative durable state.

Checkpointed Run state answers **what state is persisted for continuation**.

A cache answers **what reusable material has been retained for possible reuse**.

They may be stored in the same physical system, but their semantic roles must remain distinguishable.

## Conformance target

A runtime conforms to this contract when it can:
1. persist a cache reference with exact provenance and integrity;
2. distinguish fresh/stale/invalid/superseded/unknown;
3. preserve the cache after invalidation;
4. refuse to treat cache reuse as evidence or authority without an independent verification/evidence path.