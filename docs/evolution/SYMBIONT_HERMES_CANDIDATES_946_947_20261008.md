# Simbionte — Hermes candidates #946 / #947

Status: implementation candidate reconciled on current main; merge requires repository CI/Evolution Gate.

## Baseline
Reconciled from canonical `main` after SO identifier enforcement. The old candidate branches were 12 commits behind and therefore were not merged directly.

## Candidate #946 — Model Capability Metadata
- Owner reused: canonical ModelSelector.
- Observation: model capability/context/cost/training metadata.
- Authority: none added.
- Runtime effect: none; `routing_permitted=false`.
- Provenance: mandatory.
- Simbiont disposition: eligible for governed observation; not generalized learning.

## Candidate #947 — Session Writer Registry
- Owners reused: SessionManager/SessionStore, Context identity and access policy.
- Observation: writer handle identity/provenance/durability metadata.
- Authority: none added.
- Runtime effect: none; `write_permitted=false`.
- Provenance: mandatory.
- Simbiont disposition: eligible for governed observation; not persistence authority.

## Controlled validation
Tests cover:
1. valid evidence remains candidate-only;
2. missing provenance blocks both classes;
3. invalid model metadata is blocked;
4. unverified training tier produces review warning;
5. model metadata cannot route;
6. durable writer handles cannot write;
7. missing principal identity blocks session-writer evidence;
8. cross-candidate Simbiont boundary preserves both fail-closed invariants.

## Evolution decision
These introductions are additive evidence contracts. They do not modify Hermes, execute business operations, create canonical learning, create a second router/memory/store/Evolution Gate, or use a solicitation instance as architectural authority.

Repository CI and Evolution Gate remain the final technical validation before merge. Production proof remains separate from merge and is not claimed here.
