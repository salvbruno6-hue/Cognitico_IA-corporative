from elo.application.web_request_boundary import GovernedWebRequestBoundary, WebRequestBoundaryError


def test_web_request_preserves_identity_scope_and_provenance():
    request = GovernedWebRequestBoundary().accept(
        request_id="req-1", tenant_id="tenant-a", principal_id="principal-a",
        intent="review", scope="budget", evidence_ids=("ev-1",),
        provenance={"source_ref": "app", "source_commit": "abc"},
    )
    assert request.tenant_id == "tenant-a"
    assert request.principal_id == "principal-a"
    assert request.evidence_ids == ("ev-1",)


def test_web_request_rejects_secret_metadata():
    try:
        GovernedWebRequestBoundary().accept(
            request_id="req-1", tenant_id="tenant-a", principal_id="principal-a",
            intent="review", scope="budget", evidence_ids=(),
            provenance={"access_token": "secret"},
        )
    except WebRequestBoundaryError:
        return
    raise AssertionError("secret metadata must be rejected")
