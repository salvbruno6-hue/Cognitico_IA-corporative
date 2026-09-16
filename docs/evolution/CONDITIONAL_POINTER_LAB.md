# ELO Conditional Pointer Laboratory

## Purpose

Validate a bounded hypothesis observed in Hermes and OpenClaw: an incoming information condition can resolve to an **existing ELO capability** and an explicit destination without creating a second authority.

## Controlled chain

`information → condition → relation → existing capability → destination → policy requirement`

The laboratory is deterministic and side-effect free. It does not execute external tools, authorize real operations, mutate canonical knowledge, or promote learning.

## Current matrix

| Condition | Existing ELO capability | Destination | Policy check |
|---|---|---|---|
| semantic-recall | HERMES-MEMORY | ELO_CONTEXT_MEMORY | required |
| context-resolution | HERMES-CONTEXT | ELO_CONTEXT | not required |
| skill-execution | HERMES-SKILLS | ELO_SKILL_RUNTIME | required |
| tool-resolution | HERMES-TOOLSETS | ELO_ROUTING | required |
| delegation | HERMES-DELEGATION | ELO_ROUTING | required |
| schedule | HERMES-AUTOMATION | ELO_SCHEDULER | required |
| external-capability | HERMES-MCP | ELO_ROUTING | required |
| state-recovery | HERMES-CHECKPOINT | ELO_STATE_RECOVERY | not required |

## Safety conditions

- Existing ELO capability IDs are reused; no second capability registry is introduced.
- Unknown conditions remain `unresolved`; the lab never guesses a destination.
- Every evidence record remains `candidate_only`.
- `canonical_mutation` is always `false`.
- Successful resolution is a laboratory result, not cognitive promotion.

## Source relationship

The mapping is an ELO laboratory hypothesis derived from mechanisms observed in the Hermes and OpenClaw repositories. The external mechanisms are evidence sources, not ELO authorities.

## Next Evolution Gate requirement

Before any canonical adoption, the mapping must undergo independent consistency checks, controlled functional tests, repeatability/regression testing, governance review, and the existing Evolution Gate. No successful laboratory run is sufficient for generalized learning.
