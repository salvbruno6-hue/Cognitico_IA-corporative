"""Executor do harness cognitivo via linha de comando.

Roda uma fixture real do harness e imprime o report
estruturado. Não escreve em produção.

Uso:
    python scripts/run_cognitive_harness.py --list
    python scripts/run_cognitive_harness.py <fixture_name>

Fixtures em tests/cognitive/runtime/fixtures/harness_experiences.py

Refs: COGNITIVE_HARNESS.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))


def _load_fixtures_module():
    from tests.cognitive.runtime.fixtures import harness_experiences
    return harness_experiences


def _list_fixtures() -> list[str]:
    module = _load_fixtures_module()
    return sorted(module.ALL_FIXTURES.keys())


def _get_fixture(name: str):
    module = _load_fixtures_module()
    if name not in module.ALL_FIXTURES:
        raise ValueError(
            f"Fixture desconhecida: {name}. "
            f"Disponíveis: {', '.join(sorted(module.ALL_FIXTURES))}"
        )
    return module.ALL_FIXTURES[name]()


def _report_to_dict(fixture_name: str, report) -> dict:
    delta = report.delta or {}
    metrics = report.metrics or {}
    return {
        "fixture": fixture_name,
        "request_id": report.request_id,
        "stage_order": list(report.stage_order),
        "stages_completed": metrics.get("completed_stage_count"),
        "stages_error": metrics.get("error_stage_count"),
        "stages_skipped": metrics.get("skipped_stage_count"),
        "delta_summary": {
            "so_id": delta.get("so_id"),
            "aligned": len(delta.get("aligned", [])),
            "improvements": len(delta.get("improvements", [])),
            "corrections": len(delta.get("corrections", [])),
            "conflicts": len(delta.get("conflicts", [])),
            "overall_confidence": delta.get("overall_confidence"),
        },
        "directives": list(report.directives),
        "human_response": report.human_response,
        "isolated": report.isolated,
        "promotion_attempted": report.promotion_attempted,
        "governance_decision": report.governance_decision,
    }


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("--list", "-l"):
        print(json.dumps(_list_fixtures(), indent=2))
        return 0

    if len(sys.argv) < 2:
        print(
            "Uso: python scripts/run_cognitive_harness.py <fixture_name>",
            file=sys.stderr,
        )
        print("Fixtures disponíveis:", file=sys.stderr)
        for name in _list_fixtures():
            print(f"  - {name}", file=sys.stderr)
        return 1

    fixture_name = sys.argv[1]

    from elo.cognitive.runtime.cognitive_harness import CognitiveHarness

    try:
        fixture = _get_fixture(fixture_name)
    except ValueError as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2

    try:
        harness = CognitiveHarness()
        report = harness.run(fixture)
    except Exception as exc:
        print(f"ERRO ao executar fixture: {exc}", file=sys.stderr)
        return 3

    output = _report_to_dict(fixture_name, report)
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
