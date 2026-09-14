# P0 — Software Engineering + Absorption Governance

This cycle generalizes two mechanisms observed in external skill systems into native ELO boundaries.

## Software Engineering

`NativeSoftwareEngineering` represents the controlled loop:

`diagnosis → root cause → hypothesis → proposed change → laboratory test → regression → governance`

The implementation is candidate-only. It does not write `main`, merge a pull request, authorize execution, or promote itself.

## Absorption governance

`GovernedAbsorptionEnvelope` establishes a universal source/evidence lineage boundary for mechanisms entering ELO. It requires source reference, source commit, evidence, scope and risk, and rejects secret-bearing provenance or lineage mismatch.

The envelope is not a second authority. Promotion remains subject to the existing ELO governance and Evolution Gate.

## Hermes relationship

Hermes is comparative evidence for the mechanism, not a runtime dependency or canonical owner. The native ELO capability remains provider-neutral.

## Acceptance

- incomplete diagnosis or evidence blocks the candidate;
- failed tests produce `ADJUST_REQUIRED`;
- failed regression produces `REGRESSION_FAILED`;
- only a passing test and regression reaches `READY_FOR_GOVERNANCE`;
- absorption with mismatched lineage or secrets is rejected;
- no canonical mutation occurs inside either boundary.
