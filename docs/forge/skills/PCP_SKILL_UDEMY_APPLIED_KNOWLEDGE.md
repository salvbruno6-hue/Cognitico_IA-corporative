# ELO FORGE — PCP Skill / Udemy Applied Knowledge Plug

## Status
PROPOSED — source/skill adapter for Forge validation.

## Purpose
Provide the PCP specialist in ELO Forge with an authorized external learning source from Udemy for applied domain knowledge, with emphasis on **finding the right information, structuring a production-planning problem, calculating what can be calculated, identifying gaps, and building a governed planning solution**.

The Udemy course is a **learning source**, not canonical ELO truth and not a direct Core mutation path.

## External learning source

**Course:** PCP: Planejamento e Controle da Produção Aplicado — Uma Abordagem Prática com Cases das Áreas  
**Instructor:** Prof. Arthur Feital Leite  
**Provider:** Udemy  
**Landing page:** https://www.udemy.com/course/pcp-planejamento-e-controle-da-producao-avancado/

The course curriculum provides applied material covering demand forecasting, production systems, aggregate planning, master production scheduling, sequencing, inventory, MRP, ERP, Lean, maintenance, simulation, OEE, takt time, WIP, logistics analytics, Excel and Power BI applications.

## Architectural placement

- ELO Cognitive: governs identity, invariants, source authority and promotion rules.
- Core: provides shared cognitive faculty and receives only validated/generalized learning.
- Forge PCP Specialist: owns applied PCP technique, contextual knowledge, experiences, parameters and skill use.
- Udemy: external learning source/provider.
- Application/Infrastructure: access and execution means.

## Critical boundary

Udemy content MUST NOT be copied into Core merely because it appears in the course. Course concepts are treated as **external source knowledge** and must enter the normal evidence/analysis/validation path.

The PCP specialist may use the course as a learning aid, reference and applied-method source. A course statement does not become a company fact, a validated ELO parameter, or a canonical rule without independent evidence and governance.

## Priority knowledge map for solution building

The specialist SHOULD prioritize the following course areas because they most directly support an end-to-end planning solution.

### P1 — Demand and planning structure

Use first when the objective is to understand **what must be produced and when**:

- demand forecasting;
- seasonality and demand projection;
- sales data applied to PCP;
- production-system characteristics;
- aggregate planning;
- Master Production Schedule (MPS/PMP).

Expected use:
`DEMAND → TIME HORIZON → AGGREGATION → PRODUCTION PLAN → MPS`

### P2 — Capacity, sequencing and execution feasibility

Use to determine **whether and how the plan can actually be executed**:

- production-system type;
- sequence of production;
- sequencing rules, including Johnson where applicable;
- forward scheduling;
- backward scheduling;
- cycle time;
- lead time;
- takt time;
- throughput/output rate;
- WIP;
- OEE;
- productivity, quality and availability;
- bottleneck analysis;
- maintenance effects on available capacity.

Expected use:
`MPS → CAPACITY → CONSTRAINTS → SEQUENCE → SCHEDULE → FEASIBILITY`

### P3 — Materials and inventory

Use to determine **what is required to execute the plan**:

- inventory decisions;
- ABC analysis;
- reorder point;
- periodic review;
- stock availability and coverage;
- MRP;
- product structure/BOM;
- material requirements;
- lead times;
- ERP-related information.

Expected use:
`PLAN → BOM → STOCK → OPEN ORDERS → LEAD TIMES → MRP → MATERIAL GAPS`

### P4 — Simulation and scenario analysis

Use when deterministic planning is insufficient or a decision has material operational risk:

- production simulation;
- Arena/FlexSim concepts;
- scenario comparison;
- bottleneck experimentation;
- sensitivity to capacity, demand, setup and availability.

Expected use:
`BASE PLAN → SCENARIO → SIMULATE → COMPARE → RISK/IMPACT → RECOMMEND`

### P5 — Monitoring and continuous improvement

Use after the plan is released:

- OEE;
- productivity;
- quality;
- availability;
- MTBF;
- MTTR;
- cycle time;
- lead time;
- WIP;
- takt time;
- output rate;
- logistics indicators;
- Power BI/Excel applied analysis;
- actual-versus-plan comparison.

Expected use:
`PLAN → EXECUTE → MONITOR → VARIANCE → ROOT CAUSE → CORRECT → LEARN`

### P6 — Lean and waste reduction

Use as an improvement layer rather than as a substitute for factual planning:

- Lean/Toyota principles;
- waste identification;
- setup reduction/SMED concepts;
- flow;
- excess inventory;
- quality and process improvement.

## Governed planning-search mechanism

The PCP specialist SHOULD use the following search sequence before proposing a production plan.

### STEP 1 — Define the planning question

Search for and classify:
- demand;
- products/SKUs;
- required dates;
- planning horizon;
- production system;
- customer commitments;
- service requirements.

### STEP 2 — Search authorized enterprise sources

