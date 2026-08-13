"""Semantic directory intelligence primitives for repository governance."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DirectorySemanticProfile:
    path: str
    purpose: str
    responsibility: str
    authority: str
    lifecycle: str
    related_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class DirectoryAssessment:
    path: str
    action: str
    reason: str
    related_paths: tuple[str, ...] = ()
