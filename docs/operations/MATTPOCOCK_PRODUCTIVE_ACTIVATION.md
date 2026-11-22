---
id: ELO-MATTPOCOCK-PRODUCTIVE-ACTIVATION
name: Governed Matt Pocock skill productive activation
type: implementation
layer: system
owner: ELO Knowledge & Skills / Forge
status: implemented
authority: reference
version: 0.1.0
related:
  - docs/evolution/MATTPOCOCK_SKILLS_OPERATIONAL_INTEGRATION.md
  - docs/governance/ELO_MERGE_COORDINATOR.md
depends_on:
  - ELO ExecutionRouter
  - ELO ExecutionBoundary
  - elo-authz
  - ELO Evolution Gate
---

# Matt Pocock: productive activation path

## Current verified boundary

The pinned catalog contains 39 external skills. The canonical Orchestrator and Symbiont already support a controlled adapter. The new `MattPocockProviderExecutor` is a **real provider-capable execution adapter** that calls the existing `IntelligenceRouter.execute_routed` (and therefore an already-selected `AIProvider.generate`) without adding a provider registry or changing the ELO Core.

The `EloAuthzExternalSkillVerifier` validates a live Supabase `elo-authz` grant for the **exact** skill ID, tenant, repository, ELO identity, session, binding, grant, request and expiry. It uses the existing `check_authorization_state` action and requires an active, authenticated ELO user bearer token. A caller-supplied `AuthorizationDecision` is insufficient without server confirmation.

Operational composition by the authorized ELO application layer:

1. The existing authenticated ELO ingress establishes a session and uses the canonical `elo-authz` decision to construct `AuthorizationDecision` for resource `mattpocock:<skill>` and operation `execute`. The canonical grant being verified by the adapter must have authorization state `elo-execution-authorized` and operation `execute_external_skill`; no grant is created by this adapter.
2. The existing `ExecutionRouter.route(skill_id, models=...)` chooses a model explicitly supported by the *operator-supplied provider capability evidence*; do not hardcode a model or assume a provider is configured.
3. The application injects the existing `IntelligenceRouter` with configured providers (for example, `OpenAIProvider` with `OPENAI_API_KEY` supplied only in the protected runtime).
4. The application injects its canonical tenant-scoped `EvidenceRepository` and a verifier with the **trusted** canonical HTTPS endpoint `https://<project>.supabase.co/functions/v1/elo-authz` plus the authenticated ELO session token.
5. `GovernedOrchestrator.invoke_external_skill(..., approved_skill_ids=frozenset({skill_id}), executor=MattPocockProviderExecutor(...))` invokes the provider only after both orchestrator authorization and the server-side grant check pass.
6. The adapter stores observed provider text as tenant-scoped ELO `Evidence` with source commit, Git blob, request, correlation, provider/model, output hash and grant provenance. It returns that evidence ID to the **existing** Symbiont observer, which classifies the imported skill as REUSE without canonical promotion.

## Activation tiers

| Tier | Requirement | Authority |
| --- | --- | --- |
| Source available | Pinned upstream Git files and hashes | GitHub |
| Controlled wiring | All 39 references through mocked adapter | ELO tests/CI |
| Provider-capable read-only | Real `IntelligenceRouter` and `AIProvider` with fresh `elo-authz` verifier | ELO runtime; **not yet deployed** |
| Productive observation | An actual authenticated provider call, stored tenant-scoped evidence, independent runtime trace and validated operational outcome | ELO + Symbiont |
| Promotion | Generalization, regression evidence, repeated positive observation and Evolution Gate | Canonical ELO governance |

## Safety

- No vendor scripts are executed. External SKILL.md text is an untrusted method reference, never a system or authorization instruction. The existing OpenAI adapter exposes no tools and uses `store=False`.
- The provider executes **text-only analysis**. Claims of filesystem changes, installation, CLI use, external tool dispatch, autonomous agents or production process changes are **not supported** by this adapter.
- All skills remain manual-only. The 12 upstream nonpromoted skills require an explicit `allow_nonpromoted=True` gate in addition to resource-scoped `elo-authz`, and should not be admitted without a separate review.
- An upstream source hash mismatch, missing/expired/mismatched auth grant, missing provider route, empty provider response, or failed evidence storage blocks the observed execution.
- `EvidenceRepository` in the current codebase is **in-memory**. A production activation claim requires an independently verified durable evidence consumer and real deployed ingress. This adapter does not silently create another persistence system, database table, provider credential, or HTTP endpoint.
- No Supabase schema mutation, cognitive learning registration, canonical capability promotion or GitHub merge authorization is performed by this implementation.

## Productive activation checklist

1. Merge PR #1163 only after PR-ready, Maintenance Coordinator, CI, Evolution Gate and **an active grant `elo-merge-authorized` issued by `elo-authz` under CANONICAL_ADMIN**, through the canonical Merge Coordinator.
2. Deploy the approved application/runtime that actually constructs `MattPocockProviderExecutor`, `EloAuthzExternalSkillVerifier` and a canonical provider route; this file alone is not a deployed API.
3. Verify supported provider credentials and external spend/quotas with the operator. Do not store tokens in GitHub code or logs.
4. Issue an explicit resource-bound `elo-execution-authorized` grant through `elo-authz` for one low-risk promoted skill (prefer `mattpocock:diagnosing-bugs` in read-only analysis mode).
5. Make a real authenticated call from the deployed ELO ingress, verify the provider response and its ELO Evidence ID, and record external runtime trace/provenance without exposing private request content.
6. Repeat under independent conditions, inspect Symbiont outcomes, obtain Evolution Gate decision before expanding skill permissions.

**Status is provider-capable implementation / CI verification, not proven live productive invocation.**
