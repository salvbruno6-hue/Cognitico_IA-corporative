"""Testes do parser de linguagem natural."""
from elo.cognitive.runtime.intake.natural_language import (
    parse_natural_request,
)
from elo.cognitive.runtime.intake.intents import Intent


def test_confere_analise_variation_1():
    result = parse_natural_request(
        "ELO, confere essa análise da SO 155.26: "
        "O orçamento contempla 24 módulos."
    )
    assert result["intent"] == Intent.CONFERE_ANALISE.value
    assert result["so_id"] == "SO 155.26"
    assert "24 módulos" in result["chatgpt_analysis"]


def test_confere_analise_variation_2():
    result = parse_natural_request(
        "ELO, olha isso da SO 155.26: análise pendente"
    )
    assert result["intent"] == Intent.CONFERE_ANALISE.value
    assert result["so_id"] == "SO 155.26"


def test_o_que_sabe():
    result = parse_natural_request("ELO, o que você sabe sobre a SO 155.26")
    assert result["intent"] == Intent.O_QUE_SABE.value
    assert result["so_id"] == "SO 155.26"


def test_guarda_aprendizado():
    result = parse_natural_request(
        "ELO, guarda isso da SO 155.26: premissa de 30% para peças"
    )
    assert result["intent"] == Intent.GUARDA_APRENDIZADO.value
    assert result["so_id"] == "SO 155.26"


def test_status_decisao():
    result = parse_natural_request(
        "ELO, como está a decisão DEC_2026_0001"
    )
    assert result["intent"] == Intent.STATUS_DECISAO.value


def test_lista_abertas():
    result = parse_natural_request("ELO, o que está aberto")
    assert result["intent"] == Intent.LISTA_ABERTAS.value
    assert "state_filter" in result


def test_busca_precedente():
    result = parse_natural_request(
        "ELO, já vimos algo parecido com a SO 155.26"
    )
    assert result["intent"] == Intent.BUSCA_PRECEDENTE.value


def test_json_block_priority():
    body = """<!-- elo-request-payload
{"intent": "confere_analise", "so_id": "SO-X"}
-->"""
    result = parse_natural_request(body)
    assert result["intent"] == "confere_analise"
    assert result["so_id"] == "SO-X"


def test_unknown_intent_returns_error():
    result = parse_natural_request("bom dia, tudo bem?")
    assert "error" in result
    assert result["error"] == "intent_not_recognized"
    assert "suggestions" in result



def test_confere_analise_includes_question():
    """Regressão: confere_analise deve gerar 'question'."""
    result = parse_natural_request(
        "ELO, confere essa análise da SO 155.26: "
        "o orçamento contempla 30 módulos."
    )
    assert result["intent"] == "confere_analise"
    assert "question" in result
    assert result["question"] != ""


def test_guarda_aprendizado_includes_question():
    """Regressão: guarda_aprendizado deve gerar 'question'."""
    result = parse_natural_request(
        "ELO, guarda isso da SO 155.26: premissa de 30%"
    )
    assert result["intent"] == "guarda_aprendizado"
    assert "question" in result
    assert result["question"] != ""


def test_busca_precedente_includes_question():
    """Regressão: busca_precedente deve gerar 'question'."""
    result = parse_natural_request(
        "ELO, já vimos algo parecido com a SO 155.26"
    )
    assert result["intent"] == "busca_precedente"
    assert "question" in result
    assert result["question"] != ""


def test_o_que_sabe_includes_question():
    """o_que_sabe também deve ter question."""
    result = parse_natural_request(
        "ELO, o que você sabe sobre a SO 155.26"
    )
    assert result["intent"] == "o_que_sabe"
    assert "question" in result
