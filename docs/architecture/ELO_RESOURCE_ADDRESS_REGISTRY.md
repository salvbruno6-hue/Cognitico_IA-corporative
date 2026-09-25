# ELO — Resource Address Registry

## Objective

ELO must not rediscover where its governed knowledge and operational resources live on every request. A resource must have a stable logical identity and a registered physical address.

The registry is the navigation layer between a semantic request and the resource location. It is not a second knowledge base, memory, router, authorization system, or learning graph.

## Resolution pattern

```text
USER REQUEST
    ↓
SEMANTIC RESOURCE ID
    ↓
ELO RESOURCE ADDRESS REGISTRY
    ↓
PHYSICAL ADDRESS
    ↓
READ / EXECUTE THROUGH THE AUTHORIZED PROVIDER
```

Example:

```text
"quero conferir excedentes"
        ↓
ELO.DB.TABLE.EXCEDENTES
        ↓
public.excedentes
        ↓
authorized database read
```

A known directory follows the same pattern:

```text
"abrir a pasta de orçamento"
        ↓
registered repository directory
        ↓
<known repository path>
        ↓
authorized repository read
```

The same principle applies to canonical files:

```text
"ELO metodologia de orçamento"
        ↓
canonical artifact/resource identity
        ↓
04-knowledge-handbook/MULTITEINER_METODOLOGIA_ORCAMENTO_ELO.md
        ↓
authorized repository read
```

## Resource classes

The registry may address:

- repository files and directories;
- Supabase tables and views;
- database functions;
- governed documents;
- external source references;
- other explicitly approved resources.

Every entry must identify its provider and resource type.

## Required fields

```text
resource_id
resource_type
provider
logical_name
physical_address
canonical
status
scope
authority
provenance
```

Optional aliases may point known terminology or historical paths to the same stable `resource_id`. Aliases are explicit and governed; the locator does not perform fuzzy semantic guessing.

## Rules

1. Stable identity is the key; physical address is a location attribute.
2. A path change must not create a new logical resource when identity remains the same.
3. An alias may preserve historical paths or approved terminology.
4. The registry does not grant authorization.
5. The registry does not infer causality.
6. The registry does not create learning.
7. The registry does not replace the existing canonical artifact resolver.
8. Canonical documentary artifacts continue to use `artifact_id → canonical_path`.
9. Database resources use their governed database address, for example `public.<table>`.
10. Reads must still pass through the authorized provider boundary.
11. Ambiguous identities or addresses are blocked rather than guessed.
12. Registry entries must preserve provenance and ownership.
13. Repository directories are derived from the authoritative Git tree; they are not separately inferred resources.
14. The registry should be generated from current provider inventories, while stable semantic identities/aliases remain governed.

## Fast lookup behavior

The cognitive layer should be able to resolve in one step:

```text
"tabela excedente"
→ ELO.DB.TABLE.EXCEDENTES
→ public.excedentes
→ authorized read
```

It should not perform an unrestricted repository scan or database-wide search when a registered address already exists.

## Relationship with Context Engineering

Context Engineering supplies the semantic need.

The Resource Address Registry supplies the location.

The authorized provider performs the read.

Therefore:

```text
Context Need
    ↓
Resource Identity
    ↓
Address Registry
    ↓
Authorized Read
    ↓
Evidence / Context
```

The registry is therefore a fast navigation/index boundary, not another retrieval or reasoning engine.
