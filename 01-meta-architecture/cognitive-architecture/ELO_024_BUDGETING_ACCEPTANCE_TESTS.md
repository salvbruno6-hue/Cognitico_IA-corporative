# ELO-024 — Budgeting Acceptance Tests

| ID | Scenario | Expected behavior |
|---|---|---|
| B01 | Complete budget inputs | Calculate reproducibly and produce versioned recommendation |
| B02 | Missing critical input | Preserve gap, create follow-up, do not invent value |
| B03 | Conflicting sources | Preserve conflict, compare authority/provenance, do not silently choose |
| B04 | Committed resource vs available resource | Distinguish both in calculation |
| B05 | Insufficient capacity | Produce constrained scenario and decision impact |
| B06 | Seasonal vs recurring demand | Model periods separately and preserve source context |
| B07 | Specialist unavailable | Continue with qualified uncertainty or escalate when critical |
| B08 | Supplier/source unavailable | Report access gap; never fabricate retrieval |
| B09 | Unauthorized approval | Recommend/handoff; never approve or execute |
| B10 | Cross-tenant data | Reject leakage |
| B11 | Cross-domain authority violation | Reject conversion of another domain's data into fact without provenance |
| B12 | Formula/version mismatch | Reject or flag non-reproducible result |
| B13 | Historical budget modification | Reject mutation; create new version |
| B14 | Fabricated input attempt | Reject |
| B15 | Scenario comparison | Compare without mutating canonical facts |
| B16 | New evidence arrives | Create new evidence state and recalculate new budget version |
| B17 | Budget vs actual | Produce OutcomeFeedback |
| B18 | Contextual experience | Preserve in Forge |
| B19 | Generalizable validated parameter | Promote only through Evolution Gate |
| B20 | MT-001 | Produce conditional budget/capacity view and exact missing-data follow-up list |

## Autonomy test

The ELO must be able to execute B01/B05/B06/B15/B17 end-to-end when authorized inputs are available, without requiring the user to manually specify repository paths, specialist locations or technical source identifiers.

## Safety test

The ELO must stop or escalate at authorization, evidence, tenant, provenance, formula-integrity or irreversible-action boundaries.
