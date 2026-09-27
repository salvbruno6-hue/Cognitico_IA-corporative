"""Fixtures do harness cognitivo derivadas de experiências reais persistidas no Supabase.

Cada fixture é autocontida. Não consulta Supabase em runtime.
Conteúdo derivado das auditorias estruturais.

Proveniência:
- SO 001.26: elo_aprendizado_experiencias.id = e146f320-22bc-40ca-bde3-603770f9b9d3
- SO 162.26: elo_aprendizado_experiencias.id = 358ee63b-96d1-4d28-b0a6-10313758890f
- SO 178.26: elo_aprendizado_experiencias.id = 5e6e1a82-2f99-403d-94f0-f578a0296475
"""
from __future__ import annotations

from elo.cognitive.runtime.cognitive_harness import CognitiveHarnessFixture


def _fixture(*, provenance_id, so_id, question, intent, external_analysis, learning):
    return CognitiveHarnessFixture(
        request_id=f"real-experience-{so_id.replace('.', '-')}",
        intent=intent,
        payload={"question": question, "so_id": so_id, "provenance_id": provenance_id},
        external_analysis=external_analysis,
        so_context={
            "so_id": so_id,
            "provenance_id": provenance_id,
            "learning": learning,
            "handbook": [],
            "precedents": [],
        },
    )


def so_001_26_trelica() -> CognitiveHarnessFixture:
    """SO 001.26 — comprimento estrutural distinto de consumo de tubo."""
    summary = "comprimento estrutural da peça ≠ metragem de tubo consumida para fabricá-la"
    return _fixture(
        provenance_id="e146f320-22bc-40ca-bde3-603770f9b9d3",
        so_id="SO 001.26",
        question="ELO, o que você sabe sobre a SO 001.26",
        intent="o_que_sabe",
        external_analysis=summary,
        learning={
            "so_id": "SO 001.26", "canonical_key": "SO_001_26",
            "domain": "orcamento",
            "tags": ["trelica", "comprimento_estrutural", "metragem_tubo", "memoria_calculo"],
            "summary": summary, "origem": "ELO Aprender — interação SO 001.26",
            "confianca": 0.99, "status_validacao": "CANDIDATA",
        },
    )


def so_001_26_confere() -> CognitiveHarnessFixture:
    """SO 001.26 — conferência da premissa sobre treliça."""
    analysis = "consideramos a metragem de 3 metros como comprimento estrutural da peça de treliça."
    return _fixture(
        provenance_id="e146f320-22bc-40ca-bde3-603770f9b9d3",
        so_id="SO 001.26",
        question=f"ELO, confere essa análise da SO 001.26: {analysis}",
        intent="confere_analise",
        external_analysis=analysis,
        learning={
            "so_id": "SO 001.26", "canonical_key": "SO_001_26",
            "tags": ["trelica", "comprimento_estrutural", "metragem_tubo"],
            "summary": "comprimento estrutural da peça ≠ metragem de tubo",
        },
    )


def so_162_26_layout() -> CognitiveHarnessFixture:
    """SO 162.26 — escolha do módulo como processo de decisão."""
    summary = "escolha do módulo deve ser aprendida como processo de decisão durante a análise, e não apenas como resultado final do orçamento"
    return _fixture(
        provenance_id="358ee63b-96d1-4d28-b0a6-10313758890f",
        so_id="SO 162.26",
        question="ELO, o que você sabe sobre a SO 162.26",
        intent="o_que_sabe",
        external_analysis=summary,
        learning={
            "so_id": "SO 162.26", "canonical_key": "SO_162_26", "domain": "orcamento",
            "tags": ["layout", "modulo_20_pes", "decisao_modular", "croqui_pavimento"],
            "summary": summary,
            "origem": "SO 162.26 / decisão operacional fornecida no processo de análise",
            "confianca": 0.8, "status_validacao": "OBSERVADA",
        },
    )


def so_162_26_confere() -> CognitiveHarnessFixture:
    """SO 162.26 — conferência da modulação."""
    analysis = "adotamos módulos padrão de 20 pés como base da solução comercial em 2 pavimentos."
    return _fixture(
        provenance_id="358ee63b-96d1-4d28-b0a6-10313758890f",
        so_id="SO 162.26",
        question=f"ELO, confere essa análise da SO 162.26: {analysis}",
        intent="confere_analise",
        external_analysis=analysis,
        learning={
            "so_id": "SO 162.26", "canonical_key": "SO_162_26",
            "tags": ["layout", "modulo_20_pes"],
            "summary": "escolha do módulo como processo de decisão",
        },
    )


def so_178_26_rastreabilidade() -> CognitiveHarnessFixture:
    """SO 178.26 — rastreabilidade técnica-orçamentária."""
    summary = (
        "quantitativo de parede PIR40 segue geometria efetivamente fechada; "
        "área modular de 57,6 m² não é automaticamente área de cobertura; "
        "QGBT (Administração) separado de interligação externa (contratada)"
    )
    return _fixture(
        provenance_id="5e6e1a82-2f99-403d-94f0-f578a0296475",
        so_id="SO 178.26",
        question="ELO, o que você sabe sobre a SO 178.26",
        intent="o_que_sabe",
        external_analysis=summary,
        learning={
            "so_id": "SO 178.26", "canonical_key": "SO_178_26", "domain": "orcamento",
            "tags": ["rastreabilidade_tecnica", "geometria_efetiva", "cobertura", "interligacoes", "qgbt", "pts_tecnica", "divergencia_financeira"],
            "summary": summary, "origem": "ELO Aprender — SO 178.26",
            "confianca": 0.99, "status_validacao": "CANDIDATA",
        },
    )


def so_178_26_confere() -> CognitiveHarnessFixture:
    """SO 178.26 — conferência de geometria e responsabilidade."""
    analysis = "utilizamos a área modular de 57,6 m² como área de cobertura e somamos as interligações externas ao escopo da contratada."
    return _fixture(
        provenance_id="5e6e1a82-2f99-403d-94f0-f578a0296475",
        so_id="SO 178.26",
        question=f"ELO, confere essa análise da SO 178.26: {analysis}",
        intent="confere_analise",
        external_analysis=analysis,
        learning={
            "so_id": "SO 178.26", "canonical_key": "SO_178_26",
            "tags": ["geometria_efetiva", "cobertura", "interligacoes", "qgbt"],
            "summary": "área modular não é automaticamente área de cobertura; QGBT separado de interligação externa",
        },
    )


ALL_FIXTURES = {
    "so_001_26_trelica": so_001_26_trelica,
    "so_001_26_confere": so_001_26_confere,
    "so_162_26_layout": so_162_26_layout,
    "so_162_26_confere": so_162_26_confere,
    "so_178_26_rastreabilidade": so_178_26_rastreabilidade,
    "so_178_26_confere": so_178_26_confere,
}

__all__ = [
    "so_001_26_trelica", "so_001_26_confere", "so_162_26_layout",
    "so_162_26_confere", "so_178_26_rastreabilidade", "so_178_26_confere",
    "ALL_FIXTURES",
]
