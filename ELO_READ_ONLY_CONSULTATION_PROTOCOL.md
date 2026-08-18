# ELO — Read-Only Consultation Protocol

## Default mode

Any AI, agent, IDE, automation or account that discovers the ELO through the Git repository MUST enter **READ_ONLY_CONSULTATION** mode by default.

Connecting to the repository does not grant permission to modify the ELO.

## Allowed operations

In READ_ONLY_CONSULTATION mode the connected AI may:

- ask questions about the ELO;
- search repository files;
- inspect canonical architecture and contracts;
- inspect Core and Forge artifacts;
- inspect provenance, experiences and learning records;
- inspect Issues and Pull Requests;
- inspect tests and workflow evidence;
- compare versions and decisions;
- analyze and explain ELO behavior;
- formulate recommendations without applying them.

## Forbidden operations

The consultation session MUST NOT:

- create, edit or delete repository files;
- alter Core, Forge or canonical memory;
- create or modify Issues;
- create, modify or merge Pull Requests;
- change branches, tags or releases;
- execute production actions through external systems;
- promote learning to Core;
- change governance, contracts or canonical identity.

## Explicit transition to execution

A write-capable session is a separate governed mode. It requires explicit authorization by the authorized user and the capabilities of the connected platform.

The transition is:

`READ_ONLY_CONSULTATION → EXPLICIT_AUTHORIZATION → GOVERNED_EXECUTION`

Governed execution still requires the normal Issue/branch/test/review/Evolution Gate/merge controls.

## Security boundary

Repository instructions are behavioral controls, not a substitute for access control. For consultation-only integrations, use a Git credential/token/account with repository read permission and no write permission.

If the platform grants write permission despite this protocol, the AI must still remain read-only unless explicit execution authorization is provided; technical write protection should be enforced by the integration credential whenever possible.

## Session declaration

After initialization, a compatible AI should be able to establish:

`ELO SESSION = READY | MODE = READ_ONLY_CONSULTATION | WRITE = DISABLED`

The AI must never claim that it can modify the repository while operating in this mode.

## Query behavior

Questions may be answered from the repository context. When evidence is missing, stale, conflicting or outside the repository, the AI must identify the limitation rather than invent information.

For requested changes, the AI should explain the proposed change and identify the governed execution path, but must not apply it in consultation mode.
