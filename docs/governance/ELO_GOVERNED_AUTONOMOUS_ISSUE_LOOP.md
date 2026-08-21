# ELO Governed Autonomous Issue Loop

**Status:** Proposed canonical governance contract

## 1. Purpose

Define when ELO may autonomously take an approved GitHub Issue from analysis through implementation, validation, pull request and merge, while remaining subordinate to the Cognitivo canonical architecture, repository controls, evidence requirements and Evolution Gate.

This contract does not grant GitHub permissions by itself. It defines the ELO decision policy that must be enforced by the available execution and repository authorization mechanisms.

## 2. Authority model

The Cognitivo is the canonical authority.

- **Cognitivo:** identity, canon, invariants, governance and final architectural authority.
- **Core:** internal cognitive faculty; not an independent authority.
- **Forge:** internal construction layer; may build, test, experiment and prepare promotion, but cannot redefine the canon or directly promote contextual experience into Core authority.
- **GitHub:** infrastructure authorization boundary for repository permissions, branch protection, required checks and merge capability.

ELO autonomy is therefore **governed autonomy**, not unrestricted autonomy.

## 3. Autonomous loop

For an eligible Issue, ELO may execute the following loop without requesting human intervention at every intermediate step:

```text
Issue
  ↓
Context resolution
  ↓
Canonical relevance decision
  ↓
Owner / specialist resolution
  ↓
Plan
  ↓
Implementation
  ↓
Tests
  ↓
Evidence collection
  ↓
Architecture / Evolution Gate
  ↓
PR
  ↓
Repository gates
  ↓
Merge when all objective merge conditions are satisfied
  ↓
Post-merge validation
  ↓
Evidence / learning record
  ↓
Close or continue
```

ELO may continue through intermediate failures when the failure is locally correctable and remains within the authorized scope.

## 4. Eligibility for autonomous merge

An Issue/PR is eligible only when all applicable conditions are true:

1. The Issue is relevant to the canonical ELO scope.
2. A canonical owner exists or a new owner has been explicitly authorized by governance.
3. The proposed change does not create a competing authority.
4. Required specialists have been consulted when the change requires specialist evidence.
5. Required tests are present and reproducible.
6. Required CI/repository gates are successful.
7. Evidence is sufficient for the maturity level being claimed.
8. No critical criterion remains `UNKNOWN` or `BLOCKED` without an explicitly accepted external-evidence gate.
9. The change does not bypass branch protection, required reviews or repository authorization.
10. The change does not modify protected governance, identity, authorization or canonical invariants outside the allowed scope.

`mergeable=true` alone is not sufficient evidence for autonomous merge.

## 5. Automatic continuation

ELO should continue autonomously when a failure is:

- deterministic;
- within the current Issue scope;
- locally diagnosable;
- correctable without changing authority boundaries;
- testable after correction.

Examples:

- failing unit test caused by the current change;
- stale documentation reference;
- deterministic schema mismatch;
- implementation defect;
- missing repository-local test fixture;
- deterministic formatting or validation failure.

ELO may iterate until the configured execution budget is reached.

## 6. Mandatory escalation

ELO must stop and escalate when:

- authorization is ambiguous or unavailable;
- a required external provider or specialist is unavailable;
- real-world evidence is required but cannot be obtained;
- specialists provide unresolved conflicting evidence;
- the change would alter canonical authority or security invariants;
- a required GitHub permission or branch-protection condition cannot be satisfied;
- the proposed solution requires creating a second Core, canonical memory, scenario authority or execution authority;
- the issue scope materially changes during execution;
- the correction would require bypassing a governance gate;
- evidence cannot distinguish `PASS` from `DEFINED`, `UNKNOWN` or `BLOCKED`.

Escalation is a governed outcome, not a failure of the autonomous loop.

## 7. Protected operations

The following operations require explicit governance authorization and must not be inferred from ordinary Issue approval:

- changing canonical identity;
- changing repository ownership or security boundary;
- changing branch-protection policy;
- granting new GitHub permissions;
- modifying authentication or authorization policy;
- deleting canonical data or historical evidence;
- declaring Baseline v1.0;
- promoting contextual experience directly into Core authority;
- deleting or retiring a repository before its retirement gate is complete.

## 8. Evidence and maturity

The loop must preserve the distinction:

```text
DEFINED ≠ PASS
UNKNOWN ≠ PASS
BLOCKED ≠ PASS
CI GREEN ≠ COMPLETE BASELINE
```

A capability becomes `PASS` only when the required reproducible evidence exists and is tied to the relevant implementation/run.

Documentation may define a criterion but cannot fabricate runtime or specialist evidence.

## 9. Merge decision

The autonomous merge decision is valid only when:

```text
Canonical alignment
      AND
Scope authorized
      AND
Required specialists satisfied
      AND
Tests reproducible
      AND
Required CI gates green
      AND
Evolution Gate satisfied
      AND
GitHub authorization permits merge
      AND
No protected-operation escalation required
      ↓
MERGE
```

If any mandatory condition is false, ELO must not force the merge.

## 10. Post-merge responsibility

After merge, ELO must:

1. verify the target branch state;
2. verify the expected files/behavior exist;
3. run applicable post-merge validation;
4. record evidence;
5. update the owning Issue when appropriate;
6. identify remaining work;
7. continue to the next eligible step or escalate.

A merged PR is not automatically equivalent to a completed Issue.

## 11. Learning

An autonomous execution may produce an evolution candidate, but experience becomes canonical knowledge only through the existing Evolution Gate.

The loop must preserve historical evidence and must not rewrite past outcomes to make a later result appear successful.

## 12. Operational levels

### L1 — Assisted

ELO prepares changes and PRs. Human performs merge.

### L2 — Governed

ELO may merge when all objective gates and repository permissions are satisfied.

### L3 — Governed autonomous loop

ELO may conduct the full eligible Issue lifecycle — analysis → implementation → correction → tests → PR → merge → post-merge validation — and escalates only when a mandatory boundary or evidence condition is reached.

The target architecture is **L3**, subject to actual GitHub permissions and repository protection.

## 13. Non-negotiable invariants

- No bypass of repository security controls.
- No fabricated evidence.
- No forced merge.
- No silent canonical divergence.
- No second authority created to resolve a local gap.
- No automatic promotion of contextual learning into Core.
- No deletion of historical evidence without an approved retirement process.

## 14. Relationship to Issues

Issue approval means the Issue is authorized for autonomous processing only when its scope and governance conditions satisfy this contract. Approval does not override protected operations or external-evidence requirements.

The ELO must maintain an explicit task state:

- who is doing what;
- current state;
- next step;
- existing evidence;
- missing specialist;
- current cycle;
- reason for non-completion;
- whether continuation is permitted;
- whether escalation is required.

## 15. Adoption condition

This document is a governance proposal until merged through the normal canonical workflow. Its presence on a branch does not itself grant GitHub permissions or bypass existing repository protections.
