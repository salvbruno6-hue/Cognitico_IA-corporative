from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE = (ROOT / 'apps/elo-web/src/lib/elo-cognitive-core.ts').read_text(encoding='utf-8')
WRAPPER = (ROOT / 'apps/elo-web/src/lib/elo-cognitive.ts').read_text(encoding='utf-8')
ROUTE = (ROOT / 'apps/elo-web/src/app/api/cognitive/route.ts').read_text(encoding='utf-8')
PCP = (ROOT / 'apps/elo-web/src/lib/elo-pcp-governed-response.ts').read_text(encoding='utf-8')
WORKFLOW = (ROOT / '.github/workflows/elo-behavioral-validation.yml').read_text(encoding='utf-8')


def test_web_default_path_no_longer_echoes_user_message_as_validated_answer():
    assert 'response: { type: "analysis", content: input.message }' not in CORE
    assert 'validation_status: "validated"' not in CORE
    assert 'processGovernedPcpMission' in CORE
    assert 'unverifiedDomainResult(input.domain)' in CORE


def test_verified_bearer_stays_server_side_and_is_forwarded_only_to_governed_reader():
    assert 'supabase.auth.getUser(accessToken)' in ROUTE
    assert 'accessToken,' in ROUTE
    assert 'accessToken: input.accessToken' in WRAPPER
    assert 'Authorization: `Bearer ${accessToken}`' in PCP
    assert 'params: { name, arguments: args }' in PCP
    assert 'service_role' not in PCP.lower()


def test_pcp_lane_uses_only_existing_specific_governed_tools():
    for tool in (
        'elo_pcp_dados_pendentes',
        'elo_pcp_indicadores_status',
        'elo_pcp_decisao_externa_status',
    ):
        assert tool in PCP
    assert 'invokeTool("elo_read"' not in PCP
    assert '.slice(0, 5)' in PCP
    assert 'HUMAN_EVIDENCE_CANDIDATE' in PCP
    assert 'CURRENT_DECISION_CONTEXT_ONLY' in PCP
    assert 'canonical_mutation: false' in PCP
    assert 'must_not_infer: true' in PCP


def test_sources_and_admin_questions_reach_cognitive_response_contract():
    assert 'sources: result.sources ?? []' in WRAPPER
    assert 'suggestions: result.suggestions ?? []' in WRAPPER
    assert 'sources?: GovernedSource[]' in CORE
    assert 'suggestions?: GovernedSuggestion[]' in CORE


def test_web_behavioral_gate_runs_oauth_and_governed_response_tests():
    assert 'node --test apps/elo-web/tests/*.test.mjs' in WORKFLOW


def test_hermes_probe_path_remains_evidence_validated_only_for_real_execution():
    assert 'executeHermesInVercelSandbox' in CORE
    assert 'provider: "elo-web-local-cognitive-core-via-private-hermes"' in CORE
    assert 'validation_status: "evidence_validated"' in CORE
