"""Audience-aware read surface for the canonical GovernedOrchestrator.

This façade makes the orchestrator's two presentation responsibilities explicit:

* systemic/admin view: architecture, governance, capabilities, skills, gaps and
  their operational impact for ELO administrators/developers;
* operational view: Forge-grounded corporate analysis for ELO Web or another
  operational interface.

It does not become an authorization authority. The caller must supply the
already-resolved audience from the canonical identity/authorization boundary.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from elo.cognitive.symbiont_capability_governance import GlobalCapabilityVisibility

from .orchestrator import GovernedOrchestrator
from .orchestration_views import (
    OrchestrationAudience,
    OrchestrationViewComposer,
    OrchestrationViewResult,
)


@dataclass(slots=True)
class GovernedOrchestratorReadSurface:
    orchestrator: GovernedOrchestrator
    composer: OrchestrationViewComposer

    @classmethod
    def build(cls, orchestrator: GovernedOrchestrator) -> "GovernedOrchestratorReadSurface":
        return cls(orchestrator=orchestrator, composer=OrchestrationViewComposer())

    def systemic_overview(
        self,
        *,
        audience: OrchestrationAudience,
        visibility: GlobalCapabilityVisibility,
        skill_statuses: Sequence[Mapping[str, Any]] = (),
        forge_context: Mapping[str, Any] | None = None,
    ) -> OrchestrationViewResult:
        """Explain ELO health/architecture to an authorized admin/developer.

        ``audience`` is trusted only as an already-resolved read scope supplied
        by elo-authz/identity integration. This method does not authenticate or
        authorize a principal by itself.
        """
        return self.composer.systemic_view(
            audience=audience,
            visibility=visibility,
            skill_statuses=skill_statuses,
            operational_context=forge_context,
        )

    def operational_overview(
        self,
        *,
        audience: OrchestrationAudience,
        forge_context: Mapping[str, Any],
    ) -> OrchestrationViewResult:
        """Project an already-governed Forge context for an operational UI.

        The caller supplies the same context produced by the canonical Forge
        consultation path.  This avoids a second read and keeps presentation
        synchronized with the evidence already attached to that consultation.

        This façade deliberately does not query, execute, approve, learn or
        mutate by itself.
        """
        return self.composer.operational_view(
            audience=audience,
            forge_context=forge_context,
        )


__all__ = ["GovernedOrchestratorReadSurface"]
