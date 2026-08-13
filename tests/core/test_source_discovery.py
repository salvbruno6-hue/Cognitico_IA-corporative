from elo.core.source_discovery import SourceDiscoveryEngine


def test_company_question_discovers_sources_without_manual_path():
    plan = SourceDiscoveryEngine().plan("elo, analise a Multiteiner como possível cliente")
    kinds = [candidate.kind for candidate in plan.candidates]
    assert plan.intent == "external_entity"
    assert "CHATGPT_PROJECTS" in kinds
    assert "WEB" in kinds
    assert "ELO_MEMORY" in kinds


def test_architecture_question_prioritizes_github():
    plan = SourceDiscoveryEngine().plan("elo revise a arquitetura")
    assert plan.intent == "architecture_review"
    assert plan.candidates[0].kind == "GITHUB"


def test_empty_question_is_rejected():
    try:
        SourceDiscoveryEngine().plan("   ")
    except ValueError as exc:
        assert "question" in str(exc)
    else:
        raise AssertionError("empty question must be rejected")
