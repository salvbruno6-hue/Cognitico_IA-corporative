"""Current Hermes surface deltas observed on 2026-10-03."""
from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class HermesSurfaceDelta:
    candidate_id: str
    observation: str
    candidate_introduction: str
    dependencies: tuple[str, ...]
    relations: tuple[str, ...]
    safety_invariants: tuple[str, ...]
    status: str = "CANDIDATE_ONLY"
CURRENT_SURFACE_DELTAS = (
HermesSurfaceDelta("EXT-TOOL-SEARCH-HERMES","progressive disclosure via search/describe/call","separate discovery, schema loading and invocation",("tool-search-bridge","mcp","plugin-catalog"),("model-tool-routing","capability-discovery"),("discovery_not_authorization","invocation_requires_existing_governance")),
HermesSurfaceDelta("EXT-MCP-HERMES","capability-aware resources/prompts and opt-in per-server parallelism","carry server scope, capability type and concurrency policy as evidence metadata",("mcp-server","external-capability-gateway"),("tools","resources","prompts","sampling"),("untrusted_result_is_data","parallelism_must_be_explicit","no_authority_transfer")),
HermesSurfaceDelta("EXT-PLUGIN-CATALOG-HERMES","default-off per-server MCP allowlist, timeout and untrusted-result semantics","separate discovery, allowlisting, activation and execution evidence",("plugin-registry","external-capability-gateway"),("skills","tools","hooks"),("allowlist_required","timeout_required","discovery_not_authorization")),
HermesSurfaceDelta("EXT-MEMPROVIDER-HERMES","one active external provider while built-in memory remains active","treat providers as scoped adapters with explicit provider provenance",("memory","provider-adapter"),("context","session-search"),("provider_not_authority","provenance_preserved","scope_explicit")),
HermesSurfaceDelta("EXT-CODE-EXEC-HERMES","child-process Unix-socket RPC and final-output-only return to model context","bound programmatic orchestration and contain intermediate results",("tool-registry","execution-boundary"),("tool-routing","evidence"),("explicit-authorization","bounded-scope","no-business-side-effects")),
HermesSurfaceDelta("EXT-ACP-HERMES","curated editor toolset excludes messaging delivery and cron management","treat ACP as transport/session boundary, not authorization or workflow authority",("agent-context","external-connection"),("delegation","skills","tools","memory"),("identity_preserved","session_isolated","no_authority_transfer")),
HermesSurfaceDelta("EXT-PROMPT-CACHE-HERMES","one-hour cross-session prefix cache for supported providers","treat cached context as scoped, time-bounded derived state",("model-runtime","context"),("memory","tool-routing"),("tenant_isolated","scope_explicit","stale_data_bounded")),
)
def candidate_ids(): return tuple(x.candidate_id for x in CURRENT_SURFACE_DELTAS)
