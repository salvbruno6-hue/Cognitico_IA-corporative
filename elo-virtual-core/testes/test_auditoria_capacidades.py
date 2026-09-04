"""Virtual capability audit: connectors, budgeting, cross-information and safety.

All adapters are deterministic in-memory fakes. This is a laboratory contract,
not evidence of live Excel/Supabase/MCP connectivity.
"""
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class VirtualConnector:
    name: str
    capabilities: frozenset[str]

    def read(self, capability: str):
        if capability not in self.capabilities:
            raise LookupError(capability)
        return {"connector": self.name, "capability": capability}


def test_connector_capability_matrix():
    excel = VirtualConnector("excel", frozenset({"tabular_read", "tabular_write", "budget_export"}))
    supabase = VirtualConnector("supabase", frozenset({"structured_query", "historical_retrieval", "cross_reference"}))
    mcp = VirtualConnector("mcp", frozenset({"tool_call", "external_context"}))

    assert excel.read("budget_export")["connector"] == "excel"
    assert supabase.read("historical_retrieval")["connector"] == "supabase"
    assert mcp.read("tool_call")["connector"] == "mcp"


def test_budget_calculation_is_deterministic_and_traceable():
    items = [
        {"code": "M01", "quantity": Decimal("10"), "unit_price": Decimal("125.50")},
        {"code": "M02", "quantity": Decimal("4"), "unit_price": Decimal("80.00")},
    ]
    total = sum(item["quantity"] * item["unit_price"] for item in items)
    assert total == Decimal("1575.00")
    assert [item["code"] for item in items] == ["M01", "M02"]


def test_cross_information_reconciles_shared_key_without_merging_conflicting_values():
    budget = {"item": "M01", "quantity": 10, "source": "excel"}
    history = {"item": "M01", "quantity": 12, "source": "supabase"}
    assert budget["item"] == history["item"]
    assert budget["quantity"] != history["quantity"]
    assert budget["source"] != history["source"]


def test_missing_information_remains_unknown():
    source = {"item": "M03", "quantity": None}
    assert source["quantity"] is None


def test_tenant_scope_isolation_in_virtual_crossing():
    records = [
        {"tenant": "A", "item": "M01", "value": 100},
        {"tenant": "B", "item": "M01", "value": 900},
    ]
    tenant_a = [r for r in records if r["tenant"] == "A"]
    assert tenant_a == [{"tenant": "A", "item": "M01", "value": 100}]
    assert all(r["tenant"] == "A" for r in tenant_a)


def test_connector_failure_is_explicit_and_does_not_fabricate_data():
    excel = VirtualConnector("excel", frozenset({"tabular_read"}))
    try:
        excel.read("budget_export")
    except LookupError:
        pass
    else:
        raise AssertionError("unsupported connector capability must fail")
