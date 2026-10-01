# Native Capability Kernel v0.1

Status: EXPERIMENTALLY_SUPPORTED

The OSS campaign is now feeding our own architecture rather than becoming architecture.

## Primitive

`CapabilityRequest -> Decision -> Approval -> Execute -> Observation -> Receipt`

The kernel separates:

- **Policy decision**: typed request + explicit policy rule.
- **Relationship authorization**: subject/capability/target grant state that can be revoked.
- **Approval**: explicit request-scoped gate for side effects.
- **Execution**: fixed local working root; no vendor API is required.
- **Observation**: stdout/stderr/exit status/artifact digest.
- **Receipt**: run correlation + deterministic hashes + idempotency identity.

## What was learned from the P0 campaign

OPA demonstrated the value of an externalized policy decision point.
Cedar demonstrated that deny is a semantic result, not necessarily a process failure.
OpenFGA demonstrated that authorization is a relation state that must change immediately after revoke.
OpenSandbox demonstrated that lifecycle and terminal cleanup are distinct acceptance conditions.
Browser/OTel preflight demonstrated that a stable run identifier can correlate heterogeneous action spans.

## Non-goals

This kernel is not a replacement for a hardened container runtime, remote policy engine, identity provider, or browser automation system. It is the contract boundary at which such implementations can be attached.

## Acceptance

The direct local suite must prove:
1. policy + relationship intersection;
2. revoke -> deny;
3. side-effect request-scoped approval gate and deny precedence;
4. idempotent replay;
5. artifact digest and receipt correlation;
6. target path escape rejection.
