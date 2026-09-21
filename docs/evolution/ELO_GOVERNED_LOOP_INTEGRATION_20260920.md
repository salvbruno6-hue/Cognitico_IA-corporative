# ELO governed loop integration — 2026-09-20

## Purpose

Connect the existing Hermes capability discovery/transformation loops to the
existing implementation-loop gates and give ELO a deterministic cadence map
that identifies the next existing flow after each governed outcome.

## Architecture

There are two layers:

1. **Capability/implementation gates** decide whether a step has enough evidence.
2. **Cadence routing** decides which already-existing flow should receive the result next.

Cadence routing does not approve, promote, merge, or mutate canonical state.

## Governed chain

`HERMES CANDIDATE → DISCOVERY/TRANSFORMATION → CONTROLLED TEST → MEASURED_GAIN → REPEATABLE → ELO_REVIEW → IMPLEMENTATION_AUTHORIZED → GOVERNED PR/MERGE → POST-OUTCOME → ELO APRENDER → LOOP`

The broader ELO execution chain remains:

`OBJECTIVE → DECOMPOSE → EXECUTE → VALIDATE → SPECIALIST_REVIEW → ELO_REVIEW → CORRECT/REPLAN → REVALIDATE → COGNITIVE_MERGE → GOVERNANCE → VIRTUAL_LABORATORY → APPROVE_COMMIT → COMMIT → VERIFY → PR → APPROVE_MERGE → GIT_MERGE → VERIFY → LEARN → REPORT → OBJECTIVE`

The cadence contract in `elo_flow_cadence.py` links these stages by explicit
outcome. When no mapping exists, routing stops fail-closed instead of guessing.

## Activation semantics

Activating a flow does **not** mean "run everything without checking."

It means:

1. execute the current governed flow;
2. emit its explicit outcome;
3. resolve the registered next flow;
4. pass the evidence/provenance package forward;
5. execute the next flow only if its own entry gate is satisfied;
6. stop or escalate when no valid transition exists.

Thus ELO does not need a human to manually tell it that
`CONTROLLED_TEST` is followed by `MEASURED_GAIN`, or that a successful
verification should route to `PR`. The cadence contract supplies that relationship.

## Stamps / states

- `CANDIDATE`: bounded candidate or incomplete entry evidence.
- `CONTROLLED_TEST`: controlled evidence is being evaluated.
- `MEASURED_GAIN`: explicit metric direction is required before a gain is accepted.
- `REPEATABLE`: positive evidence must be repeatable.
- `ELO_REVIEW`: technical evidence is ready for explicit ELO review; this is not approval.
- `IMPLEMENTATION_AUTHORIZED`: explicit ELO implementation authorization has been supplied.
- `PR`: repository change is under governed PR control.
- `POST_MERGE_VERIFY`: merged state is verified before learning.
- `LEARN`: outcome is returned to the learning loop.

## Safety

The integration is evidence-only and fail-closed. It does not:

- promote canonical knowledge;
- set `canonical_mutation=True`;
- approve an Evolution Gate;
- merge a pull request;
- activate Hermes;
- create a new authority.

No measured gain is inferred from CI success or from test fixtures.

## Intended next evolution

The next architectural step is to make the cadence resolver the common routing
contract used by the ELO cognitive orchestrator, rather than allowing each
specialist flow to decide independently what comes next. That should be an
integration of existing flows, not a new parallel orchestrator.
