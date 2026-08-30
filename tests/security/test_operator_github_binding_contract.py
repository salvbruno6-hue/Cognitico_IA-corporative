"""Deterministic contract tests for the ELO operator/GitHub boundary.

These tests validate the governance decision table without claiming that a
provider/runtime integration exists. Runtime authentication and GitHub
permission enforcement remain separate integration concerns.
"""


def authorize(*, binding: bool, repository_scope: bool, capability: str,
               structural: bool, gates_pass: bool) -> str:
    if not binding:
        return "DENY"
    if not repository_scope:
        return "ACCESS_SCOPE_VIOLATION"
    if capability not in {"READ", "COMMIT", "CREATE_PR", "MERGE_OPERATIONAL"}:
        return "DENY"
    if structural:
        return "ESCALATE"
    if capability == "MERGE_OPERATIONAL" and not gates_pass:
        return "BLOCKED"
    return "ALLOW"


def test_connected_github_is_not_operator_binding():
    assert authorize(
        binding=False, repository_scope=True, capability="MERGE_OPERATIONAL",
        structural=False, gates_pass=True
    ) == "DENY"


def test_authorized_operational_merge_is_allowed_after_gates():
    assert authorize(
        binding=True, repository_scope=True, capability="MERGE_OPERATIONAL",
        structural=False, gates_pass=True
    ) == "ALLOW"


def test_out_of_scope_credential_is_denied():
    assert authorize(
        binding=True, repository_scope=False, capability="READ",
        structural=False, gates_pass=True
    ) == "ACCESS_SCOPE_VIOLATION"


def test_structural_change_requires_escalation():
    assert authorize(
        binding=True, repository_scope=True, capability="MERGE_OPERATIONAL",
        structural=True, gates_pass=True
    ) == "ESCALATE"


def test_merge_is_blocked_when_required_gates_fail():
    assert authorize(
        binding=True, repository_scope=True, capability="MERGE_OPERATIONAL",
        structural=False, gates_pass=False
    ) == "BLOCKED"


def test_untrusted_admin_capability_is_denied():
    assert authorize(
        binding=True, repository_scope=True, capability="ELO_ADMIN",
        structural=False, gates_pass=True
    ) == "DENY"
