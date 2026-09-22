"""Contract tests for the ELO execution-cycle contract."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "06-knowledge-engineering" / "CONTRATO_CICLO_EXECUCAO_ELO.md"


def test_execution_cycle_contract_exists_and_is_candidate():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Status:** V0.1 — proposta para validação" in text
    assert "CANDIDATO / NÃO CONSOLIDADO" in text


def test_execution_cycle_has_required_traceability_blocks():
    text = CONTRACT.read_text(encoding="utf-8")
    for block in (
        "IDENTIDADE", "ENTRADA", "FONTES", "DADOS ATUAIS",
        "SKILL/REGRA + VERSÃO", "ANÁLISE", "DECISÃO", "IMPACTO",
        "EXECUÇÃO", "RESULTADO", "DESVIO", "EVIDÊNCIA",
        "APRENDIZADO", "STATUS DE VALIDAÇÃO",
    ):
        assert block in text


def test_execution_cycle_blocks_unsupported_learning_promotion():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "CANDIDATO → TESTADO → VALIDADO → CONSOLIDADO" in text
    assert "não promove conhecimento automaticamente" in text
    assert "NÃO LOCALIZADO" in text


def test_execution_cycle_preserves_source_boundaries():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "DADO × FONTE VISUAL × APRENDIZADO VALIDADO × INFERÊNCIA CONTROLADA × NÃO LOCALIZADO" in text
    assert "histórico em dado atual" in text
    assert "hipótese em fato" in text


def test_execution_cycle_distinguishes_supabase_and_github_roles():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Supabase: estado operacional, execução, resultado e aprendizado persistente" in text
    assert "GitHub: skill, regra, contrato, teste e versionamento" in text
    assert "ELO: execução cognitiva, confronto, análise, decisão e registro" in text