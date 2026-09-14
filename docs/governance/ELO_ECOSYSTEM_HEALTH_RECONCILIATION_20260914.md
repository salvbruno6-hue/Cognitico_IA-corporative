# ELO — Ecosystem Health Reconciliation

## Acceptance method

`Relations → Code → Instructions → Contracts → Evidence → Governance → Tests → Merge → ON_MAIN → Post-merge Regression → Learning`

For every capability, verify ownership and relationships among Cognitive, Core, Forge, Symbiont, Governance, Application and Infrastructure; inspect contracts, dependencies, types, tests and fail-closed behavior; verify operating and architectural instructions; preserve provenance, evidence, tenant scope and candidate-only boundaries; and assess duplication, authority conflicts, security, recovery and maintainability.

A retrospective correction is justified only when it improves structural health without creating a second authority or destabilizing canonical behavior.

## Recent P0 reconciliation

| Cycle | Capability | Relation | Disposition | Potentialization |
|---|---|---|---|---|
| #501 | Research | Cognitive + Forge | Retain; evidence-bearing candidate-only path | Investigation, evidence synthesis and hypothesis formation |
| #502 | Domain Intelligence + Autonomous Reasoning | Cognitive + Core | Retain; provider-neutral and bounded | Contextual understanding, planning and governed autonomy |
| #503 | Security + MCP | Governance + Cognitive + Symbiont | Retain; security evidence-first, MCP as mechanism | Resilience and safe external capability experimentation |
| #504 | Skill Authoring + Knowledge Capture | Forge + Cognitive | Retain; deterministic candidate/conflict handling | Capability evolution and cognitive memory quality |
| #505 | Software Engineering + Absorption Governance | Core + Symbiont + Governance | Retain; diagnostic/regression cycle and provenance envelope | Self-correction and safe external-mechanism absorption |
| #506 | External Intake + Symbiont Lab | Symbiont + Cognitive + Forge | Retain; composes canonical intake/lab authorities | Controlled experimentation and mechanism absorption |
| #507 | MCP Test Harness | Symbiont + Forge | Retain; existing execution bridge, candidate-only | Bounded, measurable external-tool experimentation |
| #508 | ProcessView + Capability Absorption | Cognitive + Symbiont + Governance | Retain; reference/current/deviation/unknown separation | Operational perception and governed incorporation |

## Findings

1. No rewrite is justified for #501–#508: their critical authority boundaries remain coherent and they reuse canonical contracts rather than introducing parallel registries, gates or authorities.
2. Stale branches whose intent is already represented by newer canonical implementations are not active evolution paths and should be closed to prevent parallel evolution.
3. #489 is closed rather than merged. Its browser-boundary portion was superseded by the server-side `elo-authz` path. Its broad database migration requires a separate current-main database/schema audit before any relation is materialized.
4. Vercel `elo_elo` remains outside the current ELO evolution criterion per the project decision.

## Future invariant

A unit-test pass alone is insufficient. Promotion requires structural coherence plus post-merge validation on the resulting `main` SHA. Failures remain open until corrected or an external block is evidenced.

The next pair starts from a current-main audit, not from an assumption that new parallel DevOps/MLOps structures are required.
