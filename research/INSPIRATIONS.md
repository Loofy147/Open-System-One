# Historical Mechanism Inspirations

These are research inspirations, not evidence that any mechanism belongs in the core.

## User-origin examples

The discussion used several historic artifacts as examples of high-leverage computational ideas:

- Apollo guidance software and the BURN_BABY_BURN path as an example of a small semantic anchor affecting control execution.
- Fork bomb as an example of recursive amplification from a compact rule.
- 10 PRINT as an example of local rule + variation + iteration producing global structure.
- Quake III fast inverse square root as an example of representation-aware approximation followed by refinement.

These examples are recorded because they suggest mechanisms to extract, not because they prove a design.

## Extraction rule

For each inspiration ask:

1. What computational relation changed?
2. What is the smallest machine-readable contract?
3. Can the mechanism be isolated?
4. Can a kill test falsify its usefulness?
5. Does it compose with other primitives?
6. Does it delete complexity or merely move it?

## Relation to the primitive sweep

The project searches for mechanisms such as:
- reification
- composition
- unification
- explicit control
- memoization
- approximate prefiltering
- associative accumulation
- causal order
- content identity
- capability
- convergent merge
- dynamic scoring

The historical artifact is never the unit of acceptance. The extracted mechanism is.
