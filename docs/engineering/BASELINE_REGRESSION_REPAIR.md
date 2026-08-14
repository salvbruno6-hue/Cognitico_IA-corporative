# Baseline Regression Repair

Issue: #57

## Purpose

Restore pre-existing contracts exposed by the post-merge validation of the Diagnostic Scenario Engine without weakening the new engine.

## Required contracts

- Conversation intake preserves authorized observations in Evolution Memory with provenance and tenant/domain isolation.
- Conversation bridge preserves the established schema version contract.
- Source discovery applies the most specific semantic intent rather than allowing a generic `elo` keyword to override a more specific request.
- Contextual Memory normalizes mapping payloads into the canonical cognitive request contract before context resolution.

## Acceptance criteria

The full pytest suite passes. The Diagnostic Scenario Engine remains deterministic, evidence-preserving, and isolated from GPT/Reasoning responsibilities. No test is removed or weakened solely to make the suite green.
