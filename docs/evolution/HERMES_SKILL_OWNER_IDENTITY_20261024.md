# Hermes → ELO: skill owner identity candidate — 2026-10-24

## Observation

Hermes hardened portable-plugin skill naming so the runtime distinguishes the human-facing plugin name from hashed storage identity, prevents same-slug owners from collapsing into one qualified skill, and resolves a skill through the exact owning plugin. Follow-up compatibility handling accepts legacy qualified forms without transferring activation authority.

## ELO fit

This is not a new capability owner. It refines the already-governed `EXT-SKILL-CHANGE-AWARENESS-HERMES` path under **ELO Knowledge & Skills**.

Invariant proposed for ELO evidence:

`skill identity = governed owner + local skill name`

Two skills with the same local name but different owners must remain distinct in inventory/delta evidence. Storage hashes and display aliases must not become execution authority.

## Boundary

The candidate performs no plugin discovery, plugin loading, skill activation, tool execution, memory mutation, business operation, Hermes mutation, or Supabase mutation.

## Validation contract

The focused tests require:

1. same local name + different owners => distinct identity;
2. same owner + same local name => same identity;
3. empty or pre-qualified components => fail closed.

Promotion remains blocked until repository CI/Evolution Gate and review approve the implementation. This document does not promote the candidate.
