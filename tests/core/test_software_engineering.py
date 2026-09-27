import pytest

from elo.core.software_engineering import NativeSoftwareEngineering, SoftwareEngineeringError


def provenance():
    return {"source_ref": "repository", "source_commit": "abc123"}


def cycle_kwargs():
    return {
        "cycle_id": "c-1",
        "tenant_id": "t-1",
        "target": "module.py",
        "diagnosis": "test fails",
        "root_cause": "invalid state",
        "hypothesis": "state guard is incomplete",
        "proposed_change": "add explicit guard",
        "evidence_ids": ["e-1"],
        "provenance": provenance(),
        "reproduction_evidence_ids": ["repro-1"],
        "regression_test_ids": ["test-1"],
    }


def test_prepare_cycle_is_candidate_only():
    cycle = NativeSoftwareEngineering().prepare_cycle(**cycle_kwargs())
    assert cycle.state == "LAB_CANDIDATE"
    assert NativeSoftwareEngineering.advance(
        cycle=cycle,
        tests_passed=True,
        regression_passed=True,
        validation_evidence_ids=["validation-1"],
    ).state == "READY_FOR_GOVERNANCE"


def test_failed_test_requires_adjustment():
    cycle = NativeSoftwareEngineering().prepare_cycle(**cycle_kwargs())
    assert NativeSoftwareEngineering.advance(
        cycle=cycle,
        tests_passed=False,
        regression_passed=False,
    ).state == "ADJUST_REQUIRED"


def test_missing_reproduction_or_regression_test_is_blocked():
    with pytest.raises(SoftwareEngineeringError):
        NativeSoftwareEngineering().prepare_cycle(
            **{**cycle_kwargs(), "reproduction_evidence_ids": []},
        )
    with pytest.raises(SoftwareEngineeringError):
        NativeSoftwareEngineering().prepare_cycle(
            **{**cycle_kwargs(), "regression_test_ids": []},
        )


def test_governance_requires_validation_evidence():
    cycle = NativeSoftwareEngineering().prepare_cycle(**cycle_kwargs())
    with pytest.raises(SoftwareEngineeringError):
        NativeSoftwareEngineering.advance(
            cycle=cycle,
            tests_passed=True,
            regression_passed=True,
        )


def test_missing_evidence_or_secret_is_blocked():
    with pytest.raises(SoftwareEngineeringError):
        NativeSoftwareEngineering().prepare_cycle(
            **{**cycle_kwargs(), "evidence_ids": []},
        )
    with pytest.raises(SoftwareEngineeringError):
        NativeSoftwareEngineering().prepare_cycle(
            **{
                **cycle_kwargs(),
                "provenance": {**provenance(), "token": "forbidden"},
            },
        )
