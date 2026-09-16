# ELO — Governed Autocorrection Learning Loop

## Purpose

Unify the Autocorrection Laboratory and the Evolution Loop into one continuous governed state machine while preserving the existing architecture, gates and evidence requirements.

The loop learns from **validated outcomes**, not from raw agent output. A previous correction becomes reusable guidance only after the relevant gates, merge state and post-merge regression are evidenced.

## Authority boundary

`ELO = cognitive authority`  
`Codex = executor / laboratory instrument`  
`Supabase = consultative persistent memory`  
`GitHub = operational/versioning ledger`  
`Governance = authority over admissibility and promotion`

Codex MUST NOT autonomously:

- authorize its own execution;
- authorize its own commit;
- authorize its own merge;
- promote a hypothesis to canonical learning;
- change `main` directly;
- create or alter a governance gate to make its own work pass;
- treat its own dossier as evidence of authorization.

Authorization is an input to execution, not an output of Codex. The workflow must consume explicit ELO authorization state and never manufacture that state itself.

## Unified state machine

`DIAGNÓSTICO → CAUSA_RAIZ → HIPÓTESE_SOLUÇÃO → LABORATÓRIO_ISOLADO → TESTES → AJUSTE_AUTOCORRETIVO → VALIDAÇÃO_ARQUITETURAL_GOVERNANÇA → PR_ISSUE_GOVERNADA → EVOLUTION_GATE → MERGE_PERMITIDO → MERGED → ON_MAIN → REGRESSION → APRENDIZADO → PRÓXIMA_CORREÇÃO`

A state transition requires evidence. A failed transition keeps the cursor at the current state.

## Daily cycle

Each daily execution performs exactly one correction unit unless a real external block prevents continuation.

### 1. Diagnose

Inventory structure, current changes, Issues, PRs, commits, contracts, tests, workflows, capabilities, runtime evidence and prior learning.

### 2. Retrieve before reinventing

Calculate or identify a stable problem fingerprint and search prior learning records for:

- same fingerprint;
- same canonical capability;
- related root cause;
- previously failed approaches;
- superseded solutions;
- known correction path;
- known regression suite;
- known blockers.

A matching learning record is guidance/evidence, not automatic authority.

### 3. Root cause

Separate:

- observed symptom;
- reproducible failure;
- root cause;
- contributing factors;
- governance cause;
- environment/external blocker.

### 4. Hypothesis / solution

Prefer the smallest structurally correct change. Reconcile existing capabilities before creating anything new.

### 5. Laboratory

The laboratory is an internal phase of the same cycle. It must not become a second automation, authority or production path.

The laboratory records every attempt, including failures, rejected hypotheses and corrective iterations.

### 6. Validation

Validate contracts, dependencies, duplicates, security, architecture and the boundaries between Soul, Cognitive, Forge, Core and Governance.

### 7. Governed promotion

Only after technical validation may the cycle create/update the PR/Issue evidence package. A draft PR is never treated as merge-ready.

### 8. Merge and post-merge proof

`MERGED` is not terminal. The cycle must prove:

1. `merged=true`;
2. `merge_commit_sha` exists;
3. `main` contains the merge commit/ancestry;
4. the relevant regression executes against the actual `main` state;
5. `REGRESSION_PASS=true`.

Only then can the correction be marked `OK`.

## Learning model

Every completed correction produces two separate learning records:

### A. Problem learning

What the ELO learned about the organization/system:

- problem fingerprint;
- affected capability;
- root cause;
- validated correction;
- tests that prove it;
- merge evidence;
- post-merge regression;
- known recurrence indicators;
- reusable correction path;
- supersession relation, when applicable.

### B. Method learning

What ELO learned about the diagnostic/correction method:

- which inspection located the defect;
- which evidence was decisive;
- which hypotheses failed and why;
- which test isolated the root cause;
- which sequence reduced rework;
- which gate prevented unsafe promotion;
- which evidence was misleading or stale.

Method learning cannot silently become a governance rule. It remains a `LEARNING_CANDIDATE` until separately validated.

## Knowledge classes

Use the existing ELO taxonomy:

`CASE` → concrete occurrence  
`PRECEDENT` → reusable prior decision/context  
`LEARNING_CANDIDATE` → proposed generalization  
`VALIDATED_LEARNING` → evidence-backed reusable learning  
`CONCEPTUAL_KNOWLEDGE` → stable conceptual understanding  
`INSTRUCTIONAL_KNOWLEDGE` → validated procedure  
`RULE` → explicit governed norm

No class promotion occurs solely because Codex recommends it.

## Supersession and duplicate prevention

When a newer correction replaces an older one, record:

`supersedes: <learning_id>`

The old record remains historical and searchable but is not selected as the active correction path.

A recurrence must first reconcile existing records. It must not create a duplicate `VALIDATED_LEARNING` for the same concept and evidence unless the new evidence materially changes the conclusion.

## Cursor persistence

The cycle cursor must identify:

- task/correction id;
- problem fingerprint;
- current state;
- next action;
- cycle number;
- branch/PR when applicable;
- latest evidence;
- blocker;
- prior learning consulted;
- supersession relation;
- terminal conditions.

On restart, ELO resumes from the first state without valid evidence and does not replay already validated states.

## Authorization model

Authorization is explicit and externally established by the ELO cognitive authority.

Recommended operational states:

- `ELO_EXECUTION_AUTHORIZED` — permits the executor to prepare a correction on an isolated branch.
- `ELO_MERGE_AUTHORIZED` — permits the governed merge operation after all technical gates pass.
- `ELO_LEARNING_AUTHORIZED` — permits promotion of a learning candidate after cognitive consolidation.

Codex may consume these states but cannot create them as a consequence of its own analysis.

## Daily output

The terminal report contains only:

`deficiência atual; estado do ciclo; causa raiz; solução/hipótese; resultado do laboratório; testes e regressões; autocorreções realizadas; evidências; estado da PR/Issue; Evolution Gate; MERGED/merge_commit_sha; ON_MAIN; REGRESSION_PASS; aprendizado incorporado; bloqueios reais; próximo cursor.`
