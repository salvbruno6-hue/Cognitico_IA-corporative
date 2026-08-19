# ELO Constraints — Governance Checklist

**Status**: NORMATIVE  
**Authority**: ELO Operating Rules + Maturity Framework + Repository Navigation Rules  
**Effective**: 2026-08-19  
**Purpose**: Enforce non-negotiable architectural, governance, and security boundaries

---

## Executive Summary

These constraints are **executable gates** that must be satisfied before any work is merged or any capacity is promoted.

They are derived from:
- `ELO_OPERATING_RULES.md` — soul protection and evolution gates
- `ELO_BASELINE_MATURITY_AND_TRACEABILITY_FRAMEWORK.md` — evidence and promotion rules
- `ELO_REPOSITORY_NAVIGATION_RULES.md` — placement authority
- `ELO_AI_AGENT_WORKING_RULES.md` — operational continuity

**Not meeting these constraints is a blocker for merge.**

---

## 1. Soul and Identity Constraints

### 1.1 Identity Protection
- [ ] No modification to `ELO Soul` without explicit governance approval
- [ ] No provider output silently redefines canonical identity
- [ ] No specialist agent bypasses authority hierarchy
- [ ] Evidence order when resolving "who is ELO": Soul → Implementation → Contracts → Evidence → Roadmap
- [ ] Conflicts recorded with full provenance before resolution

### 1.2 Cognitive Core Boundary
- [ ] Only ONE Cognitive Core exists (no parallel authority)
- [ ] No provider creates a second core
- [ ] No connector reinvents core semantics
- [ ] No specialist agent redefines Core decision logic directly
- [ ] Specialized boundaries used for: context, knowledge, memory, evidence, reasoning, scenarios, decisions, agents, governance

### 1.3 Four-Layer Separation
- [ ] Cognitive layer (identity, soul, contracts) remains protected
- [ ] Core layer (shared faculty, decision logic) preserves lower-layer authority
- [ ] Forge layer (specialists, skill packs) cannot redefine Core
- [ ] Application/Infrastructure layer remains replaceable
- [ ] No layer silently violates its boundary

---

## 2. Evolution Gate Constraints

### 2.1 Candidate Change Classification
Every change must be classified before merge:
- [ ] COMPATIBLE — aligned with Soul, safe to absorb automatically
- [ ] ADAPT_REQUIRED — compatible after minor adjustment
- [ ] EVOLUTIONARY_CONFLICT — valuable but conflicts with current structure
- [ ] INCOMPATIBLE — contradicts Soul or security boundary
- [ ] DUPLICATE/SUPERSEDED — already exists or redundant

### 2.2 Conflict Management
- [ ] Conflicts explicitly classified (not silently chosen)
- [ ] Evolutionary conflicts preserved as non-canonical alternatives
- [ ] Incompatible work rejected with documented rationale
- [ ] Human decision recorded for Soul changes
- [ ] Escalation path followed when reconciliation impossible

### 2.3 Reuse-Before-Create Rule
- [ ] Searched repository for concept (exact term + synonyms)
- [ ] Canonical owner identified
- [ ] Classified as: REUSE | EXTEND | REFERENCE | CONSOLIDATE | NEW
- [ ] NEW requires gap justification and traceability
- [ ] No creation of duplicate parallel structures

---

## 3. Authorization and Provenance Constraints

### 3.1 Source Authority
- [ ] Every external information source tracked with origin
- [ ] Authorization boundary preserved (no unauthorized access)
- [ ] Tenant/domain/principal identity maintained
- [ ] Provenance chain complete
- [ ] Source reliability documented

### 3.2 Knowledge Admission
External information must pass admission gates:
- [ ] Authorization verified
- [ ] Relevance confirmed
- [ ] Provenance recorded
- [ ] Source reliability assessed
- [ ] Confidence level stated: HIGH | MEDIUM | LOW | UNKNOWN
- [ ] Contradiction with existing knowledge noted
- [ ] Freshness and policy compliance checked

### 3.3 Admission Outcomes
Information classified as:
- [ ] REJECT — does not meet criteria
- [ ] ARCHIVE — preserve for audit, not operational
- [ ] OBSERVATION — temporal memory only
- [ ] EVIDENCE — ties to decision
- [ ] KNOWLEDGE_CANDIDATE — candidate for Core after validation
- [ ] KNOWLEDGE — approved for Organizational Memory
- [ ] DECISION — governance or approved action
- [ ] POLICY — enterprise rule
- [ ] LESSON_LEARNED — durable experience
- [ ] ARCHITECTURAL_PROPOSAL — queued for governance

