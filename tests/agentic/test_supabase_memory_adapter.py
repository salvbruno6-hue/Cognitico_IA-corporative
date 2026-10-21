from elo.agentic.contracts import IntentSpec, KnowledgeRequirement
from elo.agentic.supabase_memory_adapter import MEMORY_TABLES, SupabaseLearningMemoryAdapter


def test_inventory_is_explicit_and_contains_existing_memory_layers():
    names = {item.table for item in MEMORY_TABLES}
    assert "elo_experience_records" in names
    assert "elo_orcamento_memoria" in names
    assert "elo_reasoning_patterns" in names
    assert "elo_aprendizado_padroes_raciocinio" in names
    assert {"excedentes", "excedente_itens", "excedente_mao_obra"}.issubset(names)


def test_budget_requirement_resolves_existing_rows_without_mutation():
    rows = {"elo_orcamento_memoria": [{"memoria_id": "calc-1", "premissa": "PIR 40 mm", "confidence": 0.9, "status": "VALIDADO", "source_reference": "ORC-SRC-1", "scope": "GLOBAL"}]}
    adapter = SupabaseLearningMemoryAdapter(rows)
    intent = IntentSpec(question="calcular", intent="budget", domain="orçamento", metadata={"scope": "GLOBAL"})
    result = adapter.retrieve(intent, KnowledgeRequirement("calculation_memory", "relevant calculation memory"))
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
    adapter = SupabaseLearningMemoryAdapter({"elo_orcamento_memoria": [{"memoria_id": "global", "scope": "GLOBAL", "premissa": "global"}, {"memoria_id": "local", "scope": "CLIENT-A", "premissa": "local"}]})
    intent = IntentSpec(question="x", intent="budget", domain="orçamento", metadata={"scope": "CLIENT-A"})
    result = adapter.retrieve(intent, KnowledgeRequirement("calculation_memory", "memory"))
    assert [item.source_id for item in result] == ["supabase:elo_orcamento_memoria:local"]


def test_unscoped_non_global_record_is_excluded_from_scoped_request():
    adapter = SupabaseLearningMemoryAdapter({"elo_orcamento_memoria": [{"memoria_id": "line-1", "premissa": "scopeless line"}]})
    intent = IntentSpec(question="x", intent="budget", domain="orçamento", metadata={"scope": "CLIENT-A"})
    result = adapter.retrieve(intent, KnowledgeRequirement("calculation_memory", "memory"))
    assert result == ()


def test_global_record_is_not_reused_across_a_scoped_request():
    adapter = SupabaseLearningMemoryAdapter({"elo_orcamento_memoria": [{"memoria_id": "global", "scope": "GLOBAL", "premissa": "global"}]})
    intent = IntentSpec(question="x", intent="budget", domain="orçamento", metadata={"scope": "CLIENT-A"})
    result = adapter.retrieve(intent, KnowledgeRequirement("calculation_memory", "memory"))
    assert result == ()


def test_adapter_does_not_create_persistence_or_learning_promotion():
    adapter = SupabaseLearningMemoryAdapter({"elo_aprendizado_conceitos": [{"concept_id": "l1", "status": "PROVISORIO"}]})
    intent = IntentSpec(question="x", intent="x", domain="x")
    result = adapter.retrieve(intent, KnowledgeRequirement("standards", "standards"))
    assert result[0].status == "REFERENCE"
    assert "promotion" not in result[0].metadata


def test_real_learning_statuses_remain_reference():
    rows = {
        "elo_aprendizado_experiencias": [
            {"id": "candidate", "objetivo": "candidate", "status_validacao": "CANDIDATA"},
            {"id": "observed", "objetivo": "observed", "status_validacao": "OBSERVADA"},
        ]
    }
    adapter = SupabaseLearningMemoryAdapter(rows)
    intent = IntentSpec(question="x", intent="x", domain="x")
    result = adapter.retrieve(intent, KnowledgeRequirement("requirements", "requirements"))
    assert {item.source_id: item.status for item in result} == {
        "supabase:elo_aprendizado_experiencias:candidate": "REFERENCE",
        "supabase:elo_aprendizado_experiencias:observed": "REFERENCE",
    }


