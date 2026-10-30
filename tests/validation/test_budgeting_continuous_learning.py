from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "08-ai/ELO/ESPECIALISTAS/ORCAMENTO/SKILL.md"
PACK = ROOT / "forge/skill-packs/ELO_FORGE_BUDGETING_SPECIALIST_v1.yaml"
TRIGGER = ROOT / "docs/cognitive/ELO_ANALISAR_TRIGGER.md"
REGISTRY = ROOT / "docs/cognitive/ELO_TRIGGER_REGISTRY.md"
CONTRACT = ROOT / "08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/ELO_ORCAMENTISTA_APRENDIZADO_CONTINUO.md"
EXECUTION_CONTRACT = ROOT / "prompts/ELO_ORCAMENTO_EXECUTION_CONTRACT.yaml"


def test_budgeting_skill_auto_activates_on_elo_analisar():
    pack = PACK.read_text(encoding="utf-8")
    trigger = TRIGGER.read_text(encoding="utf-8")
    registry = REGISTRY.read_text(encoding="utf-8")

    assert "auto_activate_on: ELO ANALISAR" in pack
    assert "ativar o ciclo de Análise de Solicitações" in trigger
    assert "resolver internamente a especialização Forge `FORGE-BUDGETING-001`" in trigger
    assert "**Especialização interna resolvida:** `FORGE-BUDGETING-001`" in registry
    assert "remain_active_until: encerramento da solicitação" in pack


def test_budgeting_skill_activation_is_internal_and_silent():
    pack = PACK.read_text(encoding="utf-8")
    trigger = TRIGGER.read_text(encoding="utf-8")
    registry = REGISTRY.read_text(encoding="utf-8")

    assert "activation_visibility: INTERNAL_SILENT" in pack
    assert "expose_skill_id_on_activation: false" in pack
    assert "expose_infrastructure_on_activation: false" in pack
    assert "forge_skill_is_canonical_authority: false" in pack
    assert "não deve ser apresentada ao usuário como \"Skill canônica\"" in trigger
    assert "Visibilidade da especialização:** interna/silenciosa" in registry

    response_section = trigger.split("## 9. Resposta inicial", 1)[1].split("## 10.", 1)[0]
    visible_block = "\n".join(
        line for line in response_section.splitlines() if line.lstrip().startswith(">")
    )
    assert "ELO ANALISAR ATIVADO — SO/LIC" in visible_block
    assert "SKILL DO ORÇAMENTISTA ATIVA" not in visible_block
    assert "FORGE-BUDGETING-001" not in visible_block
    assert "GitHub" not in visible_block
    assert "Supabase" not in visible_block


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
    assert "nenhuma resposta do owner, isoladamente, promove diretamente conhecimento ao Core" in contract


def test_post_analysis_learning_governance_starts_automatically_but_never_auto_promotes():
    pack = PACK.read_text(encoding="utf-8")
    trigger = TRIGGER.read_text(encoding="utf-8")
    registry = REGISTRY.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")
    execution = EXECUTION_CONTRACT.read_text(encoding="utf-8")

    assert "auto_governance_after_learning_review: true" in pack
    assert "governance_dispatch_trigger: learning_review_completed" in pack
    assert "canonical_learning_governance_owner: src/elo/core/learning_governance.py" in pack
    assert "human_approval_required_for_promotion: true" in pack
    assert "auto_approval: false" in pack
    assert "auto_promotion: false" in pack

    assert "DESPACHO AUTOMÁTICO PARA LEARNING GOVERNANCE CANÔNICA" in trigger
    assert "sem exigir novo comando `ELO APRENDER`" in trigger
    assert "despacho automático" in registry.lower()

    assert "loop de governança deve ser iniciado automaticamente" in contract
    assert "a **aprovação humana nunca é automática**" in contract
    assert "a **promoção nunca é automática**" in contract

    dispatch = execution.split("- id: learning_governance_dispatch", 1)[1].split(
        "- id: correction_loop", 1
    )[0]
    assert "mandatory: true" in dispatch
    assert "automatic_on: learning_review_completed" in dispatch
    assert "canonical_owner: src/elo/core/learning_governance.py" in dispatch
    assert "LEARNING_CANDIDATE: evaluate_without_auto_approval" in dispatch
    assert "human_approval_required: true" in dispatch
    assert "evolution_gate_required: true" in dispatch
    assert "auto_approval: false" in dispatch
    assert "auto_promotion: false" in dispatch


def test_closure_explains_how_budget_was_thought_and_priced():
    skill = SKILL.read_text(encoding="utf-8")
    trigger = TRIGGER.read_text(encoding="utf-8")

    assert "Explicação por fase e formação dos valores" in skill
    assert "como cada quantitativo material foi obtido" in skill
    assert "de onde veio cada preço unitário relevante" in skill
    assert "explicação de como os principais valores foram formados" in trigger
