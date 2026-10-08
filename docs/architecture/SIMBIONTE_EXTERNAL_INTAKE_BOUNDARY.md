# ELO — Simbionte External Intake Boundary

**Status:** FORGE / EVOLUTION LAB / CANDIDATE-ONLY  
**Classification:** CONTRACT  
**Owner:** ELO Cognitivo  
**Promotion gate:** Evolution_Gate

## 1. Purpose

Define the observation boundary through which the Simbionte receives newly encountered elements from already authorized external sources such as MCP connections, files, code, APIs, Figma and other integrations.

This contract does not create a new architectural component, authority, memory, router, authorization engine or Evolution Gate.

The source remains operationally independent within its authorized role. The Simbionte observes the mechanism, understands its behavior, identifies potentially useful capabilities and prepares evidence for governed assimilation.

## 2. Core rule

**AUTHORIZED SOURCE → OBSERVE → UNDERSTAND → RELATE → ASSESS UTILITY → CANDIDATE → GOVERN**

Authorization of a source means that the source may operate within its existing contract. It does not mean that everything it exposes becomes ELO knowledge or implementation.

## 3. Source neutrality

The intake may receive elements from:

- MCP connections;
- files and documents;
- source code and repositories;
- APIs;
- Figma and design artifacts;
- skills and plugins;
- execution results;
- other authorized integrations.

The source's own authority is preserved. The Simbionte does not block ordinary operation merely because it is observing the source.

Example:

`Figma → performs authorized design/UX work`

while simultaneously:

`Simbionte → observes available mechanisms, behavior, states and useful patterns`

Figma does not acquire authority over ELO Web, GitHub, database, authorization or governance.

## 4. Observation stages

### 4.1 DETECT

Identify that a new or changed element has entered an authorized source.

### 4.2 CAPTURE

Preserve the source reference, version/commit when available, context, scope and provenance.

### 4.3 UNDERSTAND

Determine:

- what the element does;
- how it works;
- what inputs and outputs it uses;
- which existing ELO capability it relates to;
- what constraints it has;
- whether it is merely a source artifact or an actual mechanism.

### 4.4 RELATE

Compare against canonical ELO contracts, capabilities, skills, tests and existing owners.

Classify the relationship as:

`REUSE | STRENGTHEN | EXTEND | REFACTOR | CONSOLIDATE | DEPRECATE | NEW | CONFLICT`

`NEW` requires evidence that no suitable owner exists.

### 4.5 ASSESS UTILITY

Determine whether the observed mechanism provides a testable potential benefit.

The Simbionte records:

- expected utility;
- affected capability;
- baseline;
- hypothesis;
- evidence;
- risks;
- compatibility;
- tenant/scope implications;
- required validation.

### 4.6 FORM CANDIDATE

Only after observation and comparison may the Simbionte create a learning/capability candidate.

A candidate is not canonical.

## 5. External element record

A candidate intake should preserve, where applicable:

- `source_type`
- `source_ref`
- `source_version`
- `source_scope`
- `observed_at`
- `element_id`
- `element_type`
- `mechanism_summary`
- `existing_owner`
- `relationship_class`
- `utility_hypothesis`
- `baseline`
- `evidence_refs`
- `risk`
- `compatibility_status`
- `generalization_status`
- `promotion_state`

## 6. No automatic assimilation

The following are prohibited:

- direct Core writes from an external source;
- treating a new MCP/tool/API as canonical merely because it is connected;
- copying external code into Core as knowledge;
- converting a Figma component into a frontend implementation automatically;
- promoting a skill because it appears useful;
- treating one successful execution as generalized learning;
- bypassing evidence, testing or Evolution_Gate.

The canonical sequence remains:

`OBSERVE → EVIDENCE → RELATE → EXPERIMENT → MEASURE → GENERALIZE → GOVERN → EVOLUTION_GATE → POSSIBLE ASSIMILATION`

## 7. Relationship with existing Simbionte contract

This boundary extends the existing Simbionte principles:

`OBSERVE → INTERPRET → DECOMPOSE → EXTRACT_MECHANISM → IDENTIFY_EXISTING_OWNER → CHECK_COMPATIBILITY → ADAPT → GOVERN → TEST → MEASURE → DIAGNOSE → REFINE → RETEST`

The external-intake boundary adds the earlier source-neutral reception stage without changing the canonical ownership rules.

## 8. Figma-specific clarification

Figma remains an authorized design/UX surface.

Its role is:

`DESIGN → COMPONENTS → STATES → PROTOTYPE → HANDOFF`

The Simbionte may observe the resulting design mechanisms and identify useful interface patterns.

The Simbionte does not give Figma authority over:

- ELO Web implementation;
- GitHub/Main;
- authentication or authorization;
- RLS;
- database;
- business rules;
- Core;
- governance;
- merge;
- deployment.

The frontend receives a design handoff and remains responsible for governed implementation and verification.

## 9. Authority boundary

`SOURCE OPERATES → SIMBIONTE OBSERVES/RELATES → ELO GOVERNS → CORE CANONIZES ONLY AFTER VALIDATION`

No source, connector, provider or Simbionte observation may silently redefine a higher authority.

## 10. Acceptance criteria

This candidate is considered validated only when evidence demonstrates that:

1. authorized sources continue operating normally;
2. new/changed elements can be detected without creating a parallel authority;
3. provenance survives the observation process;
4. existing ELO owners are checked before creation;
5. useful mechanisms can become candidates without automatic promotion;
6. Figma remains design/UX only;
7. authorization and tenant boundaries remain unchanged;
8. the existing Simbionte and Governed Learning contracts remain compatible.

**Final invariant:**

> The Simbionte does not control the source. It understands the source, identifies what may be useful to ELO, and returns governed candidates for validation.
