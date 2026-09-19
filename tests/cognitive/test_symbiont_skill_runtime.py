from dataclasses import dataclass

import pytest

from elo.cognitive.symbiont_skill_runtime import SymbiontSkillRuntime
from elo.cognitive.symbiont_operational_contract import SymbiontOperation


@dataclass(frozen=True)
class Request:
    operation: str = "query"
    tenant_scope: str = "tenant-a"
    confidence: float = 0.80
    evidence_ids: tuple[str, ...] = ("ev-1",)
    canonical_mutation_allowed: bool = False
    authority: str = "recommend"


def test_skill_001_is_runnable_through_runtime_adapter():
    SymbiontSkillRuntime.validate_boundary(Request())


def test_skill_001_remains_fail_closed():
    with pytest.raises(ValueError):
        SymbiontSkillRuntime.validate_boundary(
            Request(operation="write")
        )


def test_skill_001_operation_dispatch_uses_canonical_contract():
    assert SymbiontSkillRuntime.validate_operation("query") == SymbiontOperation.QUERY.value


def test_runtime_exposes_all_four_skill_paths():
    assert callable(SymbiontSkillRuntime.validate_boundary)
    assert callable(SymbiontSkillRuntime.handoff_decision)
    assert callable(SymbiontSkillRuntime.evaluate_lab)
    assert callable(SymbiontSkillRuntime.propose_capability)
