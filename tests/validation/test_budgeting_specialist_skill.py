from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "08-ai/ELO/ESPECIALISTAS/ORCAMENTO/SKILL.md"
PACK = ROOT / "forge/skill-packs/ELO_FORGE_BUDGETING_SPECIALIST_v1.yaml"
MASTER = ROOT / "08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS/ELO_APRENDER_CANONICO_MASTER_PROMPT.md"


def test_budgeting_skill_is_formalized_without_parallel_authority():
    text = PACK.read_text(encoding="utf-8")
    assert "skill_id: FORGE-BUDGETING-001" in text
    assert "domain_family: BUDGETING" in text
    assert "authority: ELO_COGNITIVO" in text
    assert "shared_faculty: Core" in text
    assert "direct_forge_to_core_promotion: false" in text
    assert "precedent_is_rule_by_default: false" in text


def test_budgeting_skill_reuses_existing_canonical_memory():
    text = PACK.read_text(encoding="utf-8")
    assert "elo_orcamento_memoria" in text
    assert "elo_orcamento_calculos_aprendidos" in text
    assert "elo_orcamento_associacoes" in text
    assert "não altera preço canônico sem fonte autorizada" in text


def test_elo_aprender_captures_reasoning_not_only_result():
    skill = SKILL.read_text(encoding="utf-8")
    master = MASTER.read_text(encoding="utf-8")
    assert "Gatilho cognitivo `ELO APRENDER`" in skill
    assert "CONDIÇÃO / REQUISITO" in skill
    assert "DEPENDÊNCIAS DE IMPLEMENTAÇÃO" in skill
    assert "FÓRMULA / SUBCÁLCULO" in skill
    assert "NÃO APRENDER SOMENTE O RESULTADO" in master


def test_pir_20ft_example_is_candidate_not_universal_rule():
    skill = SKILL.read_text(encoding="utf-8")
    pack = PACK.read_text(encoding="utf-8")
    assert "14 painéis de parede" in skill
    assert "5 painéis de teto" in skill
    assert "Status inicial: `CANDIDATO`" in skill
    assert "GAP_FORMULA_QUANTITATIVO" in skill
    assert "wall_panels_observed: 14" in pack
    assert "ceiling_panels_observed: 5" in pack


def test_pir_dependency_is_check_not_automatic_inclusion():
    skill = SKILL.read_text(encoding="utf-8")
    assert "PAINEL PIR → VERIFICAR GUIA U / PERFIS DE FIXAÇÃO E ACABAMENTO" in skill
    assert "Não transformar automaticamente" in skill
