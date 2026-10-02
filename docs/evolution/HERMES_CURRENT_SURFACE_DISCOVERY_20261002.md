# Hermes → ELO — Current Surface Discovery — 2026-10-02

**Status:** discovery + controlled validation only
**Hermes:** reference-only; not modified
**SO 001.26:** excluded from architectural evidence
**Business operations:** none executed during discovery

## 1. Current source observations

The current public Hermes documentation exposes a broader, more explicit extension surface than the earlier 2026-09 snapshots.

### Relevant current changes

| Mechanism | Current observation | Candidate ELO introduction |
|---|---|---|
| Tool Search | Deferred MCP/plugin tools and optionally named built-ins are represented through tool_search, tool_describe, tool_call; connector discovery can be remote. | Preserve progressive disclosure as a routing capability, not an execution authority. |
| MCP | stdio/HTTP servers, startup discovery, per-server filtering, connector-backed discovery. | Keep MCP behind ELO External Capability Gateway with server/tool allowlists and untrusted-result treatment. |
| Plugin catalog | General, memory-provider, context-engine and model-provider surfaces; install/update security scanning; explicit activation for general plugins. | Separate discovery, trust, activation and runtime execution metadata. |
| Memory providers | Eight external providers are currently documented; one external provider may be active while built-in memory remains additive. | Preserve ELO Memory as authority; provider identity/scope/provenance remain adapter metadata. |
| Code execution | execute_code uses a child process and RPC to call Hermes tools; intermediate results do not enter model context. | Treat programmatic orchestration as a bounded execution request behind ELO authorization and side-effect classification. |
| API server | OpenAI-compatible chat/responses plus runs/events, jobs, capability discovery, idempotency keys and session-key correlation. | Model API as an authenticated external boundary with explicit identity, idempotency and read-only discovery contracts. |
| ACP | Curated editor toolset includes terminal, code execution and delegation while excluding cron/messaging; MCP can be host/session scoped. | Treat ACP as a transport/session boundary; never infer authorization from host connectivity. |

## 2. Candidate introduction registry

All mechanisms remain candidate-only unless separately validated by the existing ELO implementation/Evolution Gate chain.

| Candidate | Hermes mechanism | Existing ELO owner | Introduction |
|---|---|---|---|
| EXT-CONTEXTREF-HERMES | context references | ELO Context | provenance-bounded reference resolution |
| EXT-CHECKPOINT-HERMES | checkpoints/rollback | ELO State Recovery | pre-mutation checkpoint contract |
| EXT-HOOK-HERMES | lifecycle hooks | ELO Workflow/Automation | lifecycle evidence/guardrail hooks |
| EXT-ROUTE-HERMES | routing/fallback/credential pools | ELO Model/Tool Routing | policy-bounded failover |
| EXT-PROFILE-HERMES | profiles/Bot Mode | ELO Agent Context & Delegation | isolated agent-context profiles |
| EXT-BATCH-HERMES | batch processing | ELO Evaluation & Learning | bounded evaluation intake |
| EXT-MEMPROVIDER-HERMES | external memory providers | ELO Memory | adapter-only provider integration |
| EXT-LEARN-HERMES | /learn / skill learning | ELO Knowledge & Skills | governed skill synthesis/admission |
| EXT-LEARNING-GRAPH-HERMES | learning graph/curator | ELO Evolution Memory | evidence-linked relations |
| EXT-CONTEXT-PLUGIN-HERMES | context-engine plugins | ELO Context | bounded context-engine adapter |
| EXT-WORKTREE-HERMES | isolated worktrees | ELO Forge | isolated technical workspace |
| EXT-MULTIAGENT-HERMES | subagent delegation | ELO Agent Delegation | bounded delegated execution |
| EXT-CRON-HERMES | scheduled tasks | ELO Workflow/Automation | governed deterministic scheduling |
| EXT-MCP-HERMES | external MCP capabilities | ELO External Capability Gateway | allowlisted external capabilities |
| EXT-TOOL-SEARCH-HERMES | progressive tool disclosure | ELO Model/Tool Routing | bounded capability discovery |
| EXT-CODE-EXEC-HERMES | programmatic tool calling | ELO Model/Tool Routing | bounded programmatic orchestration |
| EXT-API-HERMES | OpenAI-compatible API | ELO External Capability Gateway | authenticated API boundary |
| EXT-ACP-HERMES | Agent Client Protocol | ELO Agent Context & Delegation | isolated client/session boundary |
| EXT-PLUGIN-CATALOG-HERMES | plugin discovery | ELO External Capability Gateway | discover-before-activate |
| EXT-PROMPT-CACHE-HERMES | cross-session prompt caching | ELO Model/Tool Routing | bounded cache scope/invalidation |

## 3. Structural interpretation

The discovery spans the requested dimensions:

- Structure/interfaces: plugin manifests, API, ACP, MCP descriptors, tool schemas.
- Metadata: identity, provider/model, session/run identifiers, idempotency keys, provenance.
- Dependencies: MCP servers, plugin catalog, RPC sandbox, provider backends, external gateways.
- Relations: skills ↔ tools, context ↔ memory, delegation ↔ agent context, API ↔ automation, MCP ↔ external capability gateway.
- Skills: progressive disclosure and discoverable skill metadata.
- Tools: built-ins, plugin tools, MCP tools, deferred tools.
- Automations/workflows: cron, hooks, jobs API, runs/events.
- Memory: built-in memory plus one active external provider.
- Context: context files, context references, context engines, prompt-cache scope.
- Connections: MCP, API, ACP, provider routing, connector gateway.
- Agents: profiles, delegation, ACP sessions, bounded child execution.

## 4. Controlled validation boundary

The repository already contains native ELO candidate contracts and deterministic tests for the newly observed surfaces. This update adds only source-observation metadata and tests that ensure those observations:

1. remain mapped to existing ELO candidates;
2. carry explicit dependencies, relations and safety boundaries;
3. remain SOURCE_OBSERVED_CANDIDATE_ONLY;
4. do not become an authority or promotion mechanism.

No Hermes runtime is imported by this discovery layer. No external Hermes server, MCP server, API endpoint, memory provider, plugin, ACP host or business system is invoked.

## 5. What is validated vs. not validated

Validated in this cycle: the ELO-side discovery metadata contract and its deterministic tests.

Not validated: that the current Hermes mechanisms produce an operational outcome in production.

A source observation, native contract test, or controlled fixture does not establish production proof.

For already implemented ELO candidates, existing runtime integrations and evidence paths remain governed by their respective canonical owners. This discovery does not reopen or duplicate those authorities.

## 6. Sources

- Hermes Features Overview: https://hermes-agent.nousresearch.com/docs/user-guide/features/overview
- Hermes Tools & Toolsets: https://hermes-agent.nousresearch.com/docs/user-guide/features/tools
- Hermes Tool Search: https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-search
- Hermes MCP: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- Hermes Plugins: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
- Hermes Memory: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- Hermes Memory Providers: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers
- Hermes Code Execution: https://hermes-agent.nousresearch.com/docs/user-guide/features/code-execution
- Hermes API Server: https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server
- Hermes ACP: https://hermes-agent.nousresearch.com/docs/user-guide/features/acp

## Decision

The current discovery is VALID as ELO candidate evidence only.

No candidate is promoted, no Hermes source is changed, and no production capability is claimed.