from elo.agent_intake.hermes_code_exec_evaluation import FIXTURES, baseline_allows, governed_allows, evaluate

def test_governed_boundary():
    assert governed_allows(FIXTURES[0])
    assert not governed_allows(FIXTURES[1])
    assert not governed_allows(FIXTURES[2])
    assert not governed_allows(FIXTURES[3])
    assert not governed_allows(FIXTURES[4])

def test_controlled_measurement():
    result=evaluate()
    assert result["baseline_rate"] == 0.4
    assert result["adapted_rate"] == 1.0
    assert result["adapted_rate"] > result["baseline_rate"]
    assert result["repeatable"]
    assert result["regressions"] == ()

def test_policies_differ():
    assert tuple(baseline_allows(x) for x in FIXTURES) != tuple(governed_allows(x) for x in FIXTURES)
