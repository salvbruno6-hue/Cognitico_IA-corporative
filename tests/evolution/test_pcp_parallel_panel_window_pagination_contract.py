from pathlib import Path


MIGRATION = Path(
    "supabase/migrations/20261029020500_pcp_fluxo_paralelo_paginacao_paineis_esquadrias.sql"
)


def _sql() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def test_parallel_flow_is_model_dependent_and_not_module_total_only():
    sql = _sql()
    assert "PAGINACAO_PAINEIS_ESQUADRIAS" in sql
    assert "mix_modelos" in sql
    assert "não usar total de módulos como multiplicador universal" in sql


def test_parallel_flow_requires_governed_pagination_before_definitive_calculation():
    sql = _sql()
    assert "paginacao_vigente" in sql
    assert "bom_ou_projeto_vigente" in sql
    assert "PAGINACAO_NAO_LOCALIZADA" in sql
    assert "não inventar paginação ausente" in sql


def test_panel_opening_window_and_door_entities_are_not_silently_collapsed():
    sql = _sql()
    assert "painel preparado para vão, esquadria e kit de porta permanecem entidades distintas" in sql
    assert "não confundir kit de porta com porta completa" in sql


def test_parallel_flow_reuses_lista_mae_and_creates_no_new_operational_table():
    sql = _sql().lower()
    assert "lista_mae" in sql
    assert "create table" not in sql
    assert "create view" not in sql


def test_parallel_flow_participates_in_systemic_capacity_and_first_constraint_date():
    sql = _sql()
    assert "'participa_capacidade_sistemica',true" in sql
    assert "'participa_first_constraint_date',true" in sql
    assert "somente com necessidade e disponibilidade comprovadas por modelo" in sql


def test_knowledge_remains_candidate_and_is_not_auto_promoted():
    sql = _sql()
    assert "'CANDIDATO'" in sql
    assert "CANDIDATO_NAO_PROMOVIDO" in sql
    assert "'VALIDADO'" not in sql
