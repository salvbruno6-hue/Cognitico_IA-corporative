# ELO Session Modes

| Mode | Read/Search | Recommend | Write | Merge | External Actions |
|---|---|---|---|---|---|
| `READ_ONLY_CONSULTATION` | YES | YES | NO | NO | NO |
| `GOVERNED_EXECUTION` | YES | YES | YES, if authorized | Only through gates | Only if authorized |

Every new Git-connected AI session starts in `READ_ONLY_CONSULTATION`.

Transition requires explicit authorization:

`READ_ONLY_CONSULTATION → EXPLICIT_AUTHORIZATION → GOVERNED_EXECUTION`

Repository read access alone never grants write authority.
