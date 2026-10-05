# UNKNOWN_OUTCOME Reconciliation Contract v0.1

**Status:** PROVISIONAL / EXPERIMENTALLY_SUPPORTED_TARGET

## Source boundary

This contract is derived from the current Android durable-runtime semantics at the inspected source revision. It is a cross-system semantic target, not an Android-specific transport API.

## State machine

```text
absent
  -> RESERVED
  -> COMPLETED

RESERVED
  -> COMPLETED
  -> UNKNOWN

UNKNOWN
  -> COMPLETED          (explicit reconciliation: effect confirmed)
  -> CONFIRMED_NOT_EXECUTED

CONFIRMED_NOT_EXECUTED
  -> RESERVED            (a new attempt may be reserved)

COMPLETED
  -> terminal; replay blocked
UNKNOWN
  -> replay blocked until reconciliation
```

## Invariants

1. A transport/process failure that leaves the external effect ambiguous must not be classified as semantic success or definitive failure.
2. `UNKNOWN` is durable state, not an instruction to retry.
3. Repeated side-effect reservation is blocked while an effect is `UNKNOWN`.
4. Only explicit reconciliation may transition `UNKNOWN`.
5. Only `CONFIRMED_NOT_EXECUTED` permits a later reservation of the same semantic effect identity.
6. `CONFIRMED_COMPLETED` is represented as terminal `COMPLETED`; it must not cause another external side effect.
7. Recovery of a stale `RESERVED` effect converts it to `UNKNOWN` before any later retry decision.
8. Effect identity must survive process replacement and be independent of a transport handle.

## Reconciliation boundary

The reconciliation operation must identify the same semantic effect, normally through an `operation_id`/`effect_id` or an equivalent provider-supported idempotency identity.

Valid reconciliation outcomes are deliberately narrow:

- `CONFIRMED_COMPLETED`: the external effect is known to have occurred;
- `CONFIRMED_NOT_EXECUTED`: the external effect is known not to have occurred.

An inability to decide remains `UNKNOWN` and does not permit replay.

## Evidence boundary

Effect status is durable operational state. It is not itself Evidence of truth. Post-effect Verification and Evidence remain separate concerns.

## Current local evidence

Android provider-process B2/B3 evidence demonstrates the provider-side form of this state machine across a real process boundary. Caller-side durable `UNKNOWN_OUTCOME`, concurrent recovery, and stale callback ordering remain open there.

The M0/UWS conformance work will implement only the semantic core above before any Android transport adapter is introduced.

## Acceptance

A runtime passes the minimal reconciliation fixture when it can:

1. reserve one effect identity;
2. represent interruption after possible external effect as `UNKNOWN`;
3. block replay while `UNKNOWN`;
4. reconcile to `COMPLETED` without a second effect;
5. reconcile to `CONFIRMED_NOT_EXECUTED` and then allow one later reservation;
6. convert stale `RESERVED` to `UNKNOWN` during recovery.
