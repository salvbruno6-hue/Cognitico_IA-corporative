# ELO Forge → Cognitico Consolidation Matrix

| Forge class | Canonical treatment | Destination | Decision |
|---|---|---|---|
| Specialist guidance | Extract validated rules | `04-knowledge-handbook/`, `05-cognitive-platform/`, or existing agent contract | PROMOTE/EXTEND |
| Domain knowledge | Governed knowledge promotion | existing knowledge/faculty/overlay mechanism | PROMOTE/REUSE/EXTEND |
| Prompts | Convert to controlled agent assets | `15-assets/` or existing agent contract | REUSE/EXTEND |
| Automation | Reconcile with existing workflows and runtime | `.github/workflows/`, `src/elo/`, existing automation contracts | EXTEND |
| APIs | Reconcile with existing integration boundary | `src/elo/` / approved integration owner | REUSE/EXTEND |
| SQL/schema | Extract validated data rules; migrate only under explicit data task | `07-data-engineering/` / canonical schema owner | REUSE/EXTEND/ROADMAP |
| Dashboards | Evaluate as observability/UI capability | `12-systems/` or existing observability owner | REUSE/EXTEND/ROADMAP |
| Blueprint/architecture drafts | Use as evidence, not authority | `10-adr/` or `14-roadmap/` | COMPARE/ROADMAP |
| Duplicate or superseded material | Preserve traceability, do not duplicate | existing canonical owner | REJECT/SUPERSEDE |
| Generated workspace artifacts | Do not promote | none | REJECT |

## Mandatory invariant

The migration must never create a second Cognitive Core, memory authority, Orchestrator, knowledge source of truth, or security boundary.

## Promotion evidence

Every promoted artifact must identify:

- source path/repository;
- classification;
- canonical owner;
- reason;
- validation evidence;
- destination;
- status.

## Current architectural finding

The Cognitico repository already contains governed mechanisms for Forge knowledge promotion, corporate orchestration, cycle memory, learning classification and decision relationships. Therefore consolidation is selective integration, not repository cloning.
