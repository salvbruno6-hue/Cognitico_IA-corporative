# ELO Learning Extraction Authority Reconciliation

## Status

**RECONCILIATION_REQUIRED**

The live Supabase project contains an existing extraction owner:

- `public.elo_aprendizado_extrair_fontes()`
- `public.elo_aprendizado_classificar_experiencia(...)`
- `public.elo_aprendizado_gerar_conceitos_e_padroes()`
- `public.elo_aprendizado_gerar_relacoes()`

These are existing capabilities and therefore MUST NOT be recreated as a parallel Skill or second extraction engine.

## Verified live state

As of the current audit:

- 28 active/enabled learning sources exist.
- 28 have `ultima_varredura = NULL`.
- 28 have zero rows in `elo_aprendizado_extracoes`.
- The extractor is not currently represented by a matching SQL migration in the repository migration tree.

`ultima_varredura = NULL` is interpreted as **NEVER_SCANNED**, not STALE. No freshness threshold is invented by this contract.

## Authority rule

The live SQL owner is an existing capability that must be reconciled into GitHub authority before production execution is wired.

The reconciliation MUST preserve:

1. the existing function identity and responsibility;
2. provenance and duplicate protection;
3. the existing learning chain;
4. governed promotion boundaries;
5. no automatic Core/Soul mutation.

## Required execution contract before production wiring

The existing extractor currently lacks several controls required by the production scan boundary:

- per-source execution outcome;
- explicit execution envelope linkage;
- checkpoint/resume semantics;
- bounded source/row execution;
- explicit update of `ultima_varredura`;
- source-level error classification;
- evidence reference for each completed source.

The current extractor also contains a generic `LIMIT 5000` branch and does not uniformly apply the configured `regra_extracao`.

Therefore the orchestrator MUST NOT invoke the extractor broadly until these controls are reconciled.

## Symbiont classification

This condition is represented by the existing Symbiont Pattern Intake as:

`EXISTING_BUT_UNWIRED` → `INTEGRATE_EXISTING`

A proposed new Skill must not proceed while an existing owner is present but disconnected.

## Acceptance gate

Production extraction can be wired only when:

- [ ] SQL owner is versioned or an explicit canonical migration authority is documented;
- [ ] bounded execution contract exists;
- [ ] source-level evidence is persisted;
- [ ] `ultima_varredura` semantics are implemented;
- [ ] failure/resume behavior is tested;
- [ ] duplicate protection remains intact;
- [ ] orchestrator consumes the existing owner rather than creating another extractor;
- [ ] CI passes;
- [ ] first production run is explicitly observed before recurring automation is enabled.

This document is an authority-reconciliation artifact, not a second learning engine.
