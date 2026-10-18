from pathlib import Path


PROBE = Path("supabase/health/elo_mt_repair_provenance_gap.sql")


def _source() -> str:
    return PROBE.read_text(encoding="utf-8").lower()


def test_repair_provenance_probe_is_read_only() -> None:
    source = _source()
    assert "authz_mt_repair_provenance_gap" in source
    assert "gap_high" in source
    assert "mt_proveniencia_registros" in source
    assert "mt_ordens_reparo" in source
    assert "mt_unidades_modulares" in source
    assert "public.modelos" in source

    for mutation in (
        "insert into ",
        "update public.",
        "delete from ",
        "alter table ",
        "create policy ",
        "alter policy ",
        "drop policy ",
        "grant ",
        "revoke ",
    ):
        assert mutation not in source


def test_repair_provenance_probe_requires_unit_or_provenance_reconciliation() -> None:
    source = _source()
    assert "repair_rows_without_unit > 0" in source
    assert "repair_rows_without_provenance > 0" in source
    assert "numero_container" in source
    assert "does not create provenance" in source


def test_repair_provenance_probe_exposes_identity_and_registry_readiness() -> None:
    source = _source()
    assert "mltm_numeric_id" in source
    assert "six_digit_id" in source
    assert "identifier_model_codes" in source
    assert "registered_identifier_model_codes" in source
    assert "modular_unit_rows" in source
    assert "regexp_replace" in source
