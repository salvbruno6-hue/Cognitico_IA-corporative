from src.elo.agent_intake.hermes_profile_boundary import ProfileDisposition,ProfileSignal,assess_profile
def _signal(**o):
 b=dict(profile_id="p",tenant_scope="multiteiner",source_refs=("hermes:profile",),identity_digest="id",isolated_state=True,explicit_activation=True,shared_canonical_memory=False,authority_transfer=False);b.update(o);return ProfileSignal(**b)
def test_valid_is_candidate():
 a=assess_profile(_signal());assert a.disposition is ProfileDisposition.CANDIDATE and a.canonical_authority is False and a.execution_permitted is False and a.promotion_permitted is False
def test_missing_provenance_rejected(): assert assess_profile(_signal(source_refs=())).disposition is ProfileDisposition.REJECTED
def test_authority_transfer_rejected(): assert assess_profile(_signal(authority_transfer=True)).disposition is ProfileDisposition.REJECTED
def test_shared_memory_observation(): assert assess_profile(_signal(shared_canonical_memory=True)).disposition is ProfileDisposition.OBSERVATION
def test_missing_activation_observation(): assert assess_profile(_signal(explicit_activation=False)).disposition is ProfileDisposition.OBSERVATION