### 3.4 No Automatic Promotion
- [ ] Conversation not automatically retained
- [ ] Discussion not automatically canonical
- [ ] Proposal not automatically implemented
- [ ] Evidence must exist before claiming maturity
- [ ] Full provenance chain maintained through promotion path

---

## 4. Testing and Evidence Constraints

### 4.1 Stop Words — Unsupported Claims
Claims like these require **reproducible evidence**:
- [ ] "Complete" → all acceptance criteria pass tests
- [ ] "Production-ready" → security review + perf benchmarks + monitoring
- [ ] "Secure" → threat model + auth/z + audit trail
- [ ] "Compliant" → policy review + control verification
- [ ] "Autonomous" → end-to-end without intervention
- [ ] "Validated" → tests pass + manual/automated verification
- [ ] "Scalable" → load testing + resource constraints documented
- [ ] "Enterprise-ready" → UAT passed + runbooks complete

### 4.2 Minimum Test Categories
When applicable:
- [ ] Happy path (normal operation)
- [ ] Invalid input and error handling
- [ ] Authorization failure and tenant isolation
- [ ] Dependency failure and timeout
- [ ] Malformed external response
- [ ] Provenance and request correlation
- [ ] Security and privacy behavior
- [ ] Admission classification accuracy
- [ ] Consulting response contract compliance
- [ ] Uncertainty and insufficient-evidence behavior

### 4.3 Test Standards
- [ ] Tests are executable (not documentation-only)
- [ ] Tests are reproducible
- [ ] Test results tied to commit/run
- [ ] Zero-test collection is not a passing gate
- [ ] Test failures must be resolved before merge
- [ ] Coverage includes adversarial cases

---

## 5. Maturity and Promotion Constraints

### 5.1 Maturity Levels
No capability promoted without evidence:
- [ ] Level 0 (ABSENT) — no definition
- [ ] Level 1 (CONCEPTUAL) — description exists
- [ ] Level 2 (DOCUMENTED) — coherent document exists
- [ ] Level 3 (CONTRACTED) — contract/spec exists
- [ ] Level 4 (IMPLEMENTED) — code corresponds to contract
- [ ] Level 5 (TESTED) — tests pass
- [ ] Level 6 (VERIFIED) — acceptance criteria verified
- [ ] Level 7 (OPERATIONALLY EVIDENCED) — real authorized execution

### 5.2 Promotion Gates
Before advancing level:
- [ ] G0 — Existence: definition, owner, canonical location confirmed
- [ ] G1 — Documentation: purpose, scope, dependencies clear
- [ ] G2 — Architecture: boundary defined, no duplication
- [ ] G3 — Contract: inputs, outputs, errors defined
- [ ] G4 — Implementation: code respects contract
- [ ] G5 — Tests: happy path + error + boundary cases
- [ ] G6 — Verification: criteria verified, architecture reviewed
- [ ] G7 — Operation: real execution, observability, detectability

### 5.3 Promotion Blockers
Work **cannot advance** when:
- [ ] Security blocker exists
- [ ] Tenant isolation violated
- [ ] Data integrity risk
- [ ] Incompatible contracts
- [ ] Loss of provenance
- [ ] Authority violation
- [ ] No human responsibility for high-impact decision
- [ ] Tests missing when gate requires them
- [ ] Destructive action without reversibility
- [ ] Data exposure risk
- [ ] Contradiction with approved ADR

---

## 6. Repository Structure Constraints

### 6.1 Placement Authority
Artifacts placed per decision tree (see `ELO_REPOSITORY_NAVIGATION_RULES.md`):
- [ ] Constitutional concepts → `00-enterprise-manifest/`
- [ ] Meta-architecture → `01-meta-architecture/`
- [ ] Architecture → `02-architecture-library/`
- [ ] Processes → `03-process-library/`
- [ ] Knowledge → `04-knowledge-handbook/`
- [ ] Cognitive capability → `05-cognitive-platform/`
- [ ] Knowledge engineering → `06-knowledge-engineering/`
- [ ] Data engineering → `07-data-engineering/`
- [ ] AI/provider governance → `08-ai/`
- [ ] Governance/security → `09-governance/`
- [ ] Architecture decisions → `10-adr/`
- [ ] Models → `11-models-library/` or `11-modelos/`
- [ ] System engineering → `12-system-engineering/` or `12-sistemas/`
- [ ] References → `13-reference-architecture/`
- [ ] Roadmap → `14-roadmap/`
- [ ] Assets → `15-assets/`
- [ ] Implementation → `src/elo/`

