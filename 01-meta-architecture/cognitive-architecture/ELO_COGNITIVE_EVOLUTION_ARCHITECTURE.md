# ELO — Cognitive Evolution Architecture

**Status:** PROPOSED / REFERENCE  
**Layer:** `01-meta-architecture`  
**Directory:** `01-meta-architecture/cognitive-architecture/`  
**Authority:** architectural proposal; not a substitute for approved baseline or ADR  
**Purpose:** define the target cognitive architecture needed for contextual understanding, decision support, scenario analysis and adaptive replanning.

> This document must be read after `01-meta-architecture/cognitive-architecture/README.md` and the repository authority/governance documents. It does not authorize implementation by itself.

---

# 1. Objective

Evolve ELO so that it can continuously:

**understand → contextualize → diagnose → decide → plan → execute → monitor → learn → replan**

The target is not merely a repository, dashboard or conversational interface. ELO should become a governed cognitive layer capable of transforming data, events, knowledge, context, constraints and organizational experience into coherent decisions and adaptive plans.

The system should answer not only:

- What is happening?
- Why is it happening?
- What should be happening?
- What changed?
- What is affected?
- Which decisions are now invalid?
- Which alternatives are feasible?
- What is the best next step under the current context?
- Is the current plan still coherent?
- What must be replanned?
- How do we restore a clear beginning, middle and end to the flow?

---

# 2. Fundamental principle: planning is alive

Planning must be treated as **living, contextual and adaptive**.

A master plan, production plan, capacity plan, purchasing plan, project plan, target or strategic objective must not be treated as immutable when reality changes.

The core adaptive chain is:

**event → impact → dependencies → conflicts → risks → alternatives → decision → new plan → communication → monitoring**

The objective is not merely to record that a change occurred. The objective is to understand the change and reconstruct a coherent operational path.

---

# 3. ELO mental model

The cognitive cycle must continuously distinguish:

### Current state
What is happening now?

### Expected state
What should be happening?

### Deviation
What is different between expected and actual?

### Cause
Why did the deviation occur?

### Impact
What is directly or indirectly affected?

### Decision
What decision is required?

### Action
Who will do what, when and with which resources?

### New state
What should the system look like after the action?

### Learning
What must be incorporated into organizational knowledge?

---

# 4. Enterprise context layer

ELO must understand context rather than isolated values.

Relevant context may include:

- strategy;
- corporate objectives;
- goals and targets;
- OKRs;
- KPIs;
- budget;
- capacity;
- demand;
- order portfolio;
- production capacity;
- people;
- materials;
- suppliers;
- processes;
- constraints;
- risks;
- deadlines;
- priorities;
- seasonality;
- external events;
- planning changes;
- management decisions;
- operational changes.

The same data point may have different meanings under different contexts. The architecture must preserve the context required to interpret it.

---

# 5. Objective governance: Strategy → OKR → KPI → Action

Integrate:

**Strategy → Objectives → OKRs → KPIs → Processes → Actions → Results**

ELO should detect:

- objectives without measurable indicators;
- indicators without owners;
- targets without deadlines;
- actions without strategic linkage;
- results inconsistent with objectives;
- conflicts between objectives;
- operational actions that compromise strategic objectives.

Example: if increasing deliveries is a strategic objective but a planning change reduces production capacity, ELO should identify the conflict and its likely consequences.

---

# 6. Process architecture

Processes should be represented as an interdependent network.

Each process should be able to expose:

- input;
- transformation;
- output;
- owner;
- resources;
- dependencies;
- risks;
- indicators;
- rules;
- constraints;
- events;
- decisions;
- control points.

Example operational chain:

**Demand → Engineering → PCP → Procurement → Production → Quality → Logistics → Delivery**

A change in Engineering may propagate through:

**BOM → purchasing → inventory → capacity → sequencing → lead time → delivery**

The architecture must be able to represent and traverse these dependencies.

---

# 7. Impact and dependency engine

Create a capability that can answer:

> **If X changes, what is affected?**

Analyze:

- direct dependencies;
- indirect dependencies;
- shared resources;
- capacity;
- deadlines;
- inventory;
- people;
- equipment;
- suppliers;
- indicators;
- objectives;
- risks;
- commitments.

Example:

**Demand change**

→ capacity  
→ materials  
→ procurement  
→ inventory  
→ PCP  
→ sequencing  
→ bottlenecks  
→ Lead Time  
→ delivery  
→ KPIs  
→ strategic objectives

