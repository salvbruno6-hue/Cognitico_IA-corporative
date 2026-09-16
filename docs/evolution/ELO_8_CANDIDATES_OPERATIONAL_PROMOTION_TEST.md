# ELO — First Operational Promotion Test

This change starts the first governed transition of the eight Hermes capability candidates.

## Operational activation

The eight native probes are executed through `native_capabilities.execute_candidate` and evaluated by `capability_promotion.evaluate_all_candidates`.

A candidate reaches `ACTIVE_OPERATIONAL` only when its native functional evidence is green and provenance/governance checks are green.

Operational activation does **not** mean Core canonization.

## Canonical promotion

A capability may reach `CANONICAL` only when all of these are true:

- native functional proof is green;
- provenance is intact;
- governance metadata is complete;
- explicit relevance to an ELO Core pillar is established;
- Evolution Gate approval is established.

The evaluator does not mutate Core knowledge. It returns a promotion decision for the governed transition layer.

## Current test intent

The first test suite verifies:

1. all eight candidates have a native operational promotion path;
2. all eight reach `ACTIVE_OPERATIONAL` under the controlled probe;
3. canonization is not implicit;
4. a Skill/mechanism can become canonically eligible only after Core-pillar relevance and Evolution Gate approval are both supplied;
5. without the Evolution Gate, the capability remains operational rather than canonical.

This is the beginning of the promotion test, not a claim that production deployment or Core mutation has already occurred.
