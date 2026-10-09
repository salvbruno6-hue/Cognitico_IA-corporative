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

from .orchestrator import GovernedOrchestrator, OrchestrationRequest
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
        request: OrchestrationRequest,
        audience: OrchestrationAudience,
        forge,
    ) -> OrchestrationViewResult:
        """Expose governed Forge analysis to a corporate operational surface.

        The canonical orchestrator performs the Forge consultation first so
        evidence continuity remains identical to conversational ELO behavior.
        The view composer then projects the raw governed context when available.

        This façade deliberately does not execute, approve, learn or mutate.
        """
        # Preserve canonical evidence creation/human consultation side effects
        # in the read-side repository; this validates the same bounded path used
        # by CognitiveCore. The presentation view itself is built only from an
        # explicit governed context returned by the Forge adapter.
        self.orchestrator.consult_forge(request, forge)

        import re

        match = re.search(r"\b(?:MLT\.)?M\d{2}\b", request.objective, flags=re.IGNORECASE)
        if match:
            context = forge.governed_model_context(match.group(0).upper(), request.objective)
        else:
            context = forge.governed_demand_context(request.objective)

        return self.composer.operational_view(
            audience=audience,
            forge_context=context,
        )


__all__ = ["GovernedOrchestratorReadSurface"]
