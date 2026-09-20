# Hermes Batch Processing — ELO Evolution Boundary

## Source observation

Hermes documents batch trajectory generation as a bounded way to produce multiple agent trajectories for evaluation or dataset-oriented workflows.

## ELO adaptation

Candidate ID: `EXT-BATCH-HERMES`

The ELO adaptation treats batch processing as an evaluation-intake mechanism, not as autonomous learning or promotion.

## Boundary rules

1. Batch identity, tenant scope, task and output schema are mandatory.
2. Provenance is mandatory.
3. The batch must be bounded and explicitly authorized before candidate status.
4. Canonical mutation and promotion attempts are rejected.
5. Assessment grants no execution, canonical, or promotion authority.
6. Results must enter the existing ELO evaluation/learning governance path.

No production batch execution is activated by this change.
