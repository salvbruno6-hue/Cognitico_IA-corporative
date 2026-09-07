# ELO — Audit Solidification Gate — 2026-09-07

## Objective

Consolidate the complete audit cycle into executable, evidence-based gates that harden the existing canonical ELO without creating a second authority.

## Canonical rule

`REUSE → STRENGTHEN → REFACTOR → DEPRECATE → CREATE`

This document is a validation and remediation contract. It does not create a new Core, Memory, Router, Provider Registry, Authorization Engine, Evolution Gate or other authority.

## Findings from live audit

### Authorization

- Identity, role, capability and scope bindings exist and their foreign-key relationships are valid.
- At least one active session is stale/expired and remains unreleased. This is a lifecycle hygiene finding, not evidence of new authorization.
- Authorization audit has no recorded rows yet; absence of audit events is a remaining observability gap.

### Learning evidence

- `elo_orcamento_calculos_aprendidos`: 102 rows.
- 95 calculations currently have no linked row in `elo_orcamento_calculo_evidencias`.
- `elo_orcamento_memoria`: 18 `VALIDATED_LEARNING`, 0 `LEARNING_CANDIDATE`.
- Therefore the 102 calculations must not be interpreted as 102 validated learning events.

### Knowledge graph boundary

- `elo_conhecimento_itens`: 8 items.
- `elo_conhecimento_vinculos`: 0 links.
- The current state is valid only if these items are intentionally independent knowledge items; otherwise linkage evidence remains a gap. No automatic links are created by this audit.

### Core internal learning tables

`elo_core.execucoes`, `avaliacoes`, `correcoes`, `baselines` and `regras` are RLS-enabled and have no client policies. This is deliberate fail-closed behavior for the current internal-only boundary.

### Security and performance

Security advisor residual: leaked-password protection is disabled. This is an Auth configuration issue that requires an external project setting change; it is not altered by this audit because the connector exposes no direct Auth configuration mutation here.

Performance advisor currently reports only unused-index INFO findings. Unused-index cleanup is deferred until observed workload evidence exists; removal based only on an unused statistic could reduce future readiness.

## Required hardening rules

### 1. Session lifecycle

Expired active sessions must be treated as invalid for authorization decisions. Session reuse must require `revoked_at is null` and `expires_at is null or expires_at > now()`.

### 2. Evidence integrity

A calculation may remain staged without evidence, but it cannot be promoted, represented as validated learning, or used as proof of generalization without reconstructible evidence.

### 3. Learning separation

`CALCULATION → EVIDENCE → RESULT → EXPERIENCE → EVALUATION → LEARNING CANDIDATE → GOVERNED LEARNING → EVOLUTION GATE` remains mandatory.

### 4. Material evolution

Material evolution requires comparative evidence, including baseline, observed measurement, minimum delta, confidence, at least two comparable runs, no regression, evidence references and reconstructible comparison references.

### 5. Runtime integrity

`ExecutionRouter` remains the only selector of model/tool routes. `IntelligenceRouter` remains subordinate and cannot choose a route independently.

### 6. Candidate-only laboratory

Laboratory observations remain `LAB_ONLY` until the existing governed learning and evolution authorities accept them. No automatic promotion is permitted.

### 7. Audit evidence

The audit itself must distinguish structural existence from behavioral proof. Zero audit rows are not interpreted as zero events; they are interpreted as missing operational audit evidence.

## Remediation posture

This cycle fixes only objective deficiencies that can be corrected without changing the canonical architecture. It does not mutate Soul or establish parallel ownership. Every change must be followed by targeted tests and a final audit.

## Final closure criteria

The audit can be sealed only when:

- authorization bindings are valid;
- no expired session is considered active;
- learning evidence gaps are classified and no unsupported calculation is promoted;
- live and laboratory evidence are explicitly separated;
- structural and behavioral tests pass on current `main`;
- security residuals are documented as accepted external configuration gaps or corrected;
- no new orphan, duplicate authority or regression is introduced;
- post-change audit reproduces the same or stronger invariants.
