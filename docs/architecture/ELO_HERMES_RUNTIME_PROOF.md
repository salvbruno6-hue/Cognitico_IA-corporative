# ELO ↔ Hermes Runtime Proof V1

## Objective

Prove that ELO Cognitive can use Hermes capabilities as an external execution runtime while retaining governance in ELO.

## Runtime path

```text
GPT / Intent
    ↓
ELO Cognitive authorization
    ↓
HermesExecutionRequest
    ↓
Hermes /elo/v1/execute
    ↓
Hermes skill runtime
    ↓
HermesExecutionResult
    ↓
ELO evidence/outcome validation
    ↓
Governed Learning / Evolution Gate
```

## Acceptance

- an ELO-authorized capability reaches Hermes;
- Hermes executes through its existing skill runtime;
- the result returns with the same `request_id`;
- skills/evidence/outcome are visible to ELO;
- unauthorized capability is rejected;
- infrastructure identifiers cannot cross the boundary;
- learning remains non-canonical until ELO governance promotes it.

Deployment platform is not part of this proof.
