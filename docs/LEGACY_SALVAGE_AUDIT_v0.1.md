# Legacy Salvage Audit v0.1

Date: 2026-09-29

Purpose
-------
Audit earlier repositories as source material for Open-System-One without inheriting
their names, architecture claims, benchmark claims, or unverified conclusions.

Disposition vocabulary
----------------------
- RETAIN: reusable primitive with a clear contract and a bounded evidence surface.
- REIMPLEMENT: useful idea, but legacy implementation is too coupled, unsafe, or claim-heavy.
- QUARANTINE: useful research material; not eligible for production/runtime reuse until independently verified.
- KILL: evidence shows the claimed capability is not represented by the implementation or the path is misleading.
- UNKNOWN: insufficient evidence.

Current Open-System-One head inspected
---------------------------------------
4c5f24f9d34f9f0fd751047ac8d0a6011855715b
Current repository surface is intentionally small: README only. This audit is therefore
an evidence/lineage record, not an assertion that the legacy repositories are dependencies.

1. Symlib
---------
Observed ref: 090698ba721bbe8428dc7ccfa003978532d6e446

Retain
- Exact deterministic verifier: `symlib.kernel.verify.verify_sigma`.
  It explicitly constructs the color functional graphs and checks that every color has
  exactly one component. This is a reusable verification primitive, independent of the
  surrounding "intelligence manifold" narrative.
- Obstruction result as a typed record: useful shape for separating status, proof steps,
  level, parameters, and evidence.
- Construction/verifier separation: construction output is passed into an independent
  exact verifier in tests.

Reimplement
- Obstruction tower as a generic protocol. The API shape is useful, but the implementation
  currently hard-codes the m=4,k=4 H3 case and returns NO_OBSTRUCTION elsewhere. The source
  also contains a TODO for the dynamic exhaustive H3 search.
- Torsor/solution-count layer. The repository explicitly documents that its solution count
  is a lower bound except for m=3. Preserve only the distinction between lower-bound and
  exact count; rederive the mathematics independently before reuse.

Quarantine
- "Theorem" labels unless backed by an actual proof artifact.
- Lean export paths containing `sorry`.
- G3 "intelligence manifold" material. It is not required for the useful verifier/obstruction
  primitives.

Important contradiction/limitation
- `h3_fiber_uniform(m=4,k=4)` is presented as an obstruction for the fiber-uniform
  subspace only. The tests separately show a valid non-fiber-uniform solution can exist.
  Therefore the obstruction must not be generalized to the entire solution space.

Status: RETAIN verifier; REIMPLEMENT obstruction framework; QUARANTINE theorem claims.

2. Suffix Smoother
------------------
Observed ref: b79a29b7aeb8afe66648d02181a3831d7c893641

Retain
- Recursive suffix-state representation with explicit smoothing methods.
- Deterministic model serialization interfaces (`to_json/from_json`).
- Model merge operations with explicit weighting.
- Pruning/calibration as independently testable transformations.
- Existing adversarial/core feature tests are useful starting material.

Reimplement
- Public package boundary. The source tree contains multiple historical copies
  (v0.3.x, extracted, Kaggle dataset, etc.). Extract one canonical implementation only.
- Benchmark harness. Rebuild from explicit dataset/version/split/hardware specifications.
- Calibration and prediction-set semantics under the Open-System-One decision contract.

Quarantine
- Throughput, RAM reduction, ECE, "production-ready", and "GPU-free industrial AI"
  claims until reproduced from a clean benchmark with receipts.
- Domain adapters and unrelated finance/genomics/demo applications.

Observed concern
- Current README/benchmark figures are historical claims, not current experimental evidence.
  The repository itself contains several copies of the implementation, so lineage of an
  individual benchmark number to one exact source tree must be established before reuse.

Status: RETAIN algorithmic core as research candidate; REIMPLEMENT packaging/benchmark contract.

3. FSO / Moaziz / Universal-intilegence-
-----------------------------------------
Observed ref: commit 54ffa228020761af89224f298c48222e065dfef1

Retain
- Pure coordinate/hash mapping as a deterministic identity-to-location primitive,
  where the coordinate space is explicitly bounded.
- The small `FSOMessage` state carrier (`payload, current_pos, color, hops`) as a
  research data structure.
- `FSOTopology` as an experimental routing object, but only after independent cycle tests.
- Separation of topology, message, task queue, HRR, and direct-consumer modules.

Reimplement
- The package's direct-consumer interface. It dynamically imports and may auto-install
  missing packages via subprocess. This is not suitable as an authority-bearing runtime.
- Any network/service layer built around the topology. Rebuild around explicit capabilities,
  permissions, versioned interfaces, and observable execution.

Kill as stated
- "Stateless NoC / storage / OS replacement" claims as production capabilities.
  The implementation inspected uses Python dictionaries, local files, dynamic imports,
  subprocess-based package installation, and Python execution. These are experiments or
  adapters, not evidence that conventional OS/filesystem substrates have been replaced.

Security boundary
- Dynamic execution of imported/persisted code and automatic package installation are
  trust-boundary issues. They cannot be carried into a capability-controlled substrate
  unchanged.

