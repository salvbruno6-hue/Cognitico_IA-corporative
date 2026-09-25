"""Render a read-only pre-test analysis for waiting Hermes candidates.

The view reuses the existing Evolution Gate. It does not create a Hermes-specific
anti-duplication authority and does not authorize implementation, production, or
canonicalization.
"""
from __future__ import annotations

from typing import Any

from elo.agent_intake.hermes_context_plugin_evaluation import evaluate_context_plugin_candidate
from elo.agent_intake.hermes_worktree_evaluation import evaluate as evaluate_worktree
from elo.agent_intake.hermes_multiagent_evaluation import evaluate as evaluate_multiagent
from elo.agent_intake.hermes_cron_evaluation import evaluate as evaluate_cron
from elo.core.evolution_gate import EvolutionGate, EvolutionProposal

_GATE = EvolutionGate()


def _governance_classification(candidate_id: str, owner: str, metric: str) -> tuple[str, str]:
    decision = _GATE.evaluate(
        EvolutionProposal(
            proposal_id=candidate_id,
            tenant_id="ELO",
            source_id=f"HERMES:{candidate_id}",
            summary=f"Evaluate {metric} against existing owner {owner}",
            purpose_alignment=True,
            identity_compatible=True,
            architecture_compatible=True,
            governance_compatible=True,
            evidence_ids=(f"candidate:{candidate_id}",),
            maturity_score=0.0,
            existing_owner=owner,
            provenance={
                "source": "hermes-candidate-analysis",
                "owner": owner,
                "authority": "existing-evolution-gate",
            },
        )
    )
    return decision.classification.value, decision.rationale


def _row(candidate_id: str, owner: str, metric: str, result: Any) -> dict[str, Any]:
    baseline_value = getattr(result, "baseline_rate", None)
    if baseline_value is None:
        baseline_value = getattr(result, "baseline_success_rate")
    baseline = float(baseline_value)

    adapted_value = getattr(result, "adapted_rate", None)
    if adapted_value is None:
        adapted_value = getattr(result, "adapted_success_rate")
    adapted = float(adapted_value)

    gain = round(adapted - baseline, 6)
    integrity = float(result.boundary_integrity_rate)
    risk = "LOW" if integrity == 1.0 else "HIGH"
    evolution = "POSITIVE" if gain > 0 else "REGRESSION" if gain < 0 else "STABLE/NO_GAIN"
    gate_classification, gate_rationale = _governance_classification(candidate_id, owner, metric)

    return {
        "candidate": candidate_id,
        "owner": owner,
        "metric": metric,
        "baseline": baseline,
        "current": adapted,
        "gain": gain,
        "evolution": evolution,
        "repeatable": bool(result.repeatable),
        "relationship": "EVOLVE_EXISTING_OWNER",
        "functional_overlap": "BOUNDED_BY_EXISTING_OWNER",
        "governance_classification": gate_classification,
        "governance_rationale": gate_rationale,
        "competition_allowed": False,
        "duplicate_risk": "CONTROLLED_BY_EXISTING_GATE",
        "supersession_candidate": False,
        "risk": risk,
        "decision": result.result,
        "canonical_mutation": False,
        "promotion_authorized": False,
    }


def analyze_waiting_candidates() -> list[dict[str, Any]]:
    return [
        _row(
            "EXT-CONTEXT-PLUGIN-HERMES",
            "ELO Context",
            "context task success rate",
            evaluate_context_plugin_candidate(),
        ),
        _row(
            "EXT-WORKTREE-HERMES",
            "ELO Forge",
            "valid isolation recognition rate",
            evaluate_worktree(),
        ),
        _row(
            "EXT-MULTIAGENT-HERMES",
            "ELO Agent Delegation",
            "valid delegation recognition rate",
            evaluate_multiagent(),
        ),
        _row(
            "EXT-CRON-HERMES",
            "ELO Workflow/Automation",
            "authorized idempotent schedule recognition rate",
            evaluate_cron(),
        ),
    ]


def render_markdown(rows: list[dict[str, Any]]) -> str:
    ranked = sorted(
        rows,
        key=lambda r: (
            0 if r["risk"] == "HIGH" else 1,
            0 if r["gain"] <= 0 else 1,
            0 if not r["repeatable"] else 1,
            r["candidate"],
        ),
    )
    lines = [
        "# Hermes — View de Análise Pré-Teste",
        "",
        "**Natureza:** read-only; análise antes do teste; sem promoção; sem mutação canônica.",
        "",
        "## Ranking de prioridade de intervenção",
        "",
        "O ranking ordena a prioridade de investigação/intervenção. Não é ranking de qualidade.",
        "",
        "| Rank | Candidato | Owner existente | Ganho | Evolução | Risco | Repetível | Decisão |",
        "|---:|---|---|---:|---|---|---|---|",
    ]
    for i, row in enumerate(ranked, 1):
        repeatable = "SIM" if row["repeatable"] else "NÃO"
        lines.append(
            f"| {i} | `{row['candidate']}` | {row['owner']} | "
            f"{row['gain']:.4f} | {row['evolution']} | {row['risk']} | "
            f"{repeatable} | `{row['decision']}` |"
        )

    lines += [
        "",
        "## Relação com o ELO existente",
        "",
        "| Candidato | Relação | Sobreposição | Evolution Gate | Concorrência | Risco de duplicidade | Substituição automática |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in ranked:
        lines.append(
            f"| `{row['candidate']}` | {row['relationship']} | "
            f"{row['functional_overlap']} | `{row['governance_classification']}` | "
            f"{'NÃO' if not row['competition_allowed'] else 'SIM'} | "
            f"{row['duplicate_risk']} | "
            f"{'NÃO' if not row['supersession_candidate'] else 'SIM'} |"
        )

    lines += [
        "",
        "## Onde começar",
        "",
        "| Candidato | Ação inicial | Evidência necessária |",
        "|---|---|---|",
    ]
    for row in ranked:
        if row["gain"] <= 0:
            start = "reproduzir baseline/adaptado e identificar a menor intervenção mensurável"
            evidence = "ganho mensurável + ausência de regressão"
        elif not row["repeatable"]:
            start = "repetir a mesma medição antes de avançar"
            evidence = "repetibilidade da mesma medição"
        else:
            start = "prosseguir para Evolution Gate/ELO Review dentro do owner existente"
            evidence = "ganho + repetibilidade + compatibilidade governada"
        lines.append(
            f"| `{row['candidate']}` | {start} | {evidence} |"
        )

    lines += [
        "",
        "## Regra reutilizada",
        "",
        "`CANDIDATO → OWNER EXISTENTE → EVOLUTION GATE → TESTE → EVIDÊNCIA → ELO REVIEW`",
        "",
        "Nenhum candidato Hermes pode competir com uma capacidade ELO existente. Quando há owner existente, o candidato é tratado como evolução/complemento sob esse owner; não recebe nova autoridade.",
        "",
        "O Evolution Gate existente é a autoridade de classificação. Não foi criado mecanismo Hermes paralelo.",
        "",
        "Nenhuma linha autoriza merge, produção, promoção ou canonicalização. A mutação canônica permanece dependente de atualização/autorização humana explícita.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(render_markdown(analyze_waiting_candidates()))
