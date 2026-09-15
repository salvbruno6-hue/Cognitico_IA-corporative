"""Native, Hermes-independent execution surfaces for the eight capability candidates.

Deterministic and side-effect free. These primitives let ELO validate the eight
candidate contracts through GitHub Actions without a Hermes endpoint.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

CAPABILITY_IDS = (
    "HERMES-MEMORY", "HERMES-SKILLS", "HERMES-TOOLSETS", "HERMES-CONTEXT",
    "HERMES-DELEGATION", "HERMES-AUTOMATION", "HERMES-MCP", "HERMES-CHECKPOINT",
)

@dataclass(frozen=True, slots=True)
class NativeEvidence:
    capability_id: str
    request_id: str
    tenant_scope: str
    status: str
    evidence: tuple[dict[str, Any], ...]
    outcome: dict[str, Any]
    learning_candidate: dict[str, Any]

@dataclass(slots=True)
class NativeELORuntime:
    _memory: dict[tuple[str, str], Any] = field(default_factory=dict)
    _skills: dict[tuple[str, str], Callable[[dict[str, Any]], Any]] = field(default_factory=dict)
    _toolsets: dict[tuple[str, str], tuple[str, ...]] = field(default_factory=dict)
    _schedules: dict[tuple[str, str], str] = field(default_factory=dict)
    _checkpoints: dict[tuple[str, str], dict[str, Any]] = field(default_factory=dict)

    def _key(self, tenant: str, name: str) -> tuple[str, str]:
        if not tenant.strip() or not name.strip():
            raise ValueError("tenant and name are required")
        return tenant, name

    def memory(self, tenant: str, key: str, value: Any = None, *, write: bool = False) -> Any:
        k = self._key(tenant, key)
        if write:
            self._memory[k] = value
        return self._memory.get(k)

    def register_skill(self, tenant: str, name: str, handler: Callable[[dict[str, Any]], Any]) -> None:
        self._skills[self._key(tenant, name)] = handler

    def execute_skill(self, tenant: str, name: str, payload: dict[str, Any]) -> Any:
        handler = self._skills.get(self._key(tenant, name))
        if handler is None:
            raise KeyError(f"skill not registered: {name}")
        return handler(dict(payload))

    def register_toolset(self, tenant: str, name: str, capabilities: tuple[str, ...]) -> None:
        self._toolsets[self._key(tenant, name)] = tuple(capabilities)

    def resolve_tool(self, tenant: str, name: str, capability: str) -> bool:
        return capability in self._toolsets.get(self._key(tenant, name), ())

    def assemble_context(self, parent: dict[str, Any], child: dict[str, Any]) -> dict[str, Any]:
        merged = dict(parent)
        merged.update(child)
        return merged

    def delegate(self, tenant: str, worker: Callable[[dict[str, Any]], Any], payload: dict[str, Any]) -> dict[str, Any]:
        return {"tenant_scope": tenant, "result": worker(dict(payload))}

    def schedule(self, tenant: str, name: str, expression: str) -> str:
        self._schedules[self._key(tenant, name)] = expression
        return expression

    def gateway(self, tenant: str, capability: str, allowlist: tuple[str, ...]) -> dict[str, Any]:
        return {"tenant_scope": tenant, "capability": capability, "allowed": capability in allowlist}

    def checkpoint(self, tenant: str, name: str, state: dict[str, Any]) -> dict[str, Any]:
        snapshot = dict(state)
        self._checkpoints[self._key(tenant, name)] = snapshot
        return dict(snapshot)

    def restore(self, tenant: str, name: str) -> dict[str, Any]:
        return dict(self._checkpoints.get(self._key(tenant, name), {}))


def execute_candidate(capability_id: str, *, request_id: str, tenant_scope: str) -> NativeEvidence:
    if capability_id not in CAPABILITY_IDS:
        raise ValueError(f"unknown candidate: {capability_id}")
    runtime = NativeELORuntime()
    if capability_id == "HERMES-MEMORY":
        runtime.memory(tenant_scope, "probe", {"value": 1}, write=True)
        evidence = {"operation": "write_read", "value": runtime.memory(tenant_scope, "probe")}
        outcome = {"retrievable": evidence["value"] == {"value": 1}}
    elif capability_id == "HERMES-SKILLS":
        runtime.register_skill(tenant_scope, "probe", lambda payload: {"echo": payload["value"]})
        result = runtime.execute_skill(tenant_scope, "probe", {"value": "ok"})
        evidence = {"operation": "skill_execute", "result": result}
        outcome = {"executed": result == {"echo": "ok"}}
    elif capability_id == "HERMES-TOOLSETS":
        runtime.register_toolset(tenant_scope, "probe", ("read",))
        evidence = {"allow": runtime.resolve_tool(tenant_scope, "probe", "read"), "deny": runtime.resolve_tool(tenant_scope, "probe", "write")}
        outcome = {"allowlist_enforced": evidence["allow"] and not evidence["deny"]}
    elif capability_id == "HERMES-CONTEXT":
        context = runtime.assemble_context({"parent": 1, "shared": "parent"}, {"child": 2, "shared": "child"})
        evidence = {"context": context}
        outcome = {"precedence": context["shared"] == "child"}
    elif capability_id == "HERMES-DELEGATION":
        result = runtime.delegate(tenant_scope, lambda payload: payload["value"] + 1, {"value": 1})
        evidence = {"delegated": result}
        outcome = {"result_returned": result["result"] == 2}
    elif capability_id == "HERMES-AUTOMATION":
        expression = runtime.schedule(tenant_scope, "probe", "manual-safe-no-op")
        evidence = {"schedule": expression}
        outcome = {"registered": expression == "manual-safe-no-op"}
    elif capability_id == "HERMES-MCP":
        result = runtime.gateway(tenant_scope, "capability.read", ("capability.read",))
        evidence = {"gateway": result}
        outcome = {"trust_boundary_enforced": result["allowed"]}
    else:
        runtime.checkpoint(tenant_scope, "probe", {"version": 1, "value": "safe"})
        restored = runtime.restore(tenant_scope, "probe")
        evidence = {"snapshot": restored}
        outcome = {"restored": restored == {"version": 1, "value": "safe"}}
    passed = all(outcome.values())
    return NativeEvidence(
        capability_id=capability_id, request_id=request_id, tenant_scope=tenant_scope,
        status="completed" if passed else "failed", evidence=(evidence,), outcome=outcome,
        learning_candidate={"promotion_state": "candidate_only", "canonical_mutation": False},
    )

__all__ = ["CAPABILITY_IDS", "NativeEvidence", "NativeELORuntime", "execute_candidate"]
