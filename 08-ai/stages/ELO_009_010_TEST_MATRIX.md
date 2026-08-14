# ELO-009 / ELO-010 — Test Matrix

| ID | Scenario | Expected |
|---|---|---|
| S9-01 | tenant/domain graph traversal | PASS only inside boundary |
| S9-02 | foreign changed node | DENY / ValueError |
| S9-03 | indirect dependency | deterministic impact propagation |
| S9-04 | constraint exceeded | explicit conflict |
| S9-05 | alternatives | deterministic ranking |
| S9-06 | evidence | references preserved |
| S9-07 | contradiction | `PLAN WITH INCONSISTENCIES` |
| S9-08 | no alternative | explicit no-feasible state |
| S10-01 | valid replan proposal | new version + pending approval |
| S10-02 | conflicting replan | no version advance |
| S10-03 | approval | explicit human principal recorded |
| S10-04 | invalid approval transition | denied |
| S10-05 | rejection | explicit rejected state |
| S10-06 | supersession | old version marked superseded |
| S10-07 | broken lineage | denied |
| S10-08 | operational execution | not implemented by this layer |

## Adversarial coverage

- cross-tenant dependency injection;
- cross-domain changed node;
- contradictory constraints;
- missing evidence;
- empty alternative set;
- unauthorized approval transition;
- malformed supersession lineage;
- deterministic tie ordering.

The executable suite is intentionally dependency-free and runs with Python `unittest` so the gate can execute in CI without a provider, database or external service.
