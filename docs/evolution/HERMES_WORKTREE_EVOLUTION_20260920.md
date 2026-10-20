# Hermes Git Worktree Isolation -> ELO Boundary - 2026-09-20

## Finding

Hermes worktree isolation is useful as a technical execution mechanism: work can be performed in an isolated Git worktree rather than directly against the shared checkout.

## ELO adaptation

EXT-WORKTREE-HERMES belongs to ELO Forge as an isolated technical workspace mechanism.

The worktree can hold candidate implementation, tests, generated evidence and temporary changes. It cannot become a merge authority.

Required evidence:
- tenant scope;
- worktree identity;
- base reference;
- provenance;
- isolation confirmation.

A clean, verified, isolated worktree becomes CANDIDATE. A dirty worktree remains OBSERVATION. Missing provenance or isolation is REJECTED.

## Governance boundary

Worktree state does not authorize:
- merge to main;
- promotion to ELO Core;
- modification of canonical governance;
- bypass of PR review;
- bypass of Evolution Gate;
- bypass of security or behavioral validation.

The existing Git/PR governance remains authoritative.

## Non-goals

- no worktree creation/deletion from this contract;
- no Git mutation;
- no automatic merge;
- no production activation;
- no Core promotion.
