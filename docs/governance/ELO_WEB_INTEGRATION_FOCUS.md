# ELO Web — Integrated Development Focus

## Purpose

Establish the ELO Web as the primary integration surface for the current development cycle.

The objective is not to move authority into the Web layer. The objective is to make the Web the coherent product surface through which the governed ELO architecture is exercised end to end.

## Canonical architecture

```text
User / Browser
      |
      v
ELO Web
      |
      v
ELO Cognitive API
      |
      +--> Cognitive/Core governed services
      |
      v
Simbionte
      |
      v
Hermes execution boundary
      |
      v
Evidence / Outcome
      |
      v
Governed Learning / Evolution Gate
      |
      v
Canonical ELO knowledge
```

Supabase remains the governed persistence layer. GitHub remains the canonical source for implementation. Hermes remains an external execution runtime. Symbionte remains the integration, observation, experimentation, translation and capability-absorption boundary.

## Development priority

All new work should be evaluated in this order:

1. ELO Web build and deployment determinism.
2. Existing authentication/session boundary.
3. ELO Web → ELO Cognitive server boundary.
4. Cognitive-backed workspace and ProcessView integration.
5. Evidence, provenance and CURRENT/DEVIATION/UNKNOWN presentation.
6. Cognitive → Symbionte integration.
7. Governed Symbionte → Hermes execution.
8. Evidence/Outcome → Governed Learning → Evolution Gate.
9. External capabilities through Hermes, including MCP, only after the integrated path is functional.
10. Legacy frontend removal only after production and end-to-end gates pass.

## Non-negotiable boundaries

- Browser does not call Hermes directly.
- Browser does not own canonical knowledge, governance, credentials or Evolution Gate decisions.
- ELO Web does not create a second Cognitive Core.
- ELO Web does not create a second authentication authority.
- Symbionte does not become canonical authority.
- Hermes does not become Core, Memory, Router or Evolution Gate.
- MCP does not replace Symbionte; MCP is an external mechanism that Hermes may use.
- External capability success does not imply automatic ELO promotion.
- No telemetry, KPI, CURRENT state or causal claim is fabricated when governed data is unavailable.

## Integration rule for new work

Before creating or changing a component, identify:

- canonical owner;
- existing implementation to reuse;
- ELO Web integration point;
- upstream/downstream contract;
- evidence and provenance requirements;
- tenant/authentication boundary;
- Evolution Gate implications;
- regression coverage.

If the capability cannot yet be integrated through the governed path, register the GAP rather than creating a parallel implementation.

## Current workstream model

The repositories and PRs for Cognitive, Symbionte, Hermes, MCP and ELO Web are treated as one integration program. Work may remain in separate repositories or PRs when ownership requires it, but every change must have a defined place in the ELO Web end-to-end path.

### ELO Web is the acceptance surface

A backend or connector change is not considered integrated merely because its unit tests pass. When applicable, the final acceptance path is:

```text
implementation
  -> governed contract
  -> CI/evidence
  -> ELO Web integration
  -> authenticated request
  -> Cognitive
  -> Symbionte
  -> Hermes (when authorized)
  -> Evidence/Outcome
  -> Evolution Gate
```

## Vercel rule

The Vercel incident is handled from observed deployment evidence. Repository changes must not claim a root cause that has not been demonstrated by build logs or project configuration.

The ELO Web Vercel project must use `apps/elo-web` as its root and keep server-only cognitive/Hermes configuration outside public browser variables.

## Definition of integrated

ELO Web is considered integrated when the following are demonstrably true:

- production deployment comes from canonical `main`;
- authentication uses the existing governed identity/session path;
- browser requests terminate at the ELO Cognitive server boundary;
- Cognitive can return governed responses with provenance/evidence;
- ProcessView uses a Cognitive-owned provider when real operational state is required;
- authorized execution can traverse Symbionte to Hermes without bypassing governance;
- evidence/outcome reaches the existing governed learning path;
- Evolution Gate remains the only evolution authority;
- no parallel authority or secret-bearing browser path exists;
- legacy frontend removal is performed only after these conditions are validated.
