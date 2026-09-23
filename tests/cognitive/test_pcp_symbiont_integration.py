from datetime import date

from elo.cognitive.pcp_symbiont_integration import (
    bottleneck,
    capacity,
    coverage,
    delivery_date,
    material_requirement,
    net_material_requirement,
    net_requirement,
    order_date,
    potential_delay,
    rupture_risk,
    utilization,
    wip_delta,
)
from elo.cognitive.pcp_evidence_bridge import (
    handoff_symbiont_evidence,
    prepare_symbiont_evidence,
)


def test_unique_pcp_formulas_are_calculated():
    assert net_requirement(100, 30, 10).value == 80
    assert material_requirement(20, 4).value == 80
    assert net_material_requirement(80, 50, 10).value == 40
    assert coverage(40, 10).value == 4
    assert capacity(40, 2).value == 20
    assert utilization(15, 20).value == 0.75
    assert wip_delta(12, 9).value == 3


def test_temporal_chain():
    dp = order_date(date(2026, 9, 30), 10)
    assert dp.value == "2026-09-20"
    de = delivery_date(date.fromisoformat(dp.value), 10)
    assert de.value == "2026-09-30"
    assert rupture_risk(date.fromisoformat(de.value), date(2026, 9, 30)).value is False
    assert potential_delay(date.fromisoformat(de.value), date(2026, 9, 30)).value == 0


def test_bottleneck_uses_highest_load_capacity_ratio():
    result = bottleneck([
        {"id": "R1", "carga": 90, "capacidade": 100},
        {"id": "R2", "carga": 80, "capacidade": 60},
    ])
    assert result.value == 80 / 60
    assert result.inputs["recurso"] == "R2"


def test_missing_variables_are_not_invented():
    assert net_requirement(100, None, 10).status == "NAO_LOCALIZADO"
    assert coverage(10, 0).status == "NAO_LOCALIZADO"


def test_symbiont_payload_preserves_provenance():
    payload = prepare_symbiont_evidence(
        request_id="PCP-TEST-001",
        source_ref="github:SKILL_PLANEJAMENTO_MULTITEINER",
        source_commit="test-commit",
        evidence_ids=["E1", "E2"],
        baseline="baseline",
        experiment="experiment",
        result="result",
        expected_outcome="expected",
        observed_outcome="observed",
        regression_status="PASS",
        generalization_status="PARTIAL",
        existing_owner="SKILL_PLANEJAMENTO_MULTITEINER",
        scope="controlled_pcp",
    )
    assert payload["source_ref"].startswith("github:")
    assert payload["source_commit"] == "test-commit"
    assert payload["evidence_ids"] == ("E1", "E2")
    assert payload["tenant_scope"] == "pcp"



def test_pcp_evidence_uses_canonical_symbiont_handoff():
    class FakeLifecycle:
        def handoff_to_symbiont(self, *, adapter, observation, principal_id, dataset_version):
            assert observation.source_ref.startswith("github:")
            assert observation.existing_owner == "SKILL_PLANEJAMENTO_MULTITEINER"
            assert observation.evidence_ids == ("E1", "E2")
            assert principal_id == "planner"
            assert dataset_version == "pcp-test-v1"
            return "CANONICAL_HANDOFF"

    payload = prepare_symbiont_evidence(
        request_id="PCP-TEST-002",
        source_ref="github:SKILL_PLANEJAMENTO_MULTITEINER",
        source_commit="b534b624a44818a45d067b81b91aa8aec21fb8c7",
        evidence_ids=["E1", "E2"],
        baseline="baseline",
        experiment="compare diagnose and kernel",
        result="compatible",
        expected_outcome="signals align",
        observed_outcome="signals align",
        regression_status="PASS",
        generalization_status="PARTIAL",
        existing_owner="SKILL_PLANEJAMENTO_MULTITEINER",
        scope="controlled_pcp",
    )
    assert handoff_symbiont_evidence(
        FakeLifecycle(),
        adapter=object(),
        evidence_payload=payload,
        principal_id="planner",
        dataset_version="pcp-test-v1",
    ) == "CANONICAL_HANDOFF"


def test_pcp_kernel_has_no_symbiont_import_dependency():
    from pathlib import Path

    source = Path("src/elo/cognitive/pcp_symbiont_integration.py").read_text(encoding="utf-8")
    assert "SymbiontSkillRuntime" not in source
    assert "SymbiontLabObservation" not in source
    assert "DecisionLifecycle" not in source
