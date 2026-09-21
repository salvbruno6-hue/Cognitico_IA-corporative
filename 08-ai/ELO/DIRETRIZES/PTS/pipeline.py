#!/usr/bin/env python3
"""Valida a ligação PTS Técnica -> Orçamento -> PTS Pós-Orçamento.

Uso:
    python pipeline.py data/pts_tecnica.json data/pts_pos.json

A entrada é tratada como evidência da SO atual. Nenhum dado de SO de exemplo é
embutido no pipeline.
"""

import argparse
import json
import sys
from pathlib import Path

TECH_TYPES = {"PAD", "EXC", "PRJ", "FOR", "CLI"}
RESPONSAVEIS = {"ENG", "PLA", "FOR", "CONTRATADA", "FAB"}
CURVAS = {"A", "B", "C"}
STATUS = {"🟢", "🟡", "🔴"}


class ValidationError(Exception):
    pass


def load(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def require_keys(obj, keys, where):
    missing = [k for k in keys if k not in obj]
    if missing:
        raise ValidationError(f"{where}: campos obrigatórios ausentes: {', '.join(missing)}")


def validate_tecnica(data):
    require_keys(
        data,
        ["identificacao", "objetivo", "escopo", "matriz_tecnica", "consultas",
         "resumo_executivo", "legenda", "rastreabilidade"],
        "PTS Técnica",
    )
    if not isinstance(data["matriz_tecnica"], list):
        raise ValidationError("PTS Técnica: matriz_tecnica deve ser lista")
    if not isinstance(data["consultas"], list):
        raise ValidationError("PTS Técnica: consultas deve ser lista")

    ids = set()
    consulta_ids = set()
    for i, row in enumerate(data["matriz_tecnica"]):
        where = f"PTS Técnica.matriz_tecnica[{i}]"
        require_keys(
            row,
            ["id", "item_tr", "trecho_tr", "exigencia", "tipo", "adequacao",
             "status", "curva", "motivo", "responsavel", "consulta_id"],
            where,
        )
        if row["id"] in ids:
            raise ValidationError(f"{where}: ID duplicado {row['id']}")
        ids.add(row["id"])
        for key, allowed in [("tipo", TECH_TYPES), ("responsavel", RESPONSAVEIS),
                             ("curva", CURVAS), ("status", STATUS)]:
            if row[key] not in allowed:
                raise ValidationError(f"{where}: {key} inválido: {row[key]}")
        cid = row.get("consulta_id")
        if cid not in (None, "", "—") and cid not in consulta_ids:
            # consulta pode ser declarada depois; a verificação final ocorre abaixo.
            pass

    for i, q in enumerate(data["consultas"]):
        where = f"PTS Técnica.consultas[{i}]"
        require_keys(q, ["id", "texto", "item_ids"], where)
        if q["id"] in consulta_ids:
            raise ValidationError(f"{where}: ID duplicado {q['id']}")
        consulta_ids.add(q["id"])
        unknown = set(q["item_ids"]) - ids
        if unknown:
            raise ValidationError(f"{where}: item_ids órfãos: {', '.join(sorted(unknown))}")

    for row in data["matriz_tecnica"]:
        cid = row.get("consulta_id")
        if cid not in (None, "", "—") and cid not in consulta_ids:
            raise ValidationError(f"PTS Técnica: consulta_id órfão: {cid}")

    return ids, consulta_ids


def validate_pos(data):
    require_keys(
        data,
        ["so", "objetivo", "escopo_tecnico", "matriz_rastreabilidade",
         "resumo_executivo", "legenda_criterios", "registro_aprendizado"],
        "PTS Pós-Orçamento",
    )
    if not isinstance(data["matriz_rastreabilidade"], list):
        raise ValidationError("PTS Pós-Orçamento: matriz_rastreabilidade deve ser lista")
    if not isinstance(data.get("pts_tecnica_ref"), str) or not data["pts_tecnica_ref"].strip():
        raise ValidationError("PTS Pós-Orçamento: pts_tecnica_ref é obrigatório")
    if "itens_herdados" not in data:
        raise ValidationError("PTS Pós-Orçamento: seção 0 exige itens_herdados")
    if "consultas_abertas" not in data:
        raise ValidationError("PTS Pós-Orçamento: seção 0 exige consultas_abertas")

    refs = set()
    for i, row in enumerate(data["matriz_rastreabilidade"]):
        where = f"PTS Pós-Orçamento.matriz_rastreabilidade[{i}]"
        require_keys(
            row,
            ["n", "ref_tecnica", "topico_item", "referencia_tr_documento",
             "requisito_descricao_so", "quantidade_prevista", "quantidade_orcada",
             "referencia_orcamento", "valor", "status", "divergencia"],
            where,
        )
        ref = row["ref_tecnica"]
        if ref in (None, "", "—"):
            raise ValidationError(f"{where}: ref_tecnica ausente")
        refs.add(ref)
    return refs


def validate_link(tech, pos, tech_ids):
    orphan_refs = sorted(pos - tech_ids)
    if orphan_refs:
        raise ValidationError(
            "PTS Pós-Orçamento: referências técnicas órfãs: " + ", ".join(orphan_refs)
        )

    consultas_abertas = pos_data_list(pos_data_get(pos, "consultas_abertas"))
    tech_open = {
        q["id"] for q in tech.get("consultas", [])
        if q.get("id") in consultas_abertas
    }
    missing_open = sorted(set(consultas_abertas) - {q["id"] for q in tech.get("consultas", [])})
    if missing_open:
        raise ValidationError(
            "PTS Pós-Orçamento: consultas_abertas não existem na PTS Técnica: "
            + ", ".join(missing_open)
        )

    inherited = pos_data_list(pos_data_get(pos_data, "itens_herdados"))
    unknown_inherited = sorted(set(inherited) - tech_ids)
    if unknown_inherited:
        raise ValidationError(
            "PTS Pós-Orçamento: itens_herdados órfãos: " + ", ".join(unknown_inherited)
        )

    return {"orphan_refs": orphan_refs, "open_consultas": sorted(tech_open),
            "unknown_inherited": unknown_inherited}


def pos_data_get(data, key):
    return data.get(key, [])


def pos_data_list(value):
    if value in (None, "", "—"):
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [x.strip() for x in value.split(",") if x.strip()]
    raise ValidationError(f"campo deve ser lista ou texto: {value!r}")


def main():
    parser = argparse.ArgumentParser(description="Valida PTS Técnica -> PTS Pós-Orçamento.")
    parser.add_argument("pts_tecnica", type=Path)
    parser.add_argument("pts_pos", type=Path)
    args = parser.parse_args()

    try:
        tech = load(args.pts_tecnica)
        pos_data = load(args.pts_pos)
        tech_ids, _ = validate_tecnica(tech)
        pos_refs = validate_pos(pos_data)

        # A validação de vínculo usa o documento Pós real, sem incorporar dados
        # externos ao par de entradas.
        global pos_data
        pos_data = pos_data

        orphan_refs = sorted(pos_refs - tech_ids)
        inherited = pos_data_list(pos_data.get("itens_herdados"))
        unknown_inherited = sorted(set(inherited) - tech_ids)
        tech_consulta_ids = {q["id"] for q in tech.get("consultas", [])}
        open_consultas = pos_data_list(pos_data.get("consultas_abertas"))
        unknown_consultas = sorted(set(open_consultas) - tech_consulta_ids)

        if orphan_refs:
            raise ValidationError("referências técnicas órfãs: " + ", ".join(orphan_refs))
        if unknown_inherited:
            raise ValidationError("itens_herdados órfãos: " + ", ".join(unknown_inherited))
        if unknown_consultas:
            raise ValidationError("consultas_abertas inexistentes na PTS Técnica: " + ", ".join(unknown_consultas))

        print("[OK] PTS Técnica: estrutura válida")
        print("[OK] PTS Pós-Orçamento: estrutura válida")
        print("[OK] ref_tecnica: presente e sem referências órfãs")
        print(f"[OK] consultas abertas: {', '.join(open_consultas) if open_consultas else '—'}")
        print("[OK] itens herdados: sem referências órfãs")
        print("[OK] rastreabilidade: PTS Técnica -> PTS Pós validada")
        return 0
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"[ERRO] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
