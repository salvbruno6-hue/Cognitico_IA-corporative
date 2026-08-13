from elo.core.context_resolution import ContextEvidence, ContextPack, ContextQuery, ContextSource
from elo.core.gpt_handoff import GPTDecisionHandoff
from elo.core.maturity_engine import MATURITY_DIMENSIONS, MaturityAssessment


def mature():
    return MaturityAssessment({dimension: 0.9 for dimension in MATURITY_DIMENSIONS})


def test_specialist_handoff_uses_resolved_scoped_context():
    context = ContextPack(
        query=ContextQuery(
            "qual o estado da Multiteiner Caxias?",
            "Multiteiner",
            "Duque de Caxias",
            ("operacao", "pcp", "risco"),
        ),
        discovery_plan=object(),
        sources=(ContextSource("caxias", "project", "authorized", "Duque de Caxias"),),
        evidence=(ContextEvidence("caxias", "pedido ativo", 0.9),),
    )
    handoff = GPTDecisionHandoff.from_context(
        objective="validar riscos sistêmicos", context=context, maturity=mature()
    )
    assert handoff.mode == "SPECIALIST_VALIDATION"
    assert handoff.context_entity == "Multiteiner"
    assert handoff.context_scope == "Duque de Caxias"
    assert handoff.evidence_ids == ("caxias",)
    assert handoff.dimensions_to_check == ("operacao", "pcp", "risco")