### 6.2 No Duplication
- [ ] Searched for concept (exact + synonyms + abbreviations)
- [ ] Checked equivalent contracts
- [ ] Checked equivalent ADRs
- [ ] Checked implementations and tests
- [ ] Checked roadmap items
- [ ] Classified as REUSE/EXTEND/RELOCATE/CONSOLIDATE/NEW
- [ ] No duplicate parallel structures created

### 6.3 Portuguese/English Variants
- [ ] No creation of new duplicate directories
- [ ] No symmetrical copying between variants
- [ ] New canonical artifacts use English operational path (unless existing Portuguese path owns it)
- [ ] Portuguese content preserved until explicit consolidation ADR
- [ ] Conflicts recorded as structural debt, not silently deleted

---

## 7. Governance and Decision Constraints

### 7.1 Architecture Decision Records (ADRs)
Breaking changes require:
- [ ] ADR filed
- [ ] Migration plan documented
- [ ] Explicit governance approval
- [ ] Deprecation period planned (if backward compatibility needed)
- [ ] Test coverage for old and new behavior during transition
- [ ] Baseline contracts not changed without ADR

### 7.2 Issue Classification
Every GitHub issue classified:
- [ ] ARCHITECTURE — affects identity, Core, contracts
- [ ] GOVERNANCE — affects evolution gate, admission, promotion
- [ ] TESTING — acceptance criteria, validation
- [ ] ENHANCEMENT — feature/capability
- [ ] BUG — behavioral deviation
- Governance and Architecture issues require evolution gate review before merge

### 7.3 Conflict Resolution
Before stopping due to conflict:
- [ ] Conflicting artifacts inspected
- [ ] Higher-authority rule identified
- [ ] Existing contracts/ADRs/tests searched for resolution
- [ ] Smallest adjustment made preserving purpose and boundaries
- [ ] Adjustment validated against Soul
- [ ] Stop only if reconciliation would require: unsupported authority | unsafe behavior | breaking contracts without migration | Soul modification without governance

---

## 8. Consulting Response Constraints

### 8.1 Consulting Mode Behavior
- [ ] Objective clearly stated
- [ ] Context established (tenant, domain, scope, constraints)
- [ ] Facts/Evidence distinguished from assumptions
- [ ] Analysis includes reasoning and trade-offs
- [ ] Alternatives presented
- [ ] Risks and constraints explicit
- [ ] Recommendation with rationale
- [ ] Decision boundary identified (what requires human decision)
- [ ] Next actions exact
- [ ] Provenance recorded where external information affects recommendation
- [ ] Uncertainty clearly stated

### 8.2 Execution Authority Boundaries
ELO may autonomously:
- [ ] PREPARE — gather context, validate scope, collect evidence
- [ ] CALCULATE — run scenarios, analysis, comparisons
- [ ] SIMULATE — test alternatives, identify gaps, flag risks
- [ ] IDENTIFY GAPS — request specialist data
- [ ] REVISE — recalculate with new evidence
- [ ] RECOMMEND — propose with rationale and risk

ELO **may NOT**:
- [ ] INVENT INPUTS — fabricate data or assume missing information
- [ ] APPROVE COMMITMENTS — authorize financial/contractual binding
- [ ] EXECUTE IRREVERSIBLE ACTIONS — change state, contractually bind, trigger consequences
- [ ] CHANGE AUTHORIZATION BOUNDARIES — promote specialist decisions to policy without governance

---

## 9. AI Agent and Specialist Constraints

### 9.1 Agent State Reporting
Before changing anything, report:
- [ ] Repository and branch
- [ ] HEAD SHA
- [ ] Working tree state
- [ ] Target task/issue
- [ ] Current ELO phase
- [ ] Dependency phase
- [ ] Relevant existing files
- [ ] Available tests
- [ ] Blockers

