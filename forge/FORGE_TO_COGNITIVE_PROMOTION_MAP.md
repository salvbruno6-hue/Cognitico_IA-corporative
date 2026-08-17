# Forge → Cognitive Promotion Map

## Objective

Provide the permanent boundary between construction and canonical knowledge inside the same repository.

| Source / artifact class | Forge role | Cognitive promotion |
|---|---|---|
| Architectural concept | construct/refine | promote when validated |
| Governance rule | prototype/test | promote only when canonical-compatible |
| Specialist knowledge | build/test | promote as governed knowledge |
| Prompt/agent behavior | experiment | promote as reviewed capability |
| API contract | implement/validate | promote contract, not implementation |
| Automation rule | build/test | promote policy/capability |
| Prototype | experiment | never canonical by existence alone |
| SQL operational | execute | **not promoted by default** |
| Database migration | execute | **not promoted by default** |
| Operational data | execute | **not promoted** |
| Dashboard implementation | execute | promote only KPI/decision semantics when useful |
| Legacy implementation | preserve/analyze | promote only after canonical comparison |

## Canonical precedence

```text
CANONICAL RULE
      >
PROMOTION CONTRACT
      >
FORGE IMPLEMENTATION
      >
EXTERNAL SOURCE
```

This ordering prevents the constructor from becoming a second source of truth.

## Former standalone ELO-Forge

The former `salvbruno6-hue/ELO-Forge` repository is treated as a construction-source archive during migration into the monorepo. Its conceptual artifacts may be mined and reconstructed inside `forge/` and canonical areas.

No blanket repository copy is authorized.

## Promotion test

Before promotion, ELO asks:

1. Does this solve an identified canonical objective?
2. Does it preserve existing invariants?
3. Does it introduce a better capability with evidence?
4. Can the change be tested and rolled back?
5. Does it create an architectural conflict?
6. Is the knowledge more appropriate for Cognitive or only for Forge execution?

If any answer is unresolved, the artifact remains in Forge.
