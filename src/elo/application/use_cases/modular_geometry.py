"""Forge budgeting: auditable, fail-closed physical module layout estimates.

Input dimensions are EXTERNAL millimetres. This is an analytical geometry
assistant, not a structural, transport, fabrication, or procurement approval.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_CEILING
from typing import Any, Mapping, Sequence

CAPABILITY_KEY = "budgeting.modular_geometry"
CAPABILITY_VERSION = "1.0.0"
STATUSES = (
    "ENCAIXE_GEOMETRICO_EXATO",
    "ADEQUACAO_DIMENSIONAL_PENDENTE",
    "NAO_ENCAIXA",
    "DADOS_INSUFICIENTES",
)


def _positive_mm(value: Any) -> Decimal | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = Decimal(str(value))
    except (ValueError, InvalidOperation):
        return None
    if not number.is_finite() or number <= 0:
        return None
    return number


def _ceil_ratio(required: Decimal, available: Decimal) -> int:
    return int((required / available).to_integral_value(rounding=ROUND_CEILING))


def _candidate(ambiente: Mapping[str, Any], modelo: Mapping[str, Any], max_modulos: int) -> dict[str, Any]:
    required = [_positive_mm(ambiente.get(key)) for key in ("comprimento_mm", "largura_mm", "altura_mm")]
    actual = [_positive_mm(modelo.get(key)) for key in ("comprimento_mm", "largura_mm", "altura_mm")]
    base: dict[str, Any] = {
        "modelo_codigo": modelo.get("codigo"),
        "modelo_fonte": modelo.get("fonte"),
        "classe_fonte": modelo.get("classe_fonte", "NAO_CONFIRMADA"),
        "revisao_modelo": modelo.get("revisao"),
        "status": "DADOS_INSUFICIENTES",
        "modulos_por_ambiente": None,
        "orientacao": None,
        "colunas": None,
        "linhas": None,
        "dimensoes_resultantes_mm": None,
        "diferencas_mm": None,
        "gaps": [],
    }
    if modelo.get("ativo") is False:
        base["gaps"] = ["MODELO_INATIVO"]
        return base
    if not ambiente.get("fonte"):
        base["gaps"] = ["FONTE_DOCUMENTAL_AUSENTE"]
        return base
    if not modelo.get("codigo") or not modelo.get("fonte"):
        base["gaps"] = ["IDENTIDADE_OU_FONTE_MODELO_AUSENTE"]
        return base
    if modelo.get("classe_fonte") not in ("CATALOGO", "HIPOTESE"):
        base["gaps"] = ["CLASSE_FONTE_MODELO_NAO_CONFIRMADA"]
        return base
    if any(value is None for value in required[:2] + actual[:2]):
        base["gaps"] = ["DIMENSOES_PLANAS_AUSENTES"]
        return base

    comprimento, largura, altura = required
    mod_comp, mod_larg, mod_alt = actual
    options: list[tuple[int, Decimal, str, int, int, Decimal, Decimal]] = []
    for orientacao, lateral, profundidade in (
        ("LONGITUDINAL", mod_comp, mod_larg),
        ("ROTACIONADO_90", mod_larg, mod_comp),
    ):
        colunas = _ceil_ratio(comprimento, lateral)
        linhas = _ceil_ratio(largura, profundidade)
        total = colunas * linhas
        if total > max_modulos:
            continue
        result_c = colunas * lateral
        result_l = linhas * profundidade
        sobra = (result_c * result_l) - (comprimento * largura)
        options.append((total, sobra, orientacao, colunas, linhas, result_c, result_l))
    if not options:
        base.update(status="NAO_ENCAIXA", gaps=["QUANTIDADE_ACIMA_LIMITE_ANALITICO"])
        return base
    # Prefer exact footprint; then fewer modules and less surplus area.
    # No unsupported cutting, shrinking, or field modifications.
    options.sort(key=lambda op: (op[5] != comprimento or op[6] != largura, op[0], op[1], op[2]))
    count, _surplus, orientation, nx, ny, result_c, result_l = options[0]
    gaps: list[str] = []
    if result_c != comprimento:
        gaps.append("COMPRIMENTO_DIVERGENTE")
    if result_l != largura:
        gaps.append("LARGURA_DIVERGENTE")
    if altura is None or mod_alt is None:
        gaps.append("ALTURA_NAO_COMPROVADA")
    elif mod_alt != altura:
        gaps.append("ALTURA_DIVERGENTE")
    if "ALTURA_NAO_COMPROVADA" in gaps:
        status = "DADOS_INSUFICIENTES"
    elif gaps:
        status = "ADEQUACAO_DIMENSIONAL_PENDENTE"
    else:
        status = "ENCAIXE_GEOMETRICO_EXATO"
    base.update(
        status=status,
        orientacao=orientation,
        colunas=nx,
        linhas=ny,
        modulos_por_ambiente=count,
        dimensoes_resultantes_mm={
            "comprimento_mm": str(result_c),
            "largura_mm": str(result_l),
            "altura_mm": str(mod_alt) if mod_alt is not None else None,
        },
        diferencas_mm={
            "comprimento_mm": str(result_c - comprimento),
            "largura_mm": str(result_l - largura),
            "altura_mm": str(mod_alt - altura) if mod_alt is not None and altura is not None else None,
        },
        gaps=gaps,
    )
    return base


def analisar_dimensionamento(
    ambientes: Sequence[Mapping[str, Any]],
    modelos: Sequence[Mapping[str, Any]],
    *,
    max_modulos_por_ambiente: int = 100,
) -> dict[str, Any]:
    """Estimate grids, preserving candidate provenance and engineering vetoes.

    Required environment keys: id, quantidade, comprimento_mm, largura_mm,
    altura_mm, fonte. Model keys: codigo, dimensions, fonte, classe_fonte, revisao.
    """
    if not ambientes or not modelos or max_modulos_por_ambiente <= 0:
        raise ValueError("Informe ambientes, modelos e limite positivo")
    resultados: list[dict[str, Any]] = []
    total_estimado = 0
    all_quantified = True
    for ambiente in ambientes:
        quantity = ambiente.get("quantidade", 1)
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Quantidade de ambientes deve ser inteiro positivo")
        candidates = [_candidate(ambiente, model, max_modulos_por_ambiente) for model in modelos]
        rank = {
            "ENCAIXE_GEOMETRICO_EXATO": 0,
            "ADEQUACAO_DIMENSIONAL_PENDENTE": 1,
            "DADOS_INSUFICIENTES": 2,
            "NAO_ENCAIXA": 3,
        }
        candidates.sort(key=lambda c: (
            rank[c["status"]],
            c["modulos_por_ambiente"] if c["modulos_por_ambiente"] is not None else 10**9,
            str(c["modelo_codigo"]),
        ))
        selected = candidates[0]
        if selected["modulos_por_ambiente"] is None:
            all_quantified = False
        else:
            total_estimado += quantity * selected["modulos_por_ambiente"]
        resultados.append({
            "ambiente_id": ambiente.get("id"),
            "fonte_documental": ambiente.get("fonte"),
            "quantidade_ambientes": quantity,
            "dimensoes_exigidas_mm": {k: ambiente.get(k) for k in ("comprimento_mm", "largura_mm", "altura_mm")},
            "alternativas": candidates,
            "alternativa_preliminar": selected,
            "quantidade_modulos_condicional": (
                quantity * selected["modulos_por_ambiente"]
                if selected["modulos_por_ambiente"] is not None else None
            ),
        })
    return {
        "metadados": {
            "capability_key": CAPABILITY_KEY,
            "version": CAPABILITY_VERSION,
            "responsavel": "FORGE-BUDGETING-001",
            "unidade": "mm_externo",
            "status_conformidade": "NAO_VALIDADO_ENGENHARIA",
            "aprova_fabricacao": False,
            "autoriza_orcamento": False,
            "origem_dimensoes_catalogo": "Supabase public.modelos JOIN public.dimensoes",
        },
        "ambientes": resultados,
        "total_modulos_condicional": total_estimado if all_quantified else None,
        "gates_pendentes": ["ENGENHARIA_ACOPLAMENTO", "LAYOUT", "ESTRUTURA", "TRANSPORTE", "ACEITE_TR"],
    }
