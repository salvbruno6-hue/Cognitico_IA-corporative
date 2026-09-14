# ELO — Native Media + Communication Cycle — 2026-09-14

## Decision

This cycle adds provider-neutral boundaries for Media and Communication. It extends existing ELO layers and does not create a second transport, messaging, media-processing, identity, evidence, learning, registry or authorization authority.

## Relations

- **Media:** Forge/Application adapters → `GovernedMediaBoundary` → evidence/provenance → Cognitive/Learning → Governance/Evolution Gate.
- **Communication:** Application intent → `GovernedCommunicationBoundary` → authorized transport adapter → outcome/evidence → Governance/Evolution Gate.
- External providers are executors or evidence sources only; ELO remains the authority.

## Invariants

1. Tenant and execution identity remain explicit.
2. Media observations require source reference and evidence IDs.
3. Communication requires explicit authorization and idempotency identity.
4. Secret-bearing provenance is rejected.
5. Boundaries do not send messages, mutate canonical memory, grant capabilities or bypass Evolution Gate.
6. Reuse existing Application/Core/Cognitive/Forge contracts before adding new authorities.

## Ecosystem health method

`Relations → Code → Instructions → Contracts → Evidence → Governance → Tests → Merge → ON_MAIN → Post-merge Regression → Learning`

## Potentialization for ELO

- **Media:** enables ELO to ingest and reason over multimodal observations with traceable provenance, while keeping transformations reproducible and governed.
- **Communication:** enables ELO decisions to become auditable communication intents that can be executed by authorized adapters with identity, evidence and idempotency, without transferring authority to a provider.

## Acceptance

The pair is only complete after PR gates pass, merge is confirmed on `main`, exact merge-SHA post-merge validation passes, and the learning/evidence disposition is recorded. Vercel `elo_elo`/frontend failures remain outside the canonical gate when they are the explicitly excluded deployment projects.
