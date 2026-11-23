# ELO External Action Continuity

Status: **candidate**
Owner: **existing ELO orchestration / authorization / execution boundaries**
Nature: **Symbiont continuity classification; no new authority**

## Problem

A governed objective may be fully validated while the currently selected external executor is prevented by a policy outside ELO before the requested operation reaches the target system. This condition must not be reported as an ELO technical failure, a target-system rejection, or permission to bypass the external policy.

## Invariant

`VALIDATED_OBJECTIVE + GOVERNANCE_APPROVED + EXTERNAL_EXECUTOR_BLOCKED` preserves the objective as pending but does not retry the blocked executor and does not manufacture authority.

An alternative executor may continue only when it independently proves authorization for the exact operation and resource. Authorization is never inherited from the blocked path.

## States

- `CONTINUE_AUTHORIZED_ROUTE`: selected/alternative route independently authorized.
- `EXTERNAL_ACTION_BLOCKED`: objective remains valid, current external path is blocked, no authorized alternative is available.
- `AUTHORIZATION_REQUIRED`: governance or executor authority is absent.
- `TERMINAL_FAILURE`: continuation is not safe.
- `INVALID`: malformed controls fail closed.

## Non-goals

This candidate does not create credentials, tokens, bypass actors, GitHub permissions, merge authority, retries, a new Router, a new ExecutionBoundary, or a new authorization authority. It does not weaken repository rulesets and does not execute business operations.

## Evidence case

PR #1128 provides the motivating observed case: ELO gates and independent review passed, GitHub reported the PR mergeable and the repository identity had sufficient repository privileges, while the ChatGPT integration policy blocked the merge action before a GitHub merge response was produced. The case is evidence for classification only; it does not authorize a workaround.

## Promotion criteria

Promotion requires focused tests, repository CI, Evolution Gate and independent review. Runtime effectiveness remains `INDETERMINATE` until directly observed through an authorized alternative execution route.
