# Hermes Multi-Agent Delegation -> ELO Boundary - 2026-09-20

## Finding

Hermes delegate_task creates child agents with fresh context and separate terminal sessions; parallel batches can run multiple workstreams, while only the final summary returns to the parent. Structured output can constrain returned results, and worktree isolation can prevent parallel edits from colliding. This makes delegation useful as an execution pattern, not as a second cognitive authority.

## ELO adaptation

EXT-MULTIAGENT-HERMES belongs to ELO Agent Delegation.

Required evidence:
- delegation identity;
- tenant scope;
- parent and child identities;
- goal contract;
- provenance;
- bounded resource scope;
- isolated context when execution is admitted.

A verified isolated delegation becomes CANDIDATE. Shared-context delegation remains OBSERVATION. Missing provenance/identity/goal is REJECTED. A child declaring authority is rejected.

## Authority boundary

A delegated child may produce evidence, analysis, code, tests or recommendations. It cannot:
- promote learning;
- modify ELO Core authority;
- merge to main;
- approve its own promotion;
- bypass Evolution Gate;
- silently widen its tools or scope.

The parent/orchestrator remains responsible for admission, synthesis, evidence integrity and governed promotion.

## Non-goals

- no child-agent runtime;
- no automatic spawning;
- no permission changes;
- no automatic promotion;
- no merge authority.
