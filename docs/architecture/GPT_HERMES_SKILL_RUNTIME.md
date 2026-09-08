# GPT → IntentSpec → ELO Cognitive → Hermes Skill Runtime

## Runtime responsibility

- **GPT/OpenAI:** interprets natural-language requests and produces an IntentSpec.
- **ELO Cognitive:** resolves tenant/context/authorization and decides whether execution is governed.
- **Hermes:** executes the authorized mission and returns evidence/outcome.
- **Skills Factory:** may create reusable operational skills, but their state is non-canonical until ELO governance promotes them.
- **Supabase:** persists governed application data and authorization state; infrastructure identifiers remain internal.

## Existing OpenAI API

Hermes already supports the direct OpenAI API provider through `OPENAI_API_KEY` and `OPENAI_BASE_URL`; this project does not introduce a second OpenAI credential path.

## Skill execution rule

A skill may execute only after ELO supplies:

1. `request_id`
2. `intent`
3. `tenant_scope`
4. `mission_class`
5. `authorized_capabilities`
6. bounded context
7. evidence requirements

The Hermes bridge must reject infrastructure identifiers such as `project_id`, `project_ref`, Supabase URLs, or database URLs.

## Learning rule

Hermes-created skills are observations/candidates. They must remain `candidate_only`, `pending`, or `rejected`. Hermes cannot emit `decision` or `canonical_knowledge` as part of a learning candidate.

## Operational consequence

The OpenAI API being already configured is not itself the execution authority. The missing piece is the governed runtime handoff that allows Hermes' existing Skills Factory to operate on an ELO-authorized IntentSpec instead of being blocked by an absent ELO envelope.
