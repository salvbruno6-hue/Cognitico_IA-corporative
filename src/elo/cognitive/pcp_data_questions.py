"""Perguntas orientadas por lacunas de dados do PCP/Multiteiner.

Ausência de dado gera pergunta operacional; nunca gera inferência.
Este módulo é determinístico e não persiste dados nem cria decisões.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DataRequirement:
    key: str
    label: str
    table: str
    responsible_area: str
    impact: str
    question: str


@dataclass(frozen=True)
class DataGap:
    key: str
    label: str
    table: str
    responsible_area: str
    impact: str
    question: str
    priority: int


REQUIREMENTS: dict[str, tuple[DataRequirement, ...]] = {
    "atraso_op": (
        DataRequirement("quantidade_planejada", "Quantidade planejada", "mt_ordens_producao", "PCP", "Impede medir o desvio quantitativo.", "Qual é a quantidade planejada da OP?"),
        DataRequirement("quantidade_produzida", "Quantidade produzida", "mt_ordens_producao", "Produção", "Impede medir o realizado.", "Qual é a quantidade efetivamente produzida da OP?"),
        DataRequirement("fim_planejado", "Fim planejado", "mt_ordens_producao", "PCP", "Impede comparar o prazo planejado.", "Qual é a data de fim planejada da OP?"),
        DataRequirement("fim_real", "Fim real", "mt_ordens_producao", "Produção", "Impede comprovar a conclusão real.", "Qual foi a data/hora real de conclusão da OP?"),
    ),
    "capacidade_atendimento": (
        DataRequirement("demanda", "Demanda", "fonte_comercial", "Comercial", "Impede dimensionar o alvo.", "Qual é a quantidade demandada, por modelo/família e prazo?"),
        DataRequirement("capacidade_disponivel", "Capacidade disponível", "mt_capacidade_diaria", "PCP/Capacidade", "Impede confrontar demanda e capacidade.", "Qual é a capacidade disponível no período e centro de trabalho relevante?"),
        DataRequirement("estoque_disponivel", "Estoque disponível", "mt_lotes_estoque", "Almoxarifado", "Impede determinar a capacidade física disponível.", "Qual saldo físico disponível comprova o estoque?"),
    ),
    "material_op": (
        DataRequirement("quantidade_bruta", "Necessidade bruta", "mt_necessidades_materiais", "PCP/Suprimentos", "Impede dimensionar a necessidade.", "Qual é a quantidade bruta necessária para a OP?"),
        DataRequirement("quantidade_alocada", "Quantidade alocada", "mt_necessidades_materiais", "PCP/Suprimentos", "Impede saber quanto já está comprometido.", "Quanto do material já está alocado?"),
        DataRequirement("quantidade_comprada", "Quantidade comprada", "mt_necessidades_materiais", "Compras", "Impede avaliar cobertura por compra.", "Quanto do material foi efetivamente comprado?"),
        DataRequirement("quantidade_disponivel", "Estoque disponível", "mt_lotes_estoque", "Almoxarifado", "Impede confrontar necessidade com estoque físico.", "Qual quantidade está fisicamente disponível por lote/local?"),
    ),
    "atendimento_multiteiner": (
        DataRequirement("demanda", "Demanda comercial", "fonte_comercial", "Comercial", "Sem demanda não existe alvo de atendimento.", "Qual é a demanda, modelo/família, quantidade e prazo comprometido?"),
        DataRequirement("plano", "Plano PCP vigente", "mt_planos_pcp", "PCP", "Sem plano não há horizonte formal de planejamento.", "Qual plano PCP e versão estão vigentes para esse atendimento?"),
        DataRequirement("ordem_producao", "Ordem de produção", "mt_ordens_producao", "PCP", "Sem OP não é possível vincular a demanda à execução.", "Qual OP atende a demanda e qual sua quantidade/data planejada?"),
        DataRequirement("capacidade", "Capacidade disponível", "mt_capacidade_diaria", "PCP/Capacidade", "Sem capacidade não é possível testar a viabilidade operacional.", "Qual capacidade está disponível nos centros e datas relevantes?"),
        DataRequirement("material_necessidade", "Necessidade de material", "mt_necessidades_materiais", "PCP/Suprimentos", "Sem necessidade não é possível testar restrição de material.", "Quais materiais e quantidades são necessários para a OP?"),
        DataRequirement("estoque", "Estoque físico", "mt_lotes_estoque", "Almoxarifado", "Sem saldo físico não é possível medir cobertura material.", "Quais lotes e saldos disponíveis atendem às necessidades?"),
        DataRequirement("operacoes", "Operações planejadas", "mt_operacoes_ordem_producao", "Produção", "Sem roteiro operacional não é possível localizar restrições por etapa.", "Quais operações, sequências e quantidades estão planejadas?"),
        DataRequirement("eventos_reais", "Eventos de execução", "mt_eventos_fluxo_modular", "Produção/Operação", "Sem execução real não é possível confrontar plano com realizado.", "Quais eventos reais comprovam o andamento da OP/unidade?"),
    ),
}


def project_questions(target: str, available: dict[str, object]) -> tuple[DataGap, ...]:
    """Retorna perguntas dos requisitos ausentes, ordenadas por impacto no alvo."""
    gaps: list[DataGap] = []

    for index, req in enumerate(REQUIREMENTS.get(target, ()), start=1):
        value = available.get(req.key)
        if value is None or (isinstance(value, str) and not value.strip()):
            gaps.append(DataGap(
                key=req.key,
                label=req.label,
                table=req.table,
                responsible_area=req.responsible_area,
                impact=req.impact,
                question=req.question,
                priority=index,
            ))

    return tuple(gaps)


def analysis_status(target: str, available: dict[str, object]) -> str:
    """Bloqueia conclusão quando existir requisito ausente."""
    return "DADOS_INCOMPLETOS" if project_questions(target, available) else "DADOS_SUFICIENTES"


def merge_requirements(*targets: str) -> tuple[DataRequirement, ...]:
    """Compõe requisitos de vários alvos sem duplicar chaves."""
    result: list[DataRequirement] = []
    seen: set[str] = set()

    for target in targets:
        for req in REQUIREMENTS.get(target, ()):
            if req.key not in seen:
                result.append(req)
                seen.add(req.key)

    return tuple(result)
