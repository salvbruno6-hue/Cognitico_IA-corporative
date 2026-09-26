from elo.agent_intake.hermes_profile_adapter import adapt_profile
from elo.agent_intake.hermes_profile_boundary import ProfileDisposition, ProfileSignal

def signal(**overrides):
    v=dict(profile_id="profile-test",tenant_scope="multiteiner",source_refs=("controlled-eval:profile/1",),identity_digest="id-1",isolated_state=True,explicit_activation=True,shared_canonical_memory=False,authority_transfer=False)
    v.update(overrides)
    return ProfileSignal(**v)

def test_adapts_isolated_profile():
    c=adapt_profile(signal())
    assert c is not None
    assert c.disposition is ProfileDisposition.CANDIDATE
    assert not c.shared_canonical_memory and not c.authority_transfer
    assert not c.execution_permitted and not c.promotion_permitted

def test_rejects_shared_canonical_memory():
    assert adapt_profile(signal(shared_canonical_memory=True)) is None

def test_rejects_authority_transfer():
    assert adapt_profile(signal(authority_transfer=True)) is None
