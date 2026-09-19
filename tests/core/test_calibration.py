from elo.core.calibration import CalibrationObservation, ConfidenceCalibration


def test_calibration_does_not_mutate_declared_confidence():
    calibration = ConfidenceCalibration()
    calibration.add(CalibrationObservation(0.8, 1.0, "d1"))
    calibration.add(CalibrationObservation(0.8, 0.0, "d2"))
    rows = calibration.reliability()
    assert rows[0]["mean_confidence"] == 0.8
    assert rows[0]["mean_outcome"] == 0.5
