# ELO-003 — Post-Merge Regression Gate

The ELO-003 mainline reconciliation was merged, but validation exposed regressions in the current mainline behavior.

This gate is corrective, not a second agent architecture.

## Corrections

1. ContextResolver accepts canonical CognitiveRequest and mapping payloads.
2. Source discovery selects the most specific intent when multiple keywords occur.
3. Conversation intake remains temporal until explicit promotion.
4. Conversation bridge schema version 1.1 is asserted by tests.
5. ELO-002 contextual-memory intake remains compatible with mapping payloads.

## Merge criteria

- compileall succeeds;
- full pytest succeeds;
- ELO-001 regression succeeds;
- ELO-002 regression succeeds;
- tenant/domain isolation remains enforced;
- no autonomous execution is introduced;
- no second Cognitive Core is introduced.
