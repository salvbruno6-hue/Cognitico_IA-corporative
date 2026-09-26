# ELO — Hermes Functional Value Proof Method — 2026-09-26

## Objective

The candidate loop must answer whether a candidate improves an ELO-relevant function, not merely whether an adapter or contract passes.

## Evidence ladder

| Level | Meaning | Functional evolution claim? |
|---|---|---|
| CONTRACT_ONLY | schema, boundary or authority integrity | No |
| IMPLEMENTATION_BOUNDARY | candidate traverses an ELO implementation loop | No |
| FUNCTIONAL_CONTROLLED_GAIN | candidate changes an ELO-relevant task outcome with positive attributed gain | Yes, controlled evidence |
| OPERATIONAL_OUTCOME | positive gain observed in authorized operational workload | Yes, strongest |

## Anti-false-positive rule

A baseline of 0 and adapted value of 1 is not functional evidence when 0 simply means the feature was absent and 1 means a contract now exists.

The baseline and adapted paths must execute the same ELO-relevant task, with the candidate as the isolated intervention.

## Attribution rule

Functional credit requires: existing task; candidate intervention; changed outcome; measurement; repeatability; no silent contribution from another owner; no regression.

## Current result

EXT-CONTEXT-PLUGIN-HERMES and EXT-CHECKPOINT-HERMES now have positive controlled task-level gains attributable to the candidate. Context Plugin records task success 0.00 → 1.00 with provenance rejection. Checkpoint records stale-replay block rate 0.00 → 1.00 while ordinary recovery remains 1.00 → 1.00 under the existing ELO State Recovery owner. Both are accepted as valid functional-evolution evidence for the governed ELO flow. They do not require production evidence to establish the candidate's functional gain; production proof remains a separate operational claim.

EXT-CHECKPOINT-HERMES shows recovery behavior 0.00 to 1.00, but the harness invokes the existing ELO State Recovery owner directly. Therefore recovery is proven, while incremental Hermes attribution is not isolated.

The other audited candidates currently have contract/boundary evidence rather than candidate-attributed task-level gain. Learning Graph and Context Reference specifically show no incremental gain in their current controlled measurements.

## Required next experiment

same task -> baseline -> candidate intervention -> adapted task -> paired outcome -> repeat -> regression check -> attribution check -> Evolution Gate

The baseline must not be feature-absent when an equivalent ELO capability already exists.

## Promotion

`FUNCTIONAL_CONTROLLED_GAIN` is sufficient to establish functional value and advance the candidate through the existing governed ELO/Symbiont flow. It does not by itself authorize production deployment or canonical mutation. Those remain separate governance decisions.