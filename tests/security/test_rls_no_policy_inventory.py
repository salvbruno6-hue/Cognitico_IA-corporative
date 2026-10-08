"""Audit completeness and canonical authorization boundary; SQL probes run on live DB."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_FIELDS = {
    'source', 'source_type', 'source_fields', 'observed_state', 'expected_state',
    'gap', 'confidence', 'canonical_owner', 'risk', 'proposed_action', 'validation',
    'classification', 'consumer',
}


def test_every_advisor_no_policy_table_has_evidence_and_a_decision():
    audit = json.loads((ROOT / 'docs/evolution/RLS_NO_POLICY_AUDIT_2026-10-08.json').read_text())
    tables = audit['tables']
    names = [item['table'] for item in tables]
    assert len(names) == len(set(names)) == 34
    assert sum(name.startswith('public.') for name in names) == 29
    assert sum(name.startswith('elo_core.') for name in names) == 5
    for item in tables:
        assert REQUIRED_FIELDS <= item.keys()
        assert item['source_fields']
        assert 'source_field' not in item
        assert item['observed_state']['rls_enabled']
        assert item['observed_state']['policy_count'] == 0
    assert audit['stage_status'] == 'EM_EXECUCAO'


def test_mt_gates_correction_preserves_authorities_instead_of_adding_a_policy():
    sql = (ROOT / 'supabase/migrations/20261008093623_harden_mt_gates_client_grants.sql').read_text()
    statements = [line for line in sql.splitlines() if line.strip() and not line.lstrip().startswith('--')]
    assert statements == ['REVOKE ALL ON TABLE public.mt_gates FROM PUBLIC, anon, authenticated;']
    # This bounded migration cannot revoke service_role/admin or introduce a permissive policy.
    probes = (ROOT / 'tests/security/test_mt_gates_access.sql').read_text()
    for role in ('anon', 'authenticated', 'service_role'):
        assert f'SET LOCAL ROLE {role};' in probes
    assert 'ROLLBACK;' in probes
