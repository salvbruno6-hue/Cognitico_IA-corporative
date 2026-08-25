# ELO README — Canonical Alignment Contract

## Purpose

Define the evidence boundary for the README so the repository operating map evolves with the ELO without turning historical, proposed or contextual information into false canonical facts.

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

Must be labelled as proposal, target, planned or pending. Proposal is not implementation.

### Blocked state

Must remain explicitly blocked when an evidence or authorization gate is not satisfied.

### Unknown / no evidence

Must remain unknown or `NO_EVIDENCE`. Documentation alone cannot promote it to PASS.

## ELO operating model

The README must preserve the following architectural separation:

- **ELO Cognitivo** — semantic interpretation, context, evidence, learning and decisions within its authority.
- **ELO Core** — canonical contracts and governed cognitive capabilities.
- **ELO Forge** — construction/implementation layer; historical external Forge references remain transitional until dependency evidence is complete.
- **GitHub** — infrastructure and protected-merge authority.
- **Specialists** — domain validation and contextual technical authority; they do not directly promote content into Core.

No README statement may create a second Core, second runtime resolver, second canonical memory or parallel authority.

## Baseline rule

`Baseline v1.0 = NOT DECLARED` until the baseline contract and evidence gates are formally satisfied.

Passing individual workflows does not by itself declare baseline maturity.

## Knowledge consolidation rule

PT/EN consolidation, folder normalization and legacy cleanup must preserve:

- stable logical identity;
- canonical ownership;
- provenance;
- references and consumers;
- aliases for historical paths where needed;
- actual status of scaffold/discovery/pending families.

Families `05`, `13` and `15` must not be presented as complete merely because directories or registry entries exist.

## Numeric and technical data rule

Measurements such as `3010 mm` or `13,63 m²` must remain tied to the appropriate structured/versioned source and configuration. The README may orient the reader but must not become the sole source of truth for operational numeric data.

## Protected merge model

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
independent approval when required
 ↓
protected main
 ↓
post-merge validation
```

The ELO must not bypass the repository Ruleset.

## README completion gate

The README update is complete only when:

1. current statements agree with canonical sources;
2. historical statements are labelled as historical;
3. proposals are labelled as proposals;
4. unsupported numerical or maturity claims are not presented as canonical;
5. ELO Cognitivo/Core/Forge roles remain separated;
6. external Forge retirement is not claimed before dependency evidence;
7. baseline remains correctly represented;
8. the Loop of Conclusion and protected merge model are represented;
9. CI evidence exists for the final HEAD;
10. required independent review is obtained.

Until then:

```text
README = ADJUST_REQUIRED
MERGE = BLOCKED
```

## Evolution principle

README evolution is structural and explanatory. It must improve coherence, navigation, traceability and understanding of the ELO without inventing capabilities or replacing canonical authorities.
