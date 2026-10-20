#!/usr/bin/env python3
"""Valida a relação PTS Técnica → Orçamento → PTS Pós → Validação.

Uso:
    python pipeline.py data/pts_tecnica.json data/pts_pos.json

O pipeline valida estrutura, referências e coerência mínima entre as duas PTS.
Nenhum dado de SO é embutido.
"""
import argparse
import json
import sys
from pathlib import Path

from POS_ORCAMENTO_INTEGRATION import integrate

TECH_TYPES = {"PAD", "EXC", "PRJ", "FOR", "CLI"}
RESPONSAVEIS = {"ENG", "PLA", "FOR", "CONTRATADA", "FAB"}
CURVAS = {"A", "B", "C"}
STATUS = {"🟢", "🟡", "🔴"}
IMPACTOS = {"ALTO", "MEDIO", "BAIXO"}
ORIGENS = {
    "TR", "LAYOUT", "PROJETO", "VISTORIA", "CONSULTA_CLIENTE",
    "PADRAO_MULTITEINER", "SOLUCAO_TECNICA", "PREMISSA_COMERCIAL",
}
BASE_TOP_FIELDS = (
    "identificacao", "objetivo", "escopo", "matriz_tecnica", "consultas",
    "resumo_executivo", "legenda", "rastreabilidade",
)
MATURE_TOP_FIELDS = (
    "vistoria", "pontos_grande_peso", "contradicoes_escopo", "premissas",
    "quantitativos",
)
BASE_ROW_FIELDS = (
    "id", "item_tr", "trecho_tr", "exigencia", "tipo", "adequacao",
    "status", "curva", "motivo", "responsavel", "consulta_id",
)
MATURE_ROW_FIELDS = (
    "origem", "quantidade_tr", "evidencia_layout", "atendimento_multiteiner",
    "tratamento_orcamentario", "associacao_orcamento", "validacao_associacao",
    "responsabilidade", "ponto_validacao", "impacto",
)


class ValidationError(Exception):
    """Erro de validação estrutural ou de rastreabilidade."""


