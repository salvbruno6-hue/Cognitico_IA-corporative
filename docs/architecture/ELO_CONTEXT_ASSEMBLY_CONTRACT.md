# ELO Context Assembly Contract

**Status:** IMPLEMENTATION BASELINE

## Purpose

Define how ELO assembles decision context from its distributed memory fabric without creating a second memory authority.

## Boundary

```text
Intent
  -> Knowledge Need
  -> Existing Memory Adapter
  -> Scoped Candidates
  -> Stable De-duplication
  -> Provenance
  -> KnowledgeContext
  -> Cognitive interpretation / decision
```

The assembly layer is read-only. It does not write Supabase, promote learning, grant authorization, modify Core/Soul, or execute Hermes capabilities.

## Source precedence

For consequential decisions, context should be resolved in this conceptual order:

1. Soul/Core invariants;
2. applicable canonical domain rules;
3. current operational records;
4. specialized domain memory;
5. relevant experience records;
6. experience and reasoning patterns;
7. governed corporate learning;
8. prior decisions/arbitration;
9. supporting evidence;
10. objective and information gaps.

The assembler does not copy these layers into one persistent store. It resolves references into a bounded, transient `KnowledgeContext`.

## Scope

A candidate is usable only when its source record satisfies the requested scope. Unknown scope is not evidence of equivalence. Cross-scope records must not be merged into a decision context.

## Provenance

Every assembled candidate must retain a stable source identity and available provenance. Source references are preserved; the assembler must not manufacture provenance.

## Deduplication

The same source identity may be requested by multiple knowledge requirements. It appears once in the assembled context. Re-running the same assembly with identical inputs must produce the same result.

## Gaps

An unresolved requirement becomes an explicit `KnowledgeGap`. The assembler does not infer a substitute source for an unknown requirement. A blocking gap prevents the context from being treated as decision-complete.

## Status semantics

Source status is normalized by the existing adapter. Storage does not equal validation, and validation does not equal canonical promotion.

## Domain pilots

Initial context assembly is intended for Orçamento, with subsequent pilots in Qualidade and PCP. Domain-owned records remain in their source tables.

## Prohibitions

- No universal memory table.
- No duplicate operational records.
- No automatic learning promotion.
- No authorization inference.
- No cross-tenant or cross-scope context mixing.
- No mutation of historical source records.
- No external runtime becomes a knowledge authority.

## Acceptance criteria

The implementation is accepted when deterministic tests demonstrate:

- stable assembly;
- stable source identity;
- duplicate prevention;
- scope isolation;
- explicit missing-information gaps;
- provenance preservation;
- source immutability;
- no promotion side effects.
