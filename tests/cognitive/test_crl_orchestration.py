"""Testes do Cognitive Runtime Loop (ADR-0014)."""
from src.elo.cognitive.runtime.crl import (
    CognitiveRuntimeLoop,
    CRLContext,
    Stage,
)


def test_crl_runs_registered_stages_in_order():
    crl = CognitiveRuntimeLoop()
    order: list[str] = []

    def make_handler(name: str):
        def handler(ctx: CRLContext) -> CRLContext:
            order.append(name)
            return ctx
        return handler

    for stage in [Stage.OBSERVE, Stage.ANALYZE, Stage.DECIDE]:
        crl.register(stage, make_handler(stage.value))

    ctx = CRLContext(request_id="test-order")
    result = crl.run(ctx)

    assert order == ["observe", "analyze", "decide"]
    assert len(result.audit) == 10


def test_crl_skips_unregistered_stages():
    crl = CognitiveRuntimeLoop()
    crl.register(Stage.OBSERVE, lambda ctx: ctx)

    ctx = CRLContext(request_id="test-skip")
    result = crl.run(ctx)

    skipped = [a for a in result.audit if a["status"] == "skipped"]
    assert len(skipped) == 9


def test_crl_audits_errors():
    crl = CognitiveRuntimeLoop()

    def failing(ctx: CRLContext) -> CRLContext:
        raise RuntimeError("boom")

    crl.register(Stage.OBSERVE, failing)
    ctx = CRLContext(request_id="test-error")

    try:
        crl.run(ctx)
    except RuntimeError:
        pass

    errors = [a for a in ctx.audit if a["status"] == "error"]
    assert len(errors) == 1
    assert errors[0]["stage"] == "observe"


def test_crl_rejects_unknown_stage():
    crl = CognitiveRuntimeLoop()
    try:
        crl.register("invalid", lambda ctx: ctx)
        assert False, "deveria ter lançado"
    except ValueError:
        pass
