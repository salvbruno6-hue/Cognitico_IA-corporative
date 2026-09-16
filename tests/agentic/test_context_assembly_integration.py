from elo.agentic.context_assembly import ELOContextAssembler
from elo.agentic.contracts import IntentSpec
from elo.agentic.supabase_memory_adapter import SupabaseLearningMemoryAdapter


def test_context_assembly_is_scoped_deterministic_and_provenance_preserving():
    rows = {
        "elo_orcament_calculation_memory": [
            {"calculation_memory_id": "cm-1", "scope": "tenant-a", "premise": "PIR 40 mm", "confidence": 0.9, "source_reference": "SO-001"},
            {"calculation_memory_id": "cm-2", "scope": "tenant-b", "premise": "PIR 32 mm", "confidence": 1.0, "source_reference": "SO-002"},
        ]
    }
    adapter = SupabaseLearningMemoryAdapter(rows)
    assembler = ELOContextAssembler(adapter)
    intent = IntentSpec(question="budget PIR", intent="budget", active_context="SO-001", metadata={"scope": "tenant-a"})

    first = assembler.assemble(intent, ["calculation_memory", "calculation_memory"])
    second = assembler.assemble(intent, ["calculation_memory"])

    assert first == second
    assert [item.source_id for item in first.candidates] == ["supabase:elo_orcament_calculation_memory:cm-1"]
    assert first.provenance["supabase:elo_orcament_calculation_memory:cm-1"]["source_reference"] == "SO-001"
    assert all("cm-2" not in item.source_id for item in first.candidates)


def test_unknown_requirement_does_not_infer_a_source():
    adapter = SupabaseLearningMemoryAdapter({"elo_orcament_run": [{"budget_run_id": "run-1", "result": "ok"}]})
    assembler = ELOContextAssembler(adapter)
    intent = IntentSpec(question="budget", intent="budget", active_context="SO-001")

    context = assembler.assemble(intent, ["unknown_requirement"])

    assert context.candidates == ()
    assert context.gaps[0].key == "unknown_requirement"
    assert context.provenance == {}
