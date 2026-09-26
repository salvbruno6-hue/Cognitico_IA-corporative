# ELO — Hermes Current Candidates — 2026-09-26

Status: CANDIDATE-ONLY / CONTROLLED VALIDATION
Authority: ELO Governance
Hermes authority: reference-only

## Scope

Five newly observed Hermes surfaces are entering the existing ELO discovery → transformation → testing → Evolution Gate loop.

1. EXT-CODE-EXEC-HERMES — programmatic tool calling / execute_code.
2. EXT-API-HERMES — OpenAI-compatible API boundary.
3. EXT-ACP-HERMES — Agent Client Protocol / IDE integration.
4. EXT-PLUGIN-CATALOG-HERMES — curated plugin discovery.
5. EXT-PROMPT-CACHE-HERMES — cross-session prompt caching.

## Candidate introduction rule

Each candidate must:

- map to an existing ELO owner;
- preserve source revision and evidence provenance;
- define a native contract;
- remain candidate-only until implementation tests, provenance, consistency and Evolution Gate approval pass;
- avoid Hermes as a runtime dependency;
- avoid business operations during discovery/validation;
- avoid creation of parallel authority, registry, scheduler, memory or router.

## Controlled test boundary

The first loop proves structural/native-contract integrity only. It does not claim that the Hermes source mechanism itself has been functionally reproduced.

Required next evidence for functional validation:

source-level interface evidence → native implementation → controlled fixture → repeatability → measured gain → regression check → Evolution Gate.

## Explicit exclusions

- Hermes is not modified.
- SO 001.26 is not used as architectural evidence.
- No candidate is promoted to Core or canonical memory.
- No business operation is executed.
- No production deployment is authorized by this candidate package.
