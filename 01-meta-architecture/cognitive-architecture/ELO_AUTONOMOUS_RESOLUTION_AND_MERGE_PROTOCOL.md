# ELO — Autonomous Resolution and Merge Protocol

**Status:** PROPOSED / CONTROLLED-AUTONOMY
**Scope:** ELO Cognitive Architecture, agent orchestration, engineering execution

## 1. Objective

Allow ELO to remain engaged with a clearly defined engineering objective for as long as necessary to reach a validated terminal state, reducing the need for continuous human intervention while preserving the canonical architecture as the authority.

The intended operating model is:

`objective → inspect → plan → delegate → implement → validate → reconcile → correct → revalidate → approve → merge → verify`

The human should normally receive the result, not be required to manually drive every intermediate step.

## 2. Canonical authority rule

The canonical ELO architecture remains authoritative.

When an implementation diverges from the canonical architecture, the default autonomous action is **to adapt the implementation to the canonical architecture**, not to silently rewrite the canonical architecture.

The ELO may propose a change to the canonical architecture only when evidence indicates that the canonical definition is incomplete, contradictory, obsolete, or no longer fit for purpose. Such a change requires an explicit ADR/evolution record and must not be hidden inside an implementation fix.

## 3. Autonomous convergence loop

For a task with a clear objective, ELO may continue through the following loop without waiting for a human after every step:

1. Inspect repository, contracts, architecture, tests and current state.
2. Decompose the objective into bounded executable tasks.
3. Select the appropriate specialist(s).
4. Delegate implementation to the execution agent/Codex.
5. Run tests and validation.
6. Compare the result with canonical architecture and contracts.
7. Classify each divergence as:
   - implementation defect;
   - contract mismatch;
   - duplicate capability;
   - obsolete artifact;
   - missing contract;
   - genuine architectural conflict.
8. Automatically correct implementation-level divergences when the canonical intent is clear.
9. Re-run validation.
10. Repeat until convergence, failure, or an explicit stop condition is reached.
11. Prepare the PR evidence and ELO decision.
12. Merge only when all merge gates are satisfied.
13. Verify the resulting main branch and report the final state.

## 4. Permission model

Automation may be granted the minimum repository permissions required for this loop:

- read repository contents;
- create/update branches;
- create commits;
- create/update issues and task records;
- create/update pull requests;
- write PR comments and review evidence;
- execute configured tests and validation;
- request Codex execution;
- merge a PR **only through the governed ELO merge gate**.

Permissions must not be interpreted as authority to redefine the ELO architecture.

## 5. Automatic correction policy

The agent should automatically correct a divergence when all are true:

- the objective is explicit;
- the canonical contract is identifiable;
- the required change is within the task scope;
- the correction is reversible through Git history;
- tests can validate the correction;
- no new security boundary is introduced;
- no destructive operation is required;
- no competing canonical contract is created.

Examples include:

- adapting an implementation to an existing interface;
- moving an artifact to its canonical location;
- removing an accidental duplicate implementation;
- correcting naming to match canonical vocabulary;
- updating tests to match an approved contract;
- reconciling Forge-derived code with the Cognitico contract.

## 6. Architectural conflict policy

The ELO must not silently resolve a true canonical conflict by guessing.

If two authoritative contracts conflict, ELO should:

1. identify the conflict;
2. collect evidence;
3. identify impacted capabilities;
4. generate alternatives;
5. recommend the safest resolution;
6. create/update an ADR or architecture decision record;
7. apply the approved resolution;
8. continue the implementation loop.

If the repository policy permits ELO-controlled architecture evolution, the decision may be approved by the designated ELO governance mechanism. Otherwise the task enters `ESCALATED` and waits for the required authority.

## 7. Merge gate

A PR may be automatically merged only when all required conditions are true:

- objective is still within declared scope;
- canonical architecture is satisfied;
- required contracts are present and version-compatible;
- tests pass;
- required quality checks pass;
- security checks pass where configured;
- provenance/evidence is recorded;
- no unresolved architectural conflict remains;
- no prohibited file or secret change is present;
- ELO decision is `APPROVE_MERGE`;
- repository branch protection permits the merge.

If any required condition fails, ELO continues correction when safe or enters `ESCALATED` when a human/governance decision is genuinely required.

## 8. Convergence limits

Autonomy must not become an infinite repair loop.

Each task must have:

- maximum correction cycles;
- maximum execution time;
- maximum change scope;
- explicit prohibited operations;
- escalation conditions.

When a limit is reached, preserve all evidence and enter `ESCALATED` rather than making increasingly speculative changes.

## 9. Human-free operation target

For routine, reversible, testable engineering work, the desired experience is:

`user objective → ELO works → ELO reports result`

The user should not need to manually:

- copy prompts between agents;
- inspect every intermediate diff;
- request each correction;
- recreate tasks after a failed test;
- manually synchronize the branch and task state.

Human intervention remains necessary for explicitly governed high-impact decisions, unavailable credentials, irreversible operations, unresolved canonical conflicts, or repository protections that require human approval.

## 10. Evidence and auditability

Every autonomous cycle must leave an evidence trail containing, as applicable:

- task/objective;
- selected specialists;
- implementation agent;
- validation results;
- detected divergences;
- corrections applied;
- architecture decisions;
- final ELO decision;
- merge commit;
- post-merge verification.

Autonomy without evidence is not considered governed ELO execution.

## 11. Relationship to ELO-Forge

The Forge is treated as a source of implementation, experimentation and specialized knowledge during consolidation. It does not become a competing architectural authority.

When Forge-derived implementation is incorporated, the ELO should reconcile it against the Cognitico canonical contracts before merge.

## 12. Terminal states

A task must end in exactly one of these states:

- `MERGED`
- `COMPLETED_WITHOUT_MERGE`
- `ESCALATED`
- `BLOCKED`
- `ABANDONED`

`MERGED` requires post-merge verification. A successful commit alone is not sufficient.
