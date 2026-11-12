# Effect Identity and Evidence-Backed Reconciliation Contract v0.1

**Status:** Draft conformance contract  
**Parent:** Architecture Convergence Contract v0.1  
**Related gap:** G-04 UNKNOWN effect/reconciliation; G-02 cross-repository conformance  
**Issue:** [#12](https://github.com/Loofy147/Open-System-One/issues/12)

## 1. Purpose

Give independent runtimes the same meaning for a logical external effect, each execution attempt, and the evidence required to reconcile an ambiguous outcome.

This contract does not prescribe one database, journal, scheduler, operating system, provider SDK, or worker model. Implementations retain their local storage and adapters. They must preserve the semantics below when translating to or from the shared records.

## 2. Three identities, not one

### 2.1 Immutable logical effect identity

The identity is defined by `schema/effect-identity.v0.1.json`:

- `effect_id`: stable identifier for the logical effect.
- `run_id`: the run that owns the effect.
- `capability_id` and `action_id`: exact capability and action semantics.
- `action_version`: positive, exact version.
- `scope`: explicitly present canonical set; an empty array is meaningful and is not equivalent to omission.
- `attributed_to`: accountable invoking principal/service.
- `parameters_digest`: SHA-256 over the capability adapter's canonical parameter representation.

These fields are immutable for the lifetime of `effect_id`. Reusing an effect ID with a changed run, action, version, scope, attribution or parameters digest is a conflict, not a replay and not a new attempt.

The digest algorithm and canonicalization procedure belong to the adapter contract. A runtime must not invent a digest over a different serialization and claim semantic equality. For the v0.1 shared fixture, the digest string is syntactically `sha256:<64 lowercase hex>`; fixture validators separately test that changing parameters changes the digest.

### 2.2 Execution attempt identity

An attempt is defined by `schema/effect-attempt.v0.1.json`:

- `attempt_id` is unique and never reused.
- `attempt_number` increases monotonically within the logical effect.
- Every reservation creates a new attempt record.

The attempt ID is not part of the immutable logical effect identity. This distinction permits a controlled retry after authoritative confirmation that a previous attempt did not execute, while preserving the original attempt and reconciliation history.

A retry must not overwrite or mutate the prior attempt record. It creates a new attempt for the same logical effect identity.

### 2.3 Run and event identity

The run identity and event identity remain separate. An event append must be idempotent for the same event ID and exact content. The same event ID with different content is a conflict. An event journal must reject sequence gaps and invalid predecessor/successor transitions.

## 3. State machine

The legal state transitions are:

```text
RESERVED -> COMPLETED
RESERVED -> UNKNOWN
UNKNOWN -> COMPLETED
UNKNOWN -> CONFIRMED_NOT_EXECUTED
CONFIRMED_NOT_EXECUTED -> new RESERVED attempt (new attempt_id, incremented attempt_number)
```

The last transition creates a new attempt record; it does not rewrite the old attempt's terminal state.

The following are prohibited:

- `UNKNOWN -> execute` without reconciliation.
- `UNKNOWN -> RESERVED` for the same attempt.
- `COMPLETED -> any non-terminal state`.
- A second attempt using an already-used `attempt_id`.
- Reusing `effect_id` with any changed immutable identity field.
- Applying a reconciliation attestation to a different attempt, even when the logical effect ID is the same.

## 4. Reconciliation is an evidence-bearing decision

A local ledger may enforce and store state transitions. It is not automatically the authority that knows whether a remote message, payment, filesystem operation, Android intent, or provider request occurred.

A transition out of UNKNOWN requires an attestation conforming to `schema/effect-reconciliation-attestation.v0.1.json` with:

- exact effect identity and attempt identity;
- decision and timestamp;
- capability-specific authority/provider reference;
- the query and observation reference with query/observation times;
- durable evidence artifact reference and SHA-256 digest;
- verifier identity/version/result;
- accountable human or service principal;
- reason.

A confirmed decision requires verifier result PASS. If evidence is unavailable or insufficient, the decision is UNRESOLVED and the attempt remains UNKNOWN.

The runtime that receives the attestation must validate that:
1. the effect identity matches exactly;
2. the attempt ID and attempt number match the current UNKNOWN attempt;
3. the authority is authorized for this capability and scope;
4. evidence can be retrieved and its digest verified;
5. verifier/policy references are recognized and applicable;
6. the attestation principal is authenticated and authorized to reconcile.

The JSON Schema validates shape, not authenticity. The relying runtime or a designated trust service must validate signatures, credentials, authority allowlists, verifier registration and policy applicability. A bare decision string is not a trusted attestation.

## 5. Canonicalization and privacy

For v0.1 string maps, the interoperable canonical parameter byte sequence is:

1. Encode each key and value as UTF-8 without Unicode normalization.
2. Sort entries by the unsigned lexicographic order of the UTF-8 key bytes.
3. For each entry append the ASCII decimal byte length of the key, `:`, the key bytes, the ASCII decimal byte length of the value, `:`, and the value bytes.
4. Compute SHA-256 over the concatenated bytes and prefix the lowercase hexadecimal digest with `sha256:`.

The canonicalization test vector in `research/conformance/kernel-conformance-fixtures.v0.3.json` exercises this rule. The older v0.2 kernel fixture is retained unchanged for historical reproducibility; its K-UNKNOWN test-vector digests are legacy placeholders and are not valid under the v0.1 identity schema.

Implementations must retain or reference the exact canonical parameter digest used to create the effect identity. Do not export raw parameters when a digest and a minimized evidence reference are sufficient. Scope and attribution must remain explicit.

The canonicalizer is capability-version-specific. It must specify encoding, key ordering, normalization and treatment of absent/empty values. A change in canonicalization that can alter the digest requires a new capability/action version or an explicit schema/adapter revision.

## 6. Conformance

Use `research/conformance/effect-lifecycle-fixtures.v0.1.json`.

A conformant adapter must:
- reject missing or blank required identity fields;
- treat empty scope as valid when explicitly supplied;
- reject identity mutation under the same effect ID;
- require a unique attempt ID and monotonic attempt number;
- block execution for UNKNOWN;
- retain previous attempt events after confirmed non-execution;
- require an evidence-bearing attestation to leave UNKNOWN;
- reject missing authority/evidence/verifier data;
- reject a stale attestation for an older attempt;
- leave an UNRESOLVED attempt in UNKNOWN.

A fixture PASS is scoped to the assertions actually executed. It does not prove provider truth, distributed coordination, exactly-once delivery or system-wide interoperability.

## 7. Compatibility and migration

v0.1 is a draft contract. Adapters may continue to read older records, but must mark any missing identity fields as legacy/incomplete. They must not silently fill absent attribution, scope, parameter digest or attempt identity with guessed values and then claim full conformance.

Migration must preserve old raw records and append a new enriched reference or migration observation. Do not rewrite historical facts to make old records appear to have contained fields they never recorded.

## 8. Non-goals

This contract does not guarantee exactly-once execution, solve distributed transactions, define a universal lock service, or nominate one local journal as a provider authority. It defines the minimum semantic boundary needed to reason safely about ambiguous external effects.


### 5.1 Full attestation canonical bytes and signature preimage

The full reconciliation attestation uses the versioned algorithm:

`open_system_one.effect_reconciliation_attestation_canonical.v0.1`

It is not canonical JSON. Implementations MUST construct the following ordered string-field sequence:

1. canonicalization identifier;
2. attestation schema;
3. effect identity schema;
4. effect ID;
5. run ID;
6. capability ID;
7. action ID;
8. action version as base-10 decimal without leading zeroes;
9. scope item count as base-10 decimal;
10. each scope string sorted by unsigned lexicographic order of its UTF-8 bytes;
11. attributed principal;
12. parameters digest;
13. attempt ID;
14. attempt number as base-10 decimal without leading zeroes;
15. decision;
16. decided-at timestamp;
17. authority kind;
18. authority reference;
19. observation reference;
20. queried-at timestamp;
21. observed-at timestamp;
22. evidence artifact reference;
23. evidence digest;
24. verifier reference;
25. verifier version;
26. verifier result;
27. verified-at timestamp;
28. accountable principal kind;
29. accountable principal reference;
30. authentication scheme;
31. authentication key reference;
32. authentication signed digest (full attestation only);
33. authentication signature (full attestation only);
34. reason.

For each field, append the ASCII base-10 length of its UTF-8 encoding, a colon byte (`:`), then the UTF-8 bytes. Concatenate all framed fields without any additional separator. The length is a byte length, not a character count. Strings are encoded as supplied; no Unicode normalization, case folding, trimming or newline conversion occurs during canonicalization. Scope is a set: duplicate entries are invalid, and order is normalized by the specified UTF-8 byte ordering. Absent fields are invalid; empty scope is encoded as count `0`.

The full attestation digest is SHA-256 over the full sequence (including `authentication.signed_digest` and `authentication.signature`), represented as `sha256:<64 lowercase hex>`.

The signature preimage is the same sequence with only `authentication.signed_digest` and `authentication.signature` omitted. The `authentication.signed_digest` field MUST equal SHA-256 of those signature-preimage bytes. The signature scheme verifies the actual signature over those exact preimage bytes; the scheme-specific signature encoding does not alter the canonical preimage. This definition avoids self-reference while binding the signature to the attestation semantics and key reference.

The shared golden vector is `research/conformance/effect-attestation-canonicalization-v0.1.json`. Adapter test copies MUST remain byte-identical to the Open-System-One blob. The expected v0.1 preimage digest is `sha256:3f032f89aa6ca5baacfe2d971096f5292eb2bb517b9cc098bc840128a74fd46f`; the expected full attestation digest is `sha256:f4f29ce3a85e07ef63d9a69ac6aa1d4c8a06f0a48516794ebcf7d3525a02073e`.

An adapter using any other field order, framing, scope ordering or byte encoding is not conformant to this canonicalization ID. A future encoding change requires a new canonicalization ID and new golden vectors; it MUST NOT silently change v0.1.
