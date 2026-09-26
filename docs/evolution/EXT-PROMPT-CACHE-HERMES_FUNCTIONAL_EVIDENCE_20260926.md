# EXT-PROMPT-CACHE-HERMES — Functional Evidence — 2026-09-26

Stage: CONTROLLED_FUNCTIONAL_VALIDATION
Status: EVOLUTION_GATE_REQUIRED
Canonical mutation: false
Production deployment: false

Five deterministic cache-boundary fixtures were evaluated without using a real cache, prompt payload, user data, or persistent state.

| Metric | Baseline | Adapted |
|---|---:|---:|
| cache-decision accuracy | 0.40 | 1.00 |
| repeatability | PASS | PASS |
| regressions | 0 | 0 |

The baseline permits a tenant-matching prompt cache entry without checking context version or invalidation. The adapted boundary additionally requires exact scope and context-version matching and rejects explicitly invalidated or expired entries.

The evidence covers cross-tenant isolation, stale context, explicit invalidation, and expiry. It is controlled fixture evidence, not production execution evidence and not proof of Hermes runtime equivalence.

Existing ELO Cognitive Memory ownership is reused through the candidate-only HERMES-MEMORY experience surface. No new capability identity, cache authority, persistent memory record, Hermes runtime, or business operation is introduced.
