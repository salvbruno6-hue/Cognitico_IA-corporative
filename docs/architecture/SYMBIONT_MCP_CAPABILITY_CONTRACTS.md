# Symbiont MCP Capability Contracts

## Purpose

Define the ELO-owned contracts required to discover, test, benchmark and evaluate external capabilities exposed through MCP and executed by Hermes.

**Architectural distinction:** Symbiont is an ELO capability; MCP is an external protocol/mechanism. MCP does not implement, replace or subsume the Symbiont. Hermes may use MCP to invoke external capabilities during an authorized mission.

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

The descriptor is observational. It does not authorize execution, create a Core capability, or alter the Symbiont capability itself.

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

`candidate_only` is mandatory and cannot be disabled. An MCP benchmark therefore cannot directly mutate ELO Core or confer native ELO capability.

## 4. Security and authority invariants

1. MCP servers are external providers.
2. Hermes is an execution runtime, not ELO authority.
3. Symbiont is an ELO capability for observation, interpretation, experimentation, translation and capability absorption.
4. MCP is only an external mechanism/protocol available to Hermes; it is not the Symbiont capability.
5. ELO Cognitive remains responsible for authorization and routing.
6. Evolution Gate remains the only canonical evolution classification boundary.
7. Benchmark evidence must be traceable to the tested capability and request.
8. Infrastructure identifiers and secrets must not cross these contracts.
9. A benchmark result is never canonical knowledge.
10. A high score does not bypass governance.
11. Existing canonical owners must be reused rather than duplicated.
12. Successful use of an MCP tool does not automatically grant an ELO-native capability.
13. Any future ELO-facing MCP option must be introduced as a separate governed capability and must not dismantle or replace the Symbiont boundary.

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

The existing `SymbiontCapabilityAbsorber` remains the absorption boundary. This contract set supplies it with a more rigorous external-capability observation and benchmark trail. MCP remains the access mechanism used during experimentation, not the absorption authority.

## Non-goals

This contract does not:

- install MCP servers;
- store MCP credentials;
- create a second authorization system;
- create a second Evolution Gate;
- allow browser-to-Hermes direct calls;
- automatically promote MCP capabilities;
- copy Hermes internals into ELO Core;
- make an external MCP server a source of canonical truth;
- replace the Symbiont capability with MCP.
