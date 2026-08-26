# ELO CLI

The CLI is a local peripheral to the same Control Plane used by the HTTP API.

## Intended commands

```bash
elo query "qual a composição do M01?"
elo plan "qual a composição do M01?"
elo status
elo schema
```

State-changing commands must remain disabled by default until an explicit policy exists.

The CLI must never contain Supabase or GitHub secrets. Credentials are supplied through the deployment environment/secret manager and consumed only by adapters.
