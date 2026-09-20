# Hermes Worktree Controlled Evaluation — 2026-09-20

## Candidate

- ID: `EXT-WORKTREE-HERMES`
- Existing ELO owner: ELO Forge
- Primary metric: valid isolation recognition rate
- Direction: maximize
- Secondary safety signal: boundary integrity rate

## Scope

This evaluation measures the existing boundary assessor's deterministic recognition of
verified, isolated, provenance-backed worktree signals.

It does **not** claim to measure filesystem-level Git worktree creation, deletion,
performance, or productivity. The candidate contract explicitly excludes those operations.

## Controlled protocol

1. Run five deterministic baseline signals through the governed assessor.
2. Run five equivalent Hermes-adapted signals through the same existing ELO Forge boundary.
3. Measure valid-isolation recognition.
4. Verify that canonical authority and merge permission remain false.
5. Repeat the adapted set and require the same result.
6. Apply the implementation-loop decision semantics.

## Evidence

- Baseline recognition: 5/5 = 1.00
- Adapted recognition: 5/5 = 1.00
- Boundary integrity: 5/5 = 1.00
- Repeatability: PASS
- Canonical mutation: none
- Merge authority transfer: none

## Decision

**RETEST**

No incremental measurable gain was demonstrated: 1.00 → 1.00.

The evaluation implementation is safe to integrate as canonical evidence, but the
candidate itself remains candidate-only and is not promoted to ELO Core.

## Governance boundary

This evaluation cannot authorize:

- merge to `main`;
- Core promotion;
- governance modification;
- Evolution Gate bypass;
- production activation.

A future evaluation must demonstrate a genuine incremental benefit with the same
boundary integrity before it can become eligible for ELO review.
