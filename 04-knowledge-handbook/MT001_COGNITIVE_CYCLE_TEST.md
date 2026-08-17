# ELO-023 — MT-001 Cognitive Cycle Test

## Purpose

Validate the integrated ELO cognitive cycle against the Multiteiner MT-001 scenario without inventing missing information.

## Source facts supplied for the exercise

- Horizon: August through beginning of December.
- Seasonal demand: approximately 300 modules in total.
- Main models: M01, M05, M14.
- Recurring smaller demand: approximately 70 modules/month; company decided to suspend this flow.
- Current module stock: zero.
- Modules currently in quarantine are already committed to previously closed customers/leases.
- Approximately 100 modules are expected to return at the beginning of September.
- Returned modules pass through quarantine and repair.
- Repair capacity supplied: approximately 3 modules/day.
- M01 assembly time supplied: approximately 4 hours/unit.
- M05 assembly time supplied: approximately 6 hours/unit.
- M14 assembly time: not supplied.
- Some seasonal contracts require CLT employees dedicated to the contract; current CLT capacity is insufficient for part of these contracts.

## Source/provenance rule

The origin field must contain only the source excerpt or source reference that produced the fact. Analysis, interpretation and decisions are stored separately.

## Initial cognitive assessment

### Facts

The seasonal requirement is approximately 300 modules. Current stock is zero. Current quarantine modules are committed and therefore are not treated as free stock. The approximately 100 expected returns cannot be counted as seasonal availability until destination, model, repair and release status are verified.

### Inferences allowed

- The seasonal requirement should be prioritized in planning because the recurring smaller flow was suspended by the company.
- Physical return does not equal operational availability.
- A single aggregate production rate cannot safely determine feasibility while the model mix and M14 assembly time remain incomplete.
- CLT restrictions can constrain contract fulfillment independently of physical module capacity.

### Inferences prohibited

The test MUST NOT infer:

- the M01/M05/M14 mix of the 300 modules;
- exact event dates;
- exact available quantity among the 100 returns;
- M14 assembly time;
- actual total assembly capacity;
- exact CLT deficit;
- that the 300 can or cannot be fully delivered.

## Initial decision

Prioritize the seasonal portfolio, maintain the suspension of the smaller recurring flow as the stated business decision, and do not commit a definitive production quantity for the 300 until Commercial, PCP, Assembly, Rental/Yard/Repair, HR and Logistics provide the missing evidence.

Decision state: `CONDITIONAL`

## Premises requiring follow-up

| ID | Premise | Required evidence | State |
|---|---|---|---|
| P001 | Some September returns may become usable for seasonal demand | destination, model, repair and release data | WAITING_FEEDBACK |
| P002 | The supplied 3/day rate may represent an effective repair capacity | confirm what process the rate belongs to and working-day basis | WAITING_FEEDBACK |
| P003 | M14 may materially change assembly capacity | M14 assembly time | GAP |
| P004 | Suspending smaller demand releases relevant capacity | PCP capacity and committed schedule before/after suspension | WAITING_FEEDBACK |
| P005 | CLT availability may block some seasonal contracts | contract-level CLT requirement and available capacity | WAITING_FEEDBACK |

## Specialist requests

### Commercial
- confirmed versus probable seasonal events;
- required date per event;
- model mix per event;
- CLT requirements per contract.

### PCP
- productive calendar;
- committed production;
- actual assembly capacity;
- meaning and basis of the 3/day rate;
- capacity by model.

### Assembly
- M14 time;
- effective productive hours;
- team availability;
- constraints.

### Rental/Yard/Repair
- composition and destination of the 100 returns;
- quarantine and repair lead time;
- modules actually releasable for seasonal use.

### HR
- available and committed CLT capacity;
- deficit by contract/date.

### Logistics
- delivery windows and transport constraints.

## Follow-up memory rule

This exercise remains preserved until feedback is received. New feedback creates a new evidence/result state; it does not overwrite the original exercise. Any resulting parameter must retain context, provenance, validation date and conditions of application.

## Promotion rule

This MT-001 case remains a Forge/contextual experience. No case-specific number or conclusion is promoted to Core. Only a later validated and generalizable pattern or parameter may become a Core candidate through the governed promotion path.

## Expected cycle decisions

- `CONTINUE`: evidence is sufficient and next action is within scope.
- `CORRECT`: local error can be corrected without changing the objective.
- `REPLAN`: evidence invalidates the current plan but not the objective.
- `ESCALATE`: evidence is insufficient for a high-impact/irreversible decision or an authority/contract conflict exists.

For the initial state, the correct action is `CONTINUE` with specialist information requests; it is not a final production commitment.
