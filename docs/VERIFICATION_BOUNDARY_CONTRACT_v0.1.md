# Verification Boundary Contract v0.1

**Status:** PROVISIONAL / EXPERIMENTALLY SUPPORTED IN M0

## Boundary

Execution result and verification result are different semantic objects.

`Run -> Observation -> Verification -> Evidence`

The Verifier is an evaluation boundary. It does not execute the Capability and does not inherit execution authority from the Run.

## Required separation

- a Run may complete while its result later fails verification;
- an Observation records what was obtained and from which source;
- a Verification identifies an independent verifier and its status;
- Evidence references the attributable material and verification context;
- verification failure must not be upgraded to pass merely because the execution succeeded or is repeated.

## Provenance

At minimum, the verification record preserves:

- verification identity;
- Observation reference;
- verifier identity/reference;
- verification status;
- verification timestamp;
- optional reason.

## Current evidence

The M0 conformance branch executes a completed sum-of-squares Run, records an Observation with a digest, applies an independent verifier requiring an even result, obtains `value=55`, records `status=failed`, and records Evidence linking the Run, Observation, and Verification.

This is evidence for the boundary semantics only. It does not yet establish cross-repository conformance or UNKNOWN external-effect reconciliation.

## Acceptance

`execute -> observe -> verify -> evidence` is executable without model prose serving as the authority for verification.
