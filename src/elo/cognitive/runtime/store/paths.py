"""Convenção de paths para memory/cognitive/.

Refs: memory/cognitive/README.md
"""
from __future__ import annotations
from pathlib import Path
ROOT = Path("memory") / "cognitive"
DECISIONS_DIR = ROOT / "decisions"
PRECEDENTS_DIR = ROOT / "precedents"
CALIBRATION_DIR = ROOT / "calibration"

def decision_dir(decision_id: str) -> Path: return DECISIONS_DIR / decision_id
def decision_lifecycle_path(decision_id: str) -> Path: return decision_dir(decision_id) / "lifecycle.json"
def decision_readme_path(decision_id: str) -> Path: return decision_dir(decision_id) / "README.md"
def decisions_index_path() -> Path: return DECISIONS_DIR / "index.json"
def precedents_index_path() -> Path: return PRECEDENTS_DIR / "index.json"
def calibration_path() -> Path: return CALIBRATION_DIR / "index.json"
def decision_analysis_path(decision_id: str) -> Path: return decision_dir(decision_id) / "chatgpt_analysis.md"
def decision_delta_path(decision_id: str) -> Path: return decision_dir(decision_id) / "delta.json"
