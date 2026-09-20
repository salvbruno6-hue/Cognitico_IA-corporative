# Hermes Provider Routing / Fallback / Credential Pools -> ELO Boundary - 2026-09-20

EXT-ROUTE-HERMES is candidate-only.

ELO may define the governed routing policy. Hermes may execute an authorized route, but cannot become the canonical ELO router, bypass governance, silently change tenant scope, or promote a fallback outcome.

Required routing evidence: route identity, provider chain, credential strategy, tenant scope and provenance.

REJECTED: incomplete identity/scope/provenance, competing authority, or governance bypass.
OBSERVATION: mechanism exists without explicit governed policy.
CANDIDATE: verified mechanism with explicit policy; still not production-authorized.

No credential secrets, provider activation, production routing changes, promotion, or Evolution Gate approval occur here.