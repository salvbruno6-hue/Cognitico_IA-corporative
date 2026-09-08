# ELO ↔ Hermes — Symbiont Integration Contract

**Status:** COGNITIVE / GOVERNED CONTRACT / V1

## 1. Purpose

Define how `ELO Cognitive` uses the external `Hermes Agent` runtime as an operational execution extension through the cognitive nature of the `Simbionte`.

This contract belongs to ELO Cognitive. Hermes remains an external execution/orchestration provider and does not become a new ELO Core, Cognitive Core, authority, memory owner, router, or Evolution Gate.

## 2. Architectural position

```text
Especialista
    ↓
GPT / Intent
    ↓
ELO Cognitive
    ├── Context
    ├── Knowledge
    ├── Reasoning
    ├── Decision
    ├── Routing
    └── Learning
            ↓
        Simbionte
            ↓
      Hermes Agent
    ├── Skills
    ├── Plugins
    ├── Tools
    ├── Subagents
    └── Execution
            ↓
       Evidence / Outcome
            ↓
        Simbionte
            ↓
    Governed Learning
            ↓
      Evolution Gate
            ↓
          Core
```

## 3. Ownership

| Concern | Canonical owner |
|---|---|
| ELO identity / invariants | ELO Cognitive / Soul |
| governance | Core |
| context resolution | Cognitive / Context |
| knowledge | Cognitive / Knowledge |
| reasoning and task planning | Cognitive / Reasoning |
| decision | Cognitive / Decision |
| execution routing authority | Cognitive / Routing |
| learning evaluation | Cognitive / Learning |
| contextual experience | Forge |
| execution runtime | Hermes |
| operational skills | Hermes |
| external tools/plugins | Hermes |
| evidence returned from execution | ELO Cognitive contract + Forge provenance |
| learning promotion | ELO Governed Learning / Evolution Gate |

Hermes executes. ELO governs.

## 4. Symbiont role

Simbionte is not a new architectural component. It is the cognitive nature that absorbs, relates, experiments, measures, tests and generalizes experience.

The integration therefore uses the pattern:

`ELO Cognitive → Symbiont Contract → Hermes → Evidence → Symbiont → Governed Learning`

It does not use:

`ELO → Hermes Core → new authority`

## 5. Request contract

The ELO side may send only an authorized execution mission containing:

- `request_id`
- `intent`
- `context`
- `tenant_scope`
- `mission_class`
- `authorized_capabilities`
- optional `method`
- optional `constraints`
- optional `evidence_requirements`
- optional `execution_policy`
- `contract_version`

Infrastructure identifiers are deliberately excluded. In particular, `project_id`, `project_ref`, database URLs and Supabase identifiers must be resolved internally by ELO adapters and must never be requested from or exposed to the specialist through Hermes.

## 6. Result contract

Hermes returns execution evidence, not canonical knowledge or a canonical decision.

Minimum result surface:

- `request_id`
- `status`
- `execution`
- `artifacts`
- `evidence`
- `tool_usage`
- `skills_used`
- `outcome`
- `gaps`
- `conflicts`
- `metrics`
- optional `learning_candidate`
- `contract_version`

A `learning_candidate` remains a candidate. It cannot promote itself to Core.

## 7. Authority invariants

Hermes must never:

1. modify Soul;
2. redefine Core contracts;
3. promote knowledge to canonical status;
4. change canonical execution routing;
5. authorize itself or expand its scope;
6. cross tenant/domain/principal boundaries;
7. create a competing Memory, Router, Engine, Provider Registry or Evolution Gate;
8. turn an external skill into a canonical ELO rule without governed learning;
9. infer infrastructure identifiers for specialist-facing output;
10. treat one successful execution as generalized learning.

## 8. Skills Factory boundary

Hermes Skills Factory is an operational learning surface, not the ELO Canon.

```text
Hermes Skill
    ↓
execution / experience
    ↓
evidence
    ↓
Simbionte observation
    ↓
experiment / benchmark / regression
    ↓
Learning Candidate
    ↓
Governed Learning
    ↓
Evolution Gate
    ↓
possible Core promotion
```

Skill creation or modification in Hermes does not automatically modify ELO knowledge.

## 9. Tenant and authorization boundary

ELO resolves and authorizes:

`principal → tenant → domain → scope → capability → execution policy`

Hermes receives only the resulting authorized mission. Hermes may report a blocked or insufficient-capability outcome, but it cannot widen the authorization boundary.

## 10. Agentic ELO relationship

The Agentic layer remains responsible for governed decomposition and contextual resolution:

`solicitação → intenção → contexto → resolução → consulta → evidências → decisão → execução → resultado`

Hermes is the execution runtime at the execution boundary. It must not duplicate Agentic ELO as a second canonical planner.

## 11. Upstream preservation

`ELO-Hermes-Agent` remains a separate repository. Upstream Hermes code is adapted at the edge through ELO-specific adapters, skills, plugins and contracts rather than copied into ELO Cognitive.

Hermes upstream's own operational identity may remain in its repository, but it is subordinate to ELO governance whenever Hermes is operating as an ELO execution provider.

## 12. Evolution path

The implementation is intentionally staged:

1. **Contract** — ELO-owned request/result boundary.
2. **Bridge** — Hermes accepts a governed ELO mission.
3. **Evidence** — execution provenance and outcome return to ELO.
4. **Skills Factory** — Hermes skills participate in Simbionte experiments.
5. **Learning** — candidates enter Governed Learning and Evolution Gate.
6. **Expanded autonomy** — only after the preceding boundaries are validated.

## 13. Non-goals for V1

V1 does not:

- import Hermes into the ELO repository;
- replace the existing ELO Agentic layer;
- create a new Simbionte engine;
- grant Hermes direct Core write authority;
- create automatic learning promotion;
- alter Soul;
- alter Supabase schema;
- expose infrastructure identifiers;
- merge Hermes into the ELO `main` branch.

## 14. Acceptance criterion

The integration is structurally acceptable only when the following remains true:

```text
GPT interprets
ELO resolves and governs
Simbionte observes and learns
Hermes executes
Core decides what becomes canonical
```

No lower layer may silently redefine a higher layer.
