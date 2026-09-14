# Symbiont External Provider Capability Contracts

## Purpose

Define the ELO-owned boundary used by Symbiont to discover, test and evaluate external capabilities without making any external provider an ELO authority.

The contract is provider-neutral. OpenAI, Hermes, GitHub, Supabase, MCP servers and future providers can implement capabilities through the same governed boundary.

## Authority model

```text
ELO Cognitive / Core
        |
        v
     Symbiont
        |
        v
Capability Contract
        |
  +-----+------+-------+------+
  |            |       |      |
OpenAI       Hermes  GitHub  Supabase ...
  |            |       |      |
  +------------+-------+------+
               |
               v
        Evidence / Outcome
               |
               v
         Evolution Gate
               |
               v
          ELO canonical
```

External providers are capability sources/runtimes. They never become canonical ELO authority.

## Provider contract

`ExternalProviderContract` records:

- provider and capability identity;
- protocol (`api`, `mcp`, `sdk`, `local_runtime`);
- lifecycle status;
- purpose and provenance;
- tenant/domain scope;
- read/write/execution boundaries;
- mandatory evidence, provenance and Evolution Gate requirements;
- cost/rate-limit metadata;
- optional fallback provider.

Credentials, tokens, private keys and infrastructure secrets are explicitly forbidden from the contract metadata.

## Probe contract

`ExternalCapabilityProbe` defines the smallest useful experiment. It is read-only and bounded by default, requires success criteria and evidence requirements, and carries the ELO request identity.

A non-read-only or unbounded probe is rejected by the contract rather than silently weakening the default.

## Outcome contract

`ExternalCapabilityOutcome` records observed success/failure, evidence and outcome data. It is descriptive and permanently `candidate_only`.

A provider result cannot directly promote a capability into ELO Core. Promotion remains an Evolution Gate decision.

## Initial provider registry

The first contract records should cover:

| Provider | Capability | Protocol | Initial status | Cost posture |
|---|---|---|---|---|
| Hermes | runtime execution | MCP/HTTP | CONNECTED when runtime is provisioned | local/project runtime |
| OpenAI | optional reasoning | API | NOT_PROVISIONED until explicitly provisioned | metered |
| GitHub | repository operations | API | AVAILABLE/CONNECTED through governed connector | platform-dependent |
| Supabase | database operations | API/SDK | AVAILABLE/CONNECTED through governed connector | platform-dependent |

`NOT_PROVISIONED` is a valid governed state. Defining an OpenAI contract does not create an API key, incur API usage or create a parallel model authority.

## Cost principle

Symbiont must prefer the least-cost viable provider when capability equivalence has been established, but cost never overrides authorization, safety, evidence or governance.

A free provider is not automatically trusted; it must satisfy the same contract and evidence requirements.

## Required lifecycle

```text
DISCOVERED
   -> CONTRACTED
   -> TESTABLE
   -> PROBED
   -> EVIDENCED
   -> CANDIDATE
   -> Evolution Gate
   -> REUSE / ADAPT / LAB_CANDIDATE / BLOCK
```

## Non-goals

- storing credentials;
- bypassing ELO Cognitive authorization;
- direct browser-to-provider execution;
- direct canonical mutation by a provider;
- replacing Hermes or another runtime with the Symbiont;
- creating a second Evolution Gate;
- assuming OpenAI API access is free because ChatGPT access exists;
- automatically promoting an external capability into Core.
