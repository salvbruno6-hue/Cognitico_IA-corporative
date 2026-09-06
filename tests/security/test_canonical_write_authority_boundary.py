from pathlib import Path

from elo.core import AccessDecision, AccessRequest, SessionMode, authorize


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
AUTHZ_SOURCE = REPOSITORY_ROOT / "supabase" / "functions" / "elo-authz" / "index.ts"

CRITICAL_ACTIONS = (
    "modify_core",
    "modify_canonical_memory",
    "promote_to_core",
    "merge_protected_change",
)


def _consultation_request(action: str) -> AccessRequest:
    return AccessRequest(
        principal_id="principal-1",
        role="specialist",
        domain="test",
        enterprise_context="tenant-a",
        scope="test-read",
        action=action,
        session_mode=SessionMode.AUTHORIZED_SPECIALIST,
    )


def test_cognitive_policy_cannot_grant_canonical_write_authority():
    for action in CRITICAL_ACTIONS:
        result = authorize(_consultation_request(action))
        assert result.decision is AccessDecision.DENY
        assert result.reason == "action_outside_elo_authority"


def test_canonical_write_actions_remain_declared_in_elo_authz():
    source = AUTHZ_SOURCE.read_text(encoding="utf-8")
    assert 'const ACTION_CAPABILITY: Record<string, string>' in source
    for action in CRITICAL_ACTIONS:
        assert f'"{action}"' in source


def test_canonical_write_authority_is_not_claimed_by_materialization_layer():
    materialization = (
        REPOSITORY_ROOT / "src" / "elo" / "core" / "knowledge_materialization.py"
    ).read_text(encoding="utf-8")
    assert "mutation_authority": False
    assert "does not" in materialization
