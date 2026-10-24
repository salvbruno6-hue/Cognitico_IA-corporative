import pytest

from elo.agent_intake.skill_owner_identity import (
    identities_collide,
    normalize_skill_identity,
)


def test_same_display_name_different_owner_stays_distinct():
    a = normalize_skill_identity("plugin-a", "blender")
    b = normalize_skill_identity("plugin-b", "blender")
    assert a.qualified_name == "plugin-a:blender"
    assert b.qualified_name == "plugin-b:blender"
    assert not identities_collide(a, b)


def test_same_owner_and_name_is_same_identity():
    a = normalize_skill_identity("plugin-a", "blender")
    b = normalize_skill_identity("plugin-a", "blender")
    assert identities_collide(a, b)


@pytest.mark.parametrize("owner,name", [("", "x"), ("x", ""), ("a:b", "x"), ("a", "b:c")])
def test_invalid_or_prequalified_components_fail_closed(owner, name):
    with pytest.raises(ValueError):
        normalize_skill_identity(owner, name)
