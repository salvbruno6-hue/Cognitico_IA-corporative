# Symbiont Composition of the Hermes Candidate Loop — 2026-09-26

## Direct answer

The Hermes candidate loop composes canonical Symbiont components, but it is not itself the entire Symbiont.

### What is composed

1. Hermes candidate observation -> `HermesCandidate`.
2. Existing owner mapping -> `SymbiontAdaptation` / `refine_capability()`.
3. Controlled experiment -> candidate-specific evaluator.
4. Implementation evidence -> `ImplementationEvidence`.
5. Governed handoff -> `advance_to_implementation()`.
6. ELO implementation loop -> `ImplementationStage` and repeatability/regression checks.
7. Symbiont autonomy boundary -> `run_symbiont_autonomous_adjustment_loop()` exists for bounded correction iterations.
8. Laboratory -> `SymbiontLabAdapter` / `SymbiontLabObservation` when the observation is routed through the canonical Symbiont laboratory path.
9. Evolution Gate -> existing canonical gate; no Hermes gate is created.
10. Learning Governance -> existing governed learning service; no Hermes learning authority is created.

### What is not the same thing

`hermes_secondary_loop_integration.py` is an integration/handoff layer. It is not a second Symbiont runtime and should not be treated as the Symbiont itself.

The canonical Symbiont is distributed across Cognitive contracts, laboratory, capability evolution review, adaptation, execution boundary and governed learning. This is intentional: the architecture document explicitly defines Symbiont as a cognitive nature/boundary rather than a second Core or provider runtime.

## Critical correction

Before this change, a candidate could reach `READY_FOR_ELO_REVIEW` because a contract metric improved from 0 to 1. That could be infrastructure improvement without functional ELO improvement.

The governed handoff now requires `functional_value_proven=True` before the candidate can cross into `ELO_REVIEW` through `advance_to_implementation()`.

`EXT-CONTEXT-PLUGIN-HERMES` is currently the controlled candidate that satisfies this condition.

Contract-only candidates are returned as `RETEST_FUNCTIONAL_VALUE`.

## Resulting composition

`external observation → Symbiont adaptation → candidate experiment → functional-value proof → implementation evidence → governed implementation loop → Evolution Gate / ELO review → Lab/Learning where applicable → human authorization for canonical promotion`

## Governance

- no second Evolution Gate;
- no second Learning Governance;
- no second memory authority;
- no automatic canonical mutation;
- no production evidence inferred from laboratory evidence;
- human authorization remains required for canonical promotion.