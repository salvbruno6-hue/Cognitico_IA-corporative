from scripts.solicitations_learning_consolidate import _extract_so


def test_extract_so_requires_complete_canonical_identity():
    assert _extract_so("Aprendizado da SO 001.27") == "SO 001.27"
    assert _extract_so("Aprendizado da SO 001") == ""
    assert _extract_so("Aprendizado da SO 000.27") == ""
    assert _extract_so("Aprendizado da SO 001.2027") == ""


def test_extract_so_uses_only_explicit_canonical_fallback():
    assert _extract_so("sem identidade", "SO_155_26") == "SO 155.26"
    assert _extract_so("sem identidade", "155") == ""
