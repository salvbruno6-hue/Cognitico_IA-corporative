# ELO — Flow Complementarity Intelligence

## Status

**Experimental architectural contract — candidate for governed adoption.**

This component gives the ELO cognitive orchestrator a reusable mechanism for recognizing when existing flows are complementary and for selecting the next compatible flow after a governed outcome.

It is **not** a second orchestrator, approval engine, memory authority or promotion engine.

## Objective

When one ELO flow becomes active, ELO should not require a human to manually identify every subsequent flow when the repository already contains enough evidence to establish a valid relationship.

The intelligence answers:

> Which existing flow can consume the output of this flow, under which prerequisites, with what evidence, and what should happen if the relation is uncertain?

## Core principle

FLOW_A → RESULT → RELATION → ELIGIBLE_FLOW_B → ENTRY_GATE → EXECUTION

A flow is connected to another flow because of an explicit relationship between its **output contract** and the next flow's **input contract**, not merely because the flows appear adjacent in documentation.

## Complementarity relations

| Relation | Meaning |
|---|---|
| FEEDS | output of A is a valid input to B |
| REQUIRES | A cannot continue without evidence from B |
| VALIDATES | B validates an artifact/result produced by A |
| CORRECTS | B receives a failed/retest result from A |
| ENRICHES | B adds evidence/context without replacing A's authority |
| HANDOFF | responsibility moves from A to B under an explicit contract |
| RETURNS_TO | B produces an outcome that routes back to A |
| BLOCKS | B prevents A's next transition until a condition is resolved |

## Flow profile

Every flow that participates in automatic composition should eventually expose:

- flow_id
- owner
- purpose
- accepts
- produces
- prerequisites
- success_outcomes
- failure_outcomes
- evidence_required
- provenance_required
- authority
- side_effect_class
- allowed_next_relations

The profile describes the flow. It does not grant permission.

## Connection decision

The ELO should evaluate candidate connections in this order:

1. Identity — is the flow known and canonical?
2. Contract compatibility — can B consume A's output?
3. Evidence — is the relation explicitly evidenced?
4. Prerequisites — are B's entry requirements satisfied?
5. Authority — does B preserve the existing authority map?
6. Security/isolation — are scope and provenance intact?
7. Outcome — did A produce an outcome that permits this relation?
8. Cadence — is the transition registered in the governed cadence map?

Only when all applicable conditions pass may the connection become ELIGIBLE.

## Uncertainty

The intelligence must never invent a connection.

If the relation is:

- unknown → UNRESOLVED
- contradictory → CONFLICT
- insufficiently evidenced → REVIEW_REQUIRED
- blocked by prerequisites → WAITING
- valid and gated → ELIGIBLE
- explicitly activated → ACTIVE

UNRESOLVED, CONFLICT and REVIEW_REQUIRED never auto-execute the next flow.

## Learning the relationships

The intelligence may learn **relationships**, not authority.

A successful sequence can produce an experience such as:

A --FEEDS→ B

but one successful execution does not make that relation canonical.

Repeated evidence can produce a governed learning candidate. Promotion remains subject to the existing ELO learning/Evolution Gate process.

## Example

A Hermes candidate completes:

CONTROLLED_TEST → PASS

The cadence registry says:

CONTROLLED_TEST → MEASURED_GAIN

The complementarity intelligence then verifies:

- MEASURED_GAIN accepts controlled-test evidence;
- required metrics exist;
- provenance is preserved;
- no regression exists;
- the candidate remains bounded.

Result:

ELIGIBLE → MEASURED_GAIN

It does **not** skip directly to ELO approval.

## Closed-loop behavior

The intelligence should eventually support:

OBSERVE → CLASSIFY → SELECT FLOW → CHECK ENTRY → EXECUTE → CAPTURE OUTCOME → SELECT NEXT FLOW → ...

Terminal conditions:

- COMPLETED
- BLOCKED
- ESCALATED
- FAILED
- ROLLED_BACK
- WAITING_FOR_EVIDENCE

## Architectural boundary

Canonical relationship remains:

ELO decides/orchestrates → specialized flow provides evidence or executes → ELO verifies

Therefore:

- cadence is routing;
- complementarity is relationship reasoning;
- Evolution Gate is evolution authority;
- ELO Review is cognitive decision;
- Forge executes construction;
- GitHub records/version-controls;
- Supabase provides consultative memory;
- ELO remains the cognitive orchestrator.

## Adoption rule

This document is an architectural candidate until validated through the normal ELO evidence path.

It must not be treated as a runtime capability merely because it exists in the repository.
