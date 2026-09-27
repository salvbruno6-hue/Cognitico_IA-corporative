"""Isolated laboratory harness for the canonical Cognitive Runtime Loop.

The harness measures integrated CRL orchestration with controlled fixture
handlers. It does not replace the canonical CRL, production handlers, or
governance.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .crl import CRLContext, CognitiveRuntimeLoop, Stage
from .humanization.humanizer import Humanizer
from .synthesis.engine import SynthesisEngine


STAGE_ORDER = tuple(stage.value for stage in CognitiveRuntimeLoop.STAGES_ORDER)


@dataclass(frozen=True, slots=True)
class CognitiveHarnessFixture:
    """Deterministic input for one isolated CRL laboratory run."""

    request_id: str = "cognitive-harness-fixture"
    intent: str = "confere_analise"
    payload: dict[str, Any] = field(default_factory=lambda: {"question": "controlled"})
    external_analysis: str = "A análise contempla segurança, custo e prazo."
    so_context: dict[str, Any] = field(
        default_factory=lambda: {
            "so_id": "FIXTURE-SO",
            "learning": {
                "so_id": "FIXTURE-SO",
                "summary": "Fixture controlada para validação cognitiva.",
                "tags": ["segurança", "custo", "premissa pendente"],
            },
            "handbook": [],
            "precedents": [],
        }
    )


@dataclass(frozen=True, slots=True)
class CognitiveHarnessReport:
    """Measurement-only report emitted by the isolated harness."""

    request_id: str
    stage_order: tuple[str, ...]
    audit: tuple[dict[str, Any], ...]
    stage_results: dict[str, Any]
    delta: dict[str, Any]
    directives: tuple[dict[str, Any], ...]
    human_response: str
    metrics: dict[str, Any]
    isolated: bool = True
    promotion_attempted: bool = False
    governance_decision: str = "MEASUREMENT_ONLY"


class CognitiveHarness:
    """Orchestrate the existing ten-stage CRL with controlled local handlers."""

    def __init__(self) -> None:
        self._synthesis = SynthesisEngine()
        self._humanizer = Humanizer()

    def run(self, fixture: CognitiveHarnessFixture) -> CognitiveHarnessReport:
        """Run all ten canonical CRL stages without external side effects."""
        context = CRLContext(
            request_id=fixture.request_id,
            payload=dict(fixture.payload),
        )
        context.payload["fixture"] = {
            "external_analysis": fixture.external_analysis,
            "so_context": fixture.so_context,
            "intent": fixture.intent,
        }

        crl = CognitiveRuntimeLoop()
        self._register_fixture_handlers(crl, fixture)
        result = crl.run(context)

        delta = result.stage_results["delta"]
        delta_dict = delta.to_dict()
        directives = tuple(item.to_dict() for item in delta.directives)

        human_response = self._humanizer.humanize(
            {
                "intent": fixture.intent,
                "delta": delta_dict,
                "decision_brief": result.stage_results["decision_brief"],
            }
        )

        statuses = [item["status"] for item in result.audit]
        metrics = {
            "completed_stage_count": sum(status == "ok" for status in statuses),
            "audit_entry_count": len(result.audit),
            "skipped_stage_count": sum(status == "skipped" for status in statuses),
            "error_stage_count": sum(status == "error" for status in statuses),
            "network_access": False,
            "supabase_access": False,
            "mcp_access": False,
            "canonical_memory_write": False,
            "promotion_attempted": False,
        }

        stage_results = dict(result.stage_results)
        stage_results["delta"] = delta_dict

        return CognitiveHarnessReport(
            request_id=result.request_id,
            stage_order=STAGE_ORDER,
            audit=tuple(result.audit),
            stage_results=stage_results,
            delta=delta_dict,
            directives=directives,
            human_response=human_response,
            metrics=metrics,
        )

    def _register_fixture_handlers(
        self,
        crl: CognitiveRuntimeLoop,
        fixture: CognitiveHarnessFixture,
    ) -> None:
        handlers = {
            Stage.OBSERVE: lambda ctx: self._observe(ctx, fixture),
            Stage.CONTEXTUALIZE: lambda ctx: self._contextualize(ctx, fixture),
            Stage.ANALYZE: lambda ctx: self._analyze(ctx, fixture),
            Stage.FORMULATE: self._formulate,
            Stage.DECIDE: self._decide,
            Stage.EXECUTE: self._execute,
            Stage.MONITOR: self._monitor,
            Stage.LEARN: self._learn,
            Stage.FOLLOW_UP: self._follow_up,
            Stage.REASSESS: self._reassess,
        }
        for stage, handler in handlers.items():
            crl.register(stage, handler)

    @staticmethod
    def _observe(ctx: CRLContext, fixture: CognitiveHarnessFixture) -> CRLContext:
        ctx.stage_results["observation"] = {
            "payload": dict(fixture.payload),
            "source": "controlled_fixture",
        }
        return ctx

    @staticmethod
    def _contextualize(ctx: CRLContext, fixture: CognitiveHarnessFixture) -> CRLContext:
        ctx.stage_results["so_context"] = fixture.so_context
        return ctx

    def _analyze(self, ctx: CRLContext, fixture: CognitiveHarnessFixture) -> CRLContext:
        delta = self._synthesis.synthesize(
            external_analysis=fixture.external_analysis,
            so_context=fixture.so_context,
        )
        ctx.stage_results["analysis"] = delta.to_dict()
        ctx.stage_results["delta"] = delta
        return ctx

    @staticmethod
    def _formulate(ctx: CRLContext) -> CRLContext:
        delta = ctx.stage_results["delta"].to_dict()
        ctx.stage_results["decision_brief"] = {
            "recommendation": "considerar_melhorias" if delta["improvements"] else "alinhado_prosseguir",
            "confidence": delta["overall_confidence"],
            "source": "controlled_fixture",
        }
        return ctx

    @staticmethod
    def _decide(ctx: CRLContext) -> CRLContext:
        ctx.stage_results["decision"] = {
            "status": "proposed",
            "authority": "measurement_only",
        }
        return ctx

    @staticmethod
    def _execute(ctx: CRLContext) -> CRLContext:
        ctx.stage_results["execution"] = {
            "status": "simulated",
            "side_effects": False,
        }
        return ctx

    @staticmethod
    def _monitor(ctx: CRLContext) -> CRLContext:
        ctx.stage_results["monitor"] = {
            "status": "observed",
            "external_observation": False,
        }
        return ctx

    @staticmethod
    def _learn(ctx: CRLContext) -> CRLContext:
        ctx.stage_results["learning"] = {
            "status": "candidate_only",
            "promotion": "promotion_not_attempted",
            "reason": "cognitive_harness_measurement",
        }
        return ctx

    @staticmethod
    def _follow_up(ctx: CRLContext) -> CRLContext:
        ctx.stage_results["follow_up"] = {
            "status": "simulated",
            "side_effects": False,
        }
        return ctx

    @staticmethod
    def _reassess(ctx: CRLContext) -> CRLContext:
        ctx.stage_results["reassessment"] = {
            "status": "completed",
            "source": "controlled_fixture",
        }
        return ctx


__all__ = [
    "CognitiveHarness",
    "CognitiveHarnessFixture",
    "CognitiveHarnessReport",
    "STAGE_ORDER",
]
