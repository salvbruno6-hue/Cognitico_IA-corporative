from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
GUARDRAIL = REPO_ROOT / "docs" / "governance" / "ELO_CREATION_GUARDRAILS.md"


def test_universal_creation_guardrail_exists() -> None:
    assert GUARDRAIL.exists()
    text = GUARDRAIL.read_text(encoding="utf-8")
    assert "No new implementation may bypass an existing ELO contract" in text
    assert "Search exact concept" in text
    assert "IDENTIFY canonical owner" in text
    assert "REUSE | EXTEND | CORRECT | CONSOLIDATE | DEPRECATE | NEW" in text


def test_frontend_and_hermes_boundaries_are_explicit() -> None:
    text = GUARDRAIL.read_text(encoding="utf-8")
    assert "The ELO Web is an Application layer" in text
    assert "The browser MUST NOT" in text
    assert "call Hermes directly" in text
    assert "Hermes is an external execution/orchestration runtime" in text
    assert "Hermes-created skills remain non-canonical" in text


def test_preventive_control_requires_reusable_guard_after_error() -> None:
    text = GUARDRAIL.read_text(encoding="utf-8")
    assert "identify the missing preventive control" in text
    assert "add or strengthen a repository-level guard/test/check" in text
    assert "revalidate existing adjacent implementations" in text


def test_governed_integration_minimum_evidence_is_defined() -> None:
    text = GUARDRAIL.read_text(encoding="utf-8")
    for required in (
        "tenant/domain/principal isolation",
        "request/correlation ID preservation",
        "provenance",
        "secrets/infrastructure-field rejection",
        "canonical authority protection",
        "non-canonical learning candidate handling",
    ):
        assert required in text
