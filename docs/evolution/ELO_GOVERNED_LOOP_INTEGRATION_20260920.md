# ELO governed loop integration — 2026-09-20

## Purpose

Connect the existing Hermes capability discovery/transformation loops to the
existing implementation-loop gates without creating a second approval engine.

## Governed chain

`HERMES CANDIDATE → DISCOVERY/TRANSFORMATION → CONTROLLED TEST → MEASURED_GAIN → REPEATABLE → ELO_REVIEW → IMPLEMENTATION_AUTHORIZED`

The existing `HermesCapabilityLoops.approval_readiness()` remains the readiness
contract for the Evolution Gate / approval layer. The existing
`ApprovedCandidateImplementationLoop` remains the post-approval handoff.

## Stamps / states

- `CANDIDATE`: bounded candidate or incomplete entry evidence.
- `CONTROLLED_TEST`: controlled evidence is being evaluated.
- `MEASURED_GAIN`: an explicit metric direction is required before a gain is accepted.
- `REPEATABLE`: positive evidence must be repeatable.
- `ELO_REVIEW`: technical evidence is ready for explicit ELO review; this is not approval.
- `IMPLEMENTATION_AUTHORIZED`: explicit ELO implementation authorization has been supplied.
- Repository merge remains a separate governed Git operation.

## Safety

The integration is evidence-only and fail-closed. It does not:

- promote canonical knowledge;
- set `canonical_mutation=True`;
- approve an Evolution Gate;
- merge a pull request;
- activate Hermes;
- create a new authority.

No measured gain is inferred from CI success or from test fixtures.
