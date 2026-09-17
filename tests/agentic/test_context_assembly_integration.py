from elo.agentic.context_assembly import ELOContextAssembler
from elo.agentic.contracts import IntentSpec
from elo.agentic.supabase_memory_adapter import SupabaseLearningMemoryAdapter


def test_context_assembly_is_scoped_deterministic_and_provenance_preserving():
    rows = {
        "elo_orcamento_memoria": [
            {"memoria_id": "cm-1", "scope": "tenant-a", "premissa": "PIR 40 mm", "confidence": 0.9, "source_reference": "SO-001"},
            {"memoria_id": "cm-2", "scope": "tenant-b", "premissa": "PIR 32 mm", "confidence": 1.0, "source_reference": "SO-002"},
        ]
    }
    adapter = SupabaseLearningMemoryAdapter(rows)
    assembler = ELOContextAssembler(adapter)
    intent = IntentSpec(question="budget PIR", intent="budget", active_context="SO-001", metadata={"scope": "tenant-a"})

    first = assembler.assemble(intent, ["calculation_memory", "calculation_memory"])
    second = assembler.assemble(intent, ["calculation_memory"])

    assert first == second
    assert [item.source_id for item in first.candidates] == ["supabase:elo_orcamento_memoria:cm-1"]
    assert first.provenance["supabase:elo_orcamento_memoria:cm-1"]["source_reference"] == "SO-001"
    assert all("cm-2" not in item.source_id for item in first.candidates)


def test_unknown_requirement_does_not_infer_a_source():
    adapter = SupabaseLearningMemoryAdapter({"elo_orcamentos": [{"orcamento_id": "run-1", "resultado": "ok"}]})
    assembler = ELOContextAssembler(adapter)
    intent = IntentSpec(question="budget", intent="budget", active_context="SO-001")

    context = assembler.assemble(intent, ["unknown_requirement"])

    assert context.candidates == ()
    assert context.gaps[0].key == "unknown_requirement"
    assert context.provenance == {}
