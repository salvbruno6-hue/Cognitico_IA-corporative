from elo.agentic.contracts import IntentSpec, KnowledgeRequirement
from elo.agentic.supabase_memory_adapter import MEMORY_TABLES, SupabaseLearningMemoryAdapter


def test_inventory_is_explicit_and_contains_existing_memory_layers():
    names = {item.table for item in MEMORY_TABLES}
    assert "elo_experience_records" in names
    assert "elo_orcamento_memoria" in names
    assert "elo_reasoning_patterns" in names
    assert "elo_aprendizado_padroes_raciocinio" in names


def test_budget_requirement_resolves_existing_rows_without_mutation():
    rows = {
        "elo_orcamento_memoria": [
            {
                "memoria_id": "calc-1",
                "premissa": "PIR 40 mm",
                "confidence": 0.9,
                "status": "VALIDADO",
                "source_reference": "ORC-SRC-1",
                "scope": "GLOBAL",
            }
        ]
    }
    adapter = SupabaseLearningMemoryAdapter(rows)
    intent = IntentSpec(question="calcular", intent="budget", domain="orçamento", metadata={"scope": "GLOBAL"})
    requirement = KnowledgeRequirement("calculation_memory", "relevant calculation memory")

    result = adapter.retrieve(intent, requirement)

    assert len(result) == 1
    assert result[0].source_id == "supabase:elo_orcamento_memoria:calc-1"
    assert result[0].status == "GOVERNED"
    assert result[0].confidence == 0.9
    assert result[0].provenance["storage"] == "supabase"
    assert result[0].provenance["source_reference"] == "ORC-SRC-1"
    assert rows["elo_orcamento_memoria"][0]["premissa"] == "PIR 40 mm"


def test_unknown_requirement_is_not_guessed():
    adapter = SupabaseLearningMemoryAdapter({"elo_experience_records": [{"experience_id": "x"}]})
    intent = IntentSpec(question="x", intent="unknown", domain="x")

    assert adapter.retrieve(intent, KnowledgeRequirement("not_mapped", "unknown")) == ()


def test_scope_mismatch_is_excluded():
    adapter = SupabaseLearningMemoryAdapter(
        {
            "elo_orcamento_memoria": [
                {"memoria_id": "global", "scope": "GLOBAL", "premissa": "global"},
                {"memoria_id": "local", "scope": "CLIENT-A", "premissa": "local"},
            ]
        }
    )
    intent = IntentSpec(question="x", intent="budget", domain="orçamento", metadata={"scope": "CLIENT-A"})

    result = adapter.retrieve(intent, KnowledgeRequirement("calculation_memory", "memory"))

    assert [item.source_id for item in result] == ["supabase:elo_orcamento_memoria:local"]


def test_unscoped_non_global_record_is_excluded_from_scoped_request():
    adapter = SupabaseLearningMemoryAdapter(
        {
            "elo_orcamento_memoria": [
                {"memoria_id": "line-1", "premissa": "scopeless line"},
            ]
        }
    )
    intent = IntentSpec(question="x", intent="budget", domain="orçamento", metadata={"scope": "CLIENT-A"})

    result = adapter.retrieve(intent, KnowledgeRequirement("calculation_memory", "memory"))

    assert result == ()


def test_global_calculation_memory_can_be_reused_by_scoped_request():
    adapter = SupabaseLearningMemoryAdapter(
        {
            "elo_orcamento_memoria": [
                {"memoria_id": "global", "scope": "GLOBAL", "premissa": "global"},
            ]
        }
    )
    intent = IntentSpec(question="x", intent="budget", domain="orçamento", metadata={"scope": "CLIENT-A"})

    result = adapter.retrieve(intent, KnowledgeRequirement("calculation_memory", "memory"))

    assert [item.source_id for item in result] == ["supabase:elo_orcamento_memoria:global"]


def test_adapter_does_not_create_persistence_or_learning_promotion():
    adapter = SupabaseLearningMemoryAdapter({"elo_aprendizado_conceitos": [{"concept_id": "l1", "status": "PROVISORIO"}]})
    intent = IntentSpec(question="x", intent="x", domain="x")
    result = adapter.retrieve(intent, KnowledgeRequirement("standards", "standards"))

    assert result[0].status == "REFERENCE"
    assert "promotion" not in result[0].metadata
