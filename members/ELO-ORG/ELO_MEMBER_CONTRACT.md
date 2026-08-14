# ELO Member Contract

## Purpose

The Member Contract is the stable boundary between the ELO Core and specialized members. It prevents members from becoming parallel cognitive cores while allowing independent domain evolution.

## Required member capabilities

Every active member must expose:

1. identity and version;
2. declared domain and scope;
3. capability catalogue;
4. input/output contract;
5. provenance/evidence references;
6. authority and responsibility boundaries;
7. health/status information;
8. dependency declarations;
9. lifecycle state;
10. compatibility information.

## Interaction model

```text
ELO Core
  -> resolve context
  -> select member
  -> provide scoped request
  -> receive bounded result + evidence
  -> evaluate provenance/conflict/uncertainty
  -> integrate with other members
  -> reason and decide
```

The member does not make the ELO's global decision unless a separate governed policy explicitly delegates a bounded operational action.

## Result contract

A member response must distinguish:

- `SUPPORTED` — supported by declared evidence;
- `INCONCLUSIVE` — insufficient evidence;
- `CONFLICTING` — material evidence conflict;
- `BLOCKED` — cannot proceed under policy or dependency constraints.

Every result must identify the relevant member, version, scope, evidence references, validity interval and confidence/uncertainty where applicable.

## Security and isolation

Requests and results must preserve tenant/domain scope. A member must not expose information outside the authorized scope. Cross-domain access requires an explicit governed relationship.

## Failure semantics

Timeout, unavailable provider, malformed result, missing provenance, or scope violation must not be silently converted into a successful result.

## Evolution

A member may evolve independently, but contract-breaking changes require a new contract version or migration path. The Evolution Gate evaluates compatibility before activation.

## ELO-ORG implementation boundary

ELO-ORG may answer organizational structure, ownership, taxonomy, process/module relationships, dependencies and management-view definitions. It must not become the owner of global reasoning, memory, decision governance or provider orchestration.
