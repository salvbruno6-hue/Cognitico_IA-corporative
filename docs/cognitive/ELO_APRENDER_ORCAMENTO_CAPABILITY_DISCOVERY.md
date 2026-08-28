# ELO APRENDER — Budget Learning Capability Discovery

## Purpose

When `ELO APRENDER` is triggered for solicitation/budget learning, ELO must discover the knowledge already acquired before interpreting a new experience. The objective is to produce a capability report: what ELO can currently provide in future budget analyses, which evidence supports each capability, and which parts remain consultative or require validation.

## Canonical ownership

- **Git / Knowledge Handbook:** semantic, conceptual, instructional and governance knowledge; provenance of solicitation learning; examples, precedents, validated learning and interpretation parameters.
- **Supabase:** consultative structured memory and calculation-related records. Calculation evidence is retrieved for ELO interpretation; Supabase does not become the cognitive authority.
- **ELO:** reads both sources, reconciles them, evaluates applicability, avoids duplication, classifies knowledge and decides what can be offered to the budgeting specialist.

## ELO APRENDER discovery sequence

`TRIGGER → LOCATE ACQUIRED KNOWLEDGE → READ LEARNING ARTIFACTS → QUERY CONSULTATIVE CALCULATION MEMORY → RECONSTRUCT CAPABILITIES → DEDUPLICATE → CLASSIFY → PRODUCE CAPABILITY REPORT → GOVERNED COMMIT WHEN APPLICABLE`

The automation must not infer that a file or database record is a rule merely because it exists.

## Where ELO must look

### Git semantic/knowledge sources

At minimum inspect:

- `04-knowledge-handbook/`
- `memory/solicitations/`
- `memory/solicitations_learning/`
- `memory/evolution/`
- `00-core/ELO_DIRETRIZ_MESTRA_ESPECIALISTA_ORCAMENTO.md`
- `08-ai/ELO/ESPECIALISTAS/ORCAMENTO/PROMPT.md`
- relevant cognitive learning/governance contracts and solicitation-learning artifacts.

The exact canonical owner found during inspection takes precedence over creating a parallel location.

### Supabase consultative sources

When the capability depends on calculations, query the existing calculation-memory structures and related solicitation evidence. Return the evidence to ELO with provenance. Do not silently copy a calculation from another SO into the current SO.

## Capability extraction

For each material learning artifact, ELO should derive, where evidence permits:

- capability name;
- budgeting question it can answer;
- domain/family/model/product involved;
- applicable scenario;
- source SO/document;
- source type (`CASE`, `PRECEDENT`, `VALIDATED_LEARNING`, `CONCEPTUAL_KNOWLEDGE`, `INSTRUCTIONAL_KNOWLEDGE`, `RULE`);
- evidence and recurrence;
- calculation-memory references when applicable;
- applicability rationale;
- limitations/validation required;
- confidence/status.

## Reference provenance rule

Knowledge from another SO is a consultative reference, not the origin of the current solicitation. ELO must state:

`SOURCE → ORIGINAL CONTEXT → RECOVERED INFORMATION → WHY FOUND → WHY IT MAY APPLY → ASSUMPTIONS/EQUIVALENCE → VALIDATION PENDING → STATUS`

ELO may recommend applicability when evidence supports it, including recency, product identity, technical characteristics, color, thickness, unit, price/m² and commercial conditions. It must not present the reference as belonging to the current SO without evidence.

## Capability report

The automated learning cycle must generate a concise report for ELO containing:

1. new capabilities discovered;
2. capabilities strengthened by new evidence;
3. already validated capabilities reused;
4. calculation capabilities available through Supabase;
5. recurring patterns and precedents;
6. limitations and validation requirements;
7. duplicates avoided;
8. source/provenance for every material capability.

This report is an input to ELO reasoning. It is not itself authorization to promote learning.

## Budget calculation representation

Whenever a calculation is reported, preserve:

`entrada → fonte → premissa → fórmula → subcálculo → resultado → validação`

## Governance

- Existing `VALIDATED_LEARNING` is enriched, not duplicated.
- `PRECEDENT` is not automatically promoted to `RULE`.
- Conceptual and instructional knowledge may be useful without becoming operational rules.
- A capability report must distinguish what ELO **can provide as a reference** from what ELO **may decide automatically**.
- If source material is inaccessible, report `FONTE NÃO ACESSÍVEL`; never invent or simulate evidence.
- The automation is a process adapter. ELO remains the cognitive orchestrator.
