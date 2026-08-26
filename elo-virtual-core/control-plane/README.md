# ELO Control Plane

## Purpose

The Control Plane is the authoritative orchestration layer of ELO. GPT is treated as an interface/peripheral for human input and presentation of ELO results. GPT does not become the source of truth and does not receive infrastructure secrets.

## Operating model

```text
GPT / UI / CLI / API client
          |
          v
     ELO Gateway
          |
          v
    Control Plane
     |    |    |
     |    |    +--> Policy / Authorization
     |    +-------> Intent / Routing
     +------------> Decision / Execution plan
          |
          +--> Supabase Elo-forge
          +--> GitHub / CI
          +--> future adapters
```

## Authority model

1. The interface requests an operation.
2. ELO classifies the intent.
3. ELO identifies required data sources and relationships.
4. Policy is evaluated before tool execution.
5. Only an authorized adapter executes the operation.
6. ELO validates and normalizes the result.
7. ELO produces a structured response for the interface.

## Deployment targets

The same core must be usable as:

- local Python package;
- CLI;
- HTTP API;
- Docker container;
- cloud service.

The business rules must remain independent from the transport layer so that CLI, API and GPT use the same orchestration logic.

## Non-goals

- Do not store secrets in Git.
- Do not make GPT the authority for permissions.
- Do not allow an interface to bypass the ELO policy engine.
- Do not silently fabricate missing operational data.
- Do not couple the decision engine directly to Supabase SDK calls.
