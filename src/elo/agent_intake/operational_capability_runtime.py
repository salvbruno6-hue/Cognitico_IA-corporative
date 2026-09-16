"""Operational bridge from ELO capability selection to native execution.

The CapabilityRegistry remains the discovery/availability authority. This module
keeps execution in the existing NativeELORuntime and provides the missing
Registry -> Selector -> Execution link without creating a second registry.

Successful executions may be recorded in the existing persistent memory contract
as immutable historical evidence. This records execution evidence only; it does
not promote learning or mutate Core.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass
from typing import Any

from elo.agent_intake.native_capabilities import CAPABILITY_IDS, NativeELORuntime
from elo.cognitive.reasoning.capability_selection import CapabilityRequirement, CapabilitySelector
from elo.core.capability_registry import CapabilityRegistry
from elo.memory.persistent import MemoryRecord, PersistentMemoryStore


@dataclass(frozen=True, slots=True)
class OperationalExecution:
    capability_id: str
    selected: bool
    result: Any
    evidence_memory_id: str | None = None


class OperationalCapabilityRuntime:
    """Select an available native capability and execute its existing mechanism."""

    def __init__(
        self,
        registry: CapabilityRegistry,
        *,
        tenant_scope: str = "elo-operational",
        evidence_store: PersistentMemoryStore | None = None,
    ) -> None:
        self.registry = registry
        self.tenant_scope = tenant_scope
        self.evidence_store = evidence_store
        self.native = NativeELORuntime()
        self._bootstrap_skills()
        self._bootstrap_toolsets()

    def _bootstrap_skills(self) -> None:
        self.native.register_skill(
            self.tenant_scope,
            "HERMES-SKILLS",
            lambda payload: {"echo": payload.get("value")},
        )

    def _bootstrap_toolsets(self) -> None:
        self.native.register_toolset(self.tenant_scope, "HERMES-TOOLSETS", ("read",))

    def execute(self, capability_id: str, payload: dict[str, Any] | None = None) -> OperationalExecution:
        if capability_id not in CAPABILITY_IDS:
            raise ValueError(f"unknown capability: {capability_id}")

        selection = CapabilitySelector(self.registry).select(CapabilityRequirement(capability_id))
        if selection.status != "SELECTED":
            raise RuntimeError(f"capability is not selectable: {capability_id}")

        data = dict(payload or {})
        if selection.capability_name != capability_id:
            raise RuntimeError("selector returned an unexpected capability")

        result = self._execute_native(capability_id, data)
        evidence_memory_id = self._record_evidence(capability_id, result) if self.evidence_store else None
        return OperationalExecution(capability_id, True, result, evidence_memory_id)

    def _record_evidence(self, capability_id: str, result: Any) -> str:
        memory_id = f"OP-EVIDENCE::{capability_id}::{uuid.uuid4()}"
        record = MemoryRecord(
            memory_id=memory_id,
            tenant_id=self.tenant_scope,
            domain="capability_execution",
            principal_id="elo-operational-runtime",
            content=json.dumps(
                {"capability_id": capability_id, "status": "completed", "selected": True},
                sort_keys=True,
            ),
            source_id=f"elo:operational-execution:{capability_id}",
            provenance={
                "source": "ELO OperationalCapabilityRuntime",
                "capability_id": capability_id,
                "result": repr(result),
                "promotion_state": "success",
                "canonical_mutation": False,
            },
            created_at=time.time(),
            kind="historical",
        )
        self.evidence_store.admit(record)
        return memory_id

    def _execute_native(self, capability_id: str, payload: dict[str, Any]) -> Any:
        if capability_id == "HERMES-MEMORY":
            key = str(payload.get("key", "operational"))
            value = payload.get("value", True)
            self.native.memory(self.tenant_scope, key, value, write=True)
            return {"value": self.native.memory(self.tenant_scope, key)}
        if capability_id == "HERMES-SKILLS":
            return self.native.execute_skill(self.tenant_scope, "HERMES-SKILLS", payload)
        if capability_id == "HERMES-TOOLSETS":
            capability = str(payload.get("capability", "read"))
            return {"allowed": self.native.resolve_tool(self.tenant_scope, "HERMES-TOOLSETS", capability)}
        if capability_id == "HERMES-CONTEXT":
            return self.native.assemble_context(dict(payload.get("parent", {})), dict(payload.get("child", {})))
        if capability_id == "HERMES-DELEGATION":
            return self.native.delegate(self.tenant_scope, lambda item: item.get("value"), payload)
        if capability_id == "HERMES-AUTOMATION":
            expression = str(payload.get("expression", "manual-safe-no-op"))
            return {"schedule": self.native.schedule(self.tenant_scope, "HERMES-AUTOMATION", expression)}
        if capability_id == "HERMES-MCP":
            capability = str(payload.get("capability", "capability.read"))
            allowlist = tuple(payload.get("allowlist", (capability,)))
            return self.native.gateway(self.tenant_scope, capability, allowlist)
        state = dict(payload.get("state", {"operational": True}))
        snapshot = self.native.checkpoint(self.tenant_scope, "HERMES-CHECKPOINT", state)
        return {"snapshot": snapshot, "restored": self.native.restore(self.tenant_scope, "HERMES-CHECKPOINT")}


__all__ = ["OperationalCapabilityRuntime", "OperationalExecution"]
