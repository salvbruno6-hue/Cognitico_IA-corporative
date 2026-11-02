from pathlib import Path


CANDIDATE = Path(
    "docs/implementation/sql/ELO_AUTHZ_ADMIN_ROLE_BYPASS_CONTAINMENT_CANDIDATE.sql"
).read_text(encoding="utf-8")
DECISION = Path(
    "docs/architecture/ELO_AUTHZ_ADMIN_ROLE_BYPASS_CONTAINMENT_DECISION_20261102.md"
).read_text(encoding="utf-8")
CANONICAL_HELPER = Path(
    "supabase/migrations/20260919220406_elo_access_tiers.sql"
).read_text(encoding="utf-8")
HEALTH = Path("supabase/health/elo_capability_reference_integrity.sql").read_text(encoding="utf-8")


def test_candidate_is_not_an_official_migration() -> None:
    assert "CANDIDATE ONLY" in CANDIDATE
    assert "NOT AUTHORIZED FOR LIVE DDL" in CANDIDATE
    assert "docs/implementation/sql/" in str(
        Path("docs/implementation/sql/ELO_AUTHZ_ADMIN_ROLE_BYPASS_CONTAINMENT_CANDIDATE.sql")
    )


def test_normal_capabilities_still_require_explicit_role_capability_mapping() -> None:
    for token in (
        "JOIN public.elo_role_capabilities rc",
        "JOIN public.elo_capabilities c",
        "c.code = p_code",
        "c.active = true",
    ):
        assert token in CANDIDATE


def test_admin_role_compatibility_is_limited_to_the_known_pcp_admin_debt() -> None:
    assert "WHEN p_code = 'PCP_ADMIN'" in CANDIDATE
    assert "r.code IN ('ELO_ADMIN', 'CANONICAL_ADMIN')" in CANDIDATE
    assert "WHEN p_code = 'ADMIN'" not in CANDIDATE
    assert "WHEN p_code = 'CANONICAL_WRITE'" not in CANDIDATE
    assert "WHEN p_code = 'PROPOSE'" not in CANDIDATE
    assert "WHEN p_code = 'APPROVE'" not in CANDIDATE


def test_candidate_never_creates_or_assigns_authority() -> None:
    lowered = CANDIDATE.lower()
    for forbidden in (
        "insert into public.elo_capabilities",
        "insert into public.elo_role_capabilities",
        "update public.elo_capabilities",
        "update public.elo_role_capabilities",
        "delete from public.elo_capabilities",
        "delete from public.elo_role_capabilities",
        "create policy ",
        "alter policy ",
    ):
        assert forbidden not in lowered


def test_candidate_preserves_function_acl_boundary() -> None:
    assert "REVOKE ALL ON FUNCTION elo_private.has_capability(text) FROM PUBLIC" in CANDIDATE
    assert "GRANT EXECUTE ON FUNCTION elo_private.has_capability(text) TO authenticated" in CANDIDATE


def test_original_canonical_helper_was_explicit_capability_only() -> None:
    assert "JOIN public.elo_role_capabilities rc" in CANONICAL_HELPER
    assert "JOIN public.elo_capabilities c" in CANONICAL_HELPER
    assert "AND c.code = p_code" in CANONICAL_HELPER
    assert "r.code IN ('ELO_ADMIN','CANONICAL_ADMIN')" not in CANONICAL_HELPER


def test_pcp_admin_remains_review_debt_not_automatic_catalog_authority() -> None:
    assert "PCP_ADMIN" in DECISION
    assert "technical debt" in DECISION
    assert "do not insert `PCP_ADMIN`" in DECISION
    assert "REVIEW" in HEALTH
    assert "never permission to create/assign" in HEALTH


def test_decision_separates_containment_from_final_resolution() -> None:
    assert "This is containment, not final resolution." in DECISION
    assert "do not modify strategic authorization semantics" in DECISION
    assert "remote DDL" in DECISION
    assert "Objective Continuity checkpoint creation" in DECISION
