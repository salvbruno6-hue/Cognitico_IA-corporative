# EXT-PRE-INFERENCE-VETO-HERMES

Status: CANDIDATE — requires CI, review and Evolution Gate before promotion.

## Discovery

Hermes upstream on 2026-11-01 introduced a `pre_llm_call` block seam and then hardened it so a vetoed prompt is not exposed through later compaction, session search, external-memory handoff or background review. Blocked turns also skip auxiliary model work.

## ELO adaptation

The candidate does **not** copy Hermes hooks and does not create a new Core, Router, Memory owner, model runtime or plugin authority. It expresses a narrow invariant inside the existing ELO Core/Policy boundary:

> A pre-inference policy veto must stop the inference request and auxiliary context egresses for that turn; malformed policy results fail closed; a veto never grants execution authority.

The classifier accepts only explicit `allow` or explicit `block` with a non-empty operator-safe message. It never returns the raw prompt.

## Non-goals

- no Hermes mutation;
- no business operation;
- no model invocation;
- no external-memory invocation;
- no Supabase mutation;
- no new authorization authority;
- no use of SO 001.26 as architectural evidence.

## Evidence required for promotion

1. focused unit tests pass;
2. repository Behavioral/PR1/Baseline/Forge gates pass;
3. Evolution Gate passes;
4. independent review has no unresolved findings;
5. no duplicate canonical owner is introduced.

Runtime/production behavior remains INDETERMINATE until directly observed after governed promotion.
