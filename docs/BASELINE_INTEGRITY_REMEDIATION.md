# ELO — Baseline Integrity Remediation

## Objective
Restore the repository's pre-existing behavioral contracts exposed by the Diagnostic Scenario Engine integration without weakening the new deterministic diagnostic layer.

## Scope
The remediation covers conversation intake and evolution-memory persistence, ChatBridge schema compatibility, source-discovery intent precedence, and contextual-memory request normalization.

## Architectural rule
The diagnostic scenario engine remains deterministic, evidence-driven, and independent of GPT reasoning. Baseline repairs must not introduce a second cognitive core, bypass tenant/domain isolation, or silently convert observations into canonical knowledge.

## Verification gate
The complete pytest suite and compilation must pass before this remediation is eligible for merge.
