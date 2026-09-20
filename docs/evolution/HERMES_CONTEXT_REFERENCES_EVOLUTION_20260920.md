# Hermes → ELO — Context References Evolution

**Date:** 2026-09-20  
**Classification:** EXPERIMENTAL / CONTRACT  
**Candidate:** `EXT-CONTEXTREF-HERMES`

## Source observation

Current Hermes exposes inline context references for files, folders, git history/diffs and URLs. Its implementation also defines a provider extension surface for additional `@prefix:` references. The observed runtime expands references before the model turn and applies workspace/path and context-budget controls.

## ELO decision boundary

ELO must not copy Hermes' retrieval implementation or create a second source authority.

The candidate is therefore introduced as a **non-operational parsing contract** only:

```text
Hermes-style @reference
        ↓
ELO ContextReference parser
        ↓
reference intent + provenance-neutral metadata
        ↓
ArtifactResolver OR SourceDiscovery
        ↓
SourceResolver / authorized adapter
        ↓
ContextPack / Evidence / Provenance
```

The parser does not read files, execute git, fetch URLs, or mutate memory.

## Reuse map

| Hermes mechanism | ELO owner | Candidate treatment |
|---|---|---|
| `@file:` | `ArtifactResolver` | parse only; resolver remains owner |
| `@folder:` | `ArtifactResolver` / future registered artifact scope | parse only; no filesystem traversal |
| `@diff` | `SourceDiscovery` → GitHub adapter | classify required capability |
| `@staged` | `SourceDiscovery` → GitHub adapter | classify required capability |
| `@git:N` | `SourceDiscovery` → GitHub adapter | classify required capability |
| `@url:` | `SourceDiscovery` → Web adapter | classify required capability |
| plugin `@prefix:` | future ELO extension point | not admitted by this change |

## Safety and governance

- No Hermes source is modified.
- No business operation is executed.
- No SO 001.26 is used as architectural evidence.
- No file, git repository or URL is accessed by the candidate implementation.
- The parser does not create or promote knowledge.
- Source resolution remains governed by existing ELO contracts.
- Provenance is expected to be attached by the downstream resolver/adapter, not manufactured by the parser.

## Validation

The controlled test suite covers:

1. file reference with line range;
2. folder and git references;
3. diff, staged and URL references;
4. quoted targets containing spaces;
5. trailing punctuation handling;
6. messages without references;
7. ordering and non-operational behavior.

## Promotion rule

This PR validates the **contract implementation**, not production activation of the Hermes capability. Promotion remains blocked until an integration experiment demonstrates measurable benefit over the existing ELO context path, preserves provenance/scope boundaries, and passes the applicable Evolution Gate.