### 9.2 Agent Planning
Before substantial change:
- [ ] Execution plan written (objective, files, contracts, tests, risks, non-goals)
- [ ] Conflicts revealed by plan addressed
- [ ] Reconciliation attempted (inspect, identify authority, search for resolution, adjust, validate)
- [ ] Stop only if reconciliation impossible or unsafe

### 9.3 Specialist Feedback Integration
- [ ] Domain expertise recorded with provenance
- [ ] Evidence + source tracked
- [ ] Admission gate applied
- [ ] Organizational Memory / Evolution Memory updated
- [ ] Promotion to Core requires governance approval
- [ ] Direct Core logic changes **not permitted**
- [ ] Parallel memory structures **prohibited**
- [ ] Authorization and provenance **preserved**

### 9.4 No Silent Redefining
- [ ] Lower-level code does not silently redefine architecture
- [ ] Implementation does not override contracts
- [ ] Test does not override policy
- [ ] Proposal does not override approval
- [ ] AI provider output does not redefine Soul

---

## 10. Handoff and Continuity Constraints

### 10.1 Task Completion Handoff
At end of every task, document:
- [ ] Current phase
- [ ] Completed criteria with evidence
- [ ] Failed criteria with reasons
- [ ] Current branch and SHA
- [ ] Files changed
- [ ] Tests run (pass/fail/skipped)
- [ ] Unresolved questions
- [ ] Next exact action
- [ ] Residual risks

### 10.2 Repository State Documentation
- [ ] State **never inferred** from document existence alone
- [ ] Phase **never assumed** to be complete because directories exist
- [ ] Implementation **never presumed** from roadmap items
- [ ] Maturity **never declared** without evidence

---

## 11. Security and Tenant Constraints

### 11.1 Authorization
- [ ] Authorization never bypassed
- [ ] Source discovery respects authorization
- [ ] Tenant/domain/principal identity maintained
- [ ] Access policy preserved
- [ ] Confidentiality boundary protected

### 11.2 Tenant Isolation
- [ ] Tenant/domain/principal isolation **required** when applicable
- [ ] Cross-domain analysis **preserves ownership and provenance**
- [ ] Analysis results **isolated by authorized scope**
- [ ] Domain contributions **recorded**
- [ ] Generalization **not automatic** from domain-specific experience
- [ ] Only demonstrably reusable patterns **promoted after governance review**

### 11.3 Sensitive Information
- [ ] Broad data sets never used without relevance scope
- [ ] Problem → related entities → processes → systems → permitted sources → evidence defined
- [ ] Tenant, domain, principal, policy, need-to-know **applied**
- [ ] Sensitivity classifications **respected**
- [ ] Access limitations **preserved**

---

## 12. Python Baseline Constraint

### 12.1 Implementation Baseline
- [ ] New executable code supports **Python 3.14** (baseline)
- [ ] Deviations require explicit architecture decision
- [ ] Dependencies documented
- [ ] Virtual environments specified

---

## 13. Dependency and Integration Constraints

### 13.1 No Circular Dependencies
- [ ] No circular imports or definitions
- [ ] Layers respect orchestration boundaries
- [ ] Dependencies documented
- [ ] Integration contracts defined

### 13.2 External System Integration
- [ ] Contract + security + tests **required**
- [ ] Authorization boundaries **preserved**
- [ ] Provenance **tracked**
- [ ] Admission gate **applied**
- [ ] Failure modes **handled**

---

## 14. Governance Checklist for New Capabilities

Before merging, verify **all** applicable:

- [ ] Reuse Check — searched for related capability
- [ ] Classification — COMPATIBLE / ADAPT_REQUIRED / EVOLUTIONARY / INCOMPATIBLE / DUPLICATE
- [ ] Contracts — identified and reused
- [ ] Provenance — external inputs recorded
- [ ] Authorization — boundaries preserved or explicitly expanded with approval
- [ ] Tenant/Domain — isolation verified
- [ ] Tests — minimum categories covered
- [ ] Documentation — ADR filed if architecture decisions made
- [ ] Evidence — reproducible test results
- [ ] Admission Outcome — knowledge/feedback classified
- [ ] Layer Isolation — no boundary violation
- [ ] No Silent Change — Soul/Core authority not redefined without documented decision
- [ ] Handoff — next agent can understand current phase
- [ ] Security Review — when applicable
- [ ] Governance Review — when Soul/Core/Architecture affected

---

## 15. Blockers for Merge

