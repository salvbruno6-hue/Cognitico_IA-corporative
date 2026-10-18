from pathlib import Path


PROBE = Path("supabase/health/elo_mt_authorization_readiness.sql")


def _source() -> str:
    return PROBE.read_text(encoding="utf-8")


def test_mt_readiness_probe_is_read_only_and_aggregate_only() -> None:
    source = _source().lower()

    assert "authz_mt_operator_readiness" in source
    assert "gap_high" in source
    assert "enterprise" in source
    assert "multiteiner" in source
    assert "pcp_read" in source
    assert "pcp_update" in source

    forbidden_mutations = (
        "insert into ",
        "update public.",
        "delete from ",
        "alter table ",
        "alter policy ",
        "create policy ",
        "drop policy ",
        "grant ",
        "revoke ",
    )
    for statement in forbidden_mutations:
        assert statement not in source


def test_mt_readiness_probe_does_not_project_identity_details() -> None:
    source = _source().lower()

    # The probe may use eligibility columns in predicates, but evidence must stay
    # aggregate-only: no identifying values are projected into the finding.
    evidence_section = source.split("format(", 1)[1]
    assert "authorized_email" not in evidence_section
    assert "display_name" not in evidence_section
    assert "provider_subject" not in evidence_section
    assert "auth_user_id" not in evidence_section


def test_mt_readiness_probe_does_not_claim_contract_is_live() -> None:
    source = _source().lower()

    assert "does not assign scopes/capabilities" in source
    assert "does not" in source
    assert "infer tenant" in source
