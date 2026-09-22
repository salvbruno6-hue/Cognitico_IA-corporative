"""REASSESS — alimenta a calibração com o outcome."""
from __future__ import annotations
from elo.core.calibration import CalibrationObservation
from ..crl import CRLContext
from ..store.memory_store import CalibrationStore
from .base import require

def reassess_handler(ctx: CRLContext) -> CRLContext:
    lifecycle = require(ctx, "lifecycle")
    if lifecycle.outcome is None: return ctx
    calibration = CalibrationStore().load()
    calibration.add(CalibrationObservation(confidence=float(ctx.payload.get("confidence", 0.0)), outcome_score=float(ctx.payload.get("outcome_score", 0.0)), decision_id=lifecycle.decision.decision_id))
    CalibrationStore().save(calibration)
    return ctx
