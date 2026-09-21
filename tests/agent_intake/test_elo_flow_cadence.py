from elo.agent_intake.elo_flow_cadence import CadenceOutcome, FlowCadence


def test_activation_routes_to_the_next_existing_flow():
    cadence = FlowCadence()
    assert cadence.require_next("CANDIDATE", CadenceOutcome.PASS).next_flow == "CONTROLLED_TEST"
    assert cadence.require_next("CONTROLLED_TEST", CadenceOutcome.PASS).next_flow == "MEASURED_GAIN"
    assert cadence.require_next("MEASURED_GAIN", CadenceOutcome.PASS).next_flow == "REPEATABLE"
    assert cadence.require_next("REPEATABLE", CadenceOutcome.PASS).next_flow == "ELO_REVIEW"


def test_elo_approval_routes_to_cognitive_merge_not_git_merge():
    cadence = FlowCadence()
    assert cadence.require_next("ELO_REVIEW", CadenceOutcome.APPROVED).next_flow == "COGNITIVE_MERGE"


def test_implementation_authorization_is_not_merge_authorization():
    cadence = FlowCadence()
    assert cadence.require_next("ELO_REVIEW", CadenceOutcome.AUTHORIZED).next_flow == "IMPLEMENTATION_AUTHORIZED"
    assert cadence.next("IMPLEMENTATION_AUTHORIZED", CadenceOutcome.PASS) is None


def test_unmapped_outcome_stops_fail_closed():
    cadence = FlowCadence()
    assert cadence.next("ELO_REVIEW", CadenceOutcome.BLOCKED) is None
