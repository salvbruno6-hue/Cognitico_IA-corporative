from elo.agentic.context_assembly import ContextAssemblyPolicy, ELOContextAssembler
from elo.agentic.contracts import IntentSpec
from elo.agentic.supabase_memory_adapter import SupabaseLearningMemoryAdapter


def test_context_assembly_is_deterministic_and_deduplicated() -> None:
    rows = {
        "elo_orcamento_memoria": [
            {
                "memoria_id": "cm-1",
                "premissa": "base price",
                "scope": "GLOBAL",
                "confidence": 0.9,
                "status": "VALIDADO",
                "source_reference": "SRC-1",
            }
        ],
        "elo_orcamentos": [
            {
                "orcamento_id": "run-1",
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
        "supabase:elo_orcamento_memoria:cm-1",
        "supabase:elo_orcamentos:run-1",
    ]
    assert len({item.source_id for item in first.candidates}) == len(first.candidates)
    assert first.provenance["supabase:elo_orcamento_memoria:cm-1"]["source_reference"] == "SRC-1"


def test_context_assembly_preserves_scope_boundary() -> None:
    rows = {
        "elo_orcamento_memoria": [
            {
                "memoria_id": "global-1",
                "premissa": "global",
                "scope": "GLOBAL",
            },
            {
                "memoria_id": "other-1",
                "premissa": "other scope",
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
        "supabase:elo_orcamento_memoria:global-1"
    ]


def test_unknown_requirement_does_not_infer_a_source() -> None:
    adapter = SupabaseLearningMemoryAdapter(
        {"elo_orcamento_memoria": [{"memoria_id": "cm-1", "premissa": "known"}]}
    )
    intent = IntentSpec(question="x", intent="x", domain="orçamento")

    context = ELOContextAssembler(adapter).assemble(intent, ("unknown_requirement",))

    assert context.candidates == ()
    assert context.gaps[0].key == "unknown_requirement"
    assert context.gaps[0].blocks_decision is True


def test_unverified_budget_requirement_remains_unresolved():
    adapter = SupabaseLearningMemoryAdapter(
        {"elo_orcamento_memoria": [{"memoria_id": "cm-1", "premissa": "known"}]}
    )
    intent = IntentSpec(question="template", intent="calculate", domain="orçamento")

    context = ELOContextAssembler(adapter).assemble(intent, ("budget_template",))

    assert context.candidates == ()
    assert context.gaps[0].key == "budget_template"
    assert context.gaps[0].blocks_decision is True


def test_unverified_budget_lines_remain_unresolved():
    adapter = SupabaseLearningMemoryAdapter(
        {"elo_orcamento_memoria": [{"memoria_id": "cm-1", "premissa": "known"}]}
    )
    intent = IntentSpec(question="porta", intent="calculate", domain="orçamento")

    context = ELOContextAssembler(adapter).assemble(intent, ("budget_lines",))

    assert context.candidates == ()
    assert context.gaps[0].key == "budget_lines"
    assert context.gaps[0].blocks_decision is True


def test_assembly_does_not_promote_or_mutate_source_rows() -> None:
    row = {"memoria_id": "cm-1", "premissa": "immutable"}
    rows = {"elo_orcamento_memoria": [row]}
    adapter = SupabaseLearningMemoryAdapter(rows)
    intent = IntentSpec(question="x", intent="x", domain="orçamento")

    context = ELOContextAssembler(adapter).assemble(intent, ("calculation_memory",))

    assert row == {"memoria_id": "cm-1", "premissa": "immutable"}
    assert all(candidate.metadata.get("promotion_state") is None for candidate in context.candidates)
