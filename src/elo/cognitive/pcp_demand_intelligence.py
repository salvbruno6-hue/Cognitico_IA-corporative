"""Sequenciador cognitivo de indicadores do Planejamento de Demanda Multiteiner.

Este módulo NÃO cria uma nova autoridade de demanda. Ele compõe as fontes e
mecanismos já governados pelo ELO/PCP e define somente a ordem determinística
em que os indicadores devem ser consultados para responder perguntas de
Demanda Inteligente.

Fronteiras obrigatórias:
- MÓDULO e CONTÊINER sempre separados;
- SPOT e EVENTO sempre separados;
- REGISTRO_EQUIVALENTE nunca é tratado como UNIDADE_FISICA;
- RETORNO_PREVISTO nunca é tratado como ESTOQUE_LIVRE;
- ausência de dado físico gera GAP, não estimativa inventada.

Fontes canônicas reutilizadas:
- public.v_elo_diretoria_comercial_estoque;
- public.v_elo_pcp_cobertura_demanda_externa;
- public.v_elo_pcp_inteligente;
- public.mt_definicoes_kpi;
- public.elo_aprendizado_demanda;
- SKILL_PLANEJAMENTO_MULTITEINER.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class IndicatorStep:
    order: int
    code: str
    layer: str
    question: str
    physical_required: bool = False


QUALITY_CONTEXT: tuple[IndicatorStep, ...] = (
    IndicatorStep(1, "IND_FONTE_VALIDA", "QUALIDADE", "A fonte está identificada?"),
    IndicatorStep(2, "IND_UNIDADE_MEDIDA", "QUALIDADE", "A unidade é REGISTRO_EQUIVALENTE ou UNIDADE_FISICA?"),
    IndicatorStep(3, "IND_FAMILIA", "QUALIDADE", "A família é MÓDULO ou CONTÊINER?"),
    IndicatorStep(4, "IND_NATUREZA", "QUALIDADE", "A natureza é SPOT, EVENTO, VENDA ou TRANSFERÊNCIA?"),
    IndicatorStep(5, "IND_PERIODO_COMPARAVEL", "QUALIDADE", "Existe período histórico comparável?"),
)

DEMAND: tuple[IndicatorStep, ...] = (
    IndicatorStep(10, "DEM_TOTAL", "DEMANDA", "Qual a demanda total no período?"),
    IndicatorStep(11, "DEM_SPOT", "DEMANDA", "Quanto da demanda é SPOT?"),
    IndicatorStep(12, "DEM_EVENTO", "DEMANDA", "Quanto da demanda é EVENTO?"),
    IndicatorStep(13, "DEM_VENDA", "DEMANDA", "Quanto corresponde a VENDA?"),
    IndicatorStep(14, "PART_SPOT", "DEMANDA", "Qual a participação de SPOT?"),
    IndicatorStep(15, "PART_EVENTO", "DEMANDA", "Qual a participação de EVENTO?"),
)

VARIATION: tuple[IndicatorStep, ...] = (
    IndicatorStep(20, "DEM_YOY", "VARIACAO", "Como o mês mudou contra o mesmo mês do ano anterior?"),
    IndicatorStep(21, "DEM_MOM", "VARIACAO", "Como o mês mudou contra o mês anterior?"),
    IndicatorStep(22, "DELTA_ABS", "VARIACAO", "Qual a diferença absoluta?"),
    IndicatorStep(23, "DELTA_MIX", "VARIACAO", "A mistura SPOT/EVENTO mudou?"),
)

CAUSE: tuple[IndicatorStep, ...] = (
    IndicatorStep(30, "DRV_NATUREZA", "CAUSA", "SPOT ou EVENTO explica a mudança?"),
    IndicatorStep(31, "DRV_MODELO", "CAUSA", "Quais modelos explicam a mudança?"),
    IndicatorStep(32, "DRV_CLIENTE", "CAUSA", "Quais clientes explicam a mudança?"),
    IndicatorStep(33, "DRV_RECORRENCIA", "CAUSA", "O comportamento já apareceu em períodos comparáveis?"),
    IndicatorStep(34, "DRV_CONCENTRACAO", "CAUSA", "A variação está concentrada em poucos modelos/clientes?"),
)

RETURN: tuple[IndicatorStep, ...] = (
    IndicatorStep(40, "RET_PREV_TOTAL", "RETORNO", "Quantos retornos estão previstos?"),
    IndicatorStep(41, "RET_PREV_SPOT", "RETORNO", "Quantos retornos derivam de SPOT?"),
    IndicatorStep(42, "RET_PREV_EVENTO", "RETORNO", "Quantos retornos derivam de EVENTO?"),
    IndicatorStep(43, "RET_PREV_MODELO", "RETORNO", "Quais modelos retornam e em que quantidade?"),
    IndicatorStep(44, "RET_CONCENTRACAO", "RETORNO", "Há concentração de retornos em algum mês/modelo?"),
)

QUARANTINE: tuple[IndicatorStep, ...] = (
    IndicatorStep(50, "QUA_ENTRADAS", "QUARENTENA", "Quantas unidades físicas entraram em quarentena?", True),
    IndicatorStep(51, "QUA_LIBERADOS_DIRETO", "QUARENTENA", "Quantas foram liberadas sem reparo?", True),
    IndicatorStep(52, "QUA_ENCAMINHADOS_REPARO", "QUARENTENA", "Quantas seguiram para reparo?", True),
    IndicatorStep(53, "QUA_EM_REPARO", "QUARENTENA", "Quantas permanecem em reparo?", True),
    IndicatorStep(54, "QUA_LIBERADOS_REPARO", "QUARENTENA", "Quantas foram liberadas após reparo?", True),
    IndicatorStep(55, "QUA_SALDO", "QUARENTENA", "Qual o saldo físico ainda indisponível?", True),
    IndicatorStep(56, "QUA_TEMPO_MEDIO", "QUARENTENA", "Qual o tempo médio até a liberação?", True),
)

STOCK_POLICY: tuple[IndicatorStep, ...] = (
    IndicatorStep(60, "EST_SPOT_P75", "ESTOQUE", "Qual o estoque mínimo SPOT do período/modelo?"),
    IndicatorStep(61, "EST_SPOT_P90", "ESTOQUE", "Qual o estoque-alvo SPOT?"),
    IndicatorStep(62, "EST_SEGURANCA", "ESTOQUE", "Qual o buffer de segurança P90-P75?"),
    IndicatorStep(63, "RES_EVENTO", "ESTOQUE", "Qual a reserva separada para EVENTO?"),
    IndicatorStep(64, "PROTECAO_COMERCIAL", "ESTOQUE", "Qual a proteção comercial total?"),
)

AVAILABILITY: tuple[IndicatorStep, ...] = (
    IndicatorStep(70, "DISP_PATIO_ATUAL", "DISPONIBILIDADE", "Qual o estoque físico livre atual?", True),
    IndicatorStep(71, "DISP_RETORNO_LIBERADO", "DISPONIBILIDADE", "Quanto do retorno já foi liberado?", True),
    IndicatorStep(72, "DISP_REPARO_LIBERADO", "DISPONIBILIDADE", "Quanto do reparo já foi liberado?", True),
    IndicatorStep(73, "DISP_PRODUCAO_LIBERADA", "DISPONIBILIDADE", "Quanto da produção está fisicamente liberada?", True),
    IndicatorStep(74, "DISP_COMPROMETIDA", "DISPONIBILIDADE", "Quanto do estoque já está comprometido?", True),
    IndicatorStep(75, "DISP_PROJETADA", "DISPONIBILIDADE", "Qual a disponibilidade física projetada?", True),
)

COVERAGE_RISK: tuple[IndicatorStep, ...] = (
    IndicatorStep(80, "CAPACIDADE_ATENDIMENTO", "COBERTURA", "A disponibilidade cobre a proteção comercial?", True),
    IndicatorStep(81, "RISCO", "COBERTURA", "Qual o nível de risco do período/modelo?", True),
    IndicatorStep(82, "ACAO_RECOMENDADA", "DECISAO", "Qual preparação é necessária antes do período?", True),
)

MASTER_ORDER: tuple[IndicatorStep, ...] = (
    QUALITY_CONTEXT + DEMAND + VARIATION + CAUSE + RETURN + QUARANTINE
    + STOCK_POLICY + AVAILABILITY + COVERAGE_RISK
)


def _unique(steps: Iterable[IndicatorStep]) -> tuple[IndicatorStep, ...]:
    seen: set[str] = set()
    ordered: list[IndicatorStep] = []
    for step in sorted(steps, key=lambda item: item.order):
        if step.code not in seen:
            seen.add(step.code)
            ordered.append(step)
    return tuple(ordered)


def resolve_indicator_plan(intent: str, *, physical_data_available: bool = False) -> tuple[IndicatorStep, ...]:
    """Resolve quais indicadores consultar e em qual ordem.

    O resolvedor é fail-closed para disponibilidade física: indicadores que
    dependem de unidade física permanecem no plano como gates quando
    ``physical_data_available`` é False; consumidores devem retornar
    ``GAP_QUANTIDADE_FISICA`` em vez de calcular cobertura fictícia.
    """
    text = (intent or "").casefold()

    selected: list[IndicatorStep] = list(QUALITY_CONTEXT)

    # Toda pergunta de demanda inteligente começa pela demanda e comparabilidade.
    selected.extend(DEMAND)
    selected.extend(VARIATION)

    if any(term in text for term in ("pico", "alta", "subida", "queda", "crescimento", "redução", "variacao", "variação", "explica")):
        selected.extend(CAUSE)

    if any(term in text for term in ("retorno", "retorna", "devolução", "devolucao", "quarentena")):
        selected.extend(RETURN)

    if any(term in text for term in ("quarentena", "reparo", "liberação", "liberacao")):
        selected.extend(QUARANTINE)

    if any(term in text for term in ("estoque", "segurança", "seguranca", "proteção", "protecao", "reserva", "preparar", "preparação", "preparacao")):
        selected.extend(CAUSE)
        selected.extend(RETURN)
        selected.extend(STOCK_POLICY)

    coverage_or_availability = any(term in text for term in (
        "disponível", "disponivel", "disponibilidade", "cobertura",
        "capacidade de atendimento", "ruptura", "risco",
        "preparar", "preparação", "preparacao",
    ))
    if coverage_or_availability:
        # Cobertura depende de proteção comercial; disponibilidade depende do
        # fluxo físico de retorno/quarentena/liberação. Trazer pré-requisitos
        # evita responder uma razão sem o denominador governado.
        selected.extend(CAUSE)
        selected.extend(RETURN)
        selected.extend(QUARANTINE)
        selected.extend(STOCK_POLICY)
        selected.extend(AVAILABILITY)
        selected.extend(COVERAGE_RISK)

    # Explicitamente preserva os gates físicos no plano mesmo quando faltam dados.
    # Isso permite explicar por que a cadeia parou sem transformar ausência em zero.
    plan = _unique(selected)
    if physical_data_available:
        return plan
    return plan


def physical_gaps(plan: Iterable[IndicatorStep], *, physical_data_available: bool) -> tuple[str, ...]:
    """Retorna os códigos que devem falhar fechado por ausência de base física."""
    if physical_data_available:
        return ()
    return tuple(step.code for step in plan if step.physical_required)


def mandatory_dimensions() -> tuple[str, ...]:
    """Dimensões que não podem ser eliminadas na análise executiva."""
    return (
        "familia",
        "modelo",
        "cliente",
        "natureza_demanda",
        "mes",
        "ano",
        "data_proposta",
        "data_prevista_saida",
        "periodo",
        "data_retorno_prevista",
    )


def governance_invariants() -> tuple[str, ...]:
    return (
        "MÓDULO_CONTÊINER_SEPARADOS",
        "SPOT_EVENTO_SEPARADOS",
        "REGISTRO_EQUIVALENTE_NAO_E_UNIDADE_FISICA",
        "RETORNO_PREVISTO_NAO_E_ESTOQUE_LIVRE",
        "GAP_NAO_E_ZERO",
        "YOY_PRIORITARIO_PARA_COMPARABILIDADE",
        "MOM_COMPLEMENTAR",
        "CAUSA_EXIGE_EVIDENCIA",
    )
