# ELO — Hermes Batch Implementation Loop

Candidate: EXT-BATCH-HERMES.

The probe reuses the controlled evaluation, converts its measurement into
ImplementationEvidence, validates the existing batch boundary, and runs the
governed Implementation Loop.

Expected controlled result:
- baseline bounded batch candidate rate: 1.0
- adapted bounded batch candidate rate: 1.0
- repeatable: true
- boundary integrity: true
- result: RETEST

No canonical mutation, execution authority, or automatic candidate promotion
is introduced by this probe. A merge only integrates the governed evaluation
path after all ELO gates pass.