Status: RETAIN small deterministic mapping ideas; REIMPLEMENT the runtime boundary;
KILL the replacement-of-substrate claim.

4. CRISPO
----------
Observed ref: 93c51c029b186b333eb7aae4eb8d187283d9cd5f

Retain
- High-level objective -> named generation strategy as an explicit dispatch concept.
- Generator / verifier separation.
- Registry concept for retaining verified artifacts.

Reimplement
- The generation contract. Current selection is keyword-driven and the LAA path writes
  generated scripts to fixed filenames. Build a typed candidate -> verification -> artifact
  pipeline instead.
- The verification layer around actual isolated execution.

Kill as stated
- Treating the existing package as a production autonomous co-design system.

Evidence note
- The repository's own EXECUTIVE_SUMMARY identifies a pre-production state and large amounts
  of dead/over-complex legacy code. This matches the source inspection.

Status: REIMPLEMENT concepts only.

5. HAG
-------
Observed ref: 678904341c4032f4324d0f812148c1ad7a0b0a6f

Retain
- Layer separation: policy/intent, capability, execution, audit is architecturally useful.
- Explicit capability token interface as a prototype concept.
- Audit-log data model as a starting point.

Reimplement
- L1 isolation. The current code executes Python with restricted builtins in-process and
  explicitly states that real bubblewrap/seccomp isolation is not implemented.
- L2 intent verification as a typed/structured policy evaluation rather than keyword checks.
- L3 credentials/tokens as opaque, scoped, expiring capabilities.
- L4 audit as append-only, integrity-linked events rather than an in-memory list.

Kill as evidence
- "Desktop sovereignty secured" / "96% isolation" as demonstrated production properties.
- Screen/voice perception as real multimodal perception; source implements simulations/stubs.
- The desktop proof script as evidence of real OS actuation; its task path executes a
  print-oriented command.

Status: REIMPLEMENT governance primitives; KILL current security/perception claims.

6. TGI / Spike-Function-Framework
---------------------------------
Observed ref: 7d0e09f461dd9abdccb813b8eed6637050bbfad5

Retain
- Modular decomposition of a large experimental kernel.
- Explicit test files per subsystem.
- Audit tooling that can identify mocks/TODOs is itself a useful QA primitive.

Reimplement
- Any "SovereignKernel" as a thin orchestrator over independently verifiable capabilities.
- TFS/task/agent interfaces only after defining actual semantics, ownership, and failure modes.

Kill as evidence
- Treating the entire integrated stack as a verified operating system.
- Claims of O(1) storage/retrieval merely because coordinate lookup is O(1): end-to-end
  reconstruction cost still depends on the number of shards traversed.
- Test scenarios that are synthetic demos cannot establish physical/network/OS properties.

Status: REIMPLEMENT modular interfaces; quarantine the larger stack.

7. Sovereign-OS
----------------
Observed source:
- pyproject package name stratos-os, version 0.1.2
- meta_path loader in `src/stratos_os/shell/deference.py`
- local blob-backed reconstruction in `SovereignTorus`

Retain
- Import-hook experiment as a bounded research artifact.
- Explicit loader / storage separation.

Reimplement
- Runtime import capability with explicit registry, artifact digest, authority, and failure
  semantics.
- Blob addressing with cryptographic content identity rather than MD5-derived filenames.

Kill as stated
- "Replaces NTFS/ext4" or equivalent claims. The observed implementation does not establish
  replacement of a filesystem substrate.

Status: QUARANTINE import/runtime experiment.

Cross-repository salvage rules
------------------------------
1. No legacy README statement is an authority source.
2. A passing unit test establishes only the behavior covered by that test.
3. A benchmark result is UNKNOWN until tied to exact source ref, command, dataset, split,
   hardware/runtime, and raw receipt.
4. "Theorem" means mathematical claim; "proof" requires a proof artifact; "verified" means
   the stated verification actually executed.
5. No dynamic `exec`, automatic package installation, or arbitrary network execution may
   cross into Open-System-One's core contract without an explicit capability and trust
   boundary.
6. Legacy code may contribute an idea, API shape, test vector, or negative finding; it does
   not become a dependency merely because it is older or larger.

Next discriminating actions
---------------------------
A. Extract the Symlib verifier/obstruction semantics into a minimal independent specification
   and test whether the useful mathematics survives without the "intelligence" vocabulary.
B. Reproduce Suffix Smoother's smallest core benchmark from a clean tree and compare exact
   predictions before/after prune/merge/calibration.
C. Build a provenance table for each imported primitive:
   source_repo, source_ref, source_path, contract_digest, experiment_id, evidence_ref,
   disposition, and revalidation_status.

Current overall disposition
---------------------------
- Safe conceptual lineage: YES
- Safe direct dependency import: NO
- Strongest reusable primitive candidates: exact verifier, typed obstruction result,
  suffix-state classifier core, merge/prune/calibration interfaces, capability/audit data
  model.
- Highest-risk legacy material: dynamic execution/import, package auto-installation,
  "sovereign OS" replacement claims, simulated desktop/security proofs.
