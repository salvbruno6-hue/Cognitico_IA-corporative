"""Background preparation loop for unattended Symbiont R&D.

This module deliberately stops at READY_FOR_APPROVAL. Scheduling, repository
writes and promotion can be supplied by infrastructure, but the loop itself
cannot promote candidates or mutate canonical ELO authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from elo.cognitive.symbiont_meta_evolution import (
    ApprovalPackage,
    ExternalPattern,
    SymbiontMetaEvolutionEngine,
)


@dataclass(frozen=True)
class BackgroundJob:
    job_id: str
    pattern: ExternalPattern
    candidate_id: str
    branch_ref: str
    proposed_changes: tuple[str, ...]


class SymbiontBackgroundLoop:
    """Prepare evolution candidates without acquiring promotion authority."""

    def __init__(
        self,
        engine: SymbiontMetaEvolutionEngine,
        executor: Callable[[BackgroundJob], tuple[bool, bool, bool, Iterable[str], dict[str, float]]],
    ) -> None:
        self.engine = engine
        self.executor = executor

    def run_once(self, job: BackgroundJob) -> ApprovalPackage:
        candidate = self.engine.prepare_candidate(
            job.pattern,
            candidate_id=job.candidate_id,
            branch_ref=job.branch_ref,
            proposed_changes=job.proposed_changes,
        )
        tests, regressions, benchmark, evidence, metrics = self.executor(job)
        evaluation = self.engine.evaluate(
            candidate,
            tests_passed=tests,
            regressions_passed=regressions,
            benchmark_improved=benchmark,
            evidence_ids=evidence,
            metrics=metrics,
        )
        return self.engine.approval_package(candidate, evaluation)

    def run_batch(self, jobs: Iterable[BackgroundJob]) -> tuple[ApprovalPackage, ...]:
        return tuple(self.run_once(job) for job in jobs)
