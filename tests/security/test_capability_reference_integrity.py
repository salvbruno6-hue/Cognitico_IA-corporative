from pathlib import Path

import pytest

from elo.application.use_cases.system_health_symbiont_bridge import SystemHealthSymbiontBridge
from elo.cognitive.capability_reference_integrity import (
    CapabilityReferenceSignal,
    assess_capability_reference_integrity,
)
from elo.cognitive.system_health_assessment import assess_system_health


PROBE = Path("supabase/health/elo_capability_reference_integrity.sql")


def test_probe_is_read_only_and_confronts_policy_refs_with_catalog():
    source = PROBE.read_text(encoding="utf-8").lower()

    assert "has_capability" in source
    assert "public.elo_capabilities" in source
    assert "authz_capability_reference_integrity" in source
    assert "review" in source
    for forbidden in (
        "insert into ",
        "update public.",
        "delete from ",
        "create policy ",
        "alter policy ",
        "grant ",
        "revoke ",
    ):
        assert forbidden not in source


def test_orphan_reference_is_review_not_automatic_authority():
    finding = assess_capability_reference_integrity(
        CapabilityReferenceSignal(
            capability_code="PCP_ADMIN",
            reference_count=50,
            object_count=14,
            exists_in_catalog=False,
            active_in_catalog=False,
        )
    )

    assert finding.severity.value == "REVIEW"
    assert finding.owner == "elo-authz"

    orientations = SystemHealthSymbiontBridge().orient(assess_system_health((finding,)))
    assert len(orientations) == 1
    assert orientations[0].authorized is False
    assert orientations[0].owner == "elo-authz"


def test_active_catalog_reference_passes():
    finding = assess_capability_reference_integrity(
        CapabilityReferenceSignal(
            capability_code="PCP_READ",
            reference_count=2,
            object_count=1,
            exists_in_catalog=True,
            active_in_catalog=True,
        )
    )
    assert finding.severity.value == "PASS"


def test_invalid_signal_fails_closed():
    with pytest.raises(ValueError, match="must exist"):
        CapabilityReferenceSignal(
            capability_code="PCP_ADMIN",
            reference_count=1,
            object_count=1,
            exists_in_catalog=False,
            active_in_catalog=True,
        )

    with pytest.raises(ValueError, match="cannot exceed"):
        CapabilityReferenceSignal(
            capability_code="PCP_ADMIN",
            reference_count=1,
            object_count=2,
            exists_in_catalog=False,
            active_in_catalog=False,
        )
