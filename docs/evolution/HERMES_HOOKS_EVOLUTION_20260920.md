# Hermes Lifecycle Hooks — ELO Evolution Boundary

## Source observation

Hermes exposes lifecycle gateway events where hooks can observe or react to
agent lifecycle events.

## ELO adaptation

Candidate ID: `EXT-HOOK-HERMES`

The ELO adaptation treats hooks as bounded lifecycle evidence/guardrail points.
A hook is not a new governance authority and cannot independently mutate
canonical state.

## Boundary rules

1. Hook identity, tenant scope, event name, handler identity and provenance are mandatory.
2. Explicit activation is required before candidate status.
3. Hooks that mutate canonical ELO state directly are rejected.
4. Hooks that bypass ELO governance are rejected.
5. Assessment grants no execution or mutation authority.
6. Any resulting evidence must return through the existing ELO governance path.

No production hook is activated by this change.
