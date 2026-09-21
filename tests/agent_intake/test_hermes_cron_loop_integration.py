from src.elo.agent_intake.hermes_secondary_loop_integration import run_cron_loop_probe


def test_cron_candidate_enters_shared_governed_loop_without_promotion():
    implementation, evidence = run_cron_loop_probe()

    assert implementation.result == "RETEST"
    assert evidence.candidate_id == "EXT-CRON-HERMES"
    assert evidence.metric_directions == {"authorized_idempotent_schedule_recognition_rate": "maximize"}
    assert evidence.baseline == {"authorized_idempotent_schedule_recognition_rate": 1.0}
    assert evidence.adapted == {"authorized_idempotent_schedule_recognition_rate": 1.0}
    assert evidence.repeatable is True
    assert evidence.boundary_integrity is True
    assert evidence.canonical_mutation is False