This should be modeled as a dependency graph, not as a collection of isolated alerts.

---

# 8. Risk management

Use risk-management principles, including ISO 31000 as a reference where appropriate, without turning the standard itself into an operational software component.

The cognitive process is:

**identify → analyze → evaluate → treat → monitor**

A risk record should be able to represent:

- cause;
- event;
- consequence;
- probability;
- impact;
- criticality;
- owner;
- treatment;
- deadline;
- indicator;
- contingency plan.

Distinguish:

- known risk;
- emerging risk;
- materialized risk;
- mitigated risk.

---

# 9. Quality tools as cognitive knowledge

Quality and management tools must not be modeled merely as buttons. ELO should understand **when and why** a method is appropriate.

### Ishikawa
Structured investigation of possible causes.

### Pareto
Prioritization of high-impact factors.

### 5W2H
Conversion of a decision into an actionable plan.

### PDCA
Continuous improvement cycle.

### Visual Management
Visibility of state, performance and deviations.

### Kanban
Visual flow control and work signaling.

### FMEA
Preventive failure-mode analysis when applicable.

### Process Mapping
Understanding flow, dependencies and control points.

The system should be able to recommend an appropriate analytical method based on the problem, context and available evidence.

---

# 10. Scenario intelligence

ELO should support scenario analysis, including:

### Current scenario
What happens if the existing plan is maintained?

### Growth scenario
What happens if demand increases?

### Constraint scenario
What happens if a critical resource becomes unavailable?

### Delay scenario
What happens if a supplier is late?

### Change scenario
What happens if the master plan changes?

### Contingency scenario
Which alternative reduces the impact?

Each scenario should contain:

- assumptions;
- impacts;
- risks;
- resources;
- conflicts;
- KPI effects;
- objective effects;
- recommended plan.

---

# 11. Adaptive replanning

Adaptive replanning is a central capability.

When a relevant condition changes:

1. capture the event;
2. validate information reliability;
3. identify affected plan(s);
4. calculate impacts;
5. locate dependencies;
6. identify conflicts;
7. recalculate constraints;
8. generate alternatives;
9. compare alternatives;
10. recommend a decision;
11. request human approval when required;
12. generate the revised plan;
13. communicate the change;
14. monitor execution;
15. register learning.

ELO must not simply update a schedule.

It should explain:

- why the plan changed;
- what was affected;
- which alternatives existed;
- why one alternative was recommended;
- what assumptions were used;
- what risks remain.

---

# 12. Invariants and business rules

Create an explicit layer for rules and constraints that must not be violated.

Examples:

- maximum capacity;
- contractual deadline;
- material availability;
- quality requirements;
- legal restrictions;
- unavailable resources;
- activity precedence;
- mandatory competencies;
- financial limits;
- strategic priorities.

ELO should detect:

**rule conflict**  
**constraint violation**  
**infeasible plan**  
**inconsistent decision**

---

# 13. Decision explanation

Critical recommendations must be explainable.

Each recommendation should preserve:

- suggested decision;
- reason;
- evidence;
- data used;
- assumptions;
- risks;
- alternatives considered;
- impacts;
- responsible decision maker;
- confidence level.

Example:

> Reprogram order X to period Y because resource Z became a critical constraint. The alternative reduces projected delivery impact but increases utilization of resource W.

The wording is illustrative; production decisions must use actual evidence and provenance.

---

# 14. Knowledge management

Every significant decision should be able to generate organizational learning.

Capture, where applicable:

- decision;
- context;
- problem;
- selected alternative;
- expected result;
- actual result;
- deviation;
- learning;
- created rule;
- future recommendation.

Maintain conceptual distinction among:

**data → information → knowledge → rule → decision → experience → learning**

---

# 15. Continuous learning

When an outcome differs from expectation, ELO should investigate:

- which assumption was wrong;
- which variable was missing;
- which dependency was underestimated;
- which rule needs revision;
- which indicator should have signaled the issue;
- what knowledge should be incorporated.

The learning loop is:

**Plan → Execute → Measure → Compare → Explain → Learn → Replan**

---

# 16. Event and exception detection

Detect, where supported by available data and contracts:

- KPI deviation;
- demand change;
- delay;
- stockout;
- productivity drop;
- capacity change;
- supplier delay;
- priority change;
- resource change;
- target conflict;
- emerging risk.

Classify events as:

**informational → attention → critical → blocking**

Avoid alert overload. The purpose is to surface events that require understanding or decision.

---

# 17. Cognitive prioritization

