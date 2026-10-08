# ELO Governed External Data Sources

## Status

Proposed implementation boundary.

## Purpose

Define the canonical boundary that allows an authenticated ELO identity, an external AI client, or an enterprise integration to use an external data source without making the external database a second ELO authority.

## Canonical model

```text
External AI / ELO client
        |
        v
      ELO MCP
        |
        v
     elo-authz
        |
        +--> identity
        +--> role
        +--> capability
        +--> tenant/scope
        +--> data-source access
        |
        v
  governed connector
        |
        v
 external database
```

## Authority rules

ELO remains the authorization and governance boundary.

An external database remains owned by its enterprise/application owner.

GitHub stores implementation and contract state. It is not the runtime transport for database communication.

The external AI never receives ELO service-role credentials.

The external AI never receives another user's database credentials.

A data-source credential is represented only by a protected credential reference. Secret material is resolved by the runtime connector boundary.

## Required identity relation

The authorization chain is:

`identity -> role -> capability -> scope -> data_source -> operation`

Existing identity, role, capability and scope authorities are reused. A second authorization system is prohibited.

## Data-source classes

A data source may be:

- ELO canonical data;
- enterprise-owned external data;
- user-owned external data;
- integration/service data.

The source class is part of the governed request context.

## Tenant isolation

A data source is bound to an explicit tenant/enterprise scope.

A request must fail closed when:

- the identity is inactive;
- the ELO authorization session is absent or expired;
- the requested data source is outside the identity scope;
- the requested operation is not granted;
- the connector is not approved for the source;
- the credential reference is missing or invalid.

Cross-tenant reuse requires an explicit governed scope and must not be inferred from the existence of a connector.

## Credential boundary

Credential references are metadata, not secrets.

The ELO database must not become a general-purpose secret vault unless a separate approved secret-management design is introduced.

The connector runtime resolves credentials outside ordinary application tables.

## Operations

Operations must be explicit. At minimum:

`metadata_read`, `read`, `query`, `write`, `schema_change`.

Read-only is the default for external AI integrations.

Write and schema operations require explicit capabilities and additional governance.

## Audit

Every external-source request must retain:

`request_id`, identity, tenant scope, data-source id, connector type, operation, decision, reason, timestamp, evidence/audit reference.

Audit records must not contain raw credentials.

## Relationship to current ELO MCP

The existing ELO MCP remains read-only for its current canonical ELO table allowlist.

External data-source support is an extension of the governed boundary, not a replacement and not a parallel MCP authority.

## Relationship to learning

External data may produce observations or learning candidates.

It cannot directly become canonical ELO knowledge.

The existing Evolution Gate and Learning Governance remain the promotion boundary.

## Non-goals

This contract does not yet:

- store external database passwords;
- expose arbitrary SQL;
- enable arbitrary external database writes;
- create a second identity/role system;
- bypass `elo-authz`;
- make GitHub a runtime database transport.
