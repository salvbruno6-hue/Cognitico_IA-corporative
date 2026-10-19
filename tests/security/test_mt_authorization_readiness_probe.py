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


def test_mt_readiness_probe_matches_elo_authz_identity_eligibility() -> None:
    source = _source().lower()

    assert "join auth.users" in source
    assert "u.id = i.auth_user_id" in source
    assert "lower(trim(i.authorized_email)) = lower(trim(u.email))" in source


def test_mt_readiness_probe_requires_one_identity_to_hold_all_operator_prerequisites() -> None:
    source = _source().lower()

    assert "fully_ready_identities as" in source
    assert "join enterprise_links e on e.identity_id = i.identity_id" in source
    assert "join domain_links d on d.identity_id = i.identity_id" in source
    assert "join pcp_capabilities p on p.identity_id = i.identity_id" in source
    assert "fully_ready_identities = 0" in source


def test_mt_readiness_probe_exposes_typed_tenant_data_prerequisites() -> None:
    source = _source().lower()

    assert "tenant_tables as" in source
    assert "table_stats as" in source
    assert "populated_tables as" in source
    assert "tenant_data as" in source
    assert "from public.mt_tenants" in source
    assert "from public.mt_ordens_reparo" in source
    assert "where tenant_id is not null" in source
    assert "direct_tenant_tables" in source
    assert "estimated_populated_tables" in source
    assert "unverified_populated_tables" in source
    assert "unverified_populated_tables > 0" in source
    assert "repair_rows" in source
    assert "repair_rows_with_tenant" in source
    assert "repair_rows_with_tenant < repair_rows" in source


def test_mt_readiness_probe_projects_aggregate_signals_but_not_identity_details() -> None:
    source = _source().lower()

    for signal in (
        "eligible_google_identities",
        "enterprise_multiteiner_links",
        "identities_with_domain_scope",
        "identities_with_pcp_capability",
        "fully_ready_identities",
        "tenant_rows",
        "direct_tenant_tables",
        "estimated_populated_tables",
        "unverified_populated_tables",
        "repair_rows",
        "repair_rows_with_tenant",
        "legacy_policy_objects",
        "legacy_tables",
    ):
        assert signal in source

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
