import pytest

from elo.cognitive.pcp_route_demand import route_mix_demand_by_constraint


def test_m16_does_not_consume_chassi_capacity_but_still_consumes_assembly():
    result = route_mix_demand_by_constraint(
        {"M01": 10, "M16": 5},
        {
            "M01": ("CHASSI", "MONTAGEM", "TESTES"),
            "M16": ("MONTAGEM", "TESTES"),
        },
        constraints=("CHASSI", "MONTAGEM", "TESTES"),
    )
    by_constraint = {item.constraint: item for item in result}

    assert by_constraint["CHASSI"].demand_modules == 10
    assert by_constraint["CHASSI"].contributing_models == ("M01",)
    assert by_constraint["CHASSI"].excluded_models == ("M16",)
    assert by_constraint["MONTAGEM"].demand_modules == 15
    assert by_constraint["TESTES"].demand_modules == 15


def test_m16_only_mix_has_zero_chassi_demand_when_stage_is_requested():
    result = route_mix_demand_by_constraint(
        {"MLT.M16": 7},
        {"M16": ("MONTAGEM", "TESTES")},
        constraints=("CHASSI", "MONTAGEM", "TESTES"),
    )
    by_constraint = {item.constraint: item for item in result}

    assert by_constraint["CHASSI"].demand_modules == 0
    assert by_constraint["CHASSI"].excluded_models == ("M16",)
    assert by_constraint["MONTAGEM"].demand_modules == 7


def test_missing_route_for_demanded_model_fails_closed():
    with pytest.raises(ValueError, match="missing governed route"):
        route_mix_demand_by_constraint(
            {"M01": 2, "M16": 1},
            {"M01": ("CHASSI", "MONTAGEM")},
        )


def test_model_aliases_mlt_prefix_and_short_code_are_normalized():
    result = route_mix_demand_by_constraint(
        {"MLT.M01": 2, "M01": 3},
        {"M01": ("CHASSI",)},
    )
    assert result[0].constraint == "CHASSI"
    assert result[0].demand_modules == 5


def test_negative_demand_is_rejected():
    with pytest.raises(ValueError):
        route_mix_demand_by_constraint(
            {"M16": -1},
            {"M16": ("MONTAGEM",)},
        )
