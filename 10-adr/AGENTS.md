# ELO ADR — Local Agent Rules

## When to create an ADR

Create an ADR when a decision has durable architectural consequences, meaningful alternatives, migration implications, security impact, or changes to system boundaries.

Examples:

- canonical implementation root;
- tenant/security boundary;
- persistence strategy;
- AI Gateway boundary;
- decision authority;
- autonomous behavior;
- event contract strategy;
- major data model change.

## ADR structure

Use:

1. ID
2. title
3. status
4. date
5. context
6. problem
7. decision
8. alternatives considered
9. consequences
10. migration/rollback when applicable
11. related artifacts

## Rules

- Do not create duplicate ADRs for the same decision.
- Do not silently rewrite an accepted decision to accommodate code.
- Supersede old decisions explicitly.
- Keep rejected alternatives when they explain important constraints.
