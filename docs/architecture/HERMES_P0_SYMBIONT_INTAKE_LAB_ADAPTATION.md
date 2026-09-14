# P0 — External Mechanism Intake + Symbiont Lab

## Candidate pair

| Candidato | Adaptação nativa | Potencialização para o ELO |
|---|---|---|
| #404 External Mechanism Intake | `AbsorptionEnvelope` becomes the universal fail-closed intake envelope and is composed with `SymbiontPatternIntake`. | Unifies how external mechanisms enter ELO, preserving source/evidence/provenance and preventing provider authority from becoming canonical. |
| #419–421 Symbiont Lab | Existing `SymbiontLabObservation` is operationally reached through the governed intake bridge; no second laboratory is created. | Turns external observations into reproducible experiments with baseline, result, regression and generalization signals before governed learning/promotion. |

## Canonical composition

`external source → AbsorptionEnvelope → SymbiontPatternIntake → Symbiont Lab → Evolution Gate`

The implementation only composes existing ELO authorities. It does not create a second registry, memory authority, authorization engine, evolution engine or provider runtime.

## Fail-closed requirements

- missing evidence is rejected;
- source lineage mismatch is rejected;
- invalid tenant scope is rejected by the existing intake contract;
- non-compatible Evolution Gate classifications do not create a lab observation;
- Hermes remains comparative evidence only;
- no canonical promotion or main mutation occurs inside the runtime bridge.

## Validation target

The candidate must pass the repository Evolution Gate, canonical/full tests, external-access security, behavioral, baseline evidence, maintenance and Pages checks. After merge, the resulting `main` SHA must receive a post-merge regression before the next pair advances.
