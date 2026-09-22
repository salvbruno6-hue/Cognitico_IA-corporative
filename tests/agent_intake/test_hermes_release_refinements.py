import pytest

from src.elo.agent_intake.hermes_release_refinements import (
    candidate_metadata,
    observe_session_search,
    observe_skill_autoload,
)


REV = "hermes-v0.21.4@d337b73"


def test_skill_autoload_is_observation_only_and_deduplicated():
    candidate = observe_skill_autoload(
        {"skills.auto_load": ["planning", "review"]}, source_revision=REV
    )
    assert candidate.candidate_id == "EXT-SKILL-AUTOLOAD-HERMES"
    assert candidate.skills == ("planning", "review")
    assert candidate_metadata(candidate) == {
        "candidate_only": True,
        "canonical_mutation": False,
        "authority": "elo_cognitive",
        "source": "hermes",
    }


def test_skill_autoload_rejects_duplicates():
    with pytest.raises(ValueError, match="duplicate"):
        observe_skill_autoload(
            {"skills.auto_load": ["planning", "planning"]}, source_revision=REV
        )


def test_session_search_preserves_bounds_and_retry_semantics():
    candidate = observe_session_search(
        query="PCP módulos",
        after="2026-09-01",
        before="2026-09-22",
        source_revision=REV,
    )
    assert candidate.candidate_id == "EXT-SESSION-SEARCH-BOUNDS-HERMES"
    assert candidate.after == "2026-09-01"
    assert candidate.before == "2026-09-22"
    assert candidate.allow_or_relaxed_retry is True
    assert candidate.candidate_only is True
    assert candidate.canonical_mutation is False


def test_session_search_rejects_invalid_bounds():
    with pytest.raises(ValueError, match="after"):
        observe_session_search(
            query="x", after="2026-09-23", before="2026-09-22", source_revision=REV
        )


def test_session_search_rejects_empty_query():
    with pytest.raises(ValueError, match="empty"):
        observe_session_search(query=" ", source_revision=REV)
