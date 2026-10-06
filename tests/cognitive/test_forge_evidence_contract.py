from elo.evidence import Evidence


def test_forge_evidence_uses_canonical_source_fields():
    evidence = Evidence.from_forge(
        tenant_id="tenant-a",
        source_table="modelos",
        source_domain="produtos",
        source_record_id="model-01",
        source_fields=("codigo", "nome", "ativo"),
        claim="M01 está ativo.",
        value={"codigo": "M01", "ativo": True},
    )

    assert evidence.source_system == "ELO Forge"
    assert evidence.source_schema == "public"
    assert evidence.source_table == "modelos"
    assert evidence.source_record_id == "model-01"
    assert evidence.source_domain == "produtos"
    assert evidence.source_fields == ("codigo", "nome", "ativo")
    assert evidence.value["ativo"] is True
    assert evidence.provenance["read_only"] is True
    assert evidence.provenance["guessed"] is False
