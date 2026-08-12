# ELO Cognitive Platform — Local Agent Rules

## Scope

This directory owns normative design for the ELO cognitive platform. It describes cognitive capabilities and boundaries; executable implementation normally belongs in `src/elo/`.

## Required conceptual boundaries

Preserve separation between:

- Cognitive Core
- Context
- Knowledge
- Memory
- Evidence
- Reasoning
- Recommendation
- Decision
- Provenance
- Agents
- AI Gateway

## Cognitive Core

Treat Cognitive Core as an orchestration boundary. Do not place all cognitive behavior into one monolithic class merely for convenience.

The Core may coordinate specialized services and assemble a governed cognitive flow.

## Cognitive Consulting

The proposed Cognitive Consulting Mode is not yet automatically an implementation requirement.

Its intended conceptual flow is:

Observe
→ Detect
→ Contextualize
→ Identify information gaps
→ Ask
→ Retrieve relevant knowledge
→ Compare experience
→ Form hypotheses
→ Gather evidence
→ Reason
→ Model scenarios
→ Recommend
→ Human decision
→ Outcome
→ Governed learning

Any implementation must preserve evidence, provenance, tenant/domain/policy boundaries, and human decision authority.

## Organizational Health

Do not equate anomaly with incompetence. Analyze person, team, process, system, management, policy, and organizational causes before capability conclusions.

## External knowledge

External scientific, technical, consultant, or web knowledge must retain provenance and applicability context. It is not automatically organizational truth.

## No premature implementation

Do not implement Knowledge Graph, autonomous learning, advanced Decision Engine, autonomous agents, or Digital Twin here unless an approved phase explicitly authorizes it.