Search only authorized sources and identify provenance for every relevant value:

- sales/orders;
- forecasts;
- contracts;
- BOM/product structures;
- stock;
- open purchase orders;
- open production orders;
- work centers/resources;
- routings;
- standard times;
- calendars/shifts;
- maintenance constraints;
- quality constraints;
- logistics constraints;
- ERP/MES/WMS/BI data where authorized.

Do not treat the course as a substitute for enterprise data.

### STEP 3 — Build the planning fact base

Separate explicitly:

`FACT | COMMITTED | AVAILABLE | ESTIMATE | ASSUMPTION | HYPOTHESIS | GAP | CONFLICT`

Do not calculate as if a GAP were zero.

### STEP 4 — Select the appropriate planning layer

Choose the minimum sufficient method:

`DEMAND → AGGREGATE PLAN → MPS/PMP → MRP → CAPACITY → SEQUENCING → SCHEDULE`

Not every case requires every layer. The specialist must explain why a layer is applicable or not applicable.

### STEP 5 — Calculate feasibility

Calculate only from validated inputs:

- available capacity;
- required capacity;
- material requirements;
- inventory coverage;
- lead times;
- production dates;
- bottlenecks;
- setup effects;
- maintenance effects;
- resource conflicts.

### STEP 6 — Identify gaps and request follow-up

If a required input is absent, create a GAP and request the responsible specialist/source instead of inventing the value.

Examples:
- missing M14 processing time;
- missing BOM;
- missing work-center calendar;
- missing stock position;
- missing supplier lead time;
- missing maintenance window.

### STEP 7 — Compare scenarios

When more than one feasible path exists, compare at least:

- capacity;
- inventory;
- delivery/service;
- cost where authorized data exists;
- risk;
- bottleneck exposure;
- resource requirements.

### STEP 8 — Produce the planning result

The specialist may produce:

- demand view;
- aggregate production plan;
- MPS/PMP;
- MRP/material plan;
- capacity plan;
- sequencing proposal;
- schedule;
- inventory requirements;
- bottleneck analysis;
- scenario comparison;
- gaps and follow-ups;
- recommendation with evidence and uncertainty.

### STEP 9 — Monitor and learn

After execution:

`PLANNED → REALIZED → VARIANCE → CAUSE → CORRECTION → EXPERIENCE → LEARNING CANDIDATE`

The original experience remains in Forge.

## PCP specialist usage rules

When the PCP specialist lacks a technical method:

1. identify the exact PCP question;
2. identify whether the question is conceptual, computational, procedural or contextual;
3. search the authorized external learning source for the applicable method;
4. record the source reference and specific concept used;
5. separate course knowledge from enterprise facts;
6. apply the method only after validating required inputs;
7. preserve assumptions, gaps and uncertainty;
8. test the method against available evidence and results;
9. record the applied experience in Forge;
10. create a learning candidate when a reusable pattern emerges;
11. promote to Core only after generalization, validation and Evolution Gate approval.

## Example: Multiteiner planning

The course can provide methods for demand, aggregate planning, MPS, capacity, sequencing, inventory, MRP, maintenance and performance analysis.

It cannot provide Multiteiner facts.

Therefore the specialist must retrieve and validate:

- actual seasonal demand composition;
- M01/M05/M14 quantities;
- return composition;
- quarantine/release status;
- processing time for each module;
- production/resource capacity;
- CLT availability and contractual allocation;
- stock and material constraints;
- dates and customer commitments.

Known facts are used directly. Missing information becomes GAP/follow-up. The specialist then applies the appropriate PCP method and compares feasible scenarios.

## Example boundary

Course concept:
- MRP can be used to calculate material requirements.

Enterprise fact:
- actual Multiteiner BOM, stock, lead times and demand.

Applied PCP result:
- calculated requirement for a specific production plan.

Generalized candidate:
- a validated reusable relationship that applies beyond one company/case.

Only the final generalized candidate is eligible for Core consideration.

## Skill outputs

The PCP specialist may produce:

- production plan;
- master production schedule;
- material requirement analysis;
- capacity analysis;
- bottleneck analysis;
- inventory analysis;
- sequencing proposal;
- KPI analysis;
- simulation proposal;
- scenario comparison;
- specialist follow-up requests;
- applied learning candidate.

All outputs remain subject to ELO evidence, provenance, uncertainty, authority and governance contracts.

## Skill maturity

Current state: `SOURCE_CONNECTED / APPLIED_PLANNING_METHOD_DEFINED / NOT_YET_EMPIRICALLY_VALIDATED_AS_ELO_SKILL`.

This record establishes a governed external knowledge plug and a planning-search methodology. It does not claim that the ELO has completed the course, memorized the course, or validated all methods empirically.

## Provenance

Source: Udemy course metadata and curriculum retrieved through the authorized Udemy integration on 2026-08-17.

The source remains external. Any future learning derived from its application must retain source provenance and the associated enterprise/context evidence.
