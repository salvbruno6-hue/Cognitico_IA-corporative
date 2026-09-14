# ProcessView + Capability Absorption — P0 cycle

## Canonical boundary

`ProcessView` is a Cognitive boundary, not a frontend telemetry authority. The provider is injected by the owning runtime. `CURRENT` and `DEVIATION` require governed evidence and source lineage. `UNKNOWN` requires an explicit GAP; the implementation never invents endpoint, table, telemetry or authority.

Flow:

`ELO Web → Cognitive ProcessView boundary → governed provider → evidence`

## Capability absorption

The native absorption boundary is deliberately downstream of the existing `AbsorptionEnvelope → SymbiontPatternIntake → Symbiont Lab` path. It does not recreate intake, laboratory, memory, registry or Evolution Gate. It accepts only laboratory observations with regression `PASS` and confirmed generalization, then emits `CANDIDATE_ONLY` while preserving source commit, evidence, tenant and scope lineage.

Hermes is an evidence/provider source, never the canonical owner. A Hermes mechanism becomes an ELO capability only after generalization, evidence, regression and existing governance permit the candidate; this implementation does not promote it automatically.

## Required invariants

- tenant and process identity remain bound;
- CURRENT/DEVIATION cannot exist without evidence and source;
- UNKNOWN is explicit rather than synthetic;
- capability candidates retain provenance and evidence;
- regression failure or unconfirmed generalization blocks absorption;
- no authorization grant, provider registry write, Core mutation or memory mutation occurs;
- Evolution Gate remains the canonical promotion authority.

## Potencialização para o ELO

This pair closes two complementary gaps: it gives the ELO Web a truthful Cognitive process-state boundary, while turning validated external mechanisms into reusable native candidates without making the external provider a dependency or authority.
