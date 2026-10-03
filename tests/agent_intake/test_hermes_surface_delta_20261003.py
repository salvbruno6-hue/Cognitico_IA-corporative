from src.elo.agent_intake.hermes_surface_delta_20261003 import CURRENT_SURFACE_DELTAS,candidate_ids
EXPECTED={"EXT-TOOL-SEARCH-HERMES","EXT-MCP-HERMES","EXT-PLUGIN-CATALOG-HERMES","EXT-MEMPROVIDER-HERMES","EXT-CODE-EXEC-HERMES","EXT-ACP-HERMES","EXT-PROMPT-CACHE-HERMES"}
def test_registry_complete_unique():
    ids=candidate_ids(); assert set(ids)==EXPECTED; assert len(ids)==len(EXPECTED)
def test_each_delta_has_introduction_dependencies_relations_and_safety():
    for x in CURRENT_SURFACE_DELTAS:
        assert x.status=="CANDIDATE_ONLY" and x.candidate_introduction and x.dependencies and x.relations and x.safety_invariants
def test_no_promotion_or_business_execution():
    for x in CURRENT_SURFACE_DELTAS: assert x.status!="PROMOTED"
