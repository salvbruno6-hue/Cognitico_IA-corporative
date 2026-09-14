"""Native MCP capability selection and bounded execution authorization."""

from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.symbiont_mcp_contracts import MCPCapabilityDescriptor, MCPCapabilityState


@dataclass(frozen=True)
class MCPResolution:
    capability_id: str
    allowed: bool
    rationale: str
    max_tool_calls: int


class MCPCapabilityResolver:
    """Selects an already-discovered MCP capability without becoming its authority."""

    def resolve(
        self,
        descriptor: MCPCapabilityDescriptor,
        *,
        tenant_id: str,
        authorized: bool,
        requested_tool_calls: int = 1,
    ) -> MCPResolution:
        if tenant_id != descriptor.tenant_id:
            return MCPResolution(descriptor.capability_id, False, "tenant isolation failure", 0)
        if not authorized:
            return MCPResolution(descriptor.capability_id, False, "authorization required", 0)
        if descriptor.state not in {MCPCapabilityState.TESTABLE, MCPCapabilityState.TESTED, MCPCapabilityState.CANDIDATE}:
            return MCPResolution(descriptor.capability_id, False, "capability is not executable in current state", 0)
        if requested_tool_calls < 1 or requested_tool_calls > 10:
            return MCPResolution(descriptor.capability_id, False, "tool-call bound exceeded", 0)
        return MCPResolution(
            descriptor.capability_id,
            True,
            "authorized bounded MCP capability",
            requested_tool_calls,
        )
