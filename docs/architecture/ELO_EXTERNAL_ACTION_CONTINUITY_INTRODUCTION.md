# Candidate Introduction — External Action Continuity

Candidate: `EVO-EXTERNAL-ACTION-CONTINUITY`
Date: 2026-11-01
Status: CANDIDATE

## Introduction

Refine the existing Symbiont/orchestration boundary so a validated objective is not discarded when an external integration policy blocks the selected executor before the target system receives the action.

The refinement classifies the boundary, preserves the pending objective, prohibits retry of the blocked executor as an authorization workaround, and admits an alternative route only when that route independently proves authorization for the same operation/resource.

## Canonical ownership

No new owner is introduced. Orchestration remains composition; authorization remains external/canonical; execution remains governed by the existing ExecutionBoundary. The Symbiont observes and classifies continuity but cannot grant authority.

## Acceptance

- external block is distinct from target rejection;
- objective can remain pending;
- blocked executor is not automatically retried;
- alternative executor requires independent authorization;
- malformed controls fail closed;
- no bypass, credential creation, Router, Memory, Core or Evolution Gate duplication.
