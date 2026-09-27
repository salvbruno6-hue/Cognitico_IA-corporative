"""Executor do harness cognitivo via linha de comando.

Roda uma fixture real do harness e imprime o report
estruturado. Não escreve em produção.

Uso:
    python scripts/run_cognitive_harness.py <fixture_name>

Fixtures disponíveis em
tests/cognitive/runtime/fixtures/harness_experiences.py

Refs: COGNITIVE_HARNESS.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))


def _list_fixtures() -> list[str]:
    from tests.cognitive.runtime.fixtures.harness_experiences import (
        ALL_FIXTURES,
    )
    return sorted(ALL_FIXTURES.keys())


def _get_fixture(name: str):
    from tests.cognitive.runtime.fixtures.harness_experiences import (
        ALL_FIXTURES,
    )
    if name not in ALL_FIXTURES:
        raise ValueError(
            f"Fixture desconhecida: {name}. "
            f"Disponíveis: {', '.join(sorted(ALL_FIXTURES))}"
        )
    return ALL_FIXTURES[name]()


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("--list", "-l"):
        print(json.dumps(_list_fixtures(), indent=2))
        return 0

    if len(sys.argv) < 2:
        print("Uso: python scripts/run_cognitive_harness.py "
              "<fixture_name>", file=sys.stderr)
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

    harness = CognitiveHarness()
    report = harness.run(fixture)

    output = {
        "fixture": fixture_name,
        "status": report.status,
        "stages_executed": report.stages_executed,
        "final_state": report.final_state,
        "delta_summary": {
            "aligned": len((report.delta or {}).get("aligned", [])),
            "improvements": len((report.delta or {}).get("improvements", [])),
            "corrections": len((report.delta or {}).get("corrections", [])),
            "conflicts": len((report.delta or {}).get("conflicts", [])),
        } if report.delta else None,
        "directives": report.directives,
        "human_response": report.human_response,
        "escalation": report.escalation,
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
