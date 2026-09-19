from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "docs" / "symbiont-skills"
CANDIDATES = ROOT / "docs" / "symbiont-candidates"

REQUIRED_SKILL_MARKERS = (
    "- **skill_id:**", "- **owner:**", "- **executor:**", "- **authority:**",
    "- **status:**", "## Função", "## Relação na cadeia de ações",
    "## Testes", "## Aprovação",
)

REQUIRED_APPROVAL_GATES = (
    "identity", "tenant/scope", "proveniência", "evidência",
    "teste de limite", "teste de regressão", "classificação de evolução",
)

def test_each_registered_skill_has_a_governed_contract():
    expected = {
        "SKILL-001-symbiont-operational-boundary.md",
        "SKILL-002-decision-outcome-loop.md",
        "SKILL-003-symbiont-laboratory.md",
        "SKILL-004-capability-absorption.md",
    }
    actual = {p.name for p in SKILLS.glob("SKILL-*.md") if p.name not in {"SKILL-APPROVAL-LOOP.md", "SKILL-EVIDENCE-MATRIX.md"}}
    assert actual == expected
    for path in sorted(SKILLS.glob("SKILL-*.md")):
        if path.name in {"SKILL-APPROVAL-LOOP.md", "SKILL-EVIDENCE-MATRIX.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        missing = [marker for marker in REQUIRED_SKILL_MARKERS if marker not in text]
        assert not missing, f"{path.name}: missing contract markers: {missing}"

def test_approval_loop_is_fail_closed():
    text = (SKILLS / "SKILL-APPROVAL-LOOP.md").read_text(encoding="utf-8").lower()
    missing = [marker for marker in REQUIRED_APPROVAL_GATES if marker not in text]
    assert not missing, f"approval loop missing gates: {missing}"
    assert "rejected / blocked" in text
    assert "não uma memória paralela" in text

def test_candidate_templates_are_separated_from_skill_definitions():
    assert (CANDIDATES / "README.md").exists()
    assert (CANDIDATES / "_TEMPLATE" / "CANDIDATE.md").exists()
    assert (CANDIDATES / "_TEMPLATE" / "TESTS.md").exists()
    assert (CANDIDATES / "_TEMPLATE" / "APPROVAL.md").exists()
    assert (CANDIDATES / "_TEMPLATE" / "POST_APPROVAL.md").exists()
    approval = (CANDIDATES / "_TEMPLATE" / "APPROVAL.md").read_text(encoding="utf-8")
    tests = (CANDIDATES / "_TEMPLATE" / "TESTS.md").read_text(encoding="utf-8")
    assert "Evolution Gate" in approval
    assert "human_approval" in approval
    assert "Não marcar APPROVED" in tests

def test_candidate_docs_do_not_grant_canonical_authority():
    text = (CANDIDATES / "README.md").read_text(encoding="utf-8")
    for forbidden_claim in (
        "conceder autorização", "substituir Evolution Gate",
        "criar memória paralela", "declarar promoção canônica",
    ):
        assert forbidden_claim in text
