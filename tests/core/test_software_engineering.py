import pytest

from elo.core.software_engineering import NativeSoftwareEngineering, SoftwareEngineeringError


def provenance():
    return {"source_ref": "repository", "source_commit": "abc123"}


def test_prepare_cycle_is_candidate_only():
    cycle = NativeSoftwareEngineering().prepare_cycle(
        cycle_id="c-1", tenant_id="t-1", target="module.py", diagnosis="test fails",
        root_cause="invalid state", hypothesis="state guard is incomplete",
        proposed_change="add explicit guard", evidence_ids=["e-1"], provenance=provenance(),
    )
    assert cycle.state == "LAB_CANDIDATE"
    assert NativeSoftwareEngineering.advance(cycle=cycle, tests_passed=True, regression_passed=True).state == "READY_FOR_GOVERNANCE"


def test_failed_test_requires_adjustment():
    cycle = NativeSoftwareEngineering().prepare_cycle(
        cycle_id="c-2", tenant_id="t-1", target="module.py", diagnosis="failure",
        root_cause="cause", hypothesis="fix", proposed_change="patch",
        evidence_ids=["e-2"], provenance=provenance(),
    )
    assert NativeSoftwareEngineering.advance(cycle=cycle, tests_passed=False, regression_passed=False).state == "ADJUST_REQUIRED"


def test_missing_evidence_or_secret_is_blocked():
    with pytest.raises(SoftwareEngineeringError):
        NativeSoftwareEngineering().prepare_cycle(
            cycle_id="c", tenant_id="t", target="x", diagnosis="d", root_cause="r",
            hypothesis="h", proposed_change="p", evidence_ids=[], provenance=provenance(),
        )
    with pytest.raises(SoftwareEngineeringError):
        NativeSoftwareEngineering().prepare_cycle(
            cycle_id="c", tenant_id="t", target="x", diagnosis="d", root_cause="r",
            hypothesis="h", proposed_change="p", evidence_ids=["e"],
            provenance={**provenance(), "token": "forbidden"},
        )
