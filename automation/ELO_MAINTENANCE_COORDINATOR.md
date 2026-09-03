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

## Canonical non-duplication rule

**No new ELO capability, rule, table, workflow, function, authentication path, memory mechanism, gate, adapter, or source of truth may be created until the existing structure has been inventoried and reconciled.**

The default action is **REUSE → STRENGTHEN → REFACTOR → DEPRECATE**, not CREATE.

A proposed component is admissible only when ELO can identify:

1. its canonical `concept_id` and target owner;
2. the existing canonical component that already performs the responsibility, or documented evidence that no equivalent exists;
3. all known producers and consumers;
4. aliases, parallel implementations, overlapping workflows and competing sources of truth;
5. the contract it must satisfy;
6. its dependency and migration impact;
7. the test and evidence path proving that the change does not create a second authority.

### Hard blocking conditions

The coordinator must return `BLOCKED` when:

- a duplicate or parallel capability is detected and the proposal attempts to add another implementation;
- the source of truth is unresolved;
- the proposal conflicts with a canonical contract;
- a structural change is being introduced through an operational path;
- an existing canonical component can satisfy the requirement but the proposal creates a second mechanism instead of strengthening/reusing it.

Missing inventory or reuse analysis is not treated as permission to proceed; it is `WAITING_FOR_EVIDENCE`.

## Maintenance loop

`SCAN → CLASSIFY → IDENTIFY_OWNER → RESOLVE_CANONICAL_ID → CHECK_SOURCE_OF_TRUTH → CHECK_EXISTING_CAPABILITY → CHECK_PRODUCERS/CONSUMERS → CHECK_REFERENCES/ALIASES → CHECK_DUPLICATES → CHECK_CONTRACT_CONFLICTS → CHECK_SPECIALIST → AUDIT_GATES → DECIDE → REQUEST_ACTION → VALIDATE → MERGE/RETURN → REVERIFY → LEARN`

For architectural maintenance, the coordinator must apply the existing ELO completion loop before removal:

`INVENTORY → concept_id → COMPARE → CLASSIFY → OWNER → CONSUMERS → REFERENCES/ALIASES → DECISION → ABSORB → TEST → CI → DEPRECATE → REMOVE → MERGE → REVALIDATE`

## Stalled approval audit

An open Issue or PR can be audited when it carries a governed ELO marker such as `elo/pending-approval`, `elo/merge-candidate`, or `elo/domain-*`.

The audit evaluates:

1. explicit objective and acceptance criteria;
2. changed scope;
3. canonical identity and target;
4. existing capability reuse analysis;
5. producers and consumers;
6. source-of-truth ownership;
7. duplicate/parallel implementation risk;
8. canonical contract conflicts;
9. required specialist lane;
10. specialist finding status;
11. CI status;
12. unresolved review findings;
13. evidence and traceability;
14. branch/base protection;
15. destructive or irreversible operations;
16. explicit ELO merge authorization.

Only the conjunction below permits a merge recommendation:

`CANONICAL_TARGET_RESOLVED ∧ SOURCE_OF_TRUTH_RESOLVED ∧ REUSE_ANALYSIS_COMPLETE ∧ NO_DUPLICATE_OR_PARALLEL ∧ NO_CANONICAL_CONTRACT_CONFLICT ∧ ACCEPTANCE_PASS ∧ SPECIALIST_PASS ∧ CI_PASS ∧ REVIEWS_CLEAR ∧ SCOPE_COMPLIANT ∧ NO_FORBIDDEN_ACTION ∧ ELO_APPROVE_MERGE`

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

The handoff must also expose the reuse/duplication decision before implementation:

```yaml
canonicality:
  target_resolved: true
  source_of_truth_resolved: true
  reuse_analysis_complete: true
  canonical_match_found: false
  duplicate_or_parallel_found: false
  contract_conflict: false
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
