# Android T2 B6/B7 Kill-Test Specification v0.1

**Status:** HYPOTHESIS / TEST TARGET
**Source:** Loofy147/Llms-mcp-android@78afd5d3d7716fe31a5f109a5796eb3db7f99970

## B6 — Concurrent recovery

### Observed source property

`JournalRuntimeStore` protects operations with an instance-local `synchronized(lock)` while reading/replaying the shared journal file. The lock is not a file/OS-level lock and is not shared by separate processes.

### Hypothesis

Two independent recovery actors may both observe the same `UNKNOWN` state, both reconcile it, both reserve the same effect, and both dispatch.

### Kill condition

PASS condition:
- at most one provider dispatch for the semantic effect;
- at most one external effect;
- all recovery actors converge on one authoritative terminal state;
- no duplicate reservation survives.

FAIL condition:
- request/dispatch count > 1 for one semantic effect;
- two actors both become execution-authoritative;
- a second side effect occurs.

Provider idempotency must not mask the dispatch duplication; the test must measure both `request_count` and `effect_count`.

### Acceptance evidence

Prefer two actual Android processes with the same journal and effect identity. A same-process multi-instance test is useful as a lower-bound falsification but is insufficient to close B6.

## B7 — Stale callback/result ordering

### Observed source property

`JournalRuntimeStore.saveRun()` appends a complete `RunRecord` and `loadRun()` reconstructs the latest record encountered for the run id. The inspected `RunRecord` encoding does not include an attempt sequence or monotonic causal revision.

### Hypothesis

An older attempt/result written after a newer terminal state may become the loaded authoritative Run state.

### Kill condition

PASS condition:
- a stale result cannot regress a newer authoritative terminal state;
- the durable record retains the newer causal revision;
- late callbacks are explicitly rejected or recorded as non-authoritative.

FAIL condition:
- terminal state regresses to an older attempt/result;
- stale output/evidence replaces a newer result;
- ordering is decided by arrival time alone.

### Minimal discriminating fixture

1. write Run revision/attempt N as started;
2. write Run revision/attempt N+1 as completed;
3. deliver late result from N;
4. reload the durable Run;
5. assert N+1 remains authoritative.

Any failure should be recorded as a source-grounded negative result before proposing a fix.

## Non-claims

These source properties do not establish a bug by inspection alone. They establish why B6/B7 are high-value falsification targets.

Do not add a generalized distributed lock or versioning scheme before the kill test produces evidence.
