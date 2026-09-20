# ELO — Hermes Canonical Promotion Readiness — 2026-09-20

## Purpose

Create one evidence gate for the Hermes mechanisms currently under controlled ELO evaluation. This document does not promote any mechanism and does not mutate canonical state.

## Evaluated scope

The readiness evaluator covers the 13 registry mechanisms plus the separately evaluated Curator lifecycle signal:

- EXT-CONTEXTREF-HERMES
- EXT-CHECKPOINT-HERMES
- EXT-HOOK-HERMES
- EXT-ROUTE-HERMES
- EXT-PROFILE-HERMES
- EXT-BATCH-HERMES
- EXT-MEMPROVIDER-HERMES
- EXT-LEARN-HERMES
- EXT-LEARNING-GRAPH-HERMES
- EXT-CONTEXT-PLUGIN-HERMES
- EXT-WORKTREE-HERMES
- EXT-MULTIAGENT-HERMES
- EXT-CRON-HERMES
- EXT-CURATOR-HERMES

## Green definition

A mechanism is GREEN_READY_FOR_CANONICAL_REVIEW only when the evidence package contains:

1. explicit candidate identity and ELO owner;
2. baseline and experiment identifiers;
3. an explicit metric and metric direction;
4. a measured candidate result better than the baseline in that direction;
5. at least two repeatability runs with repeatability confirmed;
6. security verification;
7. isolation verification;
8. no authority conflict;
9. Evolution Gate = PASS (the gate decision is already recorded);
10. approval reference and promotion-package reference.

A fixture or unit-test example is not production/runtime evidence. No measured value is inferred by this evaluator.

## Boundary

The evaluator is evidence-only. canonical_mutation_permitted() always returns false. Production activation, canonical promotion, Git merge, and Supabase mutation remain outside this contract.

## Checkpoint overlap

EXT-CHECKPOINT-HERMES and the pre-compress checkpoint guard are treated as one capability family for promotion review. The readiness layer does not create a second checkpoint authority; consolidation remains required before any canonical promotion decision.