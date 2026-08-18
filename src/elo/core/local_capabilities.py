"""Safe local-tool capability probes. No secret values are persisted."""
from .capability_registry import CapabilityProbe


def probe_local_tools(*, ollama_health=None, codex_health=None, github_cli_health=None,
                      python_health=None, node_health=None) -> tuple[CapabilityProbe, ...]:
    return (
        CapabilityProbe("LOCAL_AI", "ollama", health_check=ollama_health,
                        metadata={"source": "runtime_probe"}),
        CapabilityProbe("LOCAL_AI", "codex_cli", health_check=codex_health,
                        metadata={"source": "runtime_probe"}),
        CapabilityProbe("LOCAL_TOOL", "github_cli", health_check=github_cli_health,
                        metadata={"source": "runtime_probe"}),
        CapabilityProbe("LOCAL_TOOL", "python", health_check=python_health,
                        metadata={"source": "runtime_probe"}),
        CapabilityProbe("LOCAL_TOOL", "node", health_check=node_health,
                        metadata={"source": "runtime_probe"}),
    )
