from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ToolSchemaSelection:
    query: str
    selected_tools: tuple[str, ...]
    disclosed_schemas: tuple[tuple[str, str], ...]
    representation_chars: int
    bounded: bool = True
    executed: bool = False
    canonical_mutation: bool = False


def progressive_tool_schema_disclosure(query: str, tool_schemas: dict[str, str], *, limit: int = 5) -> ToolSchemaSelection:
    normalized = " ".join(str(query).lower().split())
    if not normalized:
        raise ValueError("query must be non-empty")
    if limit < 1:
        raise ValueError("limit must be positive")
    tokens = tuple(normalized.split())
    selected = []
    for name, schema in tool_schemas.items():
        if any(t in str(name).lower() or t in str(schema).lower() for t in tokens):
            selected.append((str(name), str(schema)))
            if len(selected) >= limit:
                break
    disclosed = tuple(selected)
    return ToolSchemaSelection(normalized, tuple(n for n, _ in disclosed), disclosed, sum(len(n)+len(s) for n,s in disclosed))
