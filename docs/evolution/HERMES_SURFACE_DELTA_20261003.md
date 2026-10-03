# Hermes to ELO - Current Surface Delta 2026-10-03

Status: CANDIDATE-ONLY / CONTROLLED VALIDATION
Hermes mutation: NONE
Business operations during discovery: NONE
SO 001.26: EXCLUDED

Fresh Hermes documentation checked 2026-10-03 shows refinements of existing candidates: Tool Search has tiered progressive disclosure; MCP has capability-aware resources/prompts and opt-in parallel execution; plugin MCP access is default-off and per-server allowlisted with timeouts; external memory is additive to built-in memory with one external provider active; execute_code uses child-process Unix-socket RPC and returns final output only; ACP excludes messaging and cron; prompt caching is documented as a one-hour cross-session prefix cache.

Candidate introductions:
- EXT-TOOL-SEARCH-HERMES: separate discovery, schema loading and invocation; discovery never authorizes.
- EXT-MCP-HERMES: preserve server scope, capability type and concurrency policy as evidence.
- EXT-PLUGIN-CATALOG-HERMES: separate discovery, allowlisting, activation and execution evidence.
- EXT-MEMPROVIDER-HERMES: provider adapter with provenance, never memory authority.
- EXT-CODE-EXEC-HERMES: bounded programmatic orchestration with intermediate-result containment.
- EXT-ACP-HERMES: transport/session boundary, never authorization or workflow authority.
- EXT-PROMPT-CACHE-HERMES: scoped, time-bounded derived context with invalidation.

Validation: the ELO implementation is a deterministic observation registry. It does not execute Hermes, connect to MCP, invoke plugins, use external memory, open ACP sessions, run Hermes code, or execute business operations. Passing tests establish structural candidate integrity only; they do not prove runtime integration or production outcome.

Sources: Hermes Tool Search, MCP, Plugins, Memory Providers, Code Execution, ACP and Features Overview documentation, checked 2026-10-03.