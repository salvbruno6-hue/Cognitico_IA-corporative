# ELO Forge Constructor Contract

## 1. Authority model

The canonical ELO architecture is the source of truth.

Forge has execution authority inside its construction boundary, but **no canonical authority**. A Forge change becomes part of ELO only after validation and promotion.

## 2. Construction loop

```text
OBJECTIVE
  ↓
READ CANONICAL CONSTRAINTS
  ↓
PLAN
  ↓
BUILD
  ↓
TEST
  ↓
COMPARE AGAINST CANONICAL
  ↓
DETECT DIVERGENCE
  ↓
ADJUST
  ↓
VALIDATE
  ↓
PROMOTE
```

The loop may repeat until the result is compatible or the candidate is explicitly rejected.

## 3. Divergence handling

Divergence is treated as a first-class engineering event.

### Compatible
The implementation satisfies the canonical contract.

**Action:** promote after validation.

### Compatible after adjustment
The implementation initially differs but can be brought into compliance without weakening the canonical architecture.

**Action:** Forge adjusts and revalidates.

### Canonical improvement candidate
The implementation exposes a measurable improvement to the canonical architecture.

**Action:** create an architectural decision candidate. Do not silently alter the canonical source.

### Incompatible
The implementation conflicts with a non-negotiable canonical rule, security constraint or governance decision.

**Action:** reject, isolate, or redesign.

## 4. Promotion contract

Every promoted construction should identify:

- objective;
- canonical constraint(s);
- files/components affected;
- tests performed;
- evidence of compatibility;
- divergences found;
- corrections applied;
- rollback path;
- final decision.

## 5. External architecture assimilation

Forge may prototype capabilities extracted from external projects, open-source repositories or other AI systems.

The sequence is:

```text
EXTERNAL IDEA
    ↓
FORGE EXPERIMENT
    ↓
MEASURE
    ↓
CANONICAL COMPARISON
    ↓
PROMOTION CANDIDATE
```

The external project never becomes an implicit architectural authority.

## 6. Autonomous construction

Forge may execute bounded construction tasks without continuous user intervention when the task has:

- an explicit objective;
- a known canonical boundary;
- reversible changes;
- validation criteria;
- a promotion path.

If a construction requires changing a non-negotiable canonical rule, Forge must create a decision candidate rather than silently changing the rule.

## 7. Separation from operational legacy

This contract intentionally does not promote legacy SQL, migrations, operational data, or implementation details from the former standalone Forge repository. Such artifacts remain outside the cognitive promotion path unless a future explicit decision establishes their canonical relevance.
