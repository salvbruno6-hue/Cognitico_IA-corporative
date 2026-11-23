"""Regression checks for the executable Forge budgeting geometry skill."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "src/elo/application/use_cases/modular_geometry.py"
PACK = ROOT / "forge/skill-packs/ELO_FORGE_BUDGETING_SPECIALIST_v1.yaml"
SKILL = ROOT / "08-ai/ELO/ESPECIALISTAS/ORCAMENTO/SKILL.md"
CONTRACT = ROOT / "prompts/ELO_ORCAMENTO_EXECUTION_CONTRACT.yaml"
spec = importlib.util.spec_from_file_location("modular_geometry", MODULE_PATH)
geometry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(geometry)


def env(name, length, width, height=2800, quantity=1):
    return {"id": name, "comprimento_mm": length, "largura_mm": width,
            "altura_mm": height, "quantidade": quantity, "fonte": "SO249/TR7.1.1"}


def mod(width=2400, height=2800, code="HYP-2400"):
    return {"codigo": code, "comprimento_mm": 6000, "largura_mm": width,
            "altura_mm": height, "classe_fonte": "HIPOTESE", "fonte": "simulacao",
            "revisao": None, "ativo": True}


def test_so249_hypothetical_2400_three_rooms_ten_physical_modules():
    result = geometry.analisar_dimensionamento(
        [env("sala", 7200, 6000, quantity=2), env("lab", 9600, 6000)], [mod()])
    assert result["total_modulos_condicional"] == 10
    assert [a["quantidade_modulos_condicional"] for a in result["ambientes"]] == [6, 4]
    assert all(a["alternativa_preliminar"]["status"] == "ENCAIXE_GEOMETRICO_EXATO"
               for a in result["ambientes"])
    assert result["metadados"]["aprova_fabricacao"] is False


def test_live_2440_catalog_flags_geometry_and_height():
    model = dict(mod(2440, 3010, "MLT.M01"), classe_fonte="CATALOGO",
                 fonte="Supabase/modelos/dimensoes", revisao="live")
    result = geometry.analisar_dimensionamento(
        [env("sala", 7200, 6000, quantity=2), env("lab", 9600, 6000)], [model])
    assert result["total_modulos_condicional"] == 10
    a, b = [x["alternativa_preliminar"] for x in result["ambientes"]]
    assert a["dimensoes_resultantes_mm"]["comprimento_mm"] == "7320"
    assert b["dimensoes_resultantes_mm"]["comprimento_mm"] == "9760"
    assert a["status"] == b["status"] == "ADEQUACAO_DIMENSIONAL_PENDENTE"
    assert "ALTURA_DIVERGENTE" in a["gaps"]


def test_missing_height_is_fail_closed_but_area_quantity_available():
    result = geometry.analisar_dimensionamento(
        [env("sala", 7200, 6000, height=None)], [mod(height=None)])
    scenario = result["ambientes"][0]["alternativa_preliminar"]
    assert scenario["status"] == "DADOS_INSUFICIENTES"
    assert scenario["modulos_por_ambiente"] == 3


def test_missing_plan_dimensions_never_fabricates_quantity():
    result = geometry.analisar_dimensionamento([env("sala", None, 6000)], [mod()])
    assert result["total_modulos_condicional"] is None
    assert result["ambientes"][0]["alternativa_preliminar"]["modulos_por_ambiente"] is None


def test_inactive_models_cannot_be_selected_as_evidence():
    result = geometry.analisar_dimensionamento(
        [env("sala", 7200, 6000)], [dict(mod(), ativo=False)])
    assert result["total_modulos_condicional"] is None
    assert "MODELO_INATIVO" in result["ambientes"][0]["alternativa_preliminar"]["gaps"]


def test_no_fit_within_limit():
    result = geometry.analisar_dimensionamento(
        [env("big", 7200, 6000)], [mod()], max_modulos_por_ambiente=2)
    assert result["ambientes"][0]["alternativa_preliminar"]["status"] == "NAO_ENCAIXA"


def test_exact_candidate_has_priority_over_lower_count_mismatch():
    result = geometry.analisar_dimensionamento(
        [env("sala", 7200, 6000)], [mod(2440, 3010, "MLT.M01"), mod(2400, 2800, "HYP")])
    assert result["ambientes"][0]["alternativa_preliminar"]["modelo_codigo"] == "HYP"


def test_absurd_and_invalid_values_do_not_count():
    result = geometry.analisar_dimensionamento([env("sala", "nan", 6000)], [mod()])
    assert result["total_modulos_condicional"] is None


def test_skill_pack_metadata_reuses_existing_budget_specialist():
    pack = PACK.read_text(encoding="utf-8")
    skill = SKILL.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")
    assert pack.splitlines().count("  - skill_id: FORGE-BUDGETING-001") == 1
    assert "modular_geometry_capability:" in pack
    assert "capability_key: budgeting.modular_geometry" in pack
    assert "public.modelos" in pack and "public.dimensoes" in pack
    assert "cannot_use_authz_capability_table_as_skill_registry: true" in pack
    assert "## 22. Subcapacidade: inferência geométrica" in skill
    assert "id: modular_geometry_analysis" in contract
    assert contract.index("id: model_match") < contract.index("id: modular_geometry_analysis") < contract.index("id: delta_detection")


def test_source_provenance_is_required_to_claim_fit():
    source_missing = dict(env("sala", 7200, 6000), fonte=None)
    result = geometry.analisar_dimensionamento([source_missing], [mod()])
    candidate = result["ambientes"][0]["alternativa_preliminar"]
    assert candidate["status"] == "DADOS_INSUFICIENTES"
    assert "FONTE_DOCUMENTAL_AUSENTE" in candidate["gaps"]
    assert result["total_modulos_condicional"] is None


def test_model_identity_and_source_class_are_required():
    unknown = dict(mod(), codigo=None)
    result = geometry.analisar_dimensionamento([env("sala", 7200, 6000)], [unknown])
    assert "IDENTIDADE_OU_FONTE_MODELO_AUSENTE" in result["ambientes"][0]["alternativa_preliminar"]["gaps"]
    unclassified = dict(mod(), classe_fonte="NAO_CONFIRMADA")
    result = geometry.analisar_dimensionamento([env("sala", 7200, 6000)], [unclassified])
    assert "CLASSE_FONTE_MODELO_NAO_CONFIRMADA" in result["ambientes"][0]["alternativa_preliminar"]["gaps"]
