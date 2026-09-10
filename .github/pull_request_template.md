## ELO Governance Gate

### Purpose
- What problem does this change solve?
- Why is it being changed now?
- What user intent is preserved or changed?
- What is explicitly out of scope?

### Reuse-before-create
- [ ] Exact concept searched
- [ ] Synonyms/abbreviations searched
- [ ] Existing contract/interface checked
- [ ] Existing implementation checked
- [ ] Existing tests checked
- [ ] Relevant ADR/governance checked
- [ ] Canonical owner identified
- [ ] Change classified: REUSE / EXTEND / CORRECT / CONSOLIDATE / DEPRECATE / NEW
- [ ] If NEW, demonstrated gap and traceability justification included

### Architecture
- [ ] No second Cognitive Core or authority created
- [ ] Cognitive/Core/Forge/Application/Infrastructure boundaries preserved
- [ ] Existing authentication/authorization boundary reused
- [ ] Existing memory/data authority reused
- [ ] No downstream runtime called directly from browser when a governed ELO boundary exists
- [ ] Hermes remains an execution runtime, not authority

### Security / provenance
- [ ] Tenant/domain/principal isolation preserved where applicable
- [ ] Request/correlation lineage preserved where applicable
- [ ] Provenance preserved
- [ ] Secrets and infrastructure identifiers remain server-side
- [ ] External/provider output cannot silently become canonical

### Tests / evidence
- [ ] Happy path
- [ ] Invalid input/error handling
- [ ] Authorization failure/tenant isolation
- [ ] Dependency failure/timeout
- [ ] Malformed external response
- [ ] Provenance/correlation
- [ ] Security/privacy
- [ ] Connector/runtime isolation
- [ ] Canonical authority protection
- [ ] Non-canonical learning handling

### Preventive control
- [ ] If this fixes an architectural/recurring error, a reusable guard/test/check was added
- [ ] Adjacent implementations were checked for the same failure mode

### ELO Gate
- [ ] ELO_GATE: PASS / REVISE / ESCALATE
- [ ] Evidence and test results recorded
- [ ] Residual risks listed
- [ ] Material commit changes re-trigger full review
