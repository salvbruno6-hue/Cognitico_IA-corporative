# Hermes Protected Instruction Surfaces → ELO

## Decision

Hermes exposes a useful security pattern: instruction-bearing surfaces such as
AGENTS, skills and memory require explicit write authorization, while logs,
checkpoints and ACP-facing material require redaction before external exposure.

ELO does not create a second security or execution authority for this pattern.
The canonical owners remain the existing security contracts and
src/elo/core/execution_boundary.py.

## ELO introduction

The candidate is an observational contract:

- AGENTS, SKILL and MEMORY writes are blocked unless an existing authorization
  is already present;
- LOG, CHECKPOINT and ACP external exposure requires redaction;
- the contract performs no authorization;
- the contract performs no redaction;
- no business operation is executed;
- no Hermes code is modified;
- no new memory, router, Evolution Gate or promotion authority is created.

Implementation:
src/elo/security/protected_instruction_surfaces.py

Tests:
tests/security/test_protected_instruction_surfaces.py

## Validation boundary

The controlled tests prove only the ELO-side contract invariants. They do not
claim production security coverage, successful runtime redaction, or external
browser/ACP operation.

Promotion remains subject to the existing CI and Evolution Gate.
