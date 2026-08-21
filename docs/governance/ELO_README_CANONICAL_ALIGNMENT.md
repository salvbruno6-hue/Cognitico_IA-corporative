# ELO README — Canonical Alignment Contract

## Purpose

Define the evidence boundary for the README so that the repository's public operating map evolves with the ELO without turning historical, proposed or contextual information into false canonical facts.

## Authority hierarchy

```text
canonical contracts / structured registries
        ↓
validated implementation + CI evidence
        ↓
governance documents / operating maps
        ↓
historical and contextual references
```

The README is an operating map and orientation document. It is not a substitute for a canonical database, runtime resolver, identity registry, specialist authority or GitHub Ruleset.

## Required distinctions

### Current canonical state

May be stated as fact only when supported by a current canonical source and, where applicable, executable evidence.

### Historical state

Must be labelled as historical/provenance. Historical material must not be silently rewritten as current state.

### Proposed state

Must be labelled as proposal, target, planned, pending or equivalent. Proposal is not implementation.

### Blocked state

Must remain explicitly blocked when an evidence or authorization gate is not satisfied.

### Unknown / no evidence

Must remain unknown or `NO_EVIDENCE`. It must never be promoted to PASS by documentation alone.

## ELO operating model

The README must preserve the following architectural separation:

- **ELO Cognitivo** — defines semantic interpretation, context, evidence, learning and decisions within its authority.
- **ELO Core** — contains the canonical contracts and governed cognitive capabilities.
- **ELO Forge** — is the construction/implementation layer inside the Cognitivo repository; the former external `ELO-Forge` repository is historical/transitional until dependency audit and migration evidence are complete.
- **GitHub** — remains the infrastructure and protected-merge authority.
- **Specialists** — provide domain validation and contextual technical authority; they do not directly promote content into Core.

No README statement should create a second Core, second runtime resolver, second canonical memory or parallel authority.

## Baseline rule

`Baseline v1.0 = NOT DECLARED` until the baseline contract and its evidence gates are formally satisfied.

A README update must not imply baseline maturity merely because individual workflows or PRs pass.

## Knowledge consolidation rule

PT/EN consolidation, folder normalization and legacy cleanup must preserve:

- stable logical identity;
- canonical ownership;
- provenance;
- references and consumers;
- aliases for historical paths where needed;
- actual status of scaffold/discovery/pending families.

In particular, families `05`, `13` and `15` must not be presented as complete merely because their directories or registry entries exist.

## Numeric and technical data rule

Measurements such as `3010 mm` or `13,63 m²` must remain tied to the appropriate structured/versioned source and configuration. The README may orient the reader, but it must not become the sole source of truth for operational numeric data.

## Main protection rule

The current merge model is:

```text
Issue
 ↓
analysis / implementation
 ↓
CI evidence
 ↓
Evolution Gate
 ↓
Pull Request
 ↓
independent approval
 ↓
protected main
 ↓
post-merge validation
```

The ELO must not bypass the repository Ruleset.

## README completion gate

The README PR is `PASS` only when:

1. current statements agree with canonical sources;
2. historical statements are labelled as historical;
3. proposals are labelled as proposals;
4. no unsupported numerical or maturity claim is presented as canonical;
5. ELO Cognitivo/Core/Forge roles remain separated;
6. external Forge retirement is not claimed before dependency evidence;
7. baseline remains correctly represented;
8. the Loop of Conclusion and protected merge model are represented;
9. CI evidence exists for the final HEAD;
10. independent review is obtained.

Until then:

```text
README = ADJUST_REQUIRED
MERGE = BLOCKED
```

## Evolution principle

README evolution is structural and explanatory. It must improve coherence, navigation, traceability and understanding of the ELO without inventing capabilities or replacing canonical authorities.
