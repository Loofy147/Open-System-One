# Micro Activation Proof Card v0.1

Status: TEMPLATE

## Identity

Activation:
Version:
Source:
License:
Commit/release:
Date tested:

## Capability contract

Input:
Output:
Side effects:
Required permissions:
Network:
Secrets:
Persistence:

## Integration boundary

AgentSurface
  -> Activation
  -> Observation
  -> Receipt
  -> Independent Verification

The activation must remain replaceable.

## Proof

### P0 — installation

Pass:
Activation installs/loads using the declared reproducible procedure.

### P1 — narrow functionality

Pass:
One minimal task succeeds with an exact expected result.

### P2 — invalid input

Pass:
Malformed or out-of-contract input is rejected explicitly.

### P3 — side-effect boundary

Pass:
The activation cannot silently exceed the declared side-effect scope.

### P4 — provenance

Pass:
Inputs, output/artifact reference, version, and execution timestamp are recordable.

### P5 — repeatability

Pass:
The same declared input can be rerun and compared.

### P6 — failure behavior

Pass:
Timeout, cancellation, unavailable dependency, and partial failure produce explicit states.

### P7 — removal

Pass:
The activation can be disabled/removed without modifying the Open-System-One authority model.

## Evidence record

Required:
- activation_id;
- version/source;
- test_id;
- run_id;
- input reference;
- output reference;
- environment;
- permissions;
- observable actions;
- expected result;
- actual result;
- disposition;
- limitations.

## Status vocabulary

ESTABLISHED
EXPERIMENTALLY_SUPPORTED
USER_REPORTED
INFERENCE
HYPOTHESIS
CONTRADICTED
UNKNOWN
OPEN

## No-go rule

A small activation is not accepted merely because it is convenient, popular, open source, or successfully installed.

Integration requires a discriminating proof.

## Cross-link

When an activation is proven, link its proof card to:
- the consuming AgentSurface;
- the underlying capability contract;
- the durable run/evidence record;
- any independent verification;
- the rollback/removal path.