**DO NOT MERGE** if any of these exist unresolved:

- [ ] Architectural conflict without recorded decision
- [ ] Security vulnerability or risk
- [ ] Tenant isolation violation
- [ ] Data integrity compromise
- [ ] Contract incompatibility without migration plan
- [ ] Loss of provenance
- [ ] Authority violation (lower redefining higher)
- [ ] Missing human decision for high-impact change
- [ ] Tests absent or failing when gate requires them
- [ ] Destructive action without reversibility
- [ ] Data exposure or privacy violation
- [ ] Contradiction with approved ADR
- [ ] Unknown artifact status (not NORMATIVE/IMPLEMENTED/TESTED/VERIFIED)
- [ ] Unreconciled evolutionary conflict without governance approval
- [ ] No handoff documentation for continuation

---

## 16. Status Vocabulary

Use these consistently:

| Status | Meaning |
|--------|---------|
| PROPOSED | Concept proposed but not approved |
| DRAFT | Under development |
| NORMATIVE | Approved rule/architecture |
| IMPLEMENTED | Code exists |
| TESTED | Executable evidence exists |
| VERIFIED | Independently reviewed/validated |
| EXPERIMENTAL | Intentionally non-canonical |
| DEPRECATED | Retained for historical compatibility |
| SUPERSEDED | Replaced by newer approved artifact |
| ROADMAP | Future capability |
| BLOCKED | Dependency prevents progress |

---

## 17. Authority Hierarchy

When conflicts arise, use this priority:

1. **Constitutional / Enterprise Principles**
2. **Baseline Architecture**
3. **Approved ADR**
4. **Policy / Governance**
5. **Canonical Contract**
6. **Implementation**
7. **Test / Fixture**
8. **Reference**
9. **Roadmap / Proposal**

Lower cannot silently override higher.

---

## 18. Definition of Done

### Minimal DoD for Level 4 (IMPLEMENTED)
- [ ] Canonical definition exists
- [ ] Owner assigned
- [ ] Contract defined
- [ ] Implementation written
- [ ] Execution documented

### Minimal DoD for Level 5 (TESTED)
- [ ] Level 4 complete
- [ ] Happy path tests pass
- [ ] Error tests pass
- [ ] Boundary tests pass
- [ ] Results recorded

### Minimal DoD for Level 6 (VERIFIED)
- [ ] Level 5 complete
- [ ] Acceptance criteria reviewed
- [ ] Architecture verified
- [ ] Provenance sufficient
- [ ] Critical gaps resolved or formally accepted

### Minimal DoD for Level 7 (OPERATIONALLY EVIDENCED)
- [ ] Level 6 complete
- [ ] Real authorized execution exists
- [ ] Observability in place
- [ ] Failure detection working
- [ ] Audit trail adequate
- [ ] Security/governance review passed when applicable

---

## 19. Escalation Path When Constraints Violated

If a constraint is violated:

1. Record the violation with full context
2. Classify severity: BLOCKER | CRITICAL | HIGH | MEDIUM | LOW
3. Document conflicting artifacts
4. Attempt reconciliation (see Section 7.3)
5. If unresolvable, escalate to governance
6. File issue/ADR for explicit decision
7. **Do not merge until resolved**

---

## 20. How to Use This Document

### For Humans
Read the section relevant to your change. Run through the checklist before marking work "done."

### For AI Agents
1. Read `AGENTS.md`
2. Read `ELO_REPOSITORY_NAVIGATION_RULES.md`
3. Read this document (`ELO_CONSTRAINTS.md`)
4. Apply the relevant constraint section(s)
5. Verify all checkboxes **before** submitting PR
6. Report which constraints were satisfied
7. Escalate any unresolved constraints

### For Code Review
Verify constraints section-by-section. Constraints are not suggestions—they are gates.

---

## 21. Effective Date and Authority

| Property | Value |
|----------|-------|
| **Status** | NORMATIVE |
| **Authority** | ELO Operating Rules + Maturity Framework |
| **Effective** | 2026-08-19 |
| **Owner** | ELO Architecture & Governance |
| **Last Review** | 2026-08-19 |
| **Next Review** | Upon ELO-VALIDATION-001 or when constraints prevent legitimate work |

---

**These constraints exist to preserve the ELO's integrity, identity, and governance while permitting controlled evolution.**

Not following them is a blocker for merge.
