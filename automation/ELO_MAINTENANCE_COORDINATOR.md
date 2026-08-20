# ELO Maintenance Coordinator v1

## Purpose

Formalize the autonomous maintenance loop between ELO Cognitivo, GitHub, Forge and domain specialists without creating a second cognitive authority.

The coordinator may inspect stalled Issues/PRs, determine whether the evidence is sufficient for the next governed transition, identify the specialist lane, request/record specialist consultation, and prepare a merge recommendation.

It does **not** infer approval from silence, bypass branch protection, or promote experience into canonical architecture without identity and evidence validation.

## Authority model

- **ELO Cognitivo:** semantic and architectural authority; decides whether an observation becomes a canonical evolution.
- **GitHub:** durable execution ledger and merge control plane.
- **Forge:** implementation/construction plane.
- **Specialist:** bounded domain evidence provider.
- **Coordinator:** deterministic process executor. It does not become a new supervisor or Core.

## Maintenance loop

`SCAN → CLASSIFY → IDENTIFY_OWNER → CHECK_CONSUMERS → CHECK_REFERENCES → CHECK_SPECIALIST → AUDIT_GATES → DECIDE → REQUEST_ACTION → VALIDATE → MERGE/RETURN → REVERIFY → LEARN`

For architectural maintenance, the coordinator must apply the existing ELO completion loop before removal:

`INVENTORY → concept_id → COMPARE → CLASSIFY → OWNER → CONSUMERS → REFERENCES/ALIASES → DECISION → ABSORB → TEST → CI → DEPRECATE → REMOVE → MERGE → REVALIDATE`

## Stalled approval audit

An open Issue or PR can be audited when it carries a governed ELO marker such as `elo/pending-approval`, `elo/merge-candidate`, or `elo/domain-*`.

The audit evaluates:

1. explicit objective and acceptance criteria;
2. changed scope;
3. required specialist lane;
4. specialist finding status;
5. CI status;
6. unresolved review findings;
7. evidence and traceability;
8. branch/base protection;
9. destructive or irreversible operations;
10. explicit ELO merge authorization.

Only the conjunction below permits a merge recommendation:

`ACCEPTANCE_PASS ∧ SPECIALIST_PASS ∧ CI_PASS ∧ REVIEWS_CLEAR ∧ SCOPE_COMPLIANT ∧ NO_FORBIDDEN_ACTION ∧ ELO_APPROVE_MERGE`

The coordinator may enable the repository's existing auto-merge mechanism only after all gates pass and the explicit `elo/approve-merge` authorization is present. It never manufactures that authorization.

## Specialist routing

| Event class | Specialist lane |
|---|---|
| architecture, structure, duplicate folders, canonical identity | Architecture |
| budget, costing, calculation, commercial evolution | Domain + Finance/Costing |
| regulatory, standards, compliance | Domain + Regulatory |
| security, identity, access, secrets | Security |
| data, schema, migration, provenance | Data |
| automation, CI/CD, runtime, deployment | Operations/Automation |
| tests, gates, regressions | Testing |
| memory, learning, experience admission | Cognitive/Knowledge |

The coordinator records the specialist lane and creates a consultation request as durable evidence. The specialist supplies evidence; ELO makes the canonical decision.

## Conversation handoff

When a user opens a conversation about an Issue/event, ELO should resolve the event to its canonical identity and ask the specialist question before proposing an evolution when domain evidence is required.

Example contract:

```yaml
event:
  issue: 000
  concept_id: "ELO.<domain>.<canonical-id>"
  event_class: "budget"
specialist:
  lane: "domain-finance"
  question: "Can this capability be admitted as the next governed evolution?"
evidence:
  required: true
evolution:
  target: "canonical-architecture | temporal-experience | reject | roadmap"
  canonical_identity_required: true
elo_decision:
  status: "PENDING_SPECIALIST"
```

## Experience versus architecture

A useful experience is **not automatically an architectural change**.

The coordinator classifies the outcome as:

- `ARCHITECTURAL_EVOLUTION`: changes canonical structure, contracts, governance, runtime boundaries, schemas, or permanent capability ownership.
- `TEMPORAL_EXPERIENCE`: valuable bounded learning that should be retained as experience/memory without changing canonical structure.
- `ROADMAP_CANDIDATE`: valuable but insufficiently validated for admission.
- `REJECTED`: inconsistent, redundant, unsafe, unsupported, or without durable value.

For `TEMPORAL_EXPERIENCE`, the experience must have:

- canonical `concept_id` or event identity;
- provenance;
- source/evidence references;
- confidence/status;
- applicability boundary;
- timestamp/cycle;
- no contradiction with canonical rules;
- explicit ELO admission decision.

For `ARCHITECTURAL_EVOLUTION`, the normal architecture gates and PR/merge process remain mandatory.

## Optimistic high-value experience

An experience described as highly valuable or optimistic is only a **candidate**. ELO must evaluate it against canonical identity, evidence quality, repeatability/applicability, contradiction risk, and architectural impact before recording it.

No free-form conversation becomes canonical memory merely because it was useful.

## Terminal states

- `READY_FOR_SPECIALIST`
- `WAITING_FOR_EVIDENCE`
- `READY_FOR_ELO_DECISION`
- `APPROVED_FOR_MERGE`
- `RECORDED_AS_TEMPORAL_EXPERIENCE`
- `ROADMAP_CANDIDATE`
- `REJECTED`
- `BLOCKED`

Every automated transition must leave an auditable GitHub comment, label/state change, or repository evidence record.
