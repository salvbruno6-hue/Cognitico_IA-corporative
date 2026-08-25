"""Testes assertivos do comportamento do simulador."""
import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from regras.orquestrador import diagnose, load_params, load


def run_tests():
    params = load_params()
    demand = load("demanda.json")
    links_m = load("demanda_materiais.json")
    materials = load("materiais.json")
    links_r = load("demanda_recursos.json")
    resources = load("recursos.json")

    original = diagnose(params, demand, links_m, materials, links_r, resources)
    assert original["status"] == "CRITICO"
    assert any(s["tipo"] == "ATRASO_MATERIAL" and s["material_id"] == "MAT-003" for s in original["sinais"])
    assert any(s["tipo"] == "GARGALO_CAPACIDADE" and s["recurso_id"] == "REC-001" for s in original["sinais"])

    fixed_materials = copy.deepcopy(materials)
    fixed_materials["materiais"][2]["data_disponibilidade"] = "2026-09-02"
    fixed_materials["materiais"][2]["atraso_dias"] = 0
    changed = diagnose(params, demand, links_m, fixed_materials, links_r, resources)
    assert not any(s["tipo"] == "ATRASO_MATERIAL" and s["material_id"] == "MAT-003" for s in changed["sinais"])
    assert changed["total_sinais"] < original["total_sinais"]

    normal_resources = copy.deepcopy(resources)
    normal_resources["recursos"][0]["horas_comprometidas"] = 80
    normal_resources["recursos"][0]["disponibilidade_horas"] = 80
    changed_capacity = diagnose(params, demand, links_m, fixed_materials, links_r, normal_resources)
    assert not any(s["tipo"] == "GARGALO_CAPACIDADE" and s["recurso_id"] == "REC-001" for s in changed_capacity["sinais"])

    critical_resources = copy.deepcopy(resources)
    critical_resources["recursos"][1]["horas_comprometidas"] = 150
    critical_resources["recursos"][1]["disponibilidade_horas"] = 10
    critical_links = copy.deepcopy(links_r)
    critical_links["relacoes"].append({"demanda_id":"DEM-002","recurso_id":"REC-002","horas_estimadas":20})
    critical = diagnose(params, demand, links_m, materials, critical_links, critical_resources)
    assert any(s["tipo"] == "GARGALO_CAPACIDADE" and s["nivel"] == "critico" and s["recurso_id"] == "REC-002" for s in critical["sinais"])

    print("ELO VIRTUAL CORE: ASSERT TESTS PASS")


if __name__ == "__main__":
    run_tests()
