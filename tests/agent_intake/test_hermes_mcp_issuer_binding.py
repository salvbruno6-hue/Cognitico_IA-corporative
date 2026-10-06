from elo.agent_intake.hermes_mcp_issuer_binding import MCPIssuerBinding, assess_issuer_binding

def test_matching_issuer_preserves_provenance_without_authorizing():
    r=assess_issuer_binding(MCPIssuerBinding("cred-1","issuer-a","issuer-a","prov-1"))
    assert r.valid is True
    assert r.authorization_permitted is False

def test_mismatched_issuer_is_rejected():
    r=assess_issuer_binding(MCPIssuerBinding("cred-2","issuer-a","issuer-b","prov-2"))
    assert r.valid is False
    assert r.reason=="issuer_binding_mismatch"

def test_reauth_requirement_blocks_binding():
    r=assess_issuer_binding(MCPIssuerBinding("cred-3","issuer-a","issuer-a","prov-3",True))
    assert r.valid is False
    assert r.reason=="reauthentication_required"

def test_missing_provenance_is_rejected():
    try:
        assess_issuer_binding(MCPIssuerBinding("cred-4","issuer-a","issuer-a",""))
    except ValueError as exc:
        assert "provenance" in str(exc)
    else:
        raise AssertionError("missing provenance must be rejected")
