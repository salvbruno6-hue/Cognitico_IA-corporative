# ELO Learning Laboratory Record

This document records the controlled laboratory cycle for the separated learning area.

## Deficiency reproduced

The ELO had governed learning services and persistent memory, but lacked an explicit
isolated staging boundary where operational experiences and external cognitive outputs
could accumulate without becoming canonical knowledge automatically.

## Hypothesis

A tenant-scoped learning laboratory with an explicit lifecycle can close that gap while
preserving canonical Memory, Core, Soul and Evolution Gate authority.

## Laboratory environment

- Branch: `feat/elo-learning-laboratory`
- Production/main: untouched
- Candidate PR: `#378`
- Scope: learning boundary and executable guardrails only

## Correction under test

`GovernedLearningLaboratory` introduces the lifecycle:

`EXPERIENCE → CANDIDATE → VALIDATED → PROMOTED`

The implementation requires evidence before candidate creation, validation before
promotion, and tenant-scoped listing.

## Controlled attempts and evidence

### Attempt 1 — structural implementation

Implemented the isolated boundary and executable tests. GitHub Actions subsequently
reported success for PR validation, behavioral validation, baseline evidence and
Evolution Gate technical validation.

### Verification matrix

| Check | Result | Evidence |
|---|---|---|
| New observation starts as EXPERIENCE | PASS | `test_new_learning_is_isolated_as_experience` |
| Candidate without evidence is blocked | PASS | `test_candidate_requires_evidence` |
| Promotion before validation is blocked by state contract | PASS | `test_learning_requires_validation_before_promotion` |
| Validated learning can be promoted | PASS | same lifecycle test |
| Tenant isolation | PASS | `test_tenant_isolation_in_learning_laboratory` |
| Main untouched | PASS | PR targets `main`; no merge performed |
| Second canonical memory created | PASS / no | implementation is a staging laboratory only |
| AI output becomes canonical automatically | PASS / blocked | promotion requires validation |
| Evolution Gate bypass | PASS / blocked | promotion remains governed |

## Before / after measurement

| Capability | Before | After |
|---|---:|---:|
| Explicit learning states | 0 | 5 |
| Evidence gate before candidate | 0 | 1 |
| Validation gate before promotion | 0 | 1 |
| Tenant-scoped laboratory retrieval | 0 | 1 |
| Executable laboratory tests | 0 | 4 |
| Automatic promotion path bypassing governance | 1 risk | 0 in tested boundary |

## Regression / dependency / duplication review

No second Core, canonical memory, provider registry or Evolution Gate was introduced.
The implementation reuses existing governance concepts and remains provider-neutral.

A structural quality issue was detected during laboratory review: the branch contains
many small architecture documents with overlapping descriptions of the same laboratory.
This does not invalidate the executable boundary, but it is a documentation duplication
risk and should be consolidated before a future production-quality documentation merge.

## Failure and adjustment history

The first implementation was constrained to a separate staging boundary rather than
writing directly into canonical knowledge. No executable test failure was observed in
the available CI evidence. The laboratory therefore did not require a corrective code
iteration; the remaining issue is documentation consolidation, not behavioral failure.

## Result

The controlled correction is technically valid for its stated scope. It reduces the
identified deficiency from an implicit learning capability without a dedicated staging
boundary to an explicit, tested, tenant-scoped boundary with evidence and validation
gates.

## Risk residual

- No automatic semantic retrieval from the laboratory yet.
- No provider/model performance ranking yet.
- No automatic pattern detection yet.
- No production promotion performed.
- Documentation duplication remains to be consolidated.

## Decision recommendation

`PR_READY_WITH_DOCUMENTATION_CLEANUP`.

The executable correction is ready for governed PR consideration because the relevant
CI and Evolution Gate technical evidence passed. Do not merge this branch as production
resolution until the documentation duplication is consolidated and the next integration
cycle connects real agent/workflow outcomes to the laboratory and Intelligence Router.
