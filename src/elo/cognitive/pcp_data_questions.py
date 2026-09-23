"""Governança de suficiência de dados orientada à meta do PCP.

Ausência de dado não autoriza inferência e, por si só, não bloqueia uma
resposta quando os dados disponíveis são suficientes para parte ou para todo
o objetivo. Este módulo é determinístico e não persiste dados.
"""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class DataRequirement:
    key: str
    label: str
    table: str
    responsible_area: str
    impact: str
    question: str
    requirement_type: str = "CONDICIONAL"


@dataclass(frozen=True)
class DataGap:
    key: str
    label: str
    table: str
    responsible_area: str
    impact: str
    question: str
    priority: int
    requirement_type: str
    blocking: bool


@dataclass(frozen=True)
class GoalAssessment:
    target: str
    requirements: tuple[DataRequirement, ...]
    located: tuple[str, ...]
    absent: tuple[str, ...]
    essential: tuple[str, ...]
    conditional: tuple[str, ...]
    complementary: tuple[str, ...]
    blocking: tuple[str, ...]
    satisfied_groups: tuple[tuple[str, ...], ...]
    unsatisfied_groups: tuple[tuple[str, ...], ...]
    status: str
    level: str
    next_evidence: tuple[str, ...]


REQUIREMENTS: dict[str, tuple[DataRequirement, ...]] = {
    "atraso_op": (
        DataRequirement("quantidade_planejada", "Quantidade planejada", "mt_ordens_producao", "PCP", "Permite medir o plano quantitativo.", "Qual é a quantidade planejada da OP?", "ESSENCIAL"),
        DataRequirement("quantidade_produzida", "Quantidade produzida", "mt_ordens_producao", "Produção", "Permite medir o realizado.", "Qual é a quantidade efetivamente produzida da OP?", "ESSENCIAL"),
        DataRequirement("fim_planejado", "Fim planejado", "mt_ordens_producao", "PCP", "Permite medir o prazo planejado.", "Qual é a data de fim planejada da OP?", "ESSENCIAL"),
        DataRequirement("fim_real", "Fim real", "mt_ordens_producao", "Produção", "Permite comprovar o prazo realizado.", "Qual foi a data/hora real de conclusão da OP?", "ESSENCIAL"),
    ),
    "capacidade_atendimento": (
        DataRequirement("demanda", "Demanda", "fonte_comercial", "Comercial", "Define o alvo de atendimento.", "Qual é a quantidade demandada, por modelo/família e prazo?", "ESSENCIAL"),
        DataRequirement("capacidade_disponivel", "Capacidade disponível", "mt_capacidade_diaria", "PCP/Capacidade", "Permite confrontar demanda e capacidade.", "Qual é a capacidade disponível no período e centro de trabalho relevante?", "ESSENCIAL"),
        DataRequirement("estoque_disponivel", "Estoque disponível", "mt_lotes_estoque", "Almoxarifado", "Aprofunda a capacidade física efetivamente disponível.", "Qual saldo físico disponível comprova o estoque?", "COMPLEMENTAR"),
    ),
    "material_op": (
        DataRequirement("quantidade_bruta", "Necessidade bruta", "mt_necessidades_materiais", "PCP/Suprimentos", "Permite dimensionar a necessidade.", "Qual é a quantidade bruta necessária para a OP?", "ESSENCIAL"),
        DataRequirement("quantidade_alocada", "Quantidade alocada", "mt_necessidades_materiais", "PCP/Suprimentos", "Permite identificar material já comprometido.", "Quanto do material já está alocado?", "CONDICIONAL"),
        DataRequirement("quantidade_comprada", "Quantidade comprada", "mt_necessidades_materiais", "Compras", "Permite avaliar cobertura por compra.", "Quanto do material foi efetivamente comprado?", "CONDICIONAL"),
        DataRequirement("quantidade_disponivel", "Estoque disponível", "mt_lotes_estoque", "Almoxarifado", "Permite confrontar necessidade com estoque físico.", "Qual quantidade está fisicamente disponível por lote/local?", "ESSENCIAL"),
    ),
    "atendimento_multiteiner": (
        DataRequirement("demanda", "Demanda comercial", "fonte_comercial", "Comercial", "Define o alvo de atendimento.", "Qual é a demanda, modelo/família, quantidade e prazo comprometido?", "ESSENCIAL"),
        DataRequirement("plano", "Plano PCP vigente", "mt_planos_pcp", "PCP", "Formaliza o horizonte de planejamento.", "Qual plano PCP e versão estão vigentes para esse atendimento?", "CONDICIONAL"),
        DataRequirement("ordem_producao", "Ordem de produção", "mt_ordens_producao", "PCP", "Vincula demanda à execução.", "Qual OP atende a demanda e qual sua quantidade/data planejada?", "CONDICIONAL"),
        DataRequirement("capacidade", "Capacidade disponível", "mt_capacidade_diaria", "PCP/Capacidade", "Testa viabilidade operacional.", "Qual capacidade está disponível nos centros e datas relevantes?", "ESSENCIAL"),
        DataRequirement("material_necessidade", "Necessidade de material", "mt_necessidades_materiais", "PCP/Suprimentos", "Testa restrição de material.", "Quais materiais e quantidades são necessários para a OP?", "CONDICIONAL"),
        DataRequirement("estoque", "Estoque físico", "mt_lotes_estoque", "Almoxarifado", "Mede cobertura material.", "Quais lotes e saldos disponíveis atendem às necessidades?", "CONDICIONAL"),
        DataRequirement("operacoes", "Operações planejadas", "mt_operacoes_ordem_producao", "Produção", "Localiza restrições por etapa.", "Quais operações, sequências e quantidades estão planejadas?", "CONDICIONAL"),
        DataRequirement("eventos_reais", "Eventos de execução", "mt_eventos_fluxo_modular", "Produção/Operação", "Permite confrontar plano com realizado.", "Quais eventos reais comprovam o andamento da OP/unidade?", "CONDICIONAL"),
    ),
}


