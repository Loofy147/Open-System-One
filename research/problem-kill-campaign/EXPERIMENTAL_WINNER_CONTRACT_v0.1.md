# Experimental Winner Contract v0.1

Status: MANDATORY_AFTER_PRE_BUILD_FALSIFICATION

## Purpose

Build one surviving candidate only to answer research questions, not to launch a product.

## Required evidence

Every run records source, exact ref/commit, environment identity, run_id, input/state digest, result digest, observation event, verification event, status and negative findings.

Conversation statements are hypotheses or reports until reproduced.

## Epistemic chain

Live World@revision R
-> relational applicability
-> versioned observation
-> evidence
-> verification event
-> claim
-> gate
-> decision/decision revision

Historical applicability is never substituted for current authority.

## Authority

Use the native CapabilityKernel contract:
policy + relation + request-scoped approval + current revalidation + idempotency.

## Effect

Use Direct Impact Guard where the target state can expose a trustworthy snapshot:
declared scope + change budget + pre-state identity + postconditions + observed delta + rollback/compensation + replay checks.

Do not describe the local subprocess executor as a sandbox.

## Adapters

External capabilities are replaceable adapters:
capability -> narrow adapter -> contract -> receipt -> independent verification -> promote/reject.

Vendor-specific selectors and assumptions stay outside the authority layer.

## Storage

Use BlobStore / TransactionalStore / QueryStore separation where durability is required.
Version schemas and contracts. Do not treat external agent memory as authority.

## Agent-surface gate

Run the relevant A0-A10 tests: identity, read-only, untrusted content, scope, evidence fidelity, reversible mutation, approval, stop, duplicate request, environment identity and receipt reconstruction.

## Accumulated research questions

- Is the residual problem real under adversarial comparison?
- What does the incumbent already solve?
- What exact fact/action remains impossible or disproportionately costly?
- Can the surviving capability operate without surrendering authority?
- Can historical authorization remain historically true after revoke?
- Can idempotency survive authority changes and state drift?
- Can impact be bounded independently of model intent?
- Can unexpected side effects be detected?
- Can rollback/compensation be proven?
- Can agent traces be separated from authoritative evidence?
- Can browser/sandbox/policy/identity capabilities compose without vendor lock-in?
- Can interrupted/partial runs be reconstructed?
- Can one contract survive multiple execution backends?
- Which architecture claims are actually necessary rather than inherited assumptions?

## Exit criteria

Research complete only when the experiment has answered the candidate-specific questions and the general control-plane questions above with inspectable evidence.

Only after that may a separate decision ask whether any MVP should exist.