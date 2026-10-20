from __future__ import annotations

from dataclasses import dataclass

import pytest

from elo.cognitive.reasoning.requirement_analysis import (
    ClaimProvenance,
    RequirementClaim,
    RequirementNode,
    RequirementSourceType,
    RequirementState,
    ResolutionAttemptKind,
    ResolutionAttemptStatus,
)
from elo.cognitive.reasoning.requirement_resolution import (
    RequirementResolutionFlow,
    ResolutionStepResult,
)


@dataclass
class Provider:
    kind: ResolutionAttemptKind
    result: ResolutionStepResult

    def resolve(self, node, parameter, claims):
        return self.result


def _node(*, claims=(), entity: str | None = "MLT-C08"):
    return RequirementNode(
        requirement_id="SO-203.26:R1",
        text="Definir espessura do MDF",
        entity=entity,
        claims=tuple(claims),
    )


def _claim(
    *,
    claim_id: str,
    value: str = "15 mm",
    subject: str = "MLT-C08",
    state: RequirementState = RequirementState.KNOWN,
    source_type: RequirementSourceType = RequirementSourceType.RULE,
    evidence_ids=("EV-1",),
    validation_status: str = "VALIDATED",
    requires_human_validation: bool = False,
):
    return RequirementClaim(
        claim_id=claim_id,
        requirement_id="SO-203.26:R1",
        subject=subject,
        predicate="mdf.thickness",
        value=value,
        state=state,
        provenance=ClaimProvenance(
            source_type=source_type,
            source_reference=f"fixture:{claim_id}",
            reasoning_method="fixture",
            evidence_ids=tuple(evidence_ids),
            validation_status=validation_status,
        ),
        requires_human_validation=requires_human_validation,
    )


def test_preloaded_known_claim_with_llm_provenance_cannot_short_circuit():
    invalid = _claim(
        claim_id="PRELOAD-LLM",
        source_type=RequirementSourceType.LLM_INFERENCE,
    )

    with pytest.raises(ValueError, match="cannot use LLM_INFERENCE provenance"):
        RequirementResolutionFlow(providers={}).resolve(
            node=_node(claims=(invalid,)),
            parameter="mdf.thickness",
        )


def test_preloaded_known_claim_requires_governed_validation_and_evidence():
    unvalidated = _claim(
        claim_id="PRELOAD-UNVERIFIED",
        evidence_ids=(),
        validation_status="UNVERIFIED",
    )

    with pytest.raises(ValueError, match="requires nonblank evidence_ids"):
        RequirementResolutionFlow(providers={}).resolve(
            node=_node(claims=(unvalidated,)),
            parameter="mdf.thickness",
        )


def test_preloaded_automatic_claim_for_other_entity_is_rejected():
    wrong_entity = _claim(
        claim_id="PRELOAD-OTHER",
        subject="PRODUCT-B",
    )

    with pytest.raises(ValueError, match="entity does not match target entity"):
        RequirementResolutionFlow(providers={}).resolve(
            node=_node(claims=(wrong_entity,)),
            parameter="mdf.thickness",
        )


def test_explicit_documented_preloaded_claim_remains_valid_without_separate_evidence_id():
    documented = _claim(
        claim_id="DOC-EXPLICIT",
        state=RequirementState.DOCUMENTED,
        source_type=RequirementSourceType.DOCUMENT,
        evidence_ids=(),
        validation_status="EXTRACTED",
    )

    result = RequirementResolutionFlow(providers={}).resolve(
        node=_node(claims=(documented,)),
        parameter="mdf.thickness",
    )

    assert result.assessment.state is RequirementState.DOCUMENTED
    assert result.attempts == ()


def test_conflicting_preloaded_governed_values_surface_conflict():
    first = _claim(claim_id="PRELOAD-15", value="15 mm")
    second = _claim(claim_id="PRELOAD-18", value="18 mm")

    result = RequirementResolutionFlow(providers={}).resolve(
        node=_node(claims=(first, second)),
        parameter="mdf.thickness",
    )

    assert result.assessment.state is RequirementState.CONFLICT
    assert result.assessment.human_validation_required is True


def test_rule_stage_with_two_governed_values_surfaces_conflict():
    first = _claim(claim_id="RULE-15", value="15 mm")
    second = _claim(claim_id="RULE-18", value="18 mm")
    provider = Provider(
        kind=ResolutionAttemptKind.RULE,
        result=ResolutionStepResult(
            source_reference="rule-engine:v1",
            claims=(first, second),
        ),
    )

    result = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RULE: provider}
    ).resolve(node=_node(), parameter="mdf.thickness")

    assert result.attempts[0].status is ResolutionAttemptStatus.CONFLICT
    assert result.assessment.state is RequirementState.CONFLICT
    assert result.assessment.human_validation_required is True


def test_calculation_stage_with_two_governed_values_surfaces_conflict():
    first = _claim(
        claim_id="CALC-15",
        value="15 mm",
        state=RequirementState.CALCULATED,
        source_type=RequirementSourceType.CALCULATION,
    )
    second = _claim(
        claim_id="CALC-18",
        value="18 mm",
        state=RequirementState.CALCULATED,
        source_type=RequirementSourceType.CALCULATION,
    )
    provider = Provider(
        kind=ResolutionAttemptKind.CALCULATION,
        result=ResolutionStepResult(
            source_reference="calculator:v1",
            claims=(first, second),
        ),
    )

    result = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.CALCULATION: provider}
    ).resolve(node=_node(), parameter="mdf.thickness")

    assert result.attempts[0].status is ResolutionAttemptStatus.CONFLICT
    assert result.assessment.state is RequirementState.CONFLICT
