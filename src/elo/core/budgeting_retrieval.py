"""Bridge authorized retrieved evidence into the canonical budgeting contract."""
from decimal import Decimal
from .budgeting import BudgetInput, BudgetInputClass
from .source_resolver import RetrievedSource


def retrieved_to_budget_input(*, retrieved: RetrievedSource, tenant_id: str, domain: str,
                              name: str, classification: BudgetInputClass,
                              value: Decimal | int | float | str | None, unit: str,
                              request_id: str, correlation_id: str) -> BudgetInput:
    """Create one immutable BudgetInput while preserving retrieval provenance."""
    provenance = dict(retrieved.provenance)
    provenance.update({
        "request_id": request_id,
        "correlation_id": correlation_id,
        "source_id": retrieved.source_id,
        "source_type": retrieved.source_type,
        "authority": provenance.get("authority", "external_source_evidence"),
    })
    return BudgetInput.create(
        tenant_id=tenant_id,
        domain=domain,
        name=name,
        classification=classification,
        value=value,
        unit=unit,
        source_id=retrieved.source_id,
        provenance=provenance,
    )
