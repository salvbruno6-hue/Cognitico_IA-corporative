# Hermes Session Writer Registry — governed candidate

## Purpose
Register session-writer handle evidence while reusing the canonical SessionManager
and SessionStore. This candidate does not create a new store, writer, persistence
authority, or session manager.

## Governance
Required identity: session, tenant, principal, writer reference, provenance.
The assessment is deterministic and has no I/O. write_permitted is always false.
Durability is metadata only and does not authorize a write.

## Canonical owners
- src/elo/interface/session.py — Session / SessionManager / SessionStore.
- src/elo/context — session identity and tenant/principal consistency.
- src/elo/core/access_policy.py — session access authorization.

No new memory, persistence, writer, authorization, router, or Evolution Gate is introduced.

## Promotion boundary
CI/Evolution Gate success is technical governance evidence only. It does not
constitute production outcome evidence or authorize merge.
