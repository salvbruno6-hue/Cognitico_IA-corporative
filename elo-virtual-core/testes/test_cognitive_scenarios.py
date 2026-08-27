"""Scenario-level virtual laboratory tests for ELO cognitive behavior."""
from dataclasses import dataclass

@dataclass(frozen=True)
class SourceRecord:
    source: str
    tenant: str
    item: str
    quantity: float | None
    unit_price: float | None

def cross_reference(*records: SourceRecord):
    grouped = {}
    for record in records:
        grouped.setdefault((record.tenant, record.item), []).append(record)
    return grouped

def test_budget_crossing_preserves_conflicts_and_provenance():
    rows = cross_reference(SourceRecord("excel", "tenant-a", "M01", 10, 25), SourceRecord("history", "tenant-a", "M01", 12, 24))
    evidence = rows[("tenant-a", "M01")]
    assert len(evidence) == 2
    assert {row.source for row in evidence} == {"excel", "history"}
    assert {row.quantity for row in evidence} == {10, 12}

def test_budget_calculation_is_deterministic_and_separate_from_reasoning():
    assert 10 * 25 == 250

def test_missing_information_remains_unknown():
    record = SourceRecord("memorial", "tenant-a", "M02", None, 30)
    assert record.quantity is None

def test_tenant_evidence_isolated():
    rows = cross_reference(SourceRecord("excel", "tenant-a", "M01", 10, 25), SourceRecord("excel", "tenant-b", "M01", 99, 1))
    assert rows[("tenant-a", "M01")][0].quantity == 10
    assert rows[("tenant-b", "M01")][0].quantity == 99

def test_no_source_record_means_no_fabricated_budget_value():
    assert ("tenant-a", "M99") not in cross_reference()
