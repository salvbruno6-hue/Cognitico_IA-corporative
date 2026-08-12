# ELO-003 — Governed Agent Ecosystem

## Status

Implementation baseline — governed agent foundation.

## Objective

Create the canonical architecture for specialist agents that observe, analyze and report domain findings to ELO without creating competing cognitive cores or uncontrolled autonomy.

## 1. Architectural position

```text
                    ELO COGNITIVE CORE
                            |
                    AGENT ORCHESTRATOR
                            |
          +-----------------+------------------+
          |                 |                  |
      FINANCE             HR              PRODUCTION
       AGENT             AGENT              AGENT
          |                 |                  |
          +-----------------+------------------+
                            |
                   governed reports
                            |
                    Context / Evidence
                            |
                       ELO Memory
```

The ELO remains the coordinating cognitive authority. Specialist agents are capability providers, not replacement cores.

## 2. Agent contract

Every agent must have a stable identity and governed capability declaration.

```yaml
agent_id:
agent_name:
agent_version:
tenant_scope:
domain:
capabilities:
tools:
input_contract:
output_contract:
policy_profile:
autonomy_level:
status:
provenance:
```

## 3. Capability model

Capabilities must be explicit.

Examples:

```text
OBSERVE
ANALYZE
RETRIEVE
CLASSIFY
CORRELATE
RECOMMEND
REQUEST_HUMAN_INPUT
EXECUTE_LIMITED_ACTION
```

An agent may only invoke capabilities granted by its policy profile.

## 4. Autonomy levels

```text
L0 — OBSERVE ONLY
L1 — ANALYZE
L2 — RECOMMEND
L3 — EXECUTE WITH APPROVAL
L4 — EXECUTE WITHIN POLICY
L5 — GOVERNED AUTONOMY
```

Autonomy is a capability, not an implicit property of an agent.

No agent may elevate its own autonomy level.

## 5. Agent observation contract

```yaml
observation_id:
agent_id:
tenant_id:
domain:
subject:
observation:
entities:
evidence_refs:
confidence:
questions:
recommended_next_step:
provenance:
```

An agent observation is not automatically verified knowledge.

```text
Agent output
    ↓
Observation
    ↓
Evidence
    ↓
Validation
    ↓
Knowledge status
```

## 6. Agent task contract

ELO may delegate a bounded task to an agent.

```yaml
task_id:
agent_id:
tenant_id:
domain:
objective:
context_refs:
evidence_refs:
constraints:
allowed_tools:
required_output:
time_budget:
policy:
```

Agents must not receive unnecessary data. Context should follow least privilege.

## 7. Orchestration lifecycle

```text
Detect need
    ↓
Select capability
    ↓
Select agent
    ↓
Build minimum context
    ↓
Policy check
    ↓
Execute task
    ↓
Validate result
    ↓
Register evidence
    ↓
Return to ELO
```

Failures must be explicit and observable.

## 8. Tool governance

Tools must be registered before agent use.

```yaml
tool_id:
tool_type:
capabilities:
required_permissions:
input_schema:
output_schema:
risk_level:
policy:
auditable:
```

An agent cannot discover or invoke arbitrary tools outside its assigned policy.

## 9. Human approval

Actions with material consequences should require approval unless an explicit policy authorizes bounded autonomous execution.

Examples normally requiring approval:

- financial movement;
- employment action;
- legal commitment;
- destructive data operation;
- production shutdown;
- external contractual communication.

## 10. Agent result validation

ELO should evaluate:

- contract validity;
- provenance;
- evidence completeness;
- confidence;
- policy compliance;
- tenant/domain scope;
- contradictions;
- expected output format.

A failed validation must not silently enter trusted knowledge.

## 11. Multi-agent collaboration

Agents communicate through governed contracts, not shared hidden memory.

```text
Agent A
  ↓
Finding
  ↓
ELO / Orchestrator
  ↓
Agent B task
  ↓
Finding
  ↓
ELO correlation
```

This preserves traceability and prevents agent-to-agent trust from bypassing ELO governance.

## 12. Specialist domain packs

Historical agents such as Finance, HR, Production, Logistics, Quality and Engineering should be treated as domain requirements and capability sources.

They must not be copied wholesale from the legacy `ELO/agents/` tree.

The canonical implementation is:

```text
ELO Core
 +
Agent Contract
 +
Domain Pack
 +
Policy
 +
Evidence
```

## 13. Security

Mandatory isolation:

```text
tenant_id
principal_id
agent_id
domain
policy
```

Tests must prove that an agent cannot:

- read another tenant;
- impersonate another agent;
- invoke unauthorized tools;
- write directly into another domain's protected memory;
- bypass provenance;
- elevate permissions.

## 14. Memory and knowledge boundary

Agents may produce candidate knowledge and experience.

They do not own the canonical organizational memory.

```text
Agent
 ↓
Observation / Evidence
 ↓
ELO governed intake
 ↓
Knowledge / Memory
```

This allows persistent memory, vector retrieval and RAG to be added later without changing the agent contract.

## 15. Autonomous agents — future-ready design

Autonomous agents are part of the ELO target architecture but must be introduced progressively.

Required controls:

- policy;
- bounded objective;
- tool allowlist;
- action limits;
- budget/time limits;
- audit;
- provenance;
- rollback where applicable;
- human escalation;
- outcome monitoring.

## 16. Learning boundary

An agent may propose lessons or training data candidates.

It may not silently modify production models or governance rules.

```text
Agent
 ↓
Learning Candidate
 ↓
Evaluation
 ↓
Validation
 ↓
Governance
 ↓
Model Registry / Knowledge
```

## 17. Acceptance criteria

- [ ] Agent Contract exists.
- [ ] Capability Registry exists.
- [ ] Autonomy levels exist.
- [ ] Agent Task Contract exists.
- [ ] Observation Contract exists.
- [ ] Tool governance exists.
- [ ] Policy boundary exists.
- [ ] Tenant isolation is tested.
- [ ] Agent identity is tested.
- [ ] Unauthorized tools are rejected.
- [ ] Agent results preserve provenance.
- [ ] Agent observations do not become verified knowledge automatically.
- [ ] Existing ELO-001 and ELO-002 contracts remain authoritative.
- [ ] No second Cognitive Core is introduced.

## 18. Definition of Done

ELO-003 is complete only when the contracts above have executable implementations and deterministic tests covering normal operation, failures, isolation, provenance and policy enforcement.

Documentation alone does not count as implementation maturity.

## 19. Future progression

```text
ELO-003  Governed Agent Ecosystem
    ↓
ELO-004  Reasoning + Evidence Evaluation + Critique
    ↓
ELO-005  Decision Support + Human Dialogue
    ↓
ELO-006  Persistent Retrieval / RAG / Knowledge Graph
    ↓
ELO-007  Governed Autonomous Agents
    ↓
ELO-008  Outcome Learning + MLOps
    ↓
ELO-009  IoT / Enterprise Graph / Digital Twin
```

The numbering is a roadmap and may be revised by the project registry without changing the architectural principles.
