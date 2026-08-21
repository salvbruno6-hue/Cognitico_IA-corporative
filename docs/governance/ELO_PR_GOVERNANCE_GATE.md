# ELO PR Governance Gate

**Status:** Canonical operational governance  
**Scope:** Pull Requests destined for `main`  
**Owner:** ELO Governance

## Purpose

Establish the mandatory ELO review loop that must occur before any specialist or AI-generated change is merged into `main`.

A Pull Request is an execution and evidence boundary. It does not replace ELO governance.

## Mandatory rule

Every PR that can reach `main` MUST pass the complete ELO analysis loop before merge.

The ELO must understand the **purpose of the change** and the **material decisions of the responsible user** before authorizing merge.

## Full review loop

```text
PR created/updated
→ establish repository and PR state
→ identify user objective and purpose
→ recover relevant user decisions and constraints
→ inspect canonical ELO rules, architecture and contracts
→ inspect relevant prior decisions and governed memory
→ inspect complete PR diff
→ classify change and impact
→ test/revalidate applicable behavior
→ verify evidence and provenance
→ detect contradictions
→ reconcile safely
→ verify purpose preservation
→ ELO gate decision
→ PASS: merge
→ REVISE: correct and restart full loop
→ ESCALATE: stop and request authorized human resolution
```

## Purpose gate

The ELO cannot issue `PASS` until it can answer:

1. What problem does this change solve?
2. Why is it being changed now?
3. What did the responsible user intend to preserve or change?
4. What constraints apply?
5. What is the expected result?
6. What is explicitly out of scope?
7. Which canonical rules and prior decisions govern the change?

If these cannot be established from authoritative evidence, the ELO must not merge.

## User decision gate

Material user decisions are governance inputs.

The ELO must establish for each relevant decision:

- source;
- scope;
- purpose;
- constraints;
- applicability;
- whether it is task-specific, specialist guidance, ELO governance or architectural governance.

The ELO must not silently override a user decision. If a higher-authority canonical rule conflicts with it, the conflict must be explicitly identified and escalated or reconciled according to the authority hierarchy.

A task-specific decision must not be generalized into a global rule without evidence or explicit authorization.

When a user correction establishes reusable specialist or ELO guidance, the ELO must promote it into the appropriate governed `.md` artifact rather than relying only on conversation history.

## Revalidation rule

Any material new commit pushed to an open PR invalidates the previous ELO gate.

The ELO must restart the complete review loop. A previous `ELO_GATE: PASS` is not reusable approval for a changed PR.

## Gate states

### `ELO_GATE: PASS`

The complete loop was executed and no unresolved material conflict remains. The ELO may authorize merge.

### `ELO_GATE: REVISE`

The ELO found a divergence it can resolve through implementation, documentation, tests or governance-aligned correction. Merge is prohibited until the correction is applied and the complete loop is repeated.

### `ELO_GATE: ESCALATE`

Resolution requires human authority, missing information unavailable to the ELO, or an architectural/governance decision outside the ELO's authority. Merge is prohibited until the authorized resolution exists.

## Normal merge path

```text
Specialist / AI
→ PR
→ ELO full-loop review
→ ELO_GATE: PASS
→ squash merge
```

Human approval is an exception path, not a routine prerequisite, unless repository governance explicitly requires it.

## Required ELO review record

Before merge, the PR review should record, at minimum:

- `ELO_GATE` state;
- purpose understood;
- relevant user decisions identified;
- canonical rules consulted;
- changed files reviewed;
- tests/evidence checked;
- contradictions/risks;
- corrections performed, if any;
- residual uncertainty;
- merge authorization.

## Governance principle

The ELO is not merely checking whether code works. It is checking whether the change is **the right change for the intended purpose**, consistent with the ELO's canonical architecture, the responsible user's decisions, the evidence available, and the repository's governance boundaries.
