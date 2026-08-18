from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_external_bootstrap_defaults_to_read_only_and_rejects_prompt_authorization():
    bootstrap = read("ELO_BOOTSTRAP.md")
    standard = read("ELO_AUTHORIZATION_ENFORCEMENT_STANDARD.md")

    assert "READ_ONLY_CONSULTATION" in bootstrap
    assert "natural-language request" in bootstrap
    assert "NOT authorization" in bootstrap
    assert "READ_ONLY_CONSULTATION" in standard
    assert "A prompt alone is not a permission grant." in standard


def test_access_matrix_preserves_least_privilege_and_core_protection():
    matrix = read("docs/security/ELO_EXTERNAL_ACCESS_CONTROL_MATRIX.md")

    required = (
        "READ_ONLY_CONSULTATION",
        "AUTHORIZED_SPECIALIST",
        "GOVERNED_EXECUTION",
        "read-only",
        "minimum required scope",
        "Core changes require governed proposal",
    )
    for term in required:
        assert term in matrix


def test_acceptance_matrix_covers_write_escalation_and_isolation_cases():
    acceptance = read("tests/security/ELO_EXTERNAL_WRITE_DENIAL_ACCEPTANCE.md")

    required_cases = (
        "AC-01",
        "AC-02",
        "AC-03",
        "AC-04",
        "AC-05",
        "AC-06",
        "AC-07",
        "AC-08",
        "AC-09",
        "AC-10",
        "ACCESS_SCOPE_VIOLATION",
        "CROSS_COMPANY_ISOLATION",
        "ISSUE → BRANCH → TEST → REVIEW → EVOLUTION GATE → MERGE",
    )
    for case in required_cases:
        assert case in acceptance


def test_security_standard_explicitly_separates_elo_policy_from_github_permissions():
    standard = read("ELO_AUTHORIZATION_ENFORCEMENT_STANDARD.md")

    assert "ELO behavioral rules cannot revoke GitHub permissions" in standard
    assert "consultation integrations: read-only repository permission" in standard
    assert "specialist integrations: minimum required repository permission" in standard
    assert "no access to unrelated repositories" in standard
