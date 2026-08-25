"""Orquestrador somente de simulacao para cruzar demanda, material e recurso."""
import json
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
CONFIG = BASE / "configuracoes"
OUTPUT = DATA / "diagnostico_pcp.json"


def load(name):
    with (DATA / name).open(encoding="utf-8") as f:
        return json.load(f)


def load_params():
    with (CONFIG / "parametros_elo.json").open(encoding="utf-8") as f:
        return json.load(f)


def days_late(availability, deadline):
    return (date.fromisoformat(availability) - date.fromisoformat(deadline)).days


def diagnose(params, demand_data, material_links, materials_data, resource_links, resources_data):
    materials = {x["id"]: x for x in materials_data["materiais"]}
    resources = {x["id"]: x for x in resources_data["recursos"]}
    links_m = {}
    links_r = {}
    for link in material_links["relacoes"]:
        links_m.setdefault(link["demanda_id"], []).append(link)
    for link in resource_links["relacoes"]:
        links_r.setdefault(link["demanda_id"], []).append(link)

    signals = []
    tolerance = params["materiais"]["dias_tolerancia_atraso_material"]
    alert_capacity = params["capacidade"]["limite_alerta_gargalo_capacidade"]
    critical_capacity = params["capacidade"]["limite_critico_gargalo_capacidade"]

    for demand in demand_data["demandas"]:
        did = demand["id"]
        deadline = demand["prazo_entrega"]
        for link in links_m.get(did, []):
            material = materials.get(link["material_id"])
            if not material:
                signals.append({"tipo":"REFERENCIA_INVALIDA","nivel":"critico","demanda_id":did,"material_id":link["material_id"]})
                continue
            deficit = max(0, link["quantidade_necessaria"] - material["estoque_disponivel"])
            late = max(0, days_late(material["data_disponibilidade"], deadline))
            if late > tolerance:
                signals.append({"tipo":"ATRASO_MATERIAL","nivel":"critico","demanda_id":did,"material_id":material["id"],"atraso_dias":late,"tolerancia_dias":tolerance})
            if deficit > 0:
                signals.append({"tipo":"DEFICIT_MATERIAL","nivel":"alerta","demanda_id":did,"material_id":material["id"],"deficit":deficit})
        for link in links_r.get(did, []):
            resource = resources.get(link["recurso_id"])
            if not resource:
                signals.append({"tipo":"REFERENCIA_INVALIDA","nivel":"critico","demanda_id":did,"recurso_id":link["recurso_id"]})
                continue
            projected = resource["horas_comprometidas"] + link["horas_estimadas"]
            utilization = projected / resource["capacidade_total_horas"]
            if utilization >= critical_capacity:
                level = "critico"
            elif utilization >= alert_capacity:
                level = "alerta"
            else:
                continue
            signals.append({"tipo":"GARGALO_CAPACIDADE","nivel":level,"demanda_id":did,"recurso_id":resource["id"],"utilizacao_projetada":utilization,"capacidade_total_horas":resource["capacidade_total_horas"]})

    status = "CRITICO" if any(s["nivel"] == "critico" for s in signals) else "ALERTA" if signals else "NORMAL"
    return {"schema_version":"1.0.0","ambiente":"simulacao","status":status,"total_sinais":len(signals),"sinais":signals}


def run():
    params = load_params()
    result = diagnose(params, load("demanda.json"), load("demanda_materiais.json"), load("materiais.json"), load("demanda_recursos.json"), load("recursos.json"))
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2))
