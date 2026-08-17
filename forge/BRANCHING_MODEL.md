# ELO Forge Branching Model

The Forge is a construction plane inside the Cognitico monorepository.

## Branch convention

- `main`: canonical ELO state.
- `forge/<task>`: bounded construction work.
- `experiment/<task>`: isolated architectural experiments.
- `hotfix/<task>`: urgent corrective construction.

A Forge branch is not a competing architecture. It is a temporary construction line derived from `main` and must return through validation and pull request.

## Merge rule

```text
main (canonical)
   ↓
forge/<task>
   ↓
build / test / correct
   ↓
canonical validation
   ↓
PR
   ↓
main
```

The old standalone Forge repository is not the canonical construction branch. New construction work should originate from this monorepository.

## Important boundary

The presence of a file in `forge/` means **candidate construction**, not canonical approval. Canonical status comes from promotion into the appropriate canonical area and an accepted decision.
