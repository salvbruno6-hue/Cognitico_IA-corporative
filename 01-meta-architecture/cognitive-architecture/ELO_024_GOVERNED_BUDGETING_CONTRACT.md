# ELO-024 — Governed Budgeting Contract

## Purpose

Define the canonical behavior required for ELO to prepare, calculate, compare, revise, recommend and monitor corporate budgets autonomously within explicit authority boundaries.

## Architectural position

Budgeting is a capability of the ELO/Core ecosystem, not a second cognitive core and not an isolated financial authority.

```text
ELO Cognitive
  ↓ supervision / canonical identity
Core
  ↓ systemic intelligence / governed capabilities
Budgeting capability
  ↓ uses
Context + Source Discovery + Evidence + Provenance + SystemicModel
  + Scenario + Uncertainty + Decision + OutcomeFeedback
  ↓
Forge / specialist experience when contextual detail is required
```

## Autonomy definition

ELO may autonomously:

- interpret a budget request;
- identify scope and context;
- discover authorized sources;
- collect and reconcile inputs;
- classify facts, commitments, availability, assumptions, estimates and gaps;
- calculate using approved formulas/parameters;
- build scenarios and sensitivities;
- identify inconsistencies and missing evidence;
- request specialist follow-up;
- recalculate when evidence changes;
- compare versions;
- recommend a budget and decision;
- monitor budget versus actual;
- produce outcome feedback and governed learning.

ELO may not autonomously invent inputs, approve financial commitments, bind the company contractually or perform irreversible financial actions without explicit authority.

## Budget lifecycle

```text
REQUEST
  ↓
CONTEXTUALIZE
  ↓
SOURCE DISCOVERY
  ↓
EVIDENCE / PROVENANCE
  ↓
INPUT CLASSIFICATION
  ↓
BUDGET MODEL
  ↓
CALCULATION
  ↓
SCENARIOS / SENSITIVITY
  ↓
VALIDATION
  ↓
SPECIALIST FOLLOW-UP when required
  ↓
RECALCULATION
  ↓
DECISION / RECOMMENDATION
  ↓
AUTHORIZATION
  ↓
EXECUTION when authorized
  ↓
ACTUAL VS BUDGET
  ↓
OUTCOME FEEDBACK
  ↓
GOVERNED LEARNING
```

## Canonical budget objects

Create only if no existing canonical equivalent is found:

- `BudgetRequest` — intent, scope, tenant, period and objective;
- `BudgetVersion` — immutable version of the budget calculation;
- `BudgetLine` — classified cost/revenue/resource line;
- `CostComponent` — amount, unit basis, source and formula reference;
- `Assumption` — explicit premise with evidence and validity;
- `CapacityConstraint` — resource/capacity limitation and source;
- `BudgetScenario` — scenario definition and changes from baseline;
- `BudgetSensitivity` — controlled parameter variation and effect;
- `BudgetDecision` — recommendation, rationale, evidence and authority boundary;
- `BudgetOutcome` — actual result versus forecast.

## Classification rules

Every input must be classified as one of:

```text
FACT
COMMITTED
AVAILABLE
ASSUMPTION
ESTIMATE
HYPOTHESIS
GAP
CONFLICT
```

`GAP` is not zero. `UNKNOWN` is not zero. `COMMITTED` is not necessarily `AVAILABLE`.

## Calculation rules

Every calculated result must retain:

- input references;
- formula identifier/version;
- parameter identifiers/versions;
- unit and period;
- rounding policy where applicable;
- calculation timestamp;
- evidence/provenance;
- scenario/version;
- confidence/uncertainty where applicable.

A result must be reproducible from the retained inputs and calculation definition.

## Cross-domain budgeting

The ELO may relate:

```text
COMERCIAL
   ↓
LICITAÇÕES
   ↓
ORÇAMENTO
   ↓
PROJETO / ENGENHARIA
   ↓
COMPRAS / SUPRIMENTOS
   ↓
PCP
   ↓
PRODUÇÃO
   ↓
LOGÍSTICA
   ↓
RESULTADO
```

The relation does not merge domains. Each fact keeps its source authority, tenant/domain, principal, temporal validity and provenance.

## Scenario policy

When inputs support it, the ELO should evaluate:

- baseline;
- conservative;
- stress;
- counterfactual;
- sensitivity.

Scenario generation must not silently modify canonical facts or historical memory.

## Missing-data policy

If a critical input is absent, ELO must:

1. identify the exact gap;
2. state why it affects the calculation;
3. identify the responsible specialist/domain when determinable;
4. create follow-up;
5. preserve the current budget version as conditional/incomplete;
6. recalculate when feedback arrives.

No fabricated value may close a critical gap.

## Version and memory policy

A revised budget creates a new version. Previous versions remain immutable historical evidence.

Budget-specific experience remains contextual/operational in Forge unless it is generalized, validated and promoted under the Core evolution contract.

## Authorization policy

The ELO distinguishes:

```text
PREPARE
CALCULATE
RECOMMEND
APPROVE
COMMIT
EXECUTE
```

A capability to calculate does not imply authority to approve or execute.

## First integrated scenario

MT-001 is the first acceptance scenario. It must use the information actually provided about seasonal demand, recurring demand, returns, quarantine, repairs, assembly capacity, M01/M05/M14 and CLT restrictions. Missing M14 timing and other missing specialist evidence remain gaps until supplied.

## Required adversarial tests

- missing input;
- contradictory source;
- stale input;
- committed versus available resource;
- insufficient capacity;
- supplier unavailable;
- specialist unavailable;
- unauthorized approval;
- cross-tenant leakage;
- cross-domain authority violation;
- formula/version mismatch;
- historical version mutation;
- fabricated-value attempt;
- scenario state mutation;
- provider failure/retry;
- post-budget outcome deviation.

## Promotion boundary

Budget execution data may produce contextual learning. Only a generalizable, evidenced and governed pattern/parameter may be promoted to Core. The original enterprise experience remains preserved in Forge.

## Definition of Done

- canonical reuse search completed;
- no duplicate financial authority created;
- budget calculation reproducible;
- provenance complete;
- scenarios executable;
- gaps produce follow-up;
- versions immutable;
- authorization boundaries tested;
- MT-001 exercised;
- ELO PR1 Validation PASS;
- Behavioral Validation PASS;
- Evolution Gate PASS;
- post-merge verification recorded.