# ELO Capability Implementation Audit — 2026-08-17

## 1. Audit purpose

This audit distinguishes repository presence from executable capability. A document, Issue, PR, workflow or directory is not treated as implementation evidence by itself.

Evidence classes used in this audit:

- **IMPLEMENTADO** — executable code exists on current `main` and has an applicable test surface.
- **CONTRATO** — a formal executable-facing or architectural contract exists, but capability behavior is not fully implemented.
- **ESPECIFICAÇÃO** — behavior is described in documentation/issues/prompts without sufficient executable realization.
- **EXPERIMENTAL** — executable prototype exists but is intentionally bounded/non-canonical or not mature enough for general capability claims.
- **DUPLICADO** — more than one artifact attempts to own substantially the same capability.
- **INCONSISTENTE** — artifacts exist but their contracts/roles disagree or create ambiguity.
- **AUSENTE** — no meaningful executable implementation was found on current `main`.
- **HISTÓRICO** — retained for lineage/reference and not authoritative for current runtime.

## 2. Current repository truth

Current `main` contains a single executable tree under `src/elo`. The Core contains context resolution, source discovery, temporal/evolution memory, evidence-aware diagnostics, systemic model, production flow, decision/outcome primitives, learning governance and application orchestration.

The repository also contains architectural/documentary trees in Portuguese and English with overlapping names, including `01-meta-architecture` / `01-meta-arquitetura` and `07-data-engineering` / `07-engenharia-de dados`. This is structural duplication/debt, not evidence of two executable Cores. The historical PR reconciliation rule remains that `src/elo` is the executable authority.

## 3. Capability inventory

