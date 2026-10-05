"""Fail-soft adapter from response composition to orchestration orientation.

This module is intentionally not an authority. It only adapts facts already
available to the response composer into the read-only orientation builder.
"""

from __future__ import annotations

from typing import Any


def _load_builder() -> tuple[Any, Any] | None:
    try:
        from elo.cognitive.orchestration_orientation import (
            OrchestrationOrientationBuilder,
            OrientationRequest,
        )
    except Exception:
        return None
    return OrchestrationOrientationBuilder, OrientationRequest


def is_builder_available() -> bool:
    return _load_builder() is not None


def derive_orientation(
    *,
    capability: str | None,
    context: dict[str, object] | None = None,
    execution_outcome: Any = None,
    source_facts: tuple[Any, ...] = (),
    routing_decision: Any = None,
    capability_snapshot: Any = None,
) -> Any | None:
    """Return bounded orientation or None when the builder cannot be used."""
    if not isinstance(capability, str) or not capability.strip():
        return None

    if not is_builder_available():
        return None
    loaded = _load_builder()
    if loaded is None:
        return None

    builder_cls, request_cls = loaded
    try:
        request = request_cls(
            capability=capability,
            context=dict(context or {}),
            execution_outcome=execution_outcome,
            source_facts=tuple(source_facts or ()),
            routing_decision=routing_decision,
            capability_snapshot=capability_snapshot,
        )
        return builder_cls().build(request)
    except Exception:
        return None


__all__ = ["derive_orientation", "is_builder_available"]
