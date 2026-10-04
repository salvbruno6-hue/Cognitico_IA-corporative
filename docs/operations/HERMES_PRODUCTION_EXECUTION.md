# Hermes — production execution bridge

## Objective

Provide a real transport path from the canonical ELO execution boundary to an already-deployed Hermes runtime without creating a second authorization authority.

## Canonical path

`elo-authz → AuthorizationDecision → GovernedHermesRuntimeBridge → HermesHttpRuntimeClient → Hermes production runtime`

The bridge does not:
- authorize execution;
- select capabilities;
- promote candidates;
- write canonical memory;
- convert runtime execution into learning.

## Production preconditions

A production execution requires all of the following:

1. A canonical `AuthorizationDecision` issued by `elo-authz`.
2. `AuthorizationDecision.is_transport_valid() == True`.
3. `authorization.resource_id == request.skill_id`.
4. A deployed Hermes endpoint reachable over HTTPS.
5. A bearer credential supplied outside source control.
6. The Hermes response must preserve `request_id`.
7. The Hermes response must explicitly report `environment=production`.
8. The runtime must return its real execution facts; ELO does not infer them.

## Environment configuration

The transport expects:

- `HERMES_PRODUCTION_RUNTIME_URL`: HTTPS endpoint of the deployed Hermes runtime.
- `HERMES_PRODUCTION_RUNTIME_TOKEN`: runtime credential, stored in the deployment secret manager.

Do not place either value in Git, tests, evidence fixtures, or pull requests.

## Evidence boundary

This bridge makes production execution technically reachable. It does **not** by itself make any candidate production-proven.

Production proof remains governed by the existing `to_production_outcome()` boundary and requires:

- two or more independent real production observations;
- successful `ExecutionOutcome` for each;
- candidate-bound canonical authorization;
- explicit `environment=production`;
- matching execution/provenance identities;
- repeatable positive outcome.

Only after those facts exist can the existing ELO review / Evolution Gate process evaluate production evidence.

## First execution wave

Use candidates that already have canonical runtime integration and repeatable operational evidence:

- EXT-MULTIAGENT-HERMES
- EXT-MEMPROVIDER-HERMES
- EXT-ROUTE-HERMES
- EXT-BATCH-HERMES
- EXT-LEARN-HERMES
- EXT-CRON-HERMES
- EXT-PROFILE-HERMES
- EXT-CONTEXT-PLUGIN-HERMES
- EXT-LEARNING-GRAPH-HERMES
- EXT-WORKTREE-HERMES

`EXT-CONTEXTREF-HERMES` remains separately evaluated; `EXT-CHECKPOINT-HERMES` remains RETEST where no measurable gain has been established; `EXT-HOOK-HERMES` still lacks the equivalent production runtime bridge.

## Status after this change

**Implementation:** production transport bridge available.

**Production execution:** not performed by this change.

**Production proof:** unchanged until real authorized executions occur.

This distinction is mandatory: deployment of the bridge is not evidence that the skill produced a production outcome.
