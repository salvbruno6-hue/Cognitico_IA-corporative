# ELO Learning Laboratory Record

This document records the implemented architectural decision for the separated
learning area introduced in the current change.

## Implemented boundary

`GovernedLearningLaboratory` stores tenant-scoped observations and exposes a
controlled lifecycle from experience to candidate, validation and promotion.

## Invariants

1. New observations enter as `EXPERIENCE`.
2. Candidate creation requires evidence.
3. Validation is required before promotion.
4. Tenant listing is isolated by tenant identifier.
5. The laboratory does not replace canonical memory, Core or Evolution Gate.

## Example

A budgeting AI may return a calculation and a specialist may correct it.
Both can be captured as experience. Repeated evidence may create a candidate
such as "this dependency is frequently missed". Only after validation can the
learning be promoted to governed knowledge.

## Next integration

Connect the laboratory to the existing workflow/agent outcome recording and
Intelligence Router so provider/model/specialist/tool performance can be
measured from real outcomes. Do not create a second memory authority.
