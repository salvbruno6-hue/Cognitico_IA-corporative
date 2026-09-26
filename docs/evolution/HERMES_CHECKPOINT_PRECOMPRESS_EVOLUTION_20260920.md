# Hermes Checkpoint -> ELO: pre-compression durability guard — 2026-09-20

## Discovery

Current Hermes MemoryProvider architecture exposes a pre-compression checkpoint
boundary in which a memory provider can confirm durable checkpoint state before
lossy context compaction. When a required checkpoint is not confirmed, the
provider can fail closed rather than allowing the lossy boundary to proceed.

## Existing ELO comparison

ELO already contains the HERMES-CHECKPOINT candidate and a deterministic
in-memory state-recovery probe. Existing ELO state recovery covers snapshot /
restore integrity and tenant isolation. The newly observed capability is
narrower and complementary: pre-compression admission control.

It therefore does not replace state_recovery_integrity.py and does not create
a second recovery authority.

## Candidate introduction

EXT-CHECKPOINT-HERMES refinement:

- owner: ELO State Recovery;
- boundary: context/memory compaction;
- input: immutable checkpoint receipt;
- policy: if checkpoint_required=true, absence, non-confirmation,
  non-durability, or scope mismatch blocks the boundary;
- output: deterministic ALLOW/BLOCK decision with checkpoint/evidence references;
- side effects: none;
- memory promotion: none;
- authority transfer: none.

## Controlled implementation

Implemented as src/elo/agent_intake/checkpoint_compaction_guard.py.

The implementation does not:

- create checkpoints;
- compress context;
- mutate files;
- write memory;
- call providers;
- promote learning;
- authorize business or production operations.

It only validates the contract of an already-issued checkpoint receipt.

## Controlled tests

tests/agent_intake/test_checkpoint_compaction_guard.py covers:

1. optional checkpoint policy;
2. fail-closed behavior when required evidence is absent;
3. durable confirmed checkpoint acceptance;
4. unconfirmed checkpoint rejection;
5. non-durable checkpoint rejection;
6. tenant/scope mismatch rejection;
7. explicit non-transfer of authority.

## Validation state

CONTROLLED IMPLEMENTATION VALIDATED means the local contract tests pass.
This does not mean the capability is promoted to ELO operational authority.

Repository-wide CI remains separately governed. The existing unrelated
tests/security/test_operator_github_binding_runtime.py currently expects a
migration file that is absent from main; that issue must not be folded into
this Hermes evolution change.

## Governance conclusion

This is a refinement of the existing EXT-CHECKPOINT-HERMES candidate, not a
new authority. Production activation remains subject to the Evolution Gate.
