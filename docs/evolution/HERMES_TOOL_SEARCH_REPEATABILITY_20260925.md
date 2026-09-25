# Hermes Tool Search — Repeatability Validation

## Position in the governed loop

`MEASUREMENT → TASK-QUALITY VALIDATION → REPEATABILITY → EVOLUTION GATE → ELO REVIEW`

PR #729 established the controlled measurement stage. PR #730 established
controlled task-quality equivalence without regression. This stage verifies
that the same quality result remains stable across repeated controlled runs.

## Contract

Repeatability requires:

- at least three controlled quality results;
- identical baseline/adapted accuracy and delta across runs;
- no regressions or unreachable selections in any run;
- task-quality equivalence in every run.

This is deterministic repository evidence. It is not production workload
evidence and does not grant promotion authority.

## Guardrails

- reuse `ELO Model/Tool Routing` as the owner;
- do not invoke Hermes;
- do not execute tools or business operations;
- do not create a router, registry, memory store, or Evolution Gate;
- do not mutate Core or canonical memory;
- remain `candidate_only`;
- Evolution Gate remains the promotion boundary.

## Next gate

After repeatability is established, the candidate may be evaluated by the
existing Evolution Gate. Repeatability alone does not promote the candidate.
