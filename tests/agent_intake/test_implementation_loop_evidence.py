from elo.agent_intake.implementation_loop_evidence import ImplementationEvidence


def _evidence(**overrides):
    data = {
        "candidate_id": "EXT-CONTEXTREF-HERMES",
        "owner": "ELO Context",
        "baseline": {"accuracy": 0.8},
        "adapted": {"accuracy": 0.8},
        "metric_directions": {"accuracy": "maximize"},
        "regressions": (),
        "repeatable": True,
        "provenance_refs": ("controlled-test:628",),
        "boundary_integrity": True,
    }
    data.update(overrides)
    return ImplementationEvidence(**data)


def test_complete_evidence_is_bounded():
    assert _evidence().is_complete() is True


def test_evidence_requires_provenance():
    assert _evidence(provenance_refs=()).is_complete() is False


def test_evidence_blocks_boundary_violation():
    assert _evidence(boundary_integrity=False).is_complete() is False


def test_evidence_blocks_regression_and_nonrepeatability():
    assert _evidence(regressions=("scope",), repeatable=False).is_complete() is False


def test_evidence_requires_metric_direction():
    assert _evidence(metric_directions={}).is_complete() is False
