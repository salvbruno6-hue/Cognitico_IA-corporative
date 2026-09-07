from pathlib import Path


def test_live_contract_matches_existing_learning_and_memory_boundaries():
    text = Path("docs/evolution/SIMBIONTE_LAB_INTAKE_2026-09-06.md").read_text(encoding="utf-8")
    assert "Governed Learning" in text
    assert "Evolution Gate" in text
    assert "LAB_ONLY" in text
    assert "tenant" in text.lower()


def test_contract_does_not_claim_supabase_persistence_as_laboratory_authority():
    text = Path("docs/evolution/SIMBIONTE_LAB_INTAKE_2026-09-06.md").read_text(encoding="utf-8")
    forbidden = (
        "Supabase como memória da Simbionte",
        "Simbionte escreve diretamente no Supabase",
        "Simbionte é fonte de verdade",
    )
    assert not any(marker in text for marker in forbidden)
