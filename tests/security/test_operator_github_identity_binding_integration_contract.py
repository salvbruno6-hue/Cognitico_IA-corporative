"""Integration-boundary tests for ELO identity binding.

This file intentionally tests only the local binding boundary. It must not be
interpreted as proof of live ChatGPT/GitHub authentication or GitHub API
permission enforcement.
"""


def resolve_binding(*, authenticated_provider_subject: str | None,
                    authenticated_github_login: str | None,
                    registered_provider_subject: str | None,
                    registered_github_login: str | None) -> bool:
    """Allow binding only when both authenticated subjects match registry."""
    if not authenticated_provider_subject or not authenticated_github_login:
        return False
    if not registered_provider_subject or not registered_github_login:
        return False
    return (
        authenticated_provider_subject == registered_provider_subject
        and authenticated_github_login == registered_github_login
    )


def test_matching_authenticated_subjects_bind():
    assert resolve_binding(
        authenticated_provider_subject="chatgpt:user:123",
        authenticated_github_login="salvbruno6-hue",
        registered_provider_subject="chatgpt:user:123",
        registered_github_login="salvbruno6-hue",
    ) is True


def test_provider_impersonation_cannot_bind():
    assert resolve_binding(
        authenticated_provider_subject="chatgpt:user:attacker",
        authenticated_github_login="salvbruno6-hue",
        registered_provider_subject="chatgpt:user:123",
        registered_github_login="salvbruno6-hue",
    ) is False


def test_github_impersonation_cannot_bind():
    assert resolve_binding(
        authenticated_provider_subject="chatgpt:user:123",
        authenticated_github_login="attacker-account",
        registered_provider_subject="chatgpt:user:123",
        registered_github_login="salvbruno6-hue",
    ) is False


def test_missing_authentication_cannot_bind():
    assert resolve_binding(
        authenticated_provider_subject=None,
        authenticated_github_login="salvbruno6-hue",
        registered_provider_subject="chatgpt:user:123",
        registered_github_login="salvbruno6-hue",
    ) is False