Prioritization should consider more than chronology.

Candidate factors:

**impact + urgency + criticality + dependencies + strategy + risk + response capacity**

A low-volume event with high systemic impact may deserve priority over a high-volume event with low criticality.

The prioritization method itself must be transparent and configurable.

---

# 18. Systemic view

ELO must avoid optimizing one department while harming the overall system.

Analyze impacts across:

**sector → process → chain → organization → strategy**

Example: increasing output in one process may appear positive while creating excess work-in-process and congestion at the bottleneck.

The system should identify such trade-offs before recommending an action when evidence supports the conclusion.

---

# 19. Bottleneck intelligence

Incorporate constraint-oriented reasoning:

**identify → exploit → subordinate → elevate → reassess**

The architecture should detect:

- resources limiting flow;
- bottleneck migration;
- transferred constraints;
- improvements that create another bottleneck.

Capacity should be evaluated systemically, not only by local utilization.

---

# 20. Cognitive cycle and boundary allocation

The target cognitive cycle is:

**OBSERVE**
→ **DETECT**
→ **CORRELATE**
→ **CONTEXTUALIZE**
→ **IDENTIFY GAPS**
→ **ASK**
→ **RETRIEVE**
→ **COMPARE EXPERIENCES**
→ **FORM HYPOTHESES**
→ **GATHER EVIDENCE**
→ **REASON**
→ **SIMULATE SCENARIOS**
→ **RECOMMEND**
→ **ESCALATE**
→ **HUMAN DECISION**
→ **OBSERVE OUTCOME**
→ **LEARN**

This cycle must be distributed across existing ELO boundaries rather than placed entirely inside the Cognitive Core.

Conceptual allocation:

- Context Engine: contextualize and detect contextual gaps;
- Knowledge Engine: retrieve and qualify knowledge;
- Memory: compare prior experiences and outcomes;
- Reasoning: correlate, form hypotheses, reason and compare alternatives;
- Scenario Analysis: simulate scenarios;
- Decision Support: recommend and escalate;
- Provenance/Evidence: preserve sources and decision evidence;
- Agents: execute governed tasks within defined boundaries;
- Integration Layer: receive and publish external operational events;
- Cognitive Core: orchestrate the cognitive cycle.

The exact allocation must be reconciled with the current approved architecture before implementation.

---

# 21. Consulting Mode

A consulting capability should be treated primarily as a **governed cognitive/orchestration mode**, not automatically as a new monolith.

It should help the system:

- understand the business question;
- identify missing information;
- ask clarification questions;
- retrieve relevant knowledge;
- compare organizational experience;
- formulate hypotheses;
- gather evidence;
- analyze scenarios;
- identify capability gaps;
- recommend actions;
- escalate decisions requiring human authority.

The architecture must first determine which existing cognitive capabilities can be reused.

---

# 22. Information gaps, questions and responsibility

When information is insufficient, ELO should not invent certainty.

It should represent:

- missing information;
- conflicting information;
- stale information;
- low-confidence information;
- required clarification.

It should be able to generate targeted questions such as:

> Which assumption changed?

> Which resource is now constrained?

> Who owns the decision?

> Is the new deadline contractual or internal?

> Has the change been approved?

A Responsibility Graph should support identification of owners, decision rights and affected parties.

---

# 23. Organizational experience and knowledge domains

The architecture should distinguish at least:

- organizational health and operating context;
- organizational experience and lessons learned;
- scientific and technical knowledge;
- consultant or expert knowledge;
- current evidence;
- hypotheses;
- recommendations;
- decisions.

Do not silently convert experience, external material or model-generated hypotheses into authoritative organizational truth.

---

# 24. Consistency control

Before recommending a revised plan, validate:

- objectives;
- resources;
- capacity;
- deadlines;
- materials;
- risks;
- dependencies;
- rules;
- KPIs;
- constraints;
- responsible parties.

If contradictions remain, do not present the plan as valid.

Instead expose:

**PLAN WITH INCONSISTENCIES**

and identify what must be resolved.

---

# 25. Information confidence and provenance

Critical information should preserve:

- origin;
- timestamp;
- version;
- authority;
- quality;
- confidence;
- validity;
- context.

Distinguish:

- confirmed information;
- probable information;
- incomplete information;
- conflicting information;
- stale information.

Uncertain information must not silently become fact.

Preserve the existing distinction:

**AuditEvent != ProvenanceRecord != Evidence**

---

# 26. Human + AI governance

