# ELO-004 to ELO-006 — Reasoning, Decision Support and Cognitive Consulting

## Objective
Implement stages 4, 5 and 6 as governed capabilities layered on the existing ELO-001, ELO-002 and ELO-003 contracts.

## Stage 4 — Reasoning + Evidence Evaluation + Critique
- distinguish fact, observation, inference, hypothesis, recommendation, decision and unknown;
- evaluate evidence polarity, quality and relevance;
- represent hypotheses explicitly;
- retain contradictory evidence;
- critique claims through alternatives and missing information;
- never promote a hypothesis to a fact implicitly;
- never infer causation from correlation alone.

### Acceptance
- [ ] evidence evaluation contract;
- [ ] hypothesis contract;
- [ ] critique contract;
- [ ] confidence remains bounded 0..1;
- [ ] contradictions preserved;
- [ ] missing information represented;
- [ ] tests cover support and contradiction.

## Stage 5 — Decision Support + Human Dialogue
- represent scenarios;
- preserve alternatives;
- record recommendation separately from decision;
- identify decision owner;
- preserve evidence references;
- preserve risks;
- prepare questions to close information gaps.

### Acceptance
- [ ] scenario contract;
- [ ] decision support contract;
- [ ] human owner required for governed decisions;
- [ ] recommendation != decision;
- [ ] evidence and risks traceable;
- [ ] deterministic tests.

## Stage 6 — Cognitive Consulting + Organizational Health
- enter consulting mode for multi-domain/ambiguous/high-impact situations;
- preserve known and unknown information;
- create hypotheses and information gaps;
- produce recommendations with risks;
- identify capability/process/knowledge gaps in later extensions;
- avoid automatic blame or competence labeling.

### Acceptance
- [ ] consulting assessment contract;
- [ ] known/unknown distinction;
- [ ] information gap contract;
- [ ] hypothesis support;
- [ ] recommendations separate from decisions;
- [ ] risks preserved;
- [ ] tests cover unknowns and gaps.

## Architectural constraints
- no second Cognitive Core;
- no uncontrolled autonomous execution;
- ELO-002 remains authoritative for Knowledge, Evidence and Memory;
- ELO-003 remains authoritative for Agent identity, policy and autonomy;
- persistence, RAG, model training and production integrations remain adapters/future stages unless explicitly implemented by a later gate.

## Verification
The branch must pass the existing CI compile/test workflow and the full regression suite before merge.
