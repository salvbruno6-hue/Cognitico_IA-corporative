"""Render a read-only analysis view for waiting Hermes candidates."""
from __future__ import annotations

from typing import Any
from elo.agent_intake.hermes_context_plugin_evaluation import evaluate_context_plugin_candidate
from elo.agent_intake.hermes_worktree_evaluation import evaluate as evaluate_worktree
from elo.agent_intake.hermes_multiagent_evaluation import evaluate as evaluate_multiagent
from elo.agent_intake.hermes_cron_evaluation import evaluate as evaluate_cron

def _row(candidate_id: str, owner: str, metric: str, result: Any) -> dict[str, Any]:
    baseline = float(result.baseline_rate)
    adapted = float(result.adapted_rate)
    gain = round(adapted - baseline, 6)
    integrity = float(result.boundary_integrity_rate)
    risk = "LOW" if integrity == 1.0 else "HIGH"
    evolution = "POSITIVE" if gain > 0 else "REGRESSION" if gain < 0 else "STABLE/NO_GAIN"
    return {"candidate": candidate_id, "owner": owner, "metric": metric, "baseline": baseline, "current": adapted, "gain": gain, "evolution": evolution, "repeatable": bool(result.repeatable), "relationship": f"{candidate_id} extends existing owner {owner}", "risk": risk, "decision": result.result, "canonical_mutation": False}

def analyze_waiting_candidates() -> list[dict[str, Any]]:
    return [
        _row("EXT-CONTEXT-PLUGIN-HERMES", "ELO Context", "context task success rate", evaluate_context_plugin_candidate()),
        _row("EXT-WORKTREE-HERMES", "ELO Forge", "valid isolation recognition rate", evaluate_worktree()),
        _row("EXT-MULTIAGENT-HERMES", "ELO Agent Delegation", "valid delegation recognition rate", evaluate_multiagent()),
        _row("EXT-CRON-HERMES", "ELO Workflow/Automation", "authorized idempotent schedule recognition rate", evaluate_cron()),
    ]

def render_markdown(rows: list[dict[str, Any]]) -> str:
    ranked = sorted(rows, key=lambda r: (0 if r["risk"] == "HIGH" else 1, 0 if r["gain"] <= 0 else 1, 0 if not r["repeatable"] else 1, r["candidate"]))
    lines = ["# Hermes — View de Análise Pré-Teste", "", "**Natureza:** read-only; laboratório controlado; sem promoção; sem mutação canônica.", "", "## Ranking de prioridade de intervenção", "", "| Rank | Candidato | Owner | Ganho | Evolução | Risco | Repetível | Decisão |", "|---:|---|---|---:|---|---|---|---|"]
    for i, row in enumerate(ranked, 1):
        lines.append(f"| {i} | `{row["candidate"]}` | {row["owner"]} | {row["gain"]:.4f} | {row["evolution"]} | {row["risk"]} | {"SIM" if row["repeatable"] else "NÃO"} | `{row["decision"]}` |")
    lines += ["", "## Relação e risco", "", "| Candidato | Capacidade | Relação | Risco | Onde começar |", "|---|---|---|---|---|"]
    for row in ranked:
        start = "reproduzir baseline/adaptado e identificar a menor intervenção mensurável" if row["gain"] <= 0 else "repetir a mesma medição para confirmar durabilidade"
        lines.append(f"| `{row["candidate"]}` | {row["metric"]} | {row["relationship"]} | {row["risk"]} | {start} |")
    lines += ["", "## Regra", "", "`ANÁLISE → TESTE CONTROLADO → GANHO → REGRESSÃO → REPETIBILIDADE → EVOLUTION GATE → ELO REVIEW`", "", "O ranking representa prioridade de investigação/intervenção, não qualidade. Nenhuma linha autoriza merge, produção ou canonicalização."]
    return "\n".join(lines)

if __name__ == "__main__":
    print(render_markdown(analyze_waiting_candidates()))