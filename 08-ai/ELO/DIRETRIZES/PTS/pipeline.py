#!/usr/bin/env python3
"""Valida a ligação PTS Técnica -> Orçamento -> PTS Pós-Orçamento.

Uso:
    python pipeline.py data/pts_tecnica.json data/pts_pos.json

Nenhum dado de SO de exemplo é embutido no pipeline.
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


def load(path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def require_keys(obj, keys, where):
    missing = [k for k in keys if k not in obj]
    if missing:
        raise ValidationError(f"{where}: campos obrigatórios ausentes: {', '.join(missing)}")


def as_ids(value, field):
    if value in (None, "", "—"):
        return set()
    if isinstance(value, list):
        return {str(x) for x in value}
    if isinstance(value, str):
        return {x.strip() for x in value.split(",") if x.strip()}
    raise ValidationError(f"{field}: deve ser lista ou texto")


def validate_tecnica(data):
    require_keys(data, [
        "identificacao", "objetivo", "escopo", "matriz_tecnica",
        "consultas", "resumo_executivo", "legenda", "rastreabilidade"
    ], "PTS Técnica")
    if not isinstance(data["matriz_tecnica"], list):
        raise ValidationError("PTS Técnica: matriz_tecnica deve ser lista")
    if not isinstance(data["consultas"], list):
        raise ValidationError("PTS Técnica: consultas deve ser lista")

    item_ids = set()
    for i, row in enumerate(data["matriz_tecnica"]):
        where = f"PTS Técnica.matriz_tecnica[{i}]"
        require_keys(row, [
            "id", "item_tr", "trecho_tr", "exigencia", "tipo", "adequacao",
            "status", "curva", "motivo", "responsavel", "consulta_id"
        ], where)
        if row["id"] in item_ids:
            raise ValidationError(f"{where}: ID duplicado {row['id']}")
        item_ids.add(row["id"])
        for key, allowed in [
            ("tipo", TECH_TYPES), ("responsavel", RESPONSAVEIS),
            ("curva", CURVAS), ("status", STATUS)
        ]:
            if row[key] not in allowed:
                raise ValidationError(f"{where}: {key} inválido: {row[key]}")

    consulta_ids = set()
    for i, query in enumerate(data["consultas"]):
        where = f"PTS Técnica.consultas[{i}]"
        require_keys(query, ["id", "texto", "item_ids"], where)
        if query["id"] in consulta_ids:
            raise ValidationError(f"{where}: ID duplicado {query['id']}")
        consulta_ids.add(query["id"])
        unknown = set(query["item_ids"]) - item_ids
        if unknown:
            raise ValidationError(f"{where}: item_ids órfãos: {', '.join(sorted(unknown))}")

    for row in data["matriz_tecnica"]:
        cid = row.get("consulta_id")
        if cid not in (None, "", "—") and cid not in consulta_ids:
            raise ValidationError(f"PTS Técnica: consulta_id órfão: {cid}")

    return item_ids, consulta_ids


def validate_pos(data):
    require_keys(data, [
        "so", "pts_tecnica_ref", "itens_herdados", "consultas_abertas",
        "objetivo", "escopo_tecnico", "matriz_rastreabilidade",
        "resumo_executivo", "legenda_criterios", "registro_aprendizado"
    ], "PTS Pós-Orçamento")
    if not isinstance(data["matriz_rastreabilidade"], list):
        raise ValidationError("PTS Pós-Orçamento: matriz_rastreabilidade deve ser lista")

    refs = set()
    for i, row in enumerate(data["matriz_rastreabilidade"]):
        where = f"PTS Pós-Orçamento.matriz_rastreabilidade[{i}]"
        require_keys(row, [
            "n", "ref_tecnica", "topico_item", "referencia_tr_documento",
            "requisito_descricao_so", "quantidade_prevista", "quantidade_orcada",
            "referencia_orcamento", "valor", "status", "divergencia"
        ], where)
        if row["ref_tecnica"] in (None, "", "—"):
            raise ValidationError(f"{where}: ref_tecnica ausente")
        refs.add(str(row["ref_tecnica"]))

    return refs


def main():
    parser = argparse.ArgumentParser(
        description="Valida PTS Técnica -> Orçamento -> PTS Pós-Orçamento."
    )
    parser.add_argument("pts_tecnica", type=Path)
    parser.add_argument("pts_pos", type=Path)
    args = parser.parse_args()

    try:
        tecnica = load(args.pts_tecnica)
        pos = load(args.pts_pos)

        tecnica_ids, consulta_ids = validate_tecnica(tecnica)
        pos_refs = validate_pos(pos)

        orphan_refs = sorted(pos_refs - tecnica_ids)
        inherited = as_ids(pos["itens_herdados"], "itens_herdados")
        orphan_inherited = sorted(inherited - tecnica_ids)
        open_queries = as_ids(pos["consultas_abertas"], "consultas_abertas")
        unknown_queries = sorted(open_queries - consulta_ids)

        if orphan_refs:
            raise ValidationError(
                "PTS Pós-Orçamento: referências técnicas órfãs: "
                + ", ".join(orphan_refs)
            )
        if orphan_inherited:
            raise ValidationError(
                "PTS Pós-Orçamento: itens_herdados órfãos: "
                + ", ".join(orphan_inherited)
            )
        if unknown_queries:
            raise ValidationError(
                "PTS Pós-Orçamento: consultas_abertas inexistentes na PTS Técnica: "
                + ", ".join(unknown_queries)
            )

        print("[OK] PTS Técnica: estrutura válida")
        print("[OK] PTS Pós-Orçamento: estrutura válida")
        print("[OK] ref_tecnica: presente e sem referências órfãs")
        print(f"[OK] consultas abertas: {', '.join(sorted(open_queries)) if open_queries else '—'}")
        print("[OK] itens herdados: sem referências órfãs")
        print("[OK] rastreabilidade: TR -> PTS Técnica -> Orçamento -> PTS Pós validada")
        return 0
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"[ERRO] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
