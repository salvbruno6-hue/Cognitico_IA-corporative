# EXT-WORKTREE-HERMES — Governed Runtime Execution

## Purpose

This implementation closes the runtime execution boundary for \`EXT-WORKTREE-HERMES\`
without turning Hermes or a worktree into a merge or governance authority.

The path is:

\`WorktreeSignal → WorktreeAdapter → ExecutionBoundary → bounded Forge workspace descriptor → ExecutionOutcome\`

## Controls

The adapter:
- requires the canonical \`ExecutionBoundary\`;
- requires authorization, evidence and correlation controls supplied by that boundary;
- enforces tenant-scope equality;
- reuses the existing \`WorktreeAdapter\`;
- rejects missing provenance or isolation through the existing candidate boundary;
- records that no Git mutation occurred;
- never creates or deletes a worktree;
- never merges to main;
- never promotes to Core;
- does not create an Evolution Gate or learning authority.

## Evidence classification

A successful controlled execution is **runtime operational evidence for the governed boundary**.

It is **not production proof**.

Production outcome remains blocked until repeated observations from the actual Forge/worktree operational lifecycle are captured through the existing evidence and governance path.

## Rollback

Rollback is code-level PR rollback/revert. The adapter itself performs no Git mutation and therefore has no hidden worktree side effect to undo.
