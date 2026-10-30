from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "08-ai/ELO/ESPECIALISTAS/ORCAMENTO/SKILL.md"
PACK = ROOT / "forge/skill-packs/ELO_FORGE_BUDGETING_SPECIALIST_v1.yaml"
TRIGGER = ROOT / "docs/cognitive/ELO_ANALISAR_TRIGGER.md"
REGISTRY = ROOT / "docs/cognitive/ELO_TRIGGER_REGISTRY.md"
CONTRACT = ROOT / "08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/ELO_ORCAMENTISTA_APRENDIZADO_CONTINUO.md"


def test_budgeting_skill_auto_activates_on_elo_analisar():
    pack = PACK.read_text(encoding="utf-8")
    trigger = TRIGGER.read_text(encoding="utf-8")
    registry = REGISTRY.read_text(encoding="utf-8")

    assert "auto_activate_on: ELO ANALISAR" in pack
    assert "ativar a Skill formal `FORGE-BUDGETING-001`" in trigger
    assert "**Skill especializada ativada:** `FORGE-BUDGETING-001`" in registry
    assert "remain_active_until: encerramento da solicitação" in pack


def test_budgeting_skill_consults_stored_knowledge_before_composition():
    pack = PACK.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")

    assert "stored_knowledge_lookup_required: true" in pack
    assert "elo_orcamento_memoria" in contract
    assert "elo_orcamento_calculos_aprendidos" in contract
    assert "elo_orcamento_calculo_similaridades" in contract
    assert "CONSULTAR → COMPARAR CONTEXTO → TESTAR EQUIVALÊNCIA" in contract


def test_reasoning_trace_covers_pts_budget_and_value_formation():
    skill = SKILL.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")

    assert "PTS TÉCNICA → DECISÃO TÉCNICA → ORÇAMENTO → PTS PÓS-ORÇAMENTO" in skill
    assert "reasoning_trace_required: true" in PACK.read_text(encoding="utf-8")
    assert "Rastro de raciocínio por fase" in contract
    assert "Auditoria reversa do valor" in contract
    assert "VALOR → ITEM ORÇADO → COMPOSIÇÃO → QUANTITATIVO → FÓRMULA" in contract


def test_pts_pos_canonical_indicators_are_reused_not_duplicated():
    pack = PACK.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")

    for indicator in ("Conhecimento", "Flexibilidade", "Risco", "Decisão"):
        assert indicator in pack
        assert indicator in contract
    assert "A Skill não cria uma segunda família de indicadores" in contract


def test_learning_review_has_at_least_ten_adaptive_questions():
    pack = PACK.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")

    assert "minimum_learning_questions: 10" in pack
    assert "no mínimo 10 perguntas" in contract
    question_ids = set(re.findall(r"`Q(\d{2})`", contract))
    assert len(question_ids) >= 10
    assert "10 é piso, não teto" in contract
    assert "AGUARDANDO_OWNER" in contract


def test_learning_questions_do_not_auto_promote_knowledge():
    pack = PACK.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")

    assert "learning_question_is_permission_to_promote: false" in pack
    assert "As respostas do owner não alteram a Skill automaticamente" in contract
    assert "CASE" in contract
    assert "PRECEDENT" in contract
    assert "LEARNING_CANDIDATE" in contract
    assert "VALIDATED_LEARNING" in contract
    assert "Nenhuma resposta promove diretamente conhecimento ao Core" in contract


def test_closure_explains_how_budget_was_thought_and_priced():
    skill = SKILL.read_text(encoding="utf-8")
    trigger = TRIGGER.read_text(encoding="utf-8")

    assert "Explicação por fase e formação dos valores" in skill
    assert "como cada quantitativo material foi obtido" in skill
    assert "de onde veio cada preço unitário relevante" in skill
    assert "explicação de como os principais valores foram formados" in trigger
