# Hermes — external production transport boundary

## Scope

Provide an HTTPS transport from the existing GovernedHermesRuntimeBridge to an already-deployed Hermes runtime.

The transport is not an authorization authority and does not replace the canonical evidence boundary introduced by runtime evidence intake.

## Canonical composition

elo-authz → AuthorizationDecision → GovernedHermesRuntimeBridge → HermesHttpRuntimeClient → external Hermes runtime

Existing owners remain authoritative for authorization, execution identity, runtime evidence, deployment reality, production admission, Evolution Gate and promotion.

## Preconditions

The transport requires:

1. a canonical transport-valid AuthorizationDecision;
2. authorization bound to the requested skill/resource;
3. an HTTPS endpoint;
4. a bearer credential supplied outside source control;
5. request identity preserved by the external runtime;
6. explicit environment=production in the runtime response.

These are transport/runtime facts. They do not constitute production proof by themselves.

## Evidence boundary

The external runtime response can be consumed by the existing runtime evidence intake and canonical execution/evidence binding.

Production proof remains subject to to_production_outcome(), including independently verified deployment reality, authorized execution bindings and existing repeatability requirements.

No production outcome is inferred from deployment, connectivity, HTTP success, or a single execution.

## Configuration

- HERMES_PRODUCTION_RUNTIME_URL
- HERMES_PRODUCTION_RUNTIME_TOKEN

Credentials must remain outside source control and test fixtures.

## Status

This transport implementation is a runtime capability only. It does not execute the production runtime, promote candidates, mutate canonical memory or authorize itself.