ELO should act as a governed cognitive copilot, not an unrestricted autonomous authority.

### AI may, within approved boundaries:

- detect;
- analyze;
- correlate;
- simulate;
- recommend;
- explain;
- anticipate;
- alert.

### Human validation should be required where applicable for:

- strategic decisions;
- major planning changes;
- critical financial decisions;
- policy/rule changes;
- organizational changes;
- high-impact decisions.

Implement explicit autonomy levels and escalation rules.

---

# 27. Cognitive maturity model

A possible evolutionary model:

### Level 0 — Information
Data only.

### Level 1 — Visibility
Dashboards and indicators.

### Level 2 — Diagnosis
Identification of deviations and causes.

### Level 3 — Recommendation
Suggested actions.

### Level 4 — Anticipation
Prediction of relevant events and risks.

### Level 5 — Assisted replanning
Generation and comparison of revised plans.

### Level 6 — Organizational learning
Past decisions and outcomes improve future recommendations.

This is a maturity model, not an implementation promise.

---

# 28. Technical architecture direction

The target architecture should remain aligned with existing ELO boundaries and may conceptually be represented as:

**Knowledge**
↓
**Domain**
↓
**Context**
↓
**Rules**
↓
**Data**
↓
**Reasoning**
↓
**Simulation**
↓
**Decision**
↓
**Orchestration**
↓
**Execution**
↓
**Observability**
↓
**Learning**

Responsibilities must remain explicit. Do not mix knowledge, rules, application logic, infrastructure, integration and decision authority without an architectural decision.

---

# 29. Cognitive data model

Candidate conceptual entities include:

- Organization;
- Business Unit;
- Process;
- Activity;
- Resource;
- Person;
- Objective;
- OKR;
- KPI;
- Target;
- Event;
- Risk;
- Constraint;
- Dependency;
- Plan;
- Plan Version;
- Scenario;
- Decision;
- Action;
- Evidence;
- Result;
- Learning;
- Rule;
- Knowledge;
- Responsibility.

Relationships should support reconstruction of:

**what happened → why → what was decided → who decided → based on what → what happened afterward → what was learned**

This is a conceptual model only until reconciled with existing canonical schemas.

---

# 30. Plan versioning

Every relevant plan should preserve:

- version;
- date/time;
- author/source;
- origin event;
- reason for change;
- impact assessment;
- approval;
- status.

Example:

**Master Plan V1**

→ event

→ impact analysis

→ change proposal

→ approval

→ **Master Plan V2**

Historical versions must not be silently overwritten.

ELO should be able to explain the evolution of planning.

---

# 31. Decision contract

A reusable conceptual decision contract should contain:

```text
CONTEXT
EVENT
PROBLEM
EVIDENCE
CAUSES
IMPACTS
CONSTRAINTS
ALTERNATIVES
DECISION
JUSTIFICATION
RESPONSIBLE PARTY
DEADLINE
INDICATOR
RESULT
LEARNING
```

This contract must be mapped to an existing canonical contract if one already exists. A new contract should only be created after the repository's duplicate/conflict analysis.

---

# 32. Exception-oriented alerts

Alerts should be based on relevance and exception, not merely threshold color.

A useful alert contains:

**event + context + probable cause + impact + recommendation**

Example:

> The programming-compliance target is deviating. The leading correlated factor is a material-supply delay. The projected impact is an extension of the affected order's Lead Time. Recommended action: evaluate alternative sequencing and material recovery options.

Never reduce a critical alert to:

> KPI red.

---

# 33. Tests and evidence

Every cognitive capability must eventually have evidence paths for:

- normal scenarios;
- exception scenarios;
- planning changes;
- conflicts;
- missing data;
- contradictory data;
- critical events;
- replanning;
- rollback;
- invalid decisions;
- authorization boundaries.

Acceptance tests should be based on realistic business scenarios.

No phase should be marked READY merely because files exist or code compiles. The repository rules require executable evidence where applicable. fileciteturn29file0L2-L2

---

# 34. Observability and auditability

The architecture should allow authorized reviewers to determine:

- what data entered;
- what context was used;
- which rule was applied;
- which evidence was consulted;
- which alternatives were evaluated;
- what recommendation was generated;
- what decision was taken;
- who approved it;
- what result occurred;
- what was learned.

This is necessary for operational trust and governed reasoning.

---

# 35. Expected architectural analysis output

When an agent is instructed to analyze or implement this architecture, it should produce an exhaustive analysis covering:

