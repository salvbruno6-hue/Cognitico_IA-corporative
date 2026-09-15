# ELO Core Maturity — SPC-01

## Critical criterion

`Core faculty → Forge specialist → Skill → Evidence → Feedback → governed learning`

## Operational lab method

SPC-01 is validated first as a deterministic GitHub Actions laboratory execution using existing canonical components. The fixture represents a governed Forge specialist and skill, produces evidence, admits append-only specialist feedback, captures outcome experience, creates a learning candidate, evaluates it, and passes the candidate through the existing Evolution Gate.

This test does **not** represent real-world human/specialist validation. Issue #137 remains the authority for actual specialist feedback evidence and must not be inferred from this fixture.

## Non-negotiable boundaries

- Forge remains the specialist/skill domain; Core resolves but does not create a second registry.
- Evidence and provenance are mandatory.
- Feedback is append-only; historical records are immutable.
- Learning remains a candidate until evaluation and governed approval.
- Evolution Gate classifies the proposal but does not grant canonical mutation authority.
- No direct Core mutation, provider authority, credential use, or parallel learning/memory authority is introduced.

## Acceptance evidence

A final `PASS` requires a GitHub Actions run tied to the exact tested commit, with the SPC-01 integration test passing and the canonical/full regression suite passing. The evidence record must include the commit SHA, workflow/run IDs, expected versus observed results, provenance, residual risk, and post-merge regression.

## Current execution state

`EXECUTION_REQUESTED` — branch prepared from canonical main `79ed019903179cf9d4e03f2b7ff4c4f67bda3a80`; awaiting GitHub Actions evidence before promotion.

## Next correction rule

If the chain fails, correct only the broken integration boundary, rerun the isolated SPC-01 test, then run the full governed gates. Do not add a new generic capability to compensate for an integration defect.
