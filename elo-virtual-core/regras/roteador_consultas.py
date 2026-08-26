"""Roteamento determinístico das consultas de dados do ELO.

Este módulo identifica quando uma pergunta depende de dados persistidos no
Supabase Elo-forge. Ele não acessa o banco por conta própria; devolve a rota
para a camada de integração executar a consulta.
"""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CONFIG = BASE / "configuracoes" / "roteamento_dados.json"


def load_routing():
    with CONFIG.open(encoding="utf-8") as f:
        return json.load(f)


def route_query(query: str) -> dict:
    """Classifica a origem preferencial dos dados para uma consulta."""
    policy = load_routing()
    normalized = query.casefold()
    terms = policy["routing"]["supabase_when_related_to"]
    matches = [term for term in terms if term.casefold() in normalized]

    if matches:
        source = policy["sources"]["supabase_elo_forge"]
        return {
            "source": "supabase_elo_forge",
            "project_ref": source["project_ref"],
            "matched_terms": matches,
            "tables": source["tables"],
            "must_query_source": True,
        }

    return {
        "source": policy["routing"]["fallback"],
        "matched_terms": [],
        "must_query_source": False,
    }


if __name__ == "__main__":
    import sys

    query = " ".join(sys.argv[1:])
    print(json.dumps(route_query(query), ensure_ascii=False, indent=2))
