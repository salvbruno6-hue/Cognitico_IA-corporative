from elo.agent_intake.hermes_context_plugin_boundary import ContextEnginePluginSignal, PluginDisposition, assess_context_engine_plugin

def _signal(**kw):
    base = dict(signal_id="ctx-001", tenant_scope="multiteiner", plugin_id="lcm", engine_name="lcm", source_refs=("hermes:plugin:lcm",), provenance_verified=True)
    base.update(kw)
    return ContextEnginePluginSignal(**base)

def test_verified_plugin_without_explicit_activation_is_observation():
    a = assess_context_engine_plugin(_signal())
    assert a.disposition is PluginDisposition.OBSERVATION
    assert a.activation_permitted is False

def test_explicit_verified_plugin_is_candidate_only():
    a = assess_context_engine_plugin(_signal(explicit_activation=True))
    assert a.disposition is PluginDisposition.CANDIDATE
    assert a.canonical_authority is False

def test_missing_provenance_is_rejected():
    a = assess_context_engine_plugin(_signal(provenance_verified=False))
    assert a.disposition is PluginDisposition.REJECTED

def test_missing_identity_is_rejected():
    a = assess_context_engine_plugin(_signal(plugin_id=""))
    assert a.disposition is PluginDisposition.REJECTED
