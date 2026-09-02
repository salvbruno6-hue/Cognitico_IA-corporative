# ELO Symbiotic Routing Governance

## Canonical authority

`ExecutionRouter` remains the canonical selection authority for model and tool execution.

`IntelligenceRouter` is a coordination facade over that decision. It MUST NOT independently rank, override or replace the canonical routing decision.

## Provider boundary

Providers are external cognitive capabilities. They are selected through the governed routing path and remain replaceable. Provider output does not become canonical ELO knowledge automatically.

## Learning boundary

Routing performance may be learned from validated outcomes. The learning system may inform future routing only through the governed evolution path; it must not hard-code a permanent provider-to-domain assignment from a single result.

## Audit fields

A routed execution should preserve request identity, tenant, specialist, capability, routing rationale, provider, model, context, evidence, result and outcome/experience references when available.

## Blocking conditions

Execution must be blocked when the route has no executable model, the selected provider has no approved adapter, tenant authorization is absent, or required evidence/governance state is invalid.
