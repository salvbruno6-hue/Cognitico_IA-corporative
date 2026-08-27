# ELO Cognitive Capability Selection Contract

## Purpose

Define how ELO Cognitivo selects an executable capability after task decomposition. The existing `CapabilityRegistry` remains the source of availability; this contract governs cognitive selection and does not create a second registry.

## Selection chain

```text
TASK STEP
  -> REQUIRED CAPABILITY
  -> AVAILABLE REGISTERED CAPABILITIES
  -> METHOD / CONTEXT CONSTRAINTS
  -> EVIDENCE + HEALTH
  -> SCORE
  -> SELECT
  -> EXECUTE
  -> VERIFY
```

## Rules

1. A capability must be registered before selection.
2. Unavailable or unknown capabilities cannot be selected as healthy executors.
3. The selector may prefer a kind, but preference cannot override capability compatibility.
4. A minimum score may reject an otherwise available candidate.
5. Provider identity is not canonical knowledge; the capability contract is canonical.
6. If no candidate satisfies the requirement, ELO must degrade, replan or escalate rather than inventing an executor.
7. Tenant methodology and authorization remain higher-order constraints than generic provider preference.
8. Secrets never enter capability metadata or selection records.

## Provider/model/tool separation

A model, database, calculator, connector or external service is an executor of a capability. ELO reasons about the required capability first and selects an implementation second.

Example:

```text
calculate_quantity
   -> calculation capability
      -> Python / deterministic engine / approved calculator
```

The implementation can change without changing the cognitive contract.

## Evidence

Selection decisions should retain capability name/version, requirement, relevant metadata, selection score, method/context reference and subsequent verification result.
