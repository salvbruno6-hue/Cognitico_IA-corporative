from elo.agent_intake.hermes_context_plugin_adapter import ContextPluginAdapter
from elo.agent_intake.hermes_context_plugin_boundary import ContextEnginePluginSignal, PluginDisposition
from elo.core.context_resolution import ContextQuery, ContextResolutionEngine


def _pack():
    return ContextResolutionEngine().resolve(
        ContextQuery(
            question="Qual e o contexto autorizado para esta solicitacao?",
            tenant_id="multiteiner",
            domain="planning",
        )
    )


def _signal(**overrides):
    data = dict(
        signal_id="ctx-001",
        tenant_scope="multiteiner",
        plugin_id="lcm",
        engine_name="lcm",
        source_refs=("hermes:plugin:lcm",),
        explicit_activation=True,
        provenance_verified=True,
    )
    data.update(overrides)
    return ContextEnginePluginSignal(**data)


def test_verified_plugin_adapts_existing_context_without_becoming_authority():
    result = ContextPluginAdapter().adapt(_pack(), _signal())
    assert result.adapted is True
    assert result.assessment.disposition is PluginDisposition.CANDIDATE
    assert result.assessment.canonical_authority is False
    sources = result.pack.scoped_sources()
    assert len(sources) == 1
    assert sources[0].authority == "ELO Context"
    assert sources[0].source_type == "context-plugin"


def test_invalid_plugin_is_not_adapted():
    result = ContextPluginAdapter().adapt(
        _pack(),
        _signal(provenance_verified=False),
    )
    assert result.adapted is False
    assert result.assessment.disposition is PluginDisposition.REJECTED
    assert result.pack.scoped_sources() == ()
