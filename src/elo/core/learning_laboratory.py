"""Governed staging area for non-canonical ELO learning observations."""
from dataclasses import dataclass, field, replace
from typing import Mapping, Tuple

EXPERIENCE = "EXPERIENCE"
CANDIDATE = "CANDIDATE"
VALIDATED = "VALIDATED"
REJECTED = "REJECTED"
PROMOTED = "PROMOTED"


@dataclass(frozen=True)
class LearningObservation:
    observation_id: str
    tenant_id: str
    source_type: str
    problem: str
    result: str
    evidence_ids: Tuple[str, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)
    status: str = EXPERIENCE


class GovernedLearningLaboratory:
    """Store experience separately from canonical memory and knowledge."""

    def __init__(self) -> None:
        self._observations: dict[str, LearningObservation] = {}

    def record(self, observation: LearningObservation) -> LearningObservation:
        if not observation.observation_id or not observation.tenant_id:
            raise ValueError("observation_id and tenant_id are required")
        if observation.status != EXPERIENCE:
            raise ValueError("new observations must enter as EXPERIENCE")
        if observation.observation_id in self._observations:
            raise ValueError("observation_id already exists")
        self._observations[observation.observation_id] = observation
        return observation

    def list_tenant(self, tenant_id: str) -> Tuple[LearningObservation, ...]:
        return tuple(o for o in self._observations.values() if o.tenant_id == tenant_id)

    def propose(self, observation_id: str) -> LearningObservation:
        observation = self._get(observation_id)
        if not observation.evidence_ids:
            raise ValueError("learning candidate requires evidence")
        return self._transition(observation, CANDIDATE)

    def validate(self, observation_id: str) -> LearningObservation:
        observation = self._get(observation_id)
        if observation.status != CANDIDATE:
            raise ValueError("only candidates can be validated")
        return self._transition(observation, VALIDATED)

    def reject(self, observation_id: str) -> LearningObservation:
        observation = self._get(observation_id)
        if observation.status not in {CANDIDATE, VALIDATED}:
            raise ValueError("only candidates or validated observations can be rejected")
        return self._transition(observation, REJECTED)

    def promote(self, observation_id: str) -> LearningObservation:
        observation = self._get(observation_id)
        if observation.status != VALIDATED:
            raise ValueError("only validated learning can be promoted")
        return self._transition(observation, PROMOTED)

    def _get(self, observation_id: str) -> LearningObservation:
        try:
            return self._observations[observation_id]
        except KeyError as exc:
            raise KeyError(f"unknown learning observation: {observation_id}") from exc

    def _transition(self, observation: LearningObservation, status: str) -> LearningObservation:
        updated = replace(observation, status=status)
        self._observations[updated.observation_id] = updated
        return updated
