# ELO Data Engineering — Local Agent Rules

## Scope

This directory governs data contracts, ingestion, transformation, quality, storage, lineage, and data lifecycle.

## Rules

- Preserve source identity and lineage.
- Preserve tenant/domain boundaries when applicable.
- Do not mix operational data with derived analytical claims without labeling the derivation.
- Validate schemas before ingestion.
- Prefer explicit contracts over implicit field assumptions.
- Do not delete or reshape existing data models solely to simplify an implementation without migration analysis.
- Distinguish raw/source data, normalized data, derived data, evidence, and analytical conclusions.
- Treat missing data as an information gap, not permission to invent a value.
- Record quality limitations when they can affect reasoning or decision support.
