from src.elo.agent_intake.hermes_profile_boundary import (
    ProfileDisposition,
    ProfileSignal,
    assess_profile,
)


def _signal(**overrides):
    values = dict(
        profile_id="research",
        tenant_scope="tenant-a",
        source_refs=("hermes://profiles",),
        identity_digest="sha256:profile",
        isolated_state=True,
        explicit_activation=True,
        shared_canonical_memory=False,
        authority_transfer=False,
    )
    values.update(overrides)
    return ProfileSignal(**values)


def test_valid_isolated_profile_is_candidate():
    result = assess_profile(_signal())
    assert result.disposition is ProfileDisposition.CANDIDATE
    assert result.canonical_authority is False
    assert result.execution_permitted is False
    assert result.promotion_permitted is False


def test_missing_provenance_is_rejected():
    result = assess_profile(_signal(source_refs=()))
    assert result.disposition is ProfileDisposition.REJECTED


def test_authority_transfer_is_rejected():
    result = assess_profile(_signal(authority_transfer=True))
    assert result.disposition is ProfileDisposition.REJECTED


def test_shared_canonical_memory_requires_observation():
    result = assess_profile(_signal(shared_canonical_memory=True))
    assert result.disposition is ProfileDisposition.OBSERVATION


def test_activation_or_isolation_missing_is_observation():
    assert assess_profile(_signal(explicit_activation=False)).disposition is ProfileDisposition.OBSERVATION
    assert assess_profile(_signal(isolated_state=False)).disposition is ProfileDisposition.OBSERVATION
