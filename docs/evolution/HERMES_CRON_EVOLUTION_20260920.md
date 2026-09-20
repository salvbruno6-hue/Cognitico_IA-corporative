# Hermes Cron / Scheduled Tasks -> ELO Boundary - 2026-09-20

## Finding

Hermes cron provides persistent scheduled agent tasks and can attach skills or scripts to scheduled invocations. Scripts may run before an agent turn and their stdout becomes context for that turn. This is useful as an execution adapter but must not become an independent ELO scheduler authority.

## ELO adaptation

EXT-CRON-HERMES belongs to ELO Workflow/Automation.

Required:
- schedule identity;
- tenant scope;
- task identity/digest;
- owner principal;
- schedule expression;
- provenance;
- explicit authorization;
- idempotency.

A fully specified authorized and idempotent schedule becomes CANDIDATE only. Missing authorization or idempotency remains OBSERVATION. Any governance bypass is REJECTED.

## Authority boundary

A scheduled trigger is equivalent to an execution trigger, not an authorization grant. Every scheduled invocation must still pass the same policy, scope, tool authorization, security, evidence and Evolution Gate requirements applicable to the corresponding manual execution.

Cron cannot:
- promote learning;
- modify canonical governance;
- bypass approval;
- widen permissions;
- authorize itself;
- merge to main.

## Non-goals

- no scheduler implementation;
- no cron registration;
- no automatic execution;
- no permission mutation;
- no Core promotion.
