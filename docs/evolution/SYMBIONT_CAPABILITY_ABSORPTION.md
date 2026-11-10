# Symbiont Capability Absorption

## Purpose

The Symbiont is not only an integration connector. It is ELO's governed boundary for observing useful capabilities in external intelligence runtimes, experimenting with them, extracting portable principles, and preparing them for validation as ELO-native capabilities.

Hermes is an external execution runtime and an important source of capabilities. It is not a second ELO Core and does not acquire ELO canonical authority.

## Lifecycle

```text
External AI / Hermes
        |
        v
Capability observation + provenance
        |
        v
Symbiont Pattern Intake
        |
        v
Canonical Evolution Gate
        |
        +---- REUSE / BLOCK / LAB_EXPERIMENT
        |
        +---- COMPATIBLE
                  |
                  v
        Capability Absorption
                  |
                  v
        ELO Capability Candidate
                  |
                  v
        LAB + benchmark + evidence
                  |
                  v
        Governed Learning / Evolution Gate
                  |
                  v
        governed promotion
                  |
                  v
        ELO-native reusable capability
```

## Absorption is not copying

Absorption extracts a portable capability contract rather than copying a provider's implementation. A candidate records:

- purpose;
- portable mechanism/principle;
- interface contract;
- validation contract;
- source and source commit;
- evidence;
- provider provenance;
- tenant/domain scope.

The candidate is non-canonical until the existing learning and evolution governance permits promotion.

## Authority boundaries

- **ELO Cognitive/Core:** canonical reasoning, knowledge and governance.
- **Symbiont:** observation, translation, experimentation and capability absorption boundary.
- **Hermes:** external execution/orchestration runtime.
- **Governed Learning:** canonical learning lifecycle.
- **Evolution Gate:** canonical evolution classification.

No Symbiont capability absorption may write directly to Core, bypass evidence, create a second memory authority, create a second Evolution Gate, or promote automatically.

## Strategic outcome

The intended trajectory is progressive capability independence:

```text
ELO -> Symbiont -> Hermes/other AI -> capability
             |
             v
      validated capability
             |
             v
ELO -> native reusable capability
```

External runtimes remain available for capabilities ELO has not yet absorbed. Validated capabilities can become ELO-native so the system is progressively less dependent on any single external runtime while retaining external intelligence as a source of new capability.


## External engineering-skills observation — Matt Pocock (2026-11-10)

Source: [mattpocock/skills](https://github.com/mattpocock/skills), commit `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`.
This is provenance for **portable patterns**, not an installed external runtime or a new canonical authority.

| External SKILL.md | ELO existing owner | Governed disposition |
|---|---|---|
| `skills/engineering/code-review/SKILL.md` | `src/elo/agent_intake/independent_review.py` | Adapt standards-versus-spec separation as an advisory two-axis assessment; both independent reviews must pass |
| `skills/engineering/diagnosing-bugs/SKILL.md` | existing tests, Hermes implementation loop, Symbiont evidence | Research candidate: require an executable red-capable failure signal before causal claims; no automatic execution |
| `skills/engineering/tdd/SKILL.md` | current test and Evolution Gate pipeline | Reuse existing test stages, do not install a competing runner or redefine the gate |
| `skills/engineering/domain-modeling/SKILL.md` | ELO Cognitivo domain canon, Skill PCP, governed Forge | Candidate: disambiguate terms and stress-test edge cases without replacing canonical glossary/ADR conventions |
| `skills/engineering/improve-codebase-architecture/SKILL.md` | existing Symbiont capability observation and architecture audit | Candidate-only architecture observations; no autonomous refactor or authority transfer |
| `skills/engineering/retro/SKILL.md` | Forge / governed learning | Candidate-only post-execution improvement hypotheses; require traceable evidence and gate |

### Two-axis review behavior

* `STANDARDS`: compare implementation against existing repository contracts, invariants and documented standards.
* `SPEC`: compare behavior with the originating task and acceptance criteria.
* Each axis uses `IndependentReviewEvidence`: named author/reviewer, isolated context snapshot, subject, evidence and provenance.
* A single `FAIL` yields `REVIEW_FAILED`; missing/invalid/abstaining axis yields `REVIEW_INCOMPLETE`; both `PASS` require different reviewer IDs and context snapshots to yield advisory `REVIEW_PASSED`.
* `REVIEW_PASSED` **does not authorize** merge, Core promotion, production writes or rule mutation. All canonical guards, human boundaries and Evolution Gate remain unchanged.
* This observation does not install the upstream skills wholesale; the source files remain available for future bounded lab evaluations, with source commit recorded. No provider code is executed.

### PCP-specific safety regression targets

Do not interpret structural capacity as finished-module capacity; do not convert six-module recovery throughput into the ordinary nominal baseline; do not use 120-M01 purchase scenarios as 300-module real demand; do not infer BOM, supply, staffing or elapsed lead time from a name or a registered table alone.
