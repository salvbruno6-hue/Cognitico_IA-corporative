# Hermes current refinements -> ELO

Source: Hermes Agent v0.21.0, tag 29112be, released 2026-08-31.

## Live subagent steering
Refinement of EXT-MULTIAGENT-HERMES. The candidate contract requires parent execution identity, child execution identity, explicit directive identity and provenance. It does not grant ELO authorization.

## Cron memory and continuity
Refinement of EXT-CRON-HERMES. The candidate contract requires automation identity, prior-run reference, bounded continuity scope and provenance. Continuity does not become canonical ELO memory automatically.

## Validation boundary
Candidate-only and side-effect free. These contracts do not invoke Hermes, mutate Hermes, execute tools, schedule jobs, delegate agents or perform business operations. Functional validation still requires runtime integration, measurable directional gain, repeatability, regression evidence and the existing Evolution Gate.

No new owner, Evolution Gate, memory authority, scheduler or promotion path is introduced.
