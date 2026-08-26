# ELO Control Plane Specification

## 1. Core principle

ELO is the operational authority. GPT is a peripheral interface. API and CLI are additional peripherals. No peripheral is a source of truth and no peripheral may bypass ELO policy.

## 2. Layers

### Interface layer

Receives human/system requests and renders structured results. It must be stateless with respect to business rules.

### Gateway layer

Normalizes requests, assigns request IDs, validates payloads and forwards requests to the orchestrator.

### Orchestration layer

Determines intent, entities, required evidence, source, relationships and operation type.

### Policy layer

Applies least privilege, deny-by-default and approval requirements.

### Adapter layer

Provides controlled access to external systems. Adapters are the only components allowed to know integration details.

### Evidence layer

Preserves source, records used, relationship path, timestamps/status and warnings so that results can be audited.

### Decision layer

Separates facts from inference and produces a decision or answer only after validation.

## 3. Request lifecycle

```text
request
  -> normalize
  -> identify intent
  -> identify entities
  -> build data requirements
  -> select source
  -> validate authorization
  -> build execution plan
  -> execute allowed reads
  -> validate relationships
  -> classify facts/inferences/missing data
  -> decision
  -> audit
  -> response
```

## 4. Data routing example

For `Qual é a composição do M01?` ELO should identify at minimum:

- modelo M01;
- taxonomia;
- dimensão when relevant;
- kit;
- kit_itens;
- lista_mae;
- estrutura_modular when the question concerns modular composition.

The primary operational source is Supabase Elo-forge. GitHub remains the source for repository structure, implementation, issues, PRs and CI evidence.

## 5. Operation classes

| Class | Default | Approval |
|---|---|---|
| read | allowed if source policy allows | no |
| plan | allowed | no |
| write | denied | explicit |
| execute | denied | explicit |
| merge | denied | explicit + validations |
| delete | denied | explicit + audit |

## 6. Deployment contract

The core must not depend on HTTP. The HTTP API and CLI call the same orchestration service. This permits local execution, container deployment, VM deployment and cloud deployment without changing decision rules.

## 7. Configuration contract

Configuration is externalized. Environment-specific values are not hard-coded into business logic. Secrets are injected at runtime through the deployment secret mechanism.

## 8. Failure behavior

- Unknown intent: return an explicit unresolved state or request clarification.
- Missing source: report source unavailable; do not invent data.
- Unauthorized operation: deny and record the policy decision.
- Adapter failure: return source failure and preserve request ID.
- Conflicting records: surface conflict rather than silently selecting one.

## 9. Evolution

New sources must implement an adapter contract and be registered in the routing policy. New tables in Supabase should update source metadata rather than forcing GPT prompt changes.
