from src.elo.agent_intake.hermes_hooks_boundary import (
    HookDisposition,
    HookSignal,
    assess_hook,
)


def _signal(**overrides):
    values = dict(
        hook_id="hook-001",
        tenant_scope="tenant-a",
        source_refs=("hermes://hooks",),
        event_name="before_turn",
        handler_digest="sha256:handler",
        explicit_activation=True,
        mutates_canonical_state=False,
        bypasses_governance=False,
    )
    values.update(overrides)
    return HookSignal(**values)


def test_valid_explicit_hook_is_candidate():
    result = assess_hook(_signal())
    assert result.disposition is HookDisposition.CANDIDATE
    assert result.canonical_authority is False
    assert result.execution_permitted is False
    assert result.mutation_permitted is False


def test_missing_identity_or_handler_is_rejected():
    assert assess_hook(_signal(hook_id="")).disposition is HookDisposition.REJECTED
    assert assess_hook(_signal(handler_digest="")).disposition is HookDisposition.REJECTED


def test_missing_provenance_is_rejected():
    assert assess_hook(_signal(source_refs=())).disposition is HookDisposition.REJECTED


def test_canonical_mutation_or_bypass_is_rejected():
    assert assess_hook(_signal(mutates_canonical_state=True)).disposition is HookDisposition.REJECTED
    assert assess_hook(_signal(bypasses_governance=True)).disposition is HookDisposition.REJECTED


def test_missing_activation_is_observation():
    assert assess_hook(_signal(explicit_activation=False)).disposition is HookDisposition.OBSERVATION
