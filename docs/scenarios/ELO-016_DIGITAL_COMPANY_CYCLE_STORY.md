# ELO-016 — Digital Company Cycle Story

## Purpose

Run the digital company as a controlled narrative scenario for the ELO-015 orchestrator. The story is an executable test model: every chapter has a state, event, evidence, actor/domain, expected decision, possible action, and observable outcome.

## Canonical cycle

`OBSERVE → CONTEXTUALIZE → ANALYZE → PROJECT → DECIDE/HANDOFF → EXECUTE → MONITOR → OUTCOME FEEDBACK → LEARN/EVOLVE`

## Story

### Chapter 1 — The opportunity

Commercial receives a new opportunity with customer, scope, target value, requested deadline, and initial assumptions.

**Evidence:** opportunity record and source timestamp.

**Expected ELO behavior:** identify entities, domain, tenant/principal, current state, missing evidence, and relevant specialists.

### Chapter 2 — The rulebook

Licitações checks whether contractual or tender requirements change the commercial assumptions.

**Expected behavior:** distinguish confirmed requirements from assumptions; do not promote unsupported requirements.

### Chapter 3 — The number

Orçamento builds the initial cost model, margin, contingency, and dependencies.

**Expected behavior:** expose calculation inputs and provenance; mark incomplete inputs as gaps rather than inventing values.

### Chapter 4 — The change

Projeto introduces a technical change affecting material, labor, lead time, or scope.

**Expected behavior:** propagate the change through the canonical cross-domain model and identify affected downstream states.

### Chapter 5 — The capacity test

PCP evaluates capacity and schedule. Produção confirms or rejects the assumed production window.

**Expected behavior:** detect agreement, divergence, or unresolved conflict between specialist evidence.

### Chapter 6 — The delivery constraint

Logística evaluates the delivery window and dependencies.

**Expected behavior:** combine production and logistics constraints without overwriting either domain's source evidence.

### Chapter 7 — The ELO decision

The orchestrator compares the complete state and produces one of: supported path, conditional path, conflict, inconclusive result, or blocked execution.

**Execution rule:** an action may execute only when authority and evidence requirements are satisfied. Otherwise the ELO creates a structured handoff.

### Chapter 8 — The consequence

The authorized action occurs or the human handoff is resolved. New state evidence enters the system.

**Expected behavior:** monitor whether the predicted consequence matches the observed result.

### Chapter 9 — The learning event

The ELO compares prediction versus outcome.

**Promotion rule:** only validated knowledge may become canonical. A domain-specific variation remains an overlay unless promoted through the established governance path.

### Chapter 10 — The second company cycle

The same story is executed again with one controlled variation: a different specialist model, a changed rule, or a changed operational constraint.

**Expected behavior:** recognize the existing essential faculty, isolate the variation, compare it with the previous cycle, and avoid creating a duplicate structure-seed.

## Test variants

1. Nominal flow — all evidence available.
2. Premise change — technical change after budget creation.
3. Specialist conflict — two valid sources disagree.
4. Evidence gap — a required input is missing.
5. Authorization gap — action is requested without execution authority.
6. Overlay variation — new specialist uses a different but compatible mechanic.
7. Failure/recovery — an execution outcome differs from projection.
8. Repeated cycle — second run tests whether learning is consistent and traceable.

## Observation contract

For every chapter capture:

- `tenant_id`
- `principal_id`
- `domain`
- `process`
- `event`
- `state_before`
- `evidence`
- `specialist`
- `decision`
- `authorization`
- `action`
- `state_after`
- `outcome`
- `provenance`
- `knowledge_promotion_status`

## Expected monitoring

The monitor must detect:

- state transitions;
- unresolved conflicts;
- missing evidence;
- unauthorized actions;
- predicted-versus-observed deviation;
- repeated failures;
- new compatible mechanics;
- accidental duplication of canonical structures.

## Success criteria

The cycle passes only if the ELO can:

1. reconstruct the story from evidence;
2. cross the participating domains without losing provenance;
3. distinguish fact, assumption, inference, recommendation, and decision;
4. stop unauthorized execution;
5. monitor the result of authorized execution;
6. compare predicted and observed outcomes;
7. preserve the essential faculty while isolating overlays;
8. repeat the cycle without creating a second Core, memory, or organizational seed.

## Gate

`CI PASS + Behavioral Validation PASS + Evolution Gate PASS + no unresolved canonical conflict = eligible for merge.`
