"""Governed parsing of Hermes-style context references for ELO.

This module is intentionally a boundary contract: it parses and classifies
reference syntax but does not read files, execute git, fetch URLs, or create a
new source authority. Resolution remains owned by ELO's ArtifactResolver,
SourceDiscovery and SourceResolver contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Literal


ReferenceKind = Literal["file", "folder", "diff", "staged", "git", "url"]
ReferenceOwner = Literal["artifact_resolver", "source_discovery"]

_BUILTIN_SIMPLE = {"diff", "staged"}
_BUILTIN_NAMED = {"file", "folder", "git", "url"}
_PATTERN = re.compile(
    r"(?<![\\w/])@(?:(?P<simple>diff|staged)\\b|"
    r"(?P<kind>file|folder|git|url):(?P<value>`[^`\\n]+`|\"[^\"\\n]+\"|'[^'\\n]+'|\\S+))"
)
_FILE_PATTERN = re.compile(
    r"^(?:(?P<quote>`|\"|')(?P<path>.+?)(?P=quote)|(?P<bare>.+?))"
    r"(?::(?P<start>\\d+)(?:-(?P<end>\\d+))?)?$"
)


@dataclass(frozen=True, slots=True)
class ContextReference:
    """Immutable reference intent; no content is attached or fetched."""

    raw: str
    kind: ReferenceKind
    target: str
    start: int
    end: int
    line_start: int | None = None
    line_end: int | None = None

    @property
    def owner(self) -> ReferenceOwner:
        return "artifact_resolver" if self.kind in {"file", "folder"} else "source_discovery"

    @property
    def required_capability(self) -> str | None:
        if self.kind in {"diff", "staged", "git"}:
            return "source.github.read"
        if self.kind == "url":
            return "source.web.read"
        return None


def parse_context_references(message: str) -> tuple[ContextReference, ...]:
    """Parse supported Hermes-style references without executing their targets."""
    if not message:
        return ()
    references: list[ContextReference] = []
    for match in _PATTERN.finditer(message):
        kind = match.group("simple") or match.group("kind")
        value = _strip_trailing_punctuation(match.group("value") or "")
        line_start: int | None = None
        line_end: int | None = None
        if kind == "file":
            target, line_start, line_end = _parse_file_value(value)
        elif kind in _BUILTIN_NAMED:
            target = _strip_wrappers(value)
        else:
            target = ""
        references.append(
            ContextReference(
                raw=match.group(0),
                kind=kind,  # type: ignore[arg-type]
                target=target,
                start=match.start(),
                end=match.end(),
                line_start=line_start,
                line_end=line_end,
            )
        )
    return tuple(references)


def _parse_file_value(value: str) -> tuple[str, int | None, int | None]:
    match = _FILE_PATTERN.match(value)
    if not match:
        return _strip_wrappers(value), None, None
    target = match.group("path") if match.group("quote") else match.group("bare")
    start_text = match.group("start")
    end_text = match.group("end")
    start = int(start_text) if start_text else None
    end = int(end_text) if end_text else start
    return target or "", start, end


def _strip_wrappers(value: str) -> str:
    if len(value) >= 2 and value[0] in "`\"'" and value[-1] == value[0]:
        return value[1:-1]
    return value


def _strip_trailing_punctuation(value: str) -> str:
    return value.rstrip(",.;!?")


__all__ = ["ContextReference", "parse_context_references"]
