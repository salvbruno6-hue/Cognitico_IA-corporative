import pytest

from elo.adapters.chatgpt_project import ChatGPTProjectAdapter, ProjectSearchRequest


def test_unconnected_project_adapter_reports_access_gap():
    adapter = ChatGPTProjectAdapter()
    assert adapter.available is False
    with pytest.raises(RuntimeError, match="not connected"):
        adapter.search(
            ProjectSearchRequest(
                query="Multiteiner",
                tenant_id="tenant-1",
                principal="user-1",
            )
        )


def test_project_adapter_requires_identity_context():
    adapter = ChatGPTProjectAdapter()
    with pytest.raises(PermissionError):
        adapter.search(ProjectSearchRequest(query="Multiteiner"))


def test_project_adapter_rejects_unsupported_scope():
    adapter = ChatGPTProjectAdapter()
    with pytest.raises(PermissionError):
        adapter.search(
            ProjectSearchRequest(
                query="Multiteiner",
                tenant_id="tenant-1",
                principal="user-1",
                authorization_scope="chatgpt_project.write",
            )
        )
