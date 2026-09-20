# EXT-CONTEXT-PLUGIN-HERMES - Controlled Evaluation 2026-09-20

Candidate: EXT-CONTEXT-PLUGIN-HERMES
Existing authority: ELO Context
Primary metric: context task success rate (maximize)
Secondary safety signal: boundary integrity rate
Canonical mutation: none

Method: five deterministic context-resolution tasks are executed without a plugin and five with a verified, explicitly activated plugin signal. In both paths the existing ELO Context resolver remains the authority. A separate invalid-provenance signal verifies safe rejection.

Interpretation: equal baseline/adapted task success is not a measurable gain. Safety evidence is recorded separately and cannot substitute for the primary metric.

Promotion rule: feed the result to the governed implementation loop; do not promote from this experiment alone.
