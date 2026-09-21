# ELO — Hermes Profile Implementation Loop

Candidate: EXT-PROFILE-HERMES.

The probe reuses the controlled evaluation, converts its measurement into
ImplementationEvidence, validates the existing ELO Context boundary, and runs
the governed Implementation Loop.

Expected controlled result:
- baseline isolated profile candidate rate: 1.0
- adapted isolated profile candidate rate: 1.0
- repeatable: true
- boundary integrity: true
- result: RETEST

No canonical mutation, execution authority, profile authority, or automatic
candidate promotion is introduced by this probe. A merge only integrates the
governed evaluation path after all ELO gates pass.
