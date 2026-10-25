from decimal import Decimal

from elo.agent_intake.external_tool_spend_policy import evaluate_external_tool_spend


def test_no_declaration_preserves_existing_behavior():
    decision = evaluate_external_tool_spend(declared_cost=None, running_total=0, spend_limit=None, unattended=False)
    assert decision.allowed is True
    assert decision.requires_human_approval is False


def test_within_limit_is_allowed_deterministically():
    decision = evaluate_external_tool_spend(declared_cost="2.5", running_total="3.0", spend_limit="6", unattended=False)
    assert decision.allowed is True
    assert decision.projected_total == Decimal("5.5")


def test_over_limit_interactive_requires_approval_without_dispatch_authority():
    decision = evaluate_external_tool_spend(declared_cost=2, running_total=5, spend_limit=6, unattended=False)
    assert decision.allowed is False
    assert decision.requires_human_approval is True
    assert decision.reason == "spend_limit_exceeded_requires_approval"


def test_over_limit_unattended_fails_closed():
    decision = evaluate_external_tool_spend(declared_cost=2, running_total=5, spend_limit=6, unattended=True)
    assert decision.allowed is False
    assert decision.requires_human_approval is False
    assert decision.reason == "spend_limit_exceeded_unattended"


def test_malformed_or_negative_policy_fails_closed():
    malformed = evaluate_external_tool_spend(declared_cost="bad", running_total=0, spend_limit=1, unattended=False)
    negative = evaluate_external_tool_spend(declared_cost=-1, running_total=0, spend_limit=1, unattended=False)
    assert malformed.allowed is False and malformed.reason == "invalid_spend_policy"
    assert negative.allowed is False and negative.reason == "invalid_spend_policy"


def test_non_finite_policy_values_fail_closed():
    cases = (
        {"declared_cost": "NaN", "running_total": 0, "spend_limit": 1},
        {"declared_cost": "Infinity", "running_total": 0, "spend_limit": "Infinity"},
        {"declared_cost": 1, "running_total": "NaN", "spend_limit": 2},
        {"declared_cost": 1, "running_total": 0, "spend_limit": "-Infinity"},
    )
    for policy in cases:
        decision = evaluate_external_tool_spend(**policy, unattended=True)
        assert decision.allowed is False
        assert decision.requires_human_approval is False
        assert decision.reason == "invalid_spend_policy"
        assert decision.projected_total is None
