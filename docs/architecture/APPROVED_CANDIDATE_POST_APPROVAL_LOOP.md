# Approved Candidate Post-Approval Loop

This contract closes the gap between an explicit implementation decision and
already-approved candidates.

## Governed sequence

`implementation decision APPROVED`
→ `approved candidate selection`
→ `DEPLOYED/USED`
→ `OBSERVING`
→ `OUTCOME`
→ `REVIEW`

The loop is fail-closed.

It does not approve candidates, bypass human approval, replace Evolution Gate,
create a candidate registry, create a second memory authority, or promote
canonical knowledge.

Only candidates explicitly referenced by the approved implementation decision
and carrying `approval_state=approved` may enter the post-approval loop.

The implementation reference is mandatory so the activation remains tied to a
real implementation surface.

`OBSERVING` is the activation result. Outcome and review remain subsequent
steps and must use the existing Decision Outcome Loop and learning governance.