def test_budget_memory_requires_merged_approval_for_validated_learning():
    rows = {
        "elo_orcamento_memoria": [
            {
                "id": "candidate",
                "premissa": "candidate",
                "classificacao": "LEARNING_CANDIDATE",
                "status_conceito": "CANDIDATO",
                "decisao_governanca": "VALIDAR",
                "origem_so": "SO 182.26",
            },
            {
                "id": "precedent",
                "premissa": "precedent",
                "classificacao": "PRECEDENT",
                "status_conceito": "VALIDADA",
                "decisao_governanca": "DETERMINADA",
                "origem_so": "SO 178.26",
            },
            {
                "id": "validated",
                "premissa": "validated",
                "classificacao": "VALIDATED_LEARNING",
                "status_conceito": "VALIDATED_LEARNING",
                "decisao_governanca": "MERGED_APPROVED",
                "origem_so": "SO 178.26",
                "origem_documento": "PTS Pós-Orçamento",
            },
            {
                "id": "legacy-conflict",
                "premissa": "legacy",
                "classificacao": "VALIDATED_LEARNING",
                "status_conceito": "ATIVO",
                "decisao_governanca": "DETERMINADA",
                "origem_so": "SO 178.26",
            },
            {
                "id": "inactive",
                "premissa": "inactive",
                "classificacao": "VALIDATED_LEARNING",
                "status_conceito": "INATIVO",
                "decisao_governanca": "MERGED_APPROVED",
                "origem_so": "SO 178.26",
            },
        ]
    }
    adapter = SupabaseLearningMemoryAdapter(rows)
    intent = IntentSpec(question="x", intent="budget", domain="orçamento")
    result = adapter.retrieve(intent, KnowledgeRequirement("calculation_memory", "memory"))
    by_id = {item.source_id.rsplit(":", 1)[-1]: item for item in result}

    assert by_id["candidate"].status == "REFERENCE"
    assert by_id["precedent"].status == "REFERENCE"
    assert by_id["validated"].status == "GOVERNED"
    assert by_id["legacy-conflict"].status == "CONFLICTING"
    assert by_id["inactive"].status == "OUTDATED"
    assert by_id["validated"].provenance["origin_so"] == "SO 178.26"
    assert by_id["validated"].provenance["origin_document"] == "PTS Pós-Orçamento"


def test_governance_text_alone_cannot_promote_memory():
    adapter = SupabaseLearningMemoryAdapter(
        {
            "elo_orcamento_memoria": [
                {
                    "id": "not-promoted",
                    "premissa": "x",
                    "decisao_governanca": "MERGED_APPROVED",
                }
            ]
        }
    )
    intent = IntentSpec(question="x", intent="budget", domain="orçamento")
    result = adapter.retrieve(intent, KnowledgeRequirement("calculation_memory", "memory"))
    assert result[0].status == "UNVERIFIED"


def test_concept_validation_marker_requires_merged_governance_evidence():
    rows = {
        "elo_orcamento_memoria": [
            {
                "id": "legacy-concept",
                "premissa": "legacy concept status",
                "status_conceito": "VALIDADA",
                "decisao_governanca": "DETERMINADA",
            },
            {
                "id": "merged-concept",
                "premissa": "merged concept status",
                "status_conceito": "VALIDADA",
                "decisao_governanca": "MERGED_APPROVED",
            },
        ]
    }
    adapter = SupabaseLearningMemoryAdapter(rows)
    intent = IntentSpec(question="x", intent="budget", domain="orçamento")
    result = adapter.retrieve(intent, KnowledgeRequirement("calculation_memory", "memory"))
    by_id = {item.source_id.rsplit(":", 1)[-1]: item.status for item in result}

    assert by_id["legacy-concept"] == "REFERENCE"
    assert by_id["merged-concept"] == "GOVERNED"
