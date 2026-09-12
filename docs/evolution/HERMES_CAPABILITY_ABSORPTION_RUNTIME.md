# ELO — Hermes Capability Absorption Runtime

## Purpose

Operationalize the existing Symbiont capability-absorption boundary using structural patterns verified in the `salvbruno6-hue/ELO-Hermes-Agent` repository.

This implementation extracts **portable mechanisms**, not Hermes source code. Extraction is evidence-backed and feeds the existing ELO Pattern Intake, Evolution Gate and Capability Absorption pipeline.

## Verified Hermes source

- Repository: `salvbruno6-hue/ELO-Hermes-Agent`
- Branch: `main`
- Source commit: `278a7d1cc07daa3d0b73934673afccf2310a30b1`

The Hermes runtime currently exposes a governed bridge contract in `elo_bridge/contract.py`, including authorized execution requests, evidence/outcome results and explicit non-canonical learning candidates. Its CI also validates the bridge, skill runtime and HTTP runtime through `.github/workflows/elo-hermes-runtime-validation.yml`.

## Extracted capabilities

| ID | Portable capability | Evidence | ELO treatment |
|---|---|---|---|
| HERMES-CAP-001 | Governed execution boundary | `elo_bridge/contract.py`, adapter/runtime bridge | Candidate through Pattern Intake + Evolution Gate |
| HERMES-CAP-002 | Non-canonical learning candidate | `elo_bridge/contract.py`, `elo_bridge/skill_runtime.py` | Candidate; never canonical automatically |
| HERMES-CAP-003 | Runtime contract validation | Hermes bridge tests + CI workflow | Candidate for reusable regression/validation behavior |

## Runtime flow

```text
Hermes repository evidence
        ↓
HermesCapabilityExtractor
        ↓
ExternalPatternInput / ExternalCapabilityObservation
        ↓
Symbiont Pattern Intake
        ↓
Evolution Gate
        ├── duplicate → REUSE
        ├── adaptation → LAB_EXPERIMENT
        ├── conflict/incompatible → BLOCK
        └── compatible → LAB_CANDIDATE
        ↓
Symbiont Capability Absorber
        ↓
ELO capability candidate
        ↓
existing learning/promotion authorities
```

## Non-negotiable boundaries

1. The extractor does not write canonical ELO state.
2. The extractor does not grant authorization.
3. Hermes remains an execution/evidence source, not an ELO authority.
4. The Evolution Gate remains the evolution authority.
5. External learning remains candidate-only until the existing governed promotion path validates it.
6. No new database table or second Core is required.
7. Evidence must include source identity and source commit.
8. Missing evidence prevents extraction.

## Why this closes the previous gap

The previous architecture already contained Pattern Intake and Capability Absorption, but lacked a deterministic bridge from a real Hermes repository snapshot into those boundaries. `HermesCapabilityExtractor` supplies that missing operational layer while preserving the existing authority model.

The extractor is intentionally snapshot-based. A future repository adapter may obtain a snapshot from an authorized source, but acquisition remains separate from extraction so the ELO Core does not silently gain repository/network authority.
