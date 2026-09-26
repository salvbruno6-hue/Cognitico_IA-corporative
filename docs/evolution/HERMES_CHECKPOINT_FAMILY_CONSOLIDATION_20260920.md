# Hermes checkpoint family consolidation — 2026-09-20

PR #597 validates the pre-compress durability guard. PR #600 validates the same checkpoint candidate against native recovery. These are not independent canonical capabilities.

The family is consolidated as:

- EXT-CHECKPOINT-HERMES — capability family
- EXT-CHECKPOINT-HERMES-PRECOMPRESS — controlled refinement

Owner remains ELO State Recovery.

Neither experiment grants canonical mutation or promotion authority.

## Required evidence before promotion review

The two validation lines must be interpreted together:

1. native recovery compatibility;
2. pre-compress fail-closed durability behavior.

A positive result in only one line is insufficient to establish a canonical promotion case for the family.