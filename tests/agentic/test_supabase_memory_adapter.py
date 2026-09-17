from elo.agentic.contracts import IntentSpec, KnowledgeRequirement
from elo.agentic.supabase_memory_adapter import MEMORY_TABLES, SupabaseLearningMemoryAdapter


def test_inventory_is_explicit_and_contains_existing_memory_layers():
    names = {item.table for item in MEMORY_TABLES}
    assert "elo_experience_record" in names
    assert "elo_corporate_learning" in names
    assert "elo_orcament_calculation_memory" in names
    assert "elo_quality_nonconformity" in names
    assert "elo_pcp_mrp_necessidade" in names


def test_budget_requirement_resolves_existing_rows_without_mutation():
    rows = {
        "elo_orcament_calculation_memory": [
            {
                "calculation_memory_id": "calc-1",
                "premise": "PIR 40 mm",
                "confidence": 0.9,
                "status": "VALIDADO",
                "source_reference": "SO-001",
            }
        ]
    }
    adapter = SupabaseLearningMemoryAdapter(rows)
    intent = IntentSpec(question="calcular", intent="budget", domain="orçamento", metadata={"scope": "GLOBAL"})
    requirement = KnowledgeRequirement("calculation_memory", "relevant calculation memory")

    result = adapter.retrieve(intent, requirement)

    assert len(result) == 1
    assert result[0].source_id == "supabase:elo_orcament_calculation_memory:calc-1"
    assert result[0].status == "GOVERNED"
    assert result[0].confidence == 0.9
    assert result[0].provenance["storage"] == "supabase"
    assert result[0].provenance["source_reference"] == "SO-001"
    assert rows["elo_orcament_calculation_memory"][0]["premise"] == "PIR 40 mm"


def test_unknown_requirement_is_not_guessed():
    adapter = SupabaseLearningMemoryAdapter({"elo_experience_record": [{"experience_id": "x"}]})
    intent = IntentSpec(question="x", intent="unknown", domain="x")

    assert adapter.retrieve(intent, KnowledgeRequirement("not_mapped", "unknown")) == ()


def test_global_memory_is_reused_by_scoped_request():
    adapter = SupabaseLearningMemoryAdapter(
        {
            "elo_orcament_calculation_memory": [
                {"calculation_memory_id": "global", "scope": "GLOBAL", "premise": "global"},
                {"calculation_memory_id": "local", "scope": "CLIENT-A", "premise": "local"},
            ]
        }
    )
    intent = IntentSpec(question="x", intent="budget", domain="orçamento", metadata={"scope": "CLIENT-A"})

    result = adapter.retrieve(intent, KnowledgeRequirement("calculation_memory", "memory"))

    assert [item.source_id for item in result] == [
        "supabase:elo_orcament_calculation_memory:global",
        "supabase:elo_orcament_calculation_memory:local",
    ]


def test_client_scoped_memory_is_not_reused_across_clients():
    adapter = SupabaseLearningMemoryAdapter(
        {
            "elo_orcament_calculation_memory": [
                {"calculation_memory_id": "global", "scope": "GLOBAL", "premise": "global"},
                {"calculation_memory_id": "client-a", "scope": "CLIENT-A", "premise": "client a"},
                {"calculation_memory_id": "client-b", "scope": "CLIENT-B", "premise": "client b"},
            ]
        }
    )
    intent = IntentSpec(question="x", intent="budget", domain="orçamento", metadata={"scope": "CLIENT-A"})

    result = adapter.retrieve(intent, KnowledgeRequirement("calculation_memory", "memory"))

    assert [item.source_id for item in result] == [
        "supabase:elo_orcament_calculation_memory:global",
        "supabase:elo_orcament_calculation_memory:client-a",
    ]


def test_unscoped_row_is_not_reused_by_scoped_request():
    adapter = SupabaseLearningMemoryAdapter(
        {
            "elo_orcament_calculation_memory": [
                {"calculation_memory_id": "unscoped", "premise": "unscoped"},
                {"calculation_memory_id": "global", "scope": "GLOBAL", "premise": "global"},
            ]
        }
    )
    intent = IntentSpec(question="x", intent="budget", domain="orçamento", metadata={"scope": "CLIENT-A"})

    result = adapter.retrieve(intent, KnowledgeRequirement("calculation_memory", "memory"))

    assert [item.source_id for item in result] == [
        "supabase:elo_orcament_calculation_memory:global",
    ]


def test_unscoped_request_does_not_pull_client_scoped_memory():
    adapter = SupabaseLearningMemoryAdapter(
        {
            "elo_orcament_calculation_memory": [
                {"calculation_memory_id": "unscoped", "premise": "unscoped"},
                {"calculation_memory_id": "global", "scope": "GLOBAL", "premise": "global"},
                {"calculation_memory_id": "client-a", "scope": "CLIENT-A", "premise": "client a"},
            ]
        }
    )
    intent = IntentSpec(question="x", intent="budget", domain="orçamento")

    result = adapter.retrieve(intent, KnowledgeRequirement("calculation_memory", "memory"))

    assert [item.source_id for item in result] == [
        "supabase:elo_orcament_calculation_memory:unscoped",
        "supabase:elo_orcament_calculation_memory:global",
    ]


def test_adapter_does_not_create_persistence_or_learning_promotion():
    adapter = SupabaseLearningMemoryAdapter({"elo_corporate_learning": [{"learning_id": "l1", "status": "PROVISORIO"}]})
    intent = IntentSpec(question="x", intent="x", domain="x")
    result = adapter.retrieve(intent, KnowledgeRequirement("standards", "standards"))

    assert result[0].status == "REFERENCE"
    assert "promotion" not in result[0].metadata