# Cada grupo representa um caminho analítico mínimo. A meta pode ter mais de
# um grupo: satisfazer um deles permite responder parcialmente; satisfazer
# todos permite fechar a meta definida para o alvo.
ESSENTIAL_GROUPS: dict[str, tuple[tuple[str, ...], ...]] = {
    "atraso_op": (
        ("quantidade_planejada", "quantidade_produzida"),
        ("fim_planejado", "fim_real"),
    ),
    "capacidade_atendimento": (
        ("demanda", "capacidade_disponivel"),
    ),
    "material_op": (
        ("quantidade_bruta",),
        ("quantidade_bruta", "quantidade_disponivel"),
    ),
    "atendimento_multiteiner": (
        ("demanda", "capacidade"),
    ),
}


def _present(value: object) -> bool:
    return value is not None and not (isinstance(value, str) and not value.strip())


def _satisfied(group: tuple[str, ...], available: dict[str, object]) -> bool:
    return all(_present(available.get(key)) for key in group)


def evaluate_goal(target: str, available: dict[str, object]) -> GoalAssessment:
    """Avalia suficiência para a meta, sem exigir completude do banco."""
    requirements = REQUIREMENTS.get(target, ())
    located = tuple(req.key for req in requirements if _present(available.get(req.key)))
    absent = tuple(req.key for req in requirements if req.key not in located)
    essential = tuple(req.key for req in requirements if req.requirement_type == "ESSENCIAL")
    conditional = tuple(req.key for req in requirements if req.requirement_type == "CONDICIONAL")
    complementary = tuple(req.key for req in requirements if req.requirement_type == "COMPLEMENTAR")

    groups = ESSENTIAL_GROUPS.get(target, ())
    satisfied = tuple(group for group in groups if _satisfied(group, available))
    unsatisfied = tuple(group for group in groups if not _satisfied(group, available))
    blocking = tuple(key for group in unsatisfied for key in group if not _present(available.get(key)))

    if not requirements:
        status = "ANALISE_BLOQUEADA"
        level = "S0"
    elif not satisfied:
        status = "DADOS_NAO_LOCALIZADOS" if not located else "ANALISE_BLOQUEADA"
        level = "S0"
    elif len(satisfied) < len(groups):
        status = "RESPOSTA_PARCIAL"
        level = "S1"
    else:
        status = "DADOS_SUFICIENTES"
        level = "S2"

    # A próxima evidência é o menor conjunto ausente que fecha um grupo.
    candidates = [tuple(k for k in group if not _present(available.get(k))) for group in unsatisfied]
    candidates = [c for c in candidates if c]
    next_evidence = min(candidates, key=lambda c: (len(c), c)) if candidates else ()

    return GoalAssessment(
        target=target,
        requirements=requirements,
        located=located,
        absent=absent,
        essential=essential,
        conditional=conditional,
        complementary=complementary,
        blocking=blocking,
        satisfied_groups=satisfied,
        unsatisfied_groups=unsatisfied,
        status=status,
        level=level,
        next_evidence=next_evidence,
    )


def project_questions(target: str, available: dict[str, object]) -> tuple[DataGap, ...]:
    """Retorna somente lacunas relevantes para avançar a meta."""
    assessment = evaluate_goal(target, available)
    missing = set(assessment.absent)
    gaps: list[DataGap] = []

    for index, req in enumerate(assessment.requirements, start=1):
        if req.key in missing:
            gaps.append(DataGap(
                key=req.key,
                label=req.label,
                table=req.table,
                responsible_area=req.responsible_area,
                impact=req.impact,
                question=req.question,
                priority=index,
                requirement_type=req.requirement_type,
                blocking=req.key in assessment.blocking,
            ))

    return tuple(gaps)


def analysis_status(target: str, available: dict[str, object]) -> str:
    """Retorna o estado orientado à meta, não a completude das fontes."""
    return evaluate_goal(target, available).status


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


def available_keys(values: Iterable[str]) -> dict[str, bool]:
    """Converte chaves explicitamente disponíveis em mapa de presença."""
    return {key: True for key in values}