| Capability | Current evidence | State | Canonical layer | Main gap / finding |
|---|---|---|---|---|
| IDENTITY | `src/elo/core/canonical_identity.py` | IMPLEMENTADO | Cognitivo | Runtime identity exists; canonical invariants remain governance-owned. |
| COGNITIVE CORE | `src/elo/core/*` plus canonical identity/contracts | IMPLEMENTADO | Cognitivo + Core | Core is a capability collection, not a second Core. |
| CORE | Core primitives and services | IMPLEMENTADO | Core | No separate second Core found. |
| MEMÓRIA | `src/elo/memory/persistent.py`, temporal/evolution memory | IMPLEMENTADO | Core | Persistent adapter is replaceable; temporal and permanent boundaries exist. |
| KNOWLEDGE | admission/evidence/knowledge lifecycle | IMPLEMENTADO | Core | Promotion remains governed; no evidence that every documented knowledge path is fully integrated. |
| EXPERIENCE | learning/outcome records and MT-001 experience | IMPLEMENTADO | Forge/Core boundary | Contextual experience exists; promotion remains governed. |
| FORGE | architecture/contracts/docs and contextual experience artifacts | CONTRATO | Forge | Constructor/experience plane is strongly specified; not a separate runtime authority. |
| ESPECIALISTAS | AgentContract/AgentTask/AgentObservation + member tests | IMPLEMENTADO | Forge | Specialist output remains governed observation/evidence. |
| CONTEXT ENGINE | `context_resolution.py` + tests | IMPLEMENTADO | Core | Executable context boundary exists. |
| SYSTEMIC MODEL | `systemic_model.py` | IMPLEMENTADO | Core | Primitive model exists; enterprise-wide data ingestion remains adapter-dependent. |
| DEPENDENCY / IMPACT ENGINE | scenario/diagnostic and systemic relations | EXPERIMENTAL | Core | No single canonical dependency/impact service; overlapping scenario mechanisms exist. |
| SCENARIO ENGINE | `scenario_engine.py` | IMPLEMENTADO | Core | Small scenario primitive exists. |
| DIAGNOSTIC SCENARIO ENGINE | `diagnostic_scenario_engine.py`, `diagnostic_scenarios.py` | DUPLICADO / INCONSISTENTE | Core | Two scenario/diagnostic families overlap and should be consolidated before expansion. |
| DECISION ENGINE | DecisionRecord + decision memory + governed orchestration | CONTRATO | Core | Decision records exist; no independent autonomous financial decision authority exists, correctly. |
| ORCHESTRATION | `application/use_cases/orchestrator.py` | IMPLEMENTADO | Application | Deterministic execution boundary exists but is minimal and does not perform end-to-end budgeting. |
| EXECUTION | governed execution handoff/state contracts | CONTRATO | Cognitivo/Application | Execution authority is gated; operational executor remains outside canonical cognitive layer. |
| MONITORING | ProductionFlow + outcome feedback | EXPERIMENTAL | Application/Core | Flow/outcome primitives exist; generic continuous monitoring service is not complete. |
| FOLLOW-UP | MT-001 follow-up issue + execution contracts | CONTRATO | Forge/Application | Follow-up is formally represented and manually tracked; generic autonomous follow-up service is incomplete. |
| LEARNING | `learning_governance.py` | IMPLEMENTADO | Core/Forge boundary | Candidate/evaluation/human approval lifecycle exists; promotion is governed. |
| GOVERNANCE | Evolution Gate workflows/issues/contracts | IMPLEMENTADO | Cognitivo | Gate exists and explicitly separates technical failure from architectural decision. |
| VALIDATION | pytest + behavioral/PR1/evolution workflows | IMPLEMENTADO | Application/Infrastructure governance | Current main has validation workflows; current latest main commit has no connector-visible workflow run/status evidence. |
| EVOLUTION GATE | `.github/workflows/elo-evolution-gate.yml` | IMPLEMENTADO | Governance | Technical validation is executable; canonical decision handoff is recorded by workflow. |
| PROVENANCE | Evidence and memory records carry provenance/source references | IMPLEMENTADO | Core | No standalone `src/elo/provenance` authority found; provenance is embedded in existing contracts. |
| PARAMETERS | Learning candidates/evaluation and ELO-021 promotion rules | CONTRATO | Core/Forge | General parameter promotion is governed, but a dedicated versioned parameter registry was not found. |
| FACULTY | Domain faculty tests/contracts | IMPLEMENTADO | Forge/Core boundary | Faculty/overlay concepts are executable/tested; broader domain population remains bounded. |
| OVERLAY | Domain overlay tests/contracts | IMPLEMENTADO | Forge | Removable contextual overlay is represented/tested. |
| APPLICATION | `src/elo/application/*` | IMPLEMENTADO | Application | Replaceable application boundary exists. |
| INFRASTRUCTURE | GitHub Actions, adapters, SQLite reference memory | IMPLEMENTADO | Infrastructure | Infrastructure is replaceable and not treated as cognitive authority. |
| INTEGRATIONS | source discovery + adapters + GitHub workflows | CONTRATO / EXPERIMENTAL | Application/Infrastructure | Semantic discovery exists; real retrieval depends on authorized adapters/connectors. |
| BUDGETING | ELO-024 contract plus this branch implementation | CONTRATO → IMPLEMENTAÇÃO EM VALIDAÇÃO | Core | Contract was merged by PR #152; executable budgeting was absent on `main` and is now being added in this controlled branch. |
| COST | ELO-024 formula contract + `budgeting.py` baseline formula | IMPLEMENTADO (BASELINE) | Core | Only governed quantity × unit-cost calculation is implemented; broader cost catalog is absent. |
| PRICING | budgeting prompt/specification | ESPECIFICAÇÃO | Forge/Application | No canonical executable price authority found. |
| MARGIN | `budgeting.py` gross margin calculation | IMPLEMENTADO (BASELINE) | Core | Calculated only when complete revenue and cost inputs exist. |
| FORECAST | scenario/production primitives | EXPERIMENTAL | Core | No dedicated forecast service found. |
| DEMAND | ProductionFlow + MT-001 data + systemic model | EXPERIMENTAL | Core/Forge | Demand is represented as flow/evidence, not as a dedicated demand engine. |
| CAPACITY | ProductionFlow + diagnostic capacity lens + CapacityConstraint in ELO-024 | IMPLEMENTADO (BOUNDED) | Core | Capacity constraint calculation exists; enterprise capacity ingestion is not complete. |
| RESOURCE PLANNING | ProductionFlow + capacity primitives | EXPERIMENTAL | Core/Application | No complete resource-planning service found. |
| RISK | diagnostic risk lens + uncertainty | IMPLEMENTADO (BOUNDED) | Core | Risk analysis exists as diagnostic primitive, not as a complete risk register engine. |
| QUOTATION | budgeting prompt and specialist guide | ESPECIFICAÇÃO | Forge/Application | No executable quotation workflow/contract found. |
| POST-BUDGET LEARNING | OutcomeFeedback + LearningGovernanceService | IMPLEMENTADO (BOUNDARY) | Core/Forge | Outcome feedback and learning candidate lifecycle exist; automatic generalized promotion remains gated. |

