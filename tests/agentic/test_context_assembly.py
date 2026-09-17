from elo.agentic.context_assembly import ContextAssemblyPolicy, ELOContextAssembler
from elo.agentic.contracts import IntentSpec
from elo.agentic.supabase_memory_adapter import SupabaseLearningMemoryAdapter


def test_context_assembly_is_deterministic_and_deduplicated() -> None:
    rows = {
        "elo_orcamento_memoria": [{"memoria_id": "cm-1", "premissa": "base price", "scope": "GLOBAL", "confidence": 0.9, "status": "VALIDADO", "source_reference": "SRC-1"}],
        "elo_orcamentos": [{"orcamento_id": "run-1", "result": "budget result", "scope": "GLOBAL", "confidence": 0.8, "status": "FINAL"}],
    }
    adapter = SupabaseLearningMemoryAdapter(rows)
    assembler = ELOContextAssembler(adapter, ContextAssemblyPolicy(max_candidates=10))
    intent = IntentSpec(question="budget", intent="calculate", domain="orçamento", metadata={"scope": "GLOBAL"})

    first = assembler.assemble(intent, ("calculation_memory", "current_requirements"))
    second = assembler.assemble(intent, ("calculation_memory", "current_requirements"))

    assert first == second
    assert [item.source_id for item in first.candidates] == ["supabase:elo_orcamento_memoria:cm-1", "supabase:elo_orcamentos:run-1"]
    assert len({item.source_id for item in first.candidates}) == len(first.candidates)
    assert first.provenance["supabase:elo_orcamento_memoria:cm-1"]["source_reference"] == "SRC-1"


def test_context_assembly_preserves_scope_boundary() -> None:
    rows = {"elo_orcamento_memoria": [{"memoria_id": "global-1", "premissa": "global", "scope": "GLOBAL"}, {"memoria_id": "other-1", "premissa": "other scope", "scope": "OTHER"}]}
    adapter = SupabaseLearningMemoryAdapter(rows)
    intent = IntentSpec(question="budget", intent="calculate", domain="orçamento", metadata={"scope": "GLOBAL"})
    context = ELOContextAssembler(adapter).assemble(intent, ("calculation_memory",))
    assert [item.source_id for item in context.candidates] == ["supabase:elo_orcamento_memoria:global-1"]


def test_excess_context_includes_header_items_and_separate_labor() -> None:
    rows = {
        "excedentes": [{"id": "ex-1", "codigo_excedente": "EXC-001", "descricao": "Abertura adicional", "tipo_instalacao": "ESQUADRIA", "scope": "GLOBAL"}],
        "excedente_itens": [{"id": "item-1", "excedente_id": "ex-1", "cod_produt": "MAT-001", "descricao": "Perfil adicional", "tipo_componente": "MATERIAL", "scope": "GLOBAL"}],
        "excedente_mao_obra": [{"id": "labor-1", "excedente_id": "ex-1", "funcao": "Montador", "quantidade": 1, "tempo": 2, "scope": "GLOBAL"}],
    }
    adapter = SupabaseLearningMemoryAdapter(rows)
    intent = IntentSpec(question="excess", intent="assemble", domain="orçamento", metadata={"scope": "GLOBAL"})
    context = ELOContextAssembler(adapter).assemble(intent, ("excesses",))

    assert {item.source_id for item in context.candidates} == {"supabase:excedentes:ex-1", "supabase:excedente_itens:item-1", "supabase:excedente_mao_obra:labor-1"}
    assert {item.metadata["memory_role"] for item in context.candidates} == {"excess", "excess_item", "excess_labor"}
    assert context.provenance["supabase:excedente_itens:item-1"]["table"] == "excedente_itens"
    assert context.provenance["supabase:excedente_mao_obra:labor-1"]["table"] == "excedente_mao_obra"


def test_excess_inventory_exposes_verified_tables() -> None:
    inventory = {item.table for item in SupabaseLearningMemoryAdapter.inventory()}
    assert {"excedentes", "excedente_itens", "excedente_mao_obra"}.issubset(inventory)


def test_unknown_requirement_does_not_infer_a_source() -> None:
    adapter = SupabaseLearningMemoryAdapter({"elo_orcamento_memoria": [{"memoria_id": "cm-1", "premissa": "known"}]})
    intent = IntentSpec(question="x", intent="x", domain="orçamento")
    context = ELOContextAssembler(adapter).assemble(intent, ("unknown_requirement",))
    assert context.candidates == ()
    assert context.gaps[0].key == "unknown_requirement"
    assert context.gaps[0].blocks_decision is True


def test_unverified_budget_requirement_remains_unresolved():
    adapter = SupabaseLearningMemoryAdapter({"elo_orcamento_memoria": [{"memoria_id": "cm-1", "premissa": "known"}]})
    intent = IntentSpec(question="template", intent="calculate", domain="orçamento")
    context = ELOContextAssembler(adapter).assemble(intent, ("budget_template",))
    assert context.candidates == ()
    assert context.gaps[0].key == "budget_template"
    assert context.gaps[0].blocks_decision is True


def test_unverified_budget_lines_remain_unresolved():
    adapter = SupabaseLearningMemoryAdapter({"elo_orcamento_memoria": [{"memoria_id": "cm-1", "premissa": "known"}]})
    intent = IntentSpec(question="porta", intent="calculate", domain="orçamento")
    context = ELOContextAssembler(adapter).assemble(intent, ("budget_lines",))
    assert context.candidates == ()
    assert context.gaps[0].key == "budget_lines"
    assert context.gaps[0].blocks_decision is True


def test_assembly_does_not_promote_or_mutate_source_rows() -> None:
    row = {"memoria_id": "cm-1", "premissa": "immutable"}
    adapter = SupabaseLearningMemoryAdapter({"elo_orcamento_memoria": [row]})
    intent = IntentSpec(question="x", intent="x", domain="orçamento")
    context = ELOContextAssembler(adapter).assemble(intent, ("calculation_memory",))
    assert row == {"memoria_id": "cm-1", "premissa": "immutable"}
    assert all(candidate.metadata.get("promotion_state") is None for candidate in context.candidates)
