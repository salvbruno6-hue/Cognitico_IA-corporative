from elo.agentic.context_assembly import ContextAssemblyPolicy, ELOContextAssembler
from elo.agentic.contracts import IntentSpec
from elo.agentic.supabase_memory_adapter import SupabaseLearningMemoryAdapter


def test_context_assembly_is_deterministic_and_deduplicated() -> None:
    rows = {
        "elo_orcament_calculation_memory": [
            {
                "calculation_memory_id": "cm-1",
                "premise": "base price",
                "scope": "GLOBAL",
                "confidence": 0.9,
                "status": "VALIDADO",
                "source_reference": "SRC-1",
            }
        ],
        "elo_orcament_run": [
            {
                "budget_run_id": "run-1",
                "result": "budget result",
                "scope": "GLOBAL",
                "confidence": 0.8,
                "status": "FINAL",
            }
        ],
    }
    adapter = SupabaseLearningMemoryAdapter(rows)
    assembler = ELOContextAssembler(adapter, ContextAssemblyPolicy(max_candidates=10))
    intent = IntentSpec(
        question="budget",
        intent="calculate",
        domain="orçamento",
        metadata={"scope": "GLOBAL"},
    )

    first = assembler.assemble(intent, ("calculation_memory", "current_requirements"))
    second = assembler.assemble(intent, ("calculation_memory", "current_requirements"))

    assert first == second
    assert [item.source_id for item in first.candidates] == [
        "supabase:elo_orcament_calculation_memory:cm-1",
        "supabase:elo_orcament_run:run-1",
    ]
    assert len({item.source_id for item in first.candidates}) == len(first.candidates)
    assert first.provenance["supabase:elo_orcament_calculation_memory:cm-1"]["source_reference"] == "SRC-1"


def test_context_assembly_preserves_scope_boundary() -> None:
    rows = {
        "elo_orcament_calculation_memory": [
            {
                "calculation_memory_id": "global-1",
                "premise": "global",
                "scope": "GLOBAL",
            },
            {
                "calculation_memory_id": "other-1",
                "premise": "other scope",
                "scope": "OTHER",
            },
        ]
    }
    adapter = SupabaseLearningMemoryAdapter(rows)
    intent = IntentSpec(
        question="budget",
        intent="calculate",
        domain="orçamento",
        metadata={"scope": "GLOBAL"},
    )

    context = ELOContextAssembler(adapter).assemble(intent, ("calculation_memory",))

    assert [item.source_id for item in context.candidates] == [
        "supabase:elo_orcament_calculation_memory:global-1"
    ]


def test_unknown_requirement_does_not_infer_a_source() -> None:
    adapter = SupabaseLearningMemoryAdapter({
        "elo_orcament_calculation_memory": [
            {"calculation_memory_id": "cm-1", "premise": "known"}
        ]
    })
    intent = IntentSpec(question="x", intent="x", domain="orçamento")

    context = ELOContextAssembler(adapter).assemble(intent, ("unknown_requirement",))

    assert context.candidates == ()
    assert context.gaps[0].key == "unknown_requirement"
    assert context.gaps[0].blocks_decision is True


def test_assembly_does_not_promote_or_mutate_source_rows() -> None:
    row = {"calculation_memory_id": "cm-1", "premise": "immutable"}
    rows = {"elo_orcament_calculation_memory": [row]}
    adapter = SupabaseLearningMemoryAdapter(rows)
    intent = IntentSpec(question="x", intent="x", domain="orçamento")

    context = ELOContextAssembler(adapter).assemble(intent, ("calculation_memory",))

    assert row == {"calculation_memory_id": "cm-1", "premise": "immutable"}
    assert all(candidate.metadata.get("promotion_state") is None for candidate in context.candidates)
