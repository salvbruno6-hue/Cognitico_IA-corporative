# Symbiont MCP Capability Contracts

## Purpose

Define the ELO-owned contracts required to discover, test, benchmark and evaluate external capabilities exposed through MCP and executed by Hermes.

MCP is an external integration protocol. Hermes remains an external execution runtime. Neither acquires canonical ELO authority.

## Contract chain

```text
External MCP capability
        |
        v
MCPCapabilityDescriptor
        |
        v
Symbiont discovery / compatibility analysis
        |
        v
MCPCapabilityTestCase
        |
        v
ELO Cognitive authorization
        |
        v
HermesExecutionRequest
        |
        v
Hermes -> MCP tool
        |
        v
MCPCapabilityBenchmarkResult
        |
        +--> Evidence / Outcome
        |
        v
Existing Evolution Gate
        |
        +--> REUSE
        +--> ADAPT
        +--> LAB_CANDIDATE
        +--> BLOCK
```

## 1. Discovery contract

`MCPCapabilityDescriptor` records what an external MCP capability is and where it came from.

Required identity:

- `capability_id`
- `server_id`
- `provider`
- `tool_name`
- `tenant_id`
- `domain`

Required understanding:

- purpose
- mechanism
- interface contract

Required provenance:

- `source_ref`
- `source_commit`

The descriptor is observational. It does not authorize execution or create a Core capability.

## 2. Benchmark contract

`MCPCapabilityTestCase` defines a controlled experiment.

Every test must specify:

- objective;
- task;
- controlled input;
- explicit success criteria;
- required evidence;
- constraints;
- maximum tool calls.

Tests are non-destructive by default. A test that cannot be made non-destructive requires an explicit architectural/security review rather than silently changing the default.

The test is executed through the existing ELO Cognitive -> Symbiont -> Hermes governed bridge. The test contract does not bypass authorization.

## 3. Evidence/outcome contract

`MCPCapabilityBenchmarkResult` records the observed result.

It requires:

- original `test_id` and `capability_id`;
- original `request_id`;
- tenant scope;
- disposition;
- task-success, reliability, quality and latency scores;
- evidence IDs;
- outcome.

The aggregate score is descriptive only. It is not a promotion decision.

`candidate_only` is mandatory and cannot be disabled. An MCP benchmark therefore cannot directly mutate ELO Core.

## 4. Security and authority invariants

1. MCP servers are external providers.
2. Hermes is an execution runtime, not ELO authority.
3. Symbiont observes, translates, experiments and prepares candidates; it does not promote them.
4. ELO Cognitive remains responsible for authorization and routing.
5. Evolution Gate remains the only canonical evolution classification boundary.
6. Benchmark evidence must be traceable to the tested capability and request.
7. Infrastructure identifiers and secrets must not cross these contracts.
8. A benchmark result is never canonical knowledge.
9. A high score does not bypass governance.
10. Existing canonical owners must be reused rather than duplicated.

## 5. Initial benchmark families

The first proof set should use representative external capabilities rather than a large MCP catalog:

### Google Sheets

Test reading controlled data, structured extraction, a bounded write operation if approved, and preservation of source integrity.

### Browser / web

Test navigation, extraction and a controlled validation task. Browser actions must remain within the authorization and safety constraints of the mission.

### YouTube

Test search, metadata extraction and transcript retrieval where the selected MCP exposes those operations.

These are benchmark targets, not yet canonical ELO integrations.

## 6. Promotion boundary

The lifecycle is:

```text
DISCOVERED
   -> TESTABLE
   -> TESTED
   -> CANDIDATE
   -> Evolution Gate
   -> governed promotion or rejection
```

`CANDIDATE` means that evidence supports further laboratory work. It does not mean that the capability has entered Core.

The existing `SymbiontCapabilityAbsorber` remains the absorption boundary. This contract set supplies it with a more rigorous external-capability observation and benchmark trail.

## Non-goals

This contract does not:

- install MCP servers;
- store MCP credentials;
- create a second authorization system;
- create a second Evolution Gate;
- allow browser-to-Hermes direct calls;
- automatically promote MCP capabilities;
- copy Hermes internals into ELO Core;
- make an external MCP server a source of canonical truth.
