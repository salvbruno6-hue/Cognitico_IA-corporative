"""Leitura/escrita em memory/cognitive/.

Persistência fina. Não substitui o Core, apenas serializa seu estado para disco.

Refs: ADR-0014, ADR-0015.
"""
from __future__ import annotations
import json
from elo.core.calibration import ConfidenceCalibration
from elo.core.decision_outcome_loop import DecisionLifecycle
from elo.core.precedent_index import PrecedentIndex
from ..serialization import calibration_serializer, decision_serializer, precedent_serializer
from . import paths

class DecisionStore:
    def save(self, lifecycle: DecisionLifecycle) -> None:
        decision_id = lifecycle.decision.decision_id
        d = paths.decision_dir(decision_id)
        d.mkdir(parents=True, exist_ok=True)
        payload = decision_serializer.serialize(lifecycle)
        paths.decision_lifecycle_path(decision_id).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        self._update_index(lifecycle)

    def load(self, decision_id: str) -> DecisionLifecycle | None:
        p = paths.decision_lifecycle_path(decision_id)
        if not p.exists(): return None
        return decision_serializer.deserialize(json.loads(p.read_text(encoding="utf-8")))

    def _update_index(self, lifecycle: DecisionLifecycle) -> None:
        idx_path = paths.decisions_index_path()
        idx_path.parent.mkdir(parents=True, exist_ok=True)
        idx = json.loads(idx_path.read_text(encoding="utf-8")) if idx_path.exists() else []
        entry = {"canonical_key": lifecycle.decision.decision_id, "path": f"{lifecycle.decision.decision_id}/index.json", "state": lifecycle.state.value}
        idx = [e for e in idx if e.get("canonical_key") != lifecycle.decision.decision_id]
        idx.append(entry)
        idx_path.write_text(json.dumps(idx, indent=2, ensure_ascii=False), encoding="utf-8")

class PrecedentStore:
    def save(self, index: PrecedentIndex) -> None:
        p = paths.precedents_index_path()
        p.parent.mkdir(parents=True, exist_ok=True)
        payload = [precedent_serializer.to_dict(x) for x in index._items.values()]
        p.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def load(self) -> PrecedentIndex:
        p = paths.precedents_index_path()
        index = PrecedentIndex()
        if not p.exists(): return index
        for entry in json.loads(p.read_text(encoding="utf-8")):
            precedent = precedent_serializer.from_dict(entry)
            index._items[precedent.decision_id] = precedent
        return index

class CalibrationStore:
    def save(self, calibration: ConfidenceCalibration) -> None:
        p = paths.calibration_path()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(calibration_serializer.to_dict(calibration), indent=2, ensure_ascii=False), encoding="utf-8")

    def load(self) -> ConfidenceCalibration:
        p = paths.calibration_path()
        if not p.exists(): return ConfidenceCalibration()
        return calibration_serializer.from_dict(json.loads(p.read_text(encoding="utf-8")))
