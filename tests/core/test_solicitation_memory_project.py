from scripts.solicitation_memory_project import build_projection, canonical_so, detect_localities


def test_canonical_so_accepts_variants():
    assert canonical_so("SO 120.26 - FUNBIO") == "120.26"
    assert canonical_so("SO: 120.26") == "120.26"
    assert canonical_so("Solicitação 120.26") == "120.26"
    assert canonical_so("SO 001.27") == "001.27"


def test_canonical_so_rejects_invalid_identity_without_rewriting_it():
    assert canonical_so("SO 000.27") is None
    assert canonical_so("SO 1.27") is None
    assert canonical_so("SO 001.2027") is None


def test_detect_localities_uses_explicit_aliases():
    assert detect_localities("CETA Boa Vista/RR") == ["BOA_VISTA_RR"]
    assert detect_localities("Macapá/AP e Lorena/SP") == ["LORENA_SP", "MACAPA_AP"]


def test_projection_groups_only_matching_solicitation():
    events = [
        {
            "source_id": "chat-1",
            "content": "SO 120.26 - FUNBIO: CETA Boa Vista/RR",
        },
        {
            "source_id": "chat-2",
            "content": "SO 120.26 - FUNBIO: CETA Macapá/AP",
        },
        {
            "source_id": "chat-other",
            "content": "SO 121.26 - OUTRO CLIENTE: CETA Boa Vista/RR",
        },
    ]
    projection = build_projection(events, "120.26")
    assert projection["event_count"] == 2
    assert [item["id"] for item in projection["localities"]] == ["BOA_VISTA_RR", "MACAPA_AP"]
    assert "chat-other" not in projection["source_events"]


def test_projection_preserves_leading_zero_in_storage_key():
    projection = build_projection(
        [{"source_id": "chat-1", "content": "SO 001.27"}],
        "001.27",
    )
    assert projection["canonical_key"] == "SO_001_27"
