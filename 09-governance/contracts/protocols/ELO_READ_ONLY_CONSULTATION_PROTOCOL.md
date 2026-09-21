# ELO — Read-Only Consultation Protocol

## Default

Any AI, agent, IDE, automation or account that discovers the ELO through Git MUST enter `READ_ONLY_CONSULTATION` mode by default.

## Allowed

- ask questions about ELO;
- search and inspect repository evidence;
- inspect architecture, contracts, Core, Forge, provenance and experiences;
- inspect Issues, PRs, tests and workflow evidence;
- compare versions and decisions;
- analyze and explain;
- formulate recommendations without applying them.

## Forbidden in consultation mode

- create, edit or delete repository files;
- alter Core, Forge or canonical memory;
- create or modify Issues;
- create, modify or merge PRs;
- change branches, tags or releases;
- execute external production actions;
- promote learning to Core;
- change governance, contracts or canonical identity.

## Transition to execution

`READ_ONLY_CONSULTATION → EXPLICIT_AUTHORIZATION → GOVERNED_EXECUTION`

Execution still requires the normal Issue/branch/test/review/Evolution Gate/merge controls.

## Security boundary

This protocol is a behavioral contract, not a substitute for access control. Consultation-only integrations should use Git credentials/tokens with read permission and no write permission.

## Session declaration

`ELO SESSION = READY | MODE = READ_ONLY_CONSULTATION | WRITE = DISABLED`

## Query behavior

When evidence is missing, stale or conflicting, report the limitation/GAP rather than invent information.
