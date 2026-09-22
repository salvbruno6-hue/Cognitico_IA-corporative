"""Contract tests for the ELO symbiont loop definition."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOOP_DOC = ROOT / "06-knowledge-engineering" / "LOOP_SIMBIONTE_ELO.md"
PLANNING_SKILL = ROOT / "06-knowledge-engineering" / "SKILL_PLANEJAMENTO_MULTITEINER.md"


def test_symbiont_loop_document_exists_and_declares_candidate_state():
    text = LOOP_DOC.read_text(encoding="utf-8")

    assert "Status:** V0.1 — proposta para validação" in text
    assert "PERCEBER → CONSULTAR → CONFRONTAR → RACIOCINAR → DECIDIR" in text
    assert "EXECUTAR → MEDIR → APRENDER → VALIDAR → ATUALIZAR" in text


def test_symbiont_loop_has_required_governance_states():
    text = LOOP_DOC.read_text(encoding="utf-8")

    for state in (
        "PERCEPÇÃO",
        "RETRIEVAL",
        "CONFRONTAÇÃO",
        "ANÁLISE",
        "DECISÃO",
        "EXECUÇÃO",
        "RESULTADO",
        "DESVIO",
        "APRENDIZADO",
        "VALIDAÇÃO",
        "CONSOLIDAÇÃO",
        "RETORNO",
    ):
        assert state in text


def test_symbiont_loop_preserves_source_boundaries():
    text = LOOP_DOC.read_text(encoding="utf-8")

    assert "HISTÓRICO × REGRA VIGENTE × DADO ATUAL × DEMANDA ATUAL" in text
    assert "Não converter:" in text
    assert "histórico em dado atual" in text
    assert "candidato em regra consolidada" in text


def test_symbiont_loop_defines_learning_promotion_gate():
    text = LOOP_DOC.read_text(encoding="utf-8")

    assert "CANDIDATO → TESTADO → VALIDADO → CONSOLIDADO" in text
    assert "não deve virar regra imediatamente" in text


def test_symbiont_loop_integrates_the_first_specialized_skill():
    loop_text = LOOP_DOC.read_text(encoding="utf-8")
    skill_text = PLANNING_SKILL.read_text(encoding="utf-8")

    assert "SKILL_PLANEJAMENTO_MULTITEINER.md" in loop_text
    assert "DEMANDA → FLUXO → ETAPAS → DEPENDÊNCIAS" in loop_text
    assert "DEMANDA → FLUXO → ETAPAS → DEPENDÊNCIAS" in skill_text


def test_symbiont_loop_requires_explicit_incomplete_state():
    text = LOOP_DOC.read_text(encoding="utf-8")

    assert "INCOMPLETO" in text
    assert "não como aprendizado consolidado" in text