## 4. Budgeting-specific reuse decision

The repository already contains the required surrounding primitives:

- Context Resolution;
- Source Discovery;
- Evidence;
- Memory/Temporal Memory;
- SystemicModel;
- Scenario/DiagnosticScenario;
- DecisionRecord;
- UncertaintyAssessment;
- OutcomeFeedback;
- LearningGovernanceService;
- Application Orchestrator;
- Evolution Gate.

No second memory, financial Core, financial authority or autonomous executor was created.

The demonstrated gap was the executable budget object/calculation boundary itself. The implementation therefore adds one bounded Core capability: `src/elo/core/budgeting.py`.

## 5. ELO-024 implementation status

### Before this branch

- ELO-024 contract: **CONTRATO / MERGED**.
- ELO-024 acceptance matrix: **SPECIFICATION / DOCUMENTED**.
- ELO-024 executable budget model on `main`: **AUSENTE**.
- ELO-024 executable tests on `main`: **AUSENTE** as a budget service suite.
- Budget prompt/guide: **SPECIFICATION**.

PR #152 merged the contract and acceptance matrix, but its own Evolution Gate reported technical failure before merge; the merge commit was recorded as a manual architectural promotion. The latest `main` commit subsequently added contextual learning artifacts, while no connector-visible workflow run/status exists for that latest commit.

### This branch

Adds:

- `BudgetRequest`;
- immutable `BudgetVersion`;
- `BudgetInput` with explicit classification and provenance;
- `BudgetLine` and `CostComponent`;
- `Assumption`;
- `CapacityConstraint`;
- `BudgetScenario`;
- `BudgetSensitivity`;
- `BudgetDecision`;
- `BudgetOutcome`;
- governed follow-up generation;
- reproducible baseline formula version;
- authorization boundary;
- OutcomeFeedback integration;
- 20 acceptance tests covering ELO-024 and MT-001.

This does **not** yet claim full enterprise autonomous budgeting. Source adapters, price authority, demand/forecast ingestion, resource planning, quotation, continuous monitoring and broad cross-domain operational retrieval remain incomplete.

## 6. Duplicate/inconsistency findings

### A. Scenario ownership duplication

`src/elo/core/scenario_engine.py` and `src/elo/core/diagnostic_scenario_engine.py` both define scenario concepts. `diagnostic_scenarios.py` adds another diagnostic scenario model. This is the most important current executable duplication relevant to budgeting because ELO-024 needs scenario/sensitivity behavior.

Decision: **do not create another scenario engine**. ELO-024 references the existing bounded scenario contracts and its own budget scenario data structure only for budget-specific versioning.

### B. Portuguese/English documentation trees

The repository contains parallel language-named architectural/data directories. They are documentary/organizational duplication and should be consolidated through canonical-owner mapping rather than deleting historical content.

### C. Historical issue/PR duplication

The issue registry contains known duplicate markers for ELO-017 and conversation-learning work. These are historical governance debt, not new capabilities. The canonical owners are already recorded in the issue bodies.

### D. ELO-023 divergence

PR #136 diverged from current `main`; PR #151 was the clean reconciliation and is merged. The current MT-001 artifacts are therefore the canonical current-main test surface.

### E. ELO-024 PR divergence

PR #140 was based on an older `main`; PR #152 was the current-main reconciliation and is merged. The contract is therefore canonical, but its implementation claim must not be inferred from the contract alone.

## 7. Current critical gaps before autonomous budgeting maturity

1. Execute and prove the new budget test suite in GitHub Actions.
2. Integrate actual authorized source retrieval into the budgeting request path.
3. Consolidate scenario ownership before broad scenario expansion.
4. Add explicit domain-authority checks for cross-domain facts where required by the source contracts.
5. Add stale-input/temporal-validity enforcement to budgeting calculations.
6. Add a versioned parameter registry only if the existing learning/evolution structures cannot satisfy the demonstrated need.
7. Build quotation/price authority only after a real canonical source is identified.
8. Build forecast/resource-planning capabilities only after inventory confirms no existing canonical owner.
9. Execute MT-001 from the executable service, not only from Markdown assertions.
10. Perform post-merge verification and record actual test evidence.

## 8. Evidence rule

The audit does not count:

- file existence alone;
- Issue text alone;
- PR description alone;
- workflow definition alone;
- a green claim without a visible run/check;
- documentation assertions without executable coverage.

The next maturity transition requires reproducible test evidence tied to a commit/run.