def load(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def require_keys(obj, keys, where):
    if not isinstance(obj, dict):
        raise ValidationError(f"{where}: tipo inválido; esperado dict")
    missing = [k for k in keys if k not in obj]
    if missing:
        raise ValidationError(f"{where}: campos obrigatórios ausentes: {', '.join(missing)}")


def require_type(value, expected, where):
    if not isinstance(value, expected):
        name = expected.__name__ if isinstance(expected, type) else "/".join(t.__name__ for t in expected)
        raise ValidationError(f"{where}: tipo inválido; esperado {name}")


def require_string(value, where, *, nonempty=False):
    require_type(value, str, where)
    if nonempty and not value:
        raise ValidationError(f"{where}: texto vazio não permitido")


def require_enum(value, allowed, where):
    require_string(value, where)
    if value not in allowed:
        raise ValidationError(f"{where}: valor inválido: {value}")


def as_ids(value, field):
    if value in (None, "", "—"):
        return set()
    if isinstance(value, list):
        return {str(x) for x in value}
    if isinstance(value, str):
        return {x.strip() for x in value.split(",") if x.strip()}
    raise ValidationError(f"{field}: deve ser lista ou texto")


def validate_tecnica(data):
    require_keys(data, BASE_TOP_FIELDS, "PTS Técnica")
    if not isinstance(data["matriz_tecnica"], list):
        raise ValidationError("PTS Técnica: matriz_tecnica deve ser lista")
    if not isinstance(data["consultas"], list):
        raise ValidationError("PTS Técnica: consultas deve ser lista")

    item_ids = set()
    for i, row in enumerate(data["matriz_tecnica"]):
        where = f"PTS Técnica.matriz_tecnica[{i}]"
        require_keys(row, BASE_ROW_FIELDS, where)
        if row["id"] in item_ids:
            raise ValidationError(f"{where}: ID duplicado {row['id']}")
        item_ids.add(row["id"])
        for key, allowed in [
            ("tipo", TECH_TYPES),
            ("responsavel", RESPONSAVEIS),
            ("curva", CURVAS),
            ("status", STATUS),
        ]:
            if not isinstance(row[key], str) or row[key] not in allowed:
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
            raise ValidationError(
                f"{where}: item_ids órfãos: {', '.join(sorted(unknown))}"
            )

    for row in data["matriz_tecnica"]:
        cid = row.get("consulta_id")
        if cid not in (None, "", "—") and cid not in consulta_ids:
            raise ValidationError(f"PTS Técnica: consulta_id órfão: {cid}")

    if data.get("contrato_maturidade") == "1.0":
        require_keys(data, MATURE_TOP_FIELDS, "PTS Técnica madura")
        for i, row in enumerate(data["matriz_tecnica"]):
            where = f"PTS Técnica madura.matriz_tecnica[{i}]"
            require_keys(row, MATURE_ROW_FIELDS, where)
            if not isinstance(row["responsabilidade"], str) or row["responsabilidade"] not in RESPONSAVEIS:
                raise ValidationError(
                    f"{where}: responsabilidade inválida: {row['responsabilidade']}"
                )
            if not isinstance(row["impacto"], str) or row["impacto"] not in IMPACTOS:
                raise ValidationError(f"{where}: impacto inválido: {row['impacto']}")

    return item_ids, consulta_ids


def validate_current_schema_types(data):
    """Enforce the type/enum constraints declared by PTS_TECNICA_SCHEMA.json."""
    require_type(data, dict, "PTS Técnica atual")
    require_keys(data, (*BASE_TOP_FIELDS, *MATURE_TOP_FIELDS), "PTS Técnica atual")
    require_type(data["identificacao"], dict, "PTS Técnica atual.identificacao")
    require_string(data["objetivo"], "PTS Técnica atual.objetivo")
    require_type(data["escopo"], list, "PTS Técnica atual.escopo")
    require_type(data["matriz_tecnica"], list, "PTS Técnica atual.matriz_tecnica")
    require_type(data["consultas"], list, "PTS Técnica atual.consultas")
    require_type(data["resumo_executivo"], list, "PTS Técnica atual.resumo_executivo")
    require_type(data["legenda"], dict, "PTS Técnica atual.legenda")
    require_type(data["rastreabilidade"], list, "PTS Técnica atual.rastreabilidade")

    for key in MATURE_TOP_FIELDS:
        require_type(data[key], list, f"PTS Técnica atual.{key}")

    for i, row in enumerate(data["matriz_tecnica"]):
        where = f"PTS Técnica atual.matriz_tecnica[{i}]"
        require_type(row, dict, where)
        require_keys(row, (*BASE_ROW_FIELDS, *MATURE_ROW_FIELDS), where)
        for key in (
            "id", "item_tr", "trecho_tr", "exigencia", "evidencia_layout",
            "atendimento_multiteiner", "tratamento_orcamentario",
            "associacao_orcamento", "validacao_associacao", "ponto_validacao",
            "adequacao", "motivo",
        ):
            require_string(row[key], f"{where}.{key}", nonempty=(key == "id"))
        require_enum(row["tipo"], TECH_TYPES, f"{where}.tipo")
        require_enum(row["status"], STATUS, f"{where}.status")
        require_enum(row["curva"], CURVAS, f"{where}.curva")
        require_enum(row["responsavel"], RESPONSAVEIS, f"{where}.responsavel")
        require_enum(row["responsabilidade"], RESPONSAVEIS, f"{where}.responsabilidade")
        require_enum(row["impacto"], IMPACTOS, f"{where}.impacto")

        require_type(row["origem"], list, f"{where}.origem")
        for j, item in enumerate(row["origem"]):
            require_enum(item, ORIGENS, f"{where}.origem[{j}]")

        if row["consulta_id"] is not None:
            require_string(row["consulta_id"], f"{where}.consulta_id")

    for i, query in enumerate(data["consultas"]):
        where = f"PTS Técnica atual.consultas[{i}]"
        require_type(query, dict, where)
        require_keys(query, ("id", "texto", "item_ids"), where)
        require_string(query["id"], f"{where}.id")
        require_string(query["texto"], f"{where}.texto")
        require_type(query["item_ids"], list, f"{where}.item_ids")
        for j, item in enumerate(query["item_ids"]):
            require_string(item, f"{where}.item_ids[{j}]")


def validate_current_tecnica(data):
    """Validate the current canonical PTS Técnica contract used for new output.

    Historical/legacy PTS data can still be inspected with ``validate_tecnica``.
    New render/output must use the additive maturity contract so the technical
    PTS remains structurally aligned with PTS Pós and the canonical pipeline.
    """
    if not isinstance(data, dict) or data.get("contrato_maturidade") != "1.0":
        raise ValidationError(
            "PTS Técnica atual exige contrato_maturidade=1.0; "
            "estrutura legada é apenas consultiva e não pode gerar nova PTS"
        )
    # Type/schema validation runs first so malformed current data cannot leak
    # TypeError/KeyError through legacy relationship checks.
    validate_current_schema_types(data)
    return validate_tecnica(data)


def validate_pos(data, tecnica_ids):
    require_keys(
        data,
        [
            "so", "pts_tecnica_ref", "itens_herdados", "consultas_abertas",
            "documentos", "objetivo_texto", "matriz_principal",
            "blocos_quantitativos", "conferencia_valores", "auditoria_reversa",
            "itens_premissa", "logistica", "mao_de_obra", "exclusoes",
            "divergencias", "riscos", "pendencias", "itens_nao_orcados",
            "checklist", "conclusao",
        ],
        "PTS Pós-Orçamento",
    )
    if not data["pts_tecnica_ref"]:
        raise ValidationError("PTS Pós-Orçamento: pts_tecnica_ref ausente")
    if not isinstance(data["matriz_principal"], list):
        raise ValidationError("PTS Pós-Orçamento: matriz_principal deve ser lista")

    refs = set()
    for i, row in enumerate(data["matriz_principal"]):
        where = f"PTS Pós-Orçamento.matriz_principal[{i}]"
        require_keys(
            row,
            ["n", "ref_tecnica", "topico", "ref_tr", "requisito", "q_prev",
             "q_orc", "ref_orc", "valor", "status", "divergencia"],
            where,
        )
        ref = str(row["ref_tecnica"]).strip()
        if not ref:
            raise ValidationError(f"{where}: ref_tecnica ausente")
        refs.add(ref)

    orphan_refs = sorted(refs - tecnica_ids)
    if orphan_refs:
        raise ValidationError(
            "PTS Pós-Orçamento: referências técnicas órfãs: "
            + ", ".join(orphan_refs)
        )

    inherited = as_ids(data["itens_herdados"], "itens_herdados")
    orphan_inherited = sorted(inherited - tecnica_ids)
    if orphan_inherited:
        raise ValidationError(
            "PTS Pós-Orçamento: itens_herdados órfãos: "
            + ", ".join(orphan_inherited)
        )

    open_queries = as_ids(data["consultas_abertas"], "consultas_abertas")
    return open_queries


def main():
    parser = argparse.ArgumentParser(
        description="Valida PTS Técnica → Orçamento → PTS Pós → Validação."
    )
    parser.add_argument("pts_tecnica", type=Path)
    parser.add_argument("pts_pos", type=Path)
    args = parser.parse_args()

    try:
        tecnica = load(args.pts_tecnica)
        pos = load(args.pts_pos)

        if isinstance(tecnica, dict) and tecnica.get("contrato_maturidade") == "1.0":
            tecnica_ids, consulta_ids = validate_current_tecnica(tecnica)
        else:
            tecnica_ids, consulta_ids = validate_tecnica(tecnica)
        open_queries = validate_pos(pos, tecnica_ids)

        unknown_queries = sorted(open_queries - consulta_ids)
        if unknown_queries:
            raise ValidationError(
                "PTS Pós-Orçamento: consultas_abertas inexistentes na PTS Técnica: "
                + ", ".join(unknown_queries)
            )

        print("[OK] PTS Técnica: estrutura válida")
        print("[OK] PTS Pós-Orçamento: estrutura válida")
        print("[OK] ref_tecnica: presente e sem referências órfãs")
        print(
            "[OK] consultas abertas: "
            + (", ".join(sorted(open_queries)) if open_queries else "—")
        )
        print("[OK] itens herdados: sem referências órfãs")
        print("[OK] validação cruzada: PTS Técnica ↔ Orçamento ↔ PTS Pós")
        integracao = integrate(pos)
        print("[OK] camada analítica de competitividade: integrada à auditoria")
        print("[OK] validação: proposta " + integracao.validacao["status_proposto"])
        print("[OK] arbitragem: " + integracao.arbitrado["status"])
        print("[OK] ELO APRENDER: pacote candidato, sem promoção automática")
        print("[OK] rastreabilidade: TR → PTS Técnica → Orçamento → PTS Pós → Auditoria → Competitividade → Validação → Arbitragem → ELO APRENDER")
        return 0
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"[ERRO] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
