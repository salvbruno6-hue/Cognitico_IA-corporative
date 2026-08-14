# ELO-ORG Metamodel

## Core object types

| Object | Purpose | Minimum identity |
|---|---|---|
| Domain | bounded organizational responsibility | `domain_id` |
| Process | business flow | `process_id` |
| Module | bounded capability/function | `module_id` |
| Entity | business object | `entity_id` |
| Specialist | responsible knowledge authority | `specialist_id` |
| Standard | governed rule/pattern | `standard_id` |
| Indicator | measurable state/performance definition | `indicator_id` |
| Dependency | directed relation between objects | `dependency_id` |
| View | management-view projection | `view_id` |

## Required metadata

Every governed object must carry:

- stable identifier;
- human-readable name;
- object type;
- owner/responsible party;
- status;
- version;
- effective-from timestamp;
- optional effective-to timestamp;
- source/provenance reference;
- tenant/domain scope where applicable;
- change reason.

## Relationship vocabulary

Allowed relationship semantics must be explicit. Initial canonical relations are:

`contains`, `belongs_to`, `depends_on`, `provides`, `consumes`, `executes`, `governs`, `measures`, `specializes`, `impacts`, `derived_from`, `supersedes`.

Relationships must be directed and versioned. A relationship is not evidence that the related objects are operationally healthy; it only represents a governed structural assertion.

## Authority model

ELO-ORG owns structural assertions about the organizational model. It does not own operational truth merely because an object is present in the model.

Operational evidence must retain its own provenance and may contradict the model. When contradiction exists, the ELO Core must classify the conflict rather than silently rewriting the organizational model.

## Taxonomy rule

Controlled vocabulary must be canonicalized before adding aliases. Similar names must be resolved by semantic purpose, not by string similarity alone.

## Cross-domain rule

A cross-domain relation must identify source domain, target domain, relation type, validity interval, provenance, owner and status.

Example:

`LICITAÇÕES --defines_requirement--> ORÇAMENTO`

is distinct from:

`COMERCIAL --requests_quote--> ORÇAMENTO`.

The distinction preserves business semantics and prevents unrelated workflows from collapsing into a generic relationship.
