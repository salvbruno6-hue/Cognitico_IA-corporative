# ELO: Matt Pocock operational adapter (controlled runtime)

Source: mattpocock/skills pinned to 4ae2317ddb22b046e26455e4f9c9b3aaaf62212d.
Owner: ELO Knowledge & Skills / Forge, consulted through existing GovernedOrchestrator.
Authority: existing elo-authz, ExecutionBoundary, SymbiontPatternIntake and Evolution Gate.

## What was integrated

* ExternalSkillCatalog validates the 39 imported SKILL.md identities, namespace, per-file Git SHA and manual-only wrappers.
* GovernedOrchestrator.invoke_external_skill is the ELO-owned entrypoint for a caller-specified skill, approved_skill_ids, and injected executor. It rejects absent or expired elo-authz decisions, wrong resource/identity, missing evidence, and missing correlation. No automatic routing, plugin installation, command execution or model selection is introduced.
* The existing ExecutionBoundary processes an explicit ExecutionRequest and returns ExecutionOutcome.
* SymbiontSkillRuntime.observe_external_skill_invocation consumes only a successful outcome carrying runtime_evidence_ref, then calls the existing SymbiontPatternIntake / Evolution Gate as REUSE of ELO Knowledge & Skills / Forge. It does not promote.
* The upstream catalog is untrusted source text, never an authority to override ELO.

## What the controlled evidence proves

The test suite exercises all 39 skills through Orchestrator -> ExecutionBoundary -> an injected local controlled executor -> Symbiont. It also checks missing authorization, wrong principal/resource, expired authorization, missing evidence, invalid source hashes, and missing runtime evidence.

The tests are real repository-local calls, but the executor is a fixture. They **do not** prove production invocation, real provider behavior, user consent for unrestricted scripts, runtime deployment, or approval of each imported workflow for automatic execution.

## Invariants

None of the imported skill instructions, scripts, installers or hooks is executed automatically. Upstream experimental and miscellaneous skills remain manual-only, as do all other imported wrappers. No Supabase records, capability registry, Core, Forge canonical skill registry, authorizations or production datasets are modified. Operational activation beyond the controlled harness requires the canonical agent runtime to supply a real approved handler and valid elo-authz grant, then produce external runtime evidence, pass gates and merge through the established path.