1. executive definition;
2. business problem solved;
3. principles;
4. relationship with Cognitive Core;
5. existing components to reuse;
6. genuinely new concepts;
7. concepts that should not become components;
8. Consulting Mode;
9. Organizational Health Intelligence;
10. Experience Memory;
11. scientific/technical knowledge;
12. consultant knowledge;
13. Responsibility Graph;
14. information gaps;
15. clarification questions;
16. scenario analysis;
17. capability gaps;
18. ethics;
19. governance;
20. privacy;
21. provenance;
22. tenant isolation;
23. reference cases;
24. complete Finance/RH scenario;
25. complete forklift/yard scenario;
26. conceptual contracts;
27. events;
28. states;
29. failure modes;
30. metrics;
31. confidence criteria;
32. human-in-the-loop;
33. architectural risks;
34. roadmap;
35. integration with ELO-001 through ELO-013;
36. future tests;
37. future Definition of Done.

---

# 36. Duplicate and authority analysis

Before proposing a new file, capability or contract, compare against existing repository artifacts.

Classify each concept as:

**REUSE**  
**EXTEND**  
**NEW**  
**ROADMAP**  
**DUPLICATE**  
**CONFLICT**

Do not select NEW until reuse, extension and consolidation have been considered.

Do not silently override a higher-authority artifact. The repository authority order is constitutional/enterprise manifest → approved architecture baseline → approved ADR → canonical contract/schema → governance/security policy → implementation → tests/runtime evidence → roadmap/proposal. fileciteturn36file0L2-L2

---

# 37. Proposed artifact families

Potential future artifacts may include, only if duplicate analysis justifies them:

- `ELO_ORGANIZATIONAL_HEALTH_INTELLIGENCE.md`
- `ELO_COGNITIVE_CONSULTING_MODE.md`
- `ELO_ORGANIZATIONAL_EXPERIENCE_MODEL.md`
- scenario-analysis contracts;
- decision contracts;
- replanning contracts;
- cognitive data models;
- ADRs for durable architectural decisions.

For every proposed artifact specify:

- need;
- authority;
- scope;
- related documents;
- duplication risk;
- recommended directory;
- status: normative/reference/roadmap/experimental.

Do not create documentation merely to increase document count.

---

# 38. Golden rule

Never create complexity merely because it appears sophisticated.

Every component or architectural capability must answer:

> **What problem does it solve?**

> **What decision does it improve?**

> **What risk does it reduce?**

> **What information does it use?**

> **What result does it produce?**

If these questions cannot be answered clearly, do not create the component yet.

---

# 39. Evolution rule

The architecture must permit new capabilities to be added without breaking the core.

Prioritize:

- decoupling;
- contracts;
- versioning;
- tests;
- observability;
- governance;
- extensibility;
- traceability;
- explainability.

Preserve compatibility with approved existing architecture.

Do not replace historical structures without an explicit architectural decision.

---

# 40. Target state

The intended evolution is from an ELO that primarily:

**consults information**

toward an ELO that can:

**understand context**

→ **detect changes**

→ **interpret impacts**

→ **evaluate risks**

→ **identify conflicts**

→ **simulate scenarios**

→ **propose alternatives**

→ **support decisions**

→ **replan**

→ **monitor execution**

→ **measure outcomes**

→ **learn**

→ **improve the next decision**

The target capability is transversal, not a single monolithic module.

> **ELO should be able to see the complete flow, recognize when the plan no longer represents reality, and reconstruct a coherent path between the current state and the desired state while preserving a clearly defined beginning, middle and end.**

---

# 41. Final agent instruction

Before changing code or documentation:

1. read the existing architecture;
2. identify approved decisions;
3. map existing artifacts;
4. identify gaps;
5. present the proposed architecture;
6. explain impacts;
7. propose ADRs where durable decisions are required;
8. define/reuse contracts;
9. define tests;
10. only then propose implementation.

**Do not implement prematurely.**

First construct the architecture.  
Then validate the architecture.  
Then decompose it into increments.  
Then implement.  
Then test.  
Then record evidence.

The goal is not merely to add features. The goal is to establish an **evolutionary, governable, explainable and adaptive enterprise cognitive architecture capable of supporting coherent replanning when real-world context changes.**

---

## Status note

This document is intentionally **PROPOSED / REFERENCE**. It must be reconciled with the repository's canonical architecture, contracts, ADRs, roadmap gates, governance and implementation evidence before any part of it is promoted to normative architecture or implemented as a production capability.
