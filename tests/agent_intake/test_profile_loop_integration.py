from elo.agent_intake.hermes_profile_boundary import ProfileDisposition, ProfileSignal, assess_profile
from elo.agent_intake.profile_loop_integration import run_profile_loop_probe
from elo.agent_intake.implementation_loop import ImplementationStage


def test_profile_boundary_rejects_authority_transfer():
    base = dict(profile_id="p1", tenant_scope="t1", source_refs=("ref:1",),
                identity_digest="d1", isolated_state=True,
                explicit_activation=True)
    assert assess_profile(
        ProfileSignal(**base, shared_canonical_memory=False, authority_transfer=False)
    ).disposition is ProfileDisposition.CANDIDATE
    assert assess_profile(
        ProfileSignal(**base, shared_canonical_memory=False, authority_transfer=True)
    ).disposition is ProfileDisposition.REJECTED
    assert assess_profile(
        ProfileSignal(**base, shared_canonical_memory=True, authority_transfer=False)
    ).disposition is ProfileDisposition.OBSERVATION


def test_profile_loop_has_positive_repeatable_gain_and_stops_at_review():
    decision, evidence = run_profile_loop_probe(repeats=5)
    assert evidence.baseline["profile_isolation_compliance"] == 0.0
    assert evidence.adapted["profile_isolation_compliance"] == 1.0
    assert evidence.repeatable is True
    assert evidence.boundary_integrity is True
    assert evidence.is_complete() is True
    assert decision.stage is ImplementationStage.ELO_REVIEW
    assert decision.result == "READY_FOR_ELO_REVIEW"
    assert decision.canonical_mutation is False
