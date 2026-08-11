# ELO — Artifact Metadata Standard

## 1. Purpose

This standard gives every important ELO artifact a minimal semantic identity so humans and AI agents can understand what it is, who owns it, what authority it has, and whether it is implemented.

It is intentionally lightweight. Metadata must not become bureaucracy that prevents useful work.

## 2. Required semantic metadata

For normative or reusable artifacts, use a metadata block when the file format permits it.

Recommended fields:

```yaml
id: ELO-<DOMAIN>-<NUMBER>
name: <human-readable name>
type: normative|contract|implementation|test|governance|reference|roadmap|asset
layer: enterprise|architecture|process|knowledge|cognitive|data|ai|governance|system|roadmap
owner: <canonical conceptual owner>
status: proposed|draft|normative|implemented|tested|verified|experimental|deprecated|superseded|roadmap|blocked
authority: constitutional|baseline|adr|policy|contract|implementation|test|reference|proposal
version: <version>
related: []
depends_on: []
```

## 3. Interpretation

### id
Stable identifier for cross-document references.

### name
Human-readable title.

### type
What kind of artifact this is.

### layer
Where the artifact belongs semantically, independent of its physical path.

### owner
The canonical capability/domain responsible for meaning and lifecycle.

### status
Current maturity state.

### authority
How much authority the artifact has when conflicts occur.

### version
Useful when the artifact has a meaningful lifecycle. Do not invent versions for transient notes.

### related
Concepts that should be read together.

### depends_on
Artifacts that must exist or be approved first.

## 4. Suggested metadata for code modules

Python modules do not need YAML front matter. Instead, use a module docstring and, when useful, a small comment block or package metadata.

Example:

```python
"""ELO Cognitive API application boundary.

Layer: cognitive
Owner: cognitive-interface
Status: implemented
Authority: contract
Related: CognitiveRequest, CognitiveResponse, Session
"""
```

Do not add metadata comments to every function.

## 5. Suggested metadata for ADRs

ADRs should contain:

- ADR ID;
- title;
- status;
- date;
- decision owners when appropriate;
- context;
- decision;
- alternatives;
- consequences;
- supersedes/superseded-by when applicable.

## 6. Suggested metadata for tests

Tests should make clear:

- capability under test;
- requirement/criterion covered;
- expected behavior;
- governance boundary if relevant.

Test names should communicate behavior rather than implementation detail.

Example:

```text
test_missing_tenant_id_is_rejected
```

## 7. Status transition model

Normal lifecycle:

PROPOSED
→ DRAFT
→ NORMATIVE
→ IMPLEMENTED
→ TESTED
→ VERIFIED

Possible alternate paths:

DRAFT → DEPRECATED
NORMATIVE → SUPERSEDED
IMPLEMENTED → BLOCKED
EXPERIMENTAL → NORMATIVE

A status transition must not be implied merely by a file existing.

## 8. Authority rules

If metadata says `status: proposed`, the content must not be treated as an approved requirement.

If metadata says `authority: reference`, it must not override an ELO baseline.

If metadata says `status: implemented` but no executable evidence exists, the artifact is misclassified and should be corrected.

## 9. Maturity vocabulary

For architecture reviews, use:

0 — absent
1 — conceptual
2 — documented
3 — contracted
4 — implemented
5 — tested
6 — verified
7 — operationally evidenced

Do not claim a maturity level above the evidence available.

## 10. AI behavior

AI agents must use metadata as context, not as permission to bypass higher-authority rules.

For example:

```yaml
status: proposed
```

means:

"This exists as a proposal. Do not implement it unless the task explicitly authorizes implementation or an approval gate promotes it."

## 11. Example — Cognitive Consulting

A proposed capability could be represented as:

```yaml
id: ELO-COG-CONSULT-001
name: Cognitive Consulting Mode
type: normative
layer: cognitive
owner: cognitive-core
status: proposed
authority: proposal
version: 0.1
related:
  - Cognitive Core
  - Context
  - Knowledge
  - Experience Memory
  - Reasoning
  - Decision Support
depends_on:
  - ELO-001
  - ELO-002
  - ELO-003
```

Correct interpretation:

The concept exists and is being designed, but it is not yet an implementation requirement until approved.
