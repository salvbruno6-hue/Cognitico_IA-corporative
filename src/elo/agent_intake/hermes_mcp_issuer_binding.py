"""Candidate-only issuer binding evidence for the canonical MCP gateway.
This module does not issue, refresh, revoke, store, or authorize tokens.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class MCPIssuerBinding:
    credential_ref: str
    issuer: str
    bound_issuer: str
    provenance_ref: str
    reauth_required: bool = False

@dataclass(frozen=True, slots=True)
class MCPIssuerAssessment:
    valid: bool
    reason: str
    authorization_permitted: bool = False

def assess_issuer_binding(binding: MCPIssuerBinding) -> MCPIssuerAssessment:
    if not binding.credential_ref.strip() or not binding.issuer.strip() or not binding.bound_issuer.strip():
        raise ValueError("credential and issuer binding are required")
    if not binding.provenance_ref.strip():
        raise ValueError("provenance_ref is required")
    if binding.issuer != binding.bound_issuer:
        return MCPIssuerAssessment(False, "issuer_binding_mismatch")
    if binding.reauth_required:
        return MCPIssuerAssessment(False, "reauthentication_required")
    return MCPIssuerAssessment(True, "issuer_binding_valid", False)
