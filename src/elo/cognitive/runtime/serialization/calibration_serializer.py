"""Serialização de ConfidenceCalibration ↔ JSON."""
from __future__ import annotations
from typing import Any
from elo.core.calibration import CalibrationObservation, ConfidenceCalibration

def to_dict(calibration: ConfidenceCalibration) -> dict[str, Any]:
    return {"bins": calibration._bins, "observations": [{"confidence": o.confidence, "outcome_score": o.outcome_score, "decision_id": o.decision_id} for o in calibration.observations()]}

def from_dict(data: dict[str, Any]) -> ConfidenceCalibration:
    calibration = ConfidenceCalibration(bins=data.get("bins", 10))
    for obs in data.get("observations", []):
        calibration.add(CalibrationObservation(confidence=obs["confidence"], outcome_score=obs["outcome_score"], decision_id=obs["decision_id"]))
    return calibration
