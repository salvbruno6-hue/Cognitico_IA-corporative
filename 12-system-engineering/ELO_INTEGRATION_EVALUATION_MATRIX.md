# ELO Integration Evaluation Matrix

## Purpose

Evaluate external infrastructure only when a verified deficiency justifies it.

## Candidates

| Tool | Intended role | ELO boundary | Initial decision |
|---|---|---|---|
| MLflow | tracing, evaluation, experiments, lineage | observability/MLOps adapter | POC |
| Kedro | data pipelines and reproducibility | data-engineering adapter | POC |
| Airflow | scheduling and batch orchestration | workflow adapter | POC |
| TFX | traditional ML lifecycle | optional ML adapter | DEFER |
| Rasa | conversational interface | application adapter | DEFER |
| Robocorp | RPA execution | automation adapter | DEFER |
| Jenkins | CI/CD | delivery infrastructure | OUTSIDE ELO COGNITIVE CORE |

## Admission gate

`DEFICIENCY → CANDIDATE → POC → LAB → TEST → COMPARISON → VALUE → GOVERNANCE → ADOPT / ADAPT / REJECT`

## Evaluation criteria

- solves a documented deficiency;
- no duplicate canonical capability;
- provider neutrality preserved;
- tenant isolation preserved;
- provenance preserved;
- security and authorization boundaries preserved;
- measurable operational value;
- acceptable latency/cost/complexity;
- reversible integration;
- reproducible tests and evidence.

## Rule

Installing a tool does not promote it to canonical architecture. Integrations remain replaceable infrastructure adapters.
