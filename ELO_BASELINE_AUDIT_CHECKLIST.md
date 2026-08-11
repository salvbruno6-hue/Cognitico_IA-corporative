# ELO — Baseline Audit Checklist

Use this checklist before declaring a baseline frozen.

## A. Repository inventory

- [ ] All top-level directories inventoried.
- [ ] Portuguese/English parallel directories identified.
- [ ] Canonical owner for each relevant concept identified.
- [ ] Duplicate/conflicting artifacts registered.
- [ ] Historical content preserved unless explicitly deprecated/moved.

## B. Architecture

- [ ] Enterprise principles identified.
- [ ] Architecture baseline identified.
- [ ] Cognitive Core boundary identified.
- [ ] Context boundary identified.
- [ ] Knowledge boundary identified.
- [ ] Memory boundary identified.
- [ ] Reasoning boundary identified.
- [ ] Decision boundary identified.
- [ ] Agent/autonomy boundary identified.
- [ ] Integration boundary identified.
- [ ] Data boundary identified.
- [ ] Governance boundary identified.

## C. Contracts

- [ ] Canonical request contracts identified.
- [ ] Canonical response contracts identified.
- [ ] Error contracts identified.
- [ ] Event contracts identified where applicable.
- [ ] Tenant identity rules identified.
- [ ] Session rules identified.
- [ ] Provenance rules identified.

## D. Implementation

- [ ] Every declared implemented capability maps to code.
- [ ] Code is located under the correct owner.
- [ ] No implementation silently duplicates another implementation.
- [ ] Runtime entry points are identified.

## E. Testing

- [ ] Test discovery is documented.
- [ ] Happy paths exist for implemented vertical slices.
- [ ] Error paths exist.
- [ ] Boundary conditions exist where relevant.
- [ ] Security tests exist where relevant.
- [ ] Tenant isolation tests exist where relevant.
- [ ] Test execution result is recorded.
- [ ] A zero-test collection result is treated as a gap, not as success.

## F. Evidence

- [ ] Each maturity claim has evidence.
- [ ] Evidence source is reproducible or auditable.
- [ ] Historical commits are distinguished from current execution evidence.
- [ ] Evidence limitations are recorded.

## G. Governance

- [ ] Owner exists for each critical capability.
- [ ] Authority is identified.
- [ ] Human decision boundary is identified.
- [ ] Autonomous actions are explicitly controlled.
- [ ] Security-sensitive changes have review.
- [ ] Provenance requirements are addressed.

## H. Cognitive Consulting / Organizational Health

- [ ] Consulting Mode remains clearly separated from approved implementation.
- [ ] Experience Memory is classified as proposed unless verified.
- [ ] Scientific/technical knowledge is distinguished from organizational experience.
- [ ] Information Gap is defined before automated questions are generated.
- [ ] Recommendations are distinguished from decisions.
- [ ] Person-level inferences have ethical/governance controls.
- [ ] Organizational health conclusions remain evidence-based.

## I. Baseline decision

- [ ] All blockers are resolved or formally accepted.
- [ ] Snapshot is generated against a fixed commit SHA.
- [ ] Maturity levels are conservative.
- [ ] Open gaps have owners.
- [ ] Next actions have Definition of Done.
- [ ] Baseline approval is recorded.
- [ ] Baseline tag/version is created only after approval.
