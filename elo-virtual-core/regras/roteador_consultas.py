"""Roteamento determinístico das consultas de dados do ELO.

Este módulo identifica quando uma pergunta depende de dados persistidos na
camada Forge interna do ELO Cognitivo e devolve apenas o contrato necessário
para retrieval. Detalhes de infraestrutura (project_ref/project_id)
permanecem internos ao adaptador e nunca fazem parte da interface destinada
ao especialista.
"""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CONFIG = BASE / "configuracoes" / "roteamento_dados.json"


def load_routing():
    with CONFIG.open(encoding="utf-8") as f:
        return json.load(f)


def route_query(query: str) -> dict:
    """Classifica a origem preferencial e o contrato de retrieval.

    O resultado não expõe identificadores de infraestrutura do Supabase.
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query is required")

    policy = load_routing()
    normalized = query.casefold()
    terms = policy["routing"]["supabase_when_related_to"]
    matches = [term for term in terms if term.casefold() in normalized]

    if matches:
        source_key = "supabase_elo_forge"
        source = policy["sources"][source_key]
        return {
            "source": source_key,
            "layer": source.get("canonical_layer", "forge"),
            "architectural_parent": source.get("architectural_parent", "ELO Cognitivo"),
            "matched_terms": matches,
            "tables": source["tables"],
            "adapter": "integracoes.supabase_elo_forge",
            "retrieval_contract": "read_only_relationship_aware",
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
