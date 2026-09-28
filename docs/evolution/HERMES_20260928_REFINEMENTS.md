# Hermes 0.21.x — ELO Refinement Candidates

## Discovery

Two relevant refinements were identified in the current Hermes 0.21.x surface:

1. Live subagent steering: a parent agent can steer an active delegated worker
   during execution. ELO maps this to the existing HERMES-DELEGATION owner.
2. Automation memory/continuity: scheduled runs can preserve continuity across
   executions. ELO maps this to the existing HERMES-AUTOMATION owner while
   keeping memory authority in existing ELO governance.

Bot Mode is not duplicated here: ELO already has the EXT-PROFILE-HERMES runtime
integration path under PR #830.

## Candidate contracts

### Live steering

Required evidence:
- parent execution identity;
- child agent identity;
- explicit directive;
- provenance;
- no transfer of ELO authorization.

### Cron continuity

Required evidence:
- automation identity;
- previous-run reference;
- continuity scope;
- provenance;
- explicit continuity signal.

Neither contract invokes Hermes, reads/writes memory, schedules a job, or executes
a business operation.

## Validation boundary

A passing deterministic contract test establishes only structural candidate
validity. Functional gain, runtime outcome, ELO Review and Evolution Gate remain
required before promotion.

No Hermes source is modified. SO 001.26 is not used.
