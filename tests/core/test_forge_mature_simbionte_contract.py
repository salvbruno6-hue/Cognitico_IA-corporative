from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_forge_mature_is_internal_forge_layer():
    text = read("forge/mature/README.md")
    assert "não é um pilar" in text
    assert "não é um pilar ou autoridade independente" in text
    assert "FORGE.MATURE" in text


def test_old_elo_mature_is_historical_source_not_architecture():
    text = read("forge/mature/README.md")
    assert "Elo_mature" in text
    assert "fontes históricas" in text
    assert "Nenhum deles é autoridade arquitetural" in text


def test_simbionte_is_cognitive_nature_not_structure():
    text = read("src/elo/cognitive/README.md")
    assert "Simbionte é uma natureza do ELO Cognitivo" in text
    assert "Não é pilar, camada, núcleo, autoridade ou componente arquitetural independente" in text
    assert "conhecimento recuperado do Forge é alimento" in text


def test_maturity_engine_is_not_redeclared_as_forge_mature():
    text = read("src/elo/core/maturity_engine.py")
    assert "MaturityAssessment" in text
    assert "SPECIALIST_VALIDATION" in text
    assert "FORGE.MATURE" not in text


def test_structural_boundaries_preserve_canonical_precedence():
    forge = read("forge/README.md")
    cognitive = read("src/elo/cognitive/README.md")
    assert "não cria uma segunda autoridade arquitetural" in forge
    assert "aprendizagem não redefine a tricotomia" in cognitive
