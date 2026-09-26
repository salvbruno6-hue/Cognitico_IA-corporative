from src.elo.agent_intake.hermes_secondary_loop_integration import run_cron_loop_probe


def test_cron_candidate_enters_shared_governed_loop_without_promotion():
    implementation, evidence = run_cron_loop_probe()

    assert implementation.result == "READY_FOR_ELO_REVIEW"
    assert evidence.candidate_id == "EXT-CRON-HERMES"
    assert evidence.metric_directions == {"bounded_schedule_registration_integrity_rate": "maximize"}
    assert evidence.baseline == {"bounded_schedule_registration_integrity_rate": 0.0}
    assert evidence.adapted == {"bounded_schedule_registration_integrity_rate": 1.0}
    assert evidence.repeatable is True
    assert evidence.boundary_integrity is True
    assert implementation.canonical_mutation is False
