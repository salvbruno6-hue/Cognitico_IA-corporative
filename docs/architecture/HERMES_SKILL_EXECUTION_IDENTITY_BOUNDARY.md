# Hermes Skill Execution Identity Boundary

## Purpose

Record the validated ELO boundary derived from Hermes' explicit skill execution metadata: a governed skill execution must carry both `skill_id` and `decision_id`.

This mechanism is an ELO contract boundary. It does not authorize a capability, execute Hermes, persist memory, or promote learning.

## Contract

```text
authorized capability
        +
skill_id
        +
decision_id
        ↓
HermesExecutionRequest
```

The validation occurs when `HermesExecutionRequest` is constructed, making the constraint part of the existing canonical ELO ↔ Hermes request contract rather than a second authorization mechanism.

Capabilities unrelated to skill execution are not required to provide these fields.

## Evidence boundary

The fields identify provenance:

- `skill_id`: which ELO/Hermes skill is being invoked;
- `decision_id`: which prior governed decision provides the execution context.

They do not establish that the skill is authorized. Authorization remains the responsibility of the existing ELO capability boundary.

They do not establish learning or canonical knowledge. Hermes results remain evidence/outcome and learning candidates remain non-canonical.

## Controlled validation

The acceptance tests cover:

1. `skill:create` without identity → rejected;
2. `skill:execute` without identity → rejected;
3. missing `decision_id` → rejected;
4. both identifiers present → accepted;
5. non-skill capabilities → not forced to carry skill identity;
6. blank identifiers → rejected.

No business operation or Hermes runtime call is required by these tests.
## Validation status

CI validation is required before this candidate can be considered validated or merged.
