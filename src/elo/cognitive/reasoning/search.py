from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Iterable, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class SearchNode(Generic[T]):
    state: T
    score: float
    depth: int
    path: tuple[T, ...] = ()


@dataclass(frozen=True, slots=True)
class SearchResult(Generic[T]):
    state: T
    score: float
    path: tuple[T, ...]
    explored: int


class BreadthDeliberativeSearch(Generic[T]):
    """Small dependency-free search primitive inspired by deliberative ToT.

    Domain code supplies expansion and evaluation. The engine itself remains
    agnostic to LLM providers and can later be backed by a learned policy.
    """

    def __init__(self, *, width: int = 3, depth: int = 3) -> None:
        if width < 1 or depth < 1:
            raise ValueError("width and depth must be >= 1")
        self.width = width
        self.depth = depth

    def solve(
        self,
        initial: T,
        expand: Callable[[T], Iterable[T]],
        evaluate: Callable[[T], float],
        accept: Callable[[T, float], bool] | None = None,
    ) -> SearchResult[T]:
        frontier = [SearchNode(initial, evaluate(initial), 0, (initial,))]
        best = frontier[0]
        explored = 1

        if accept and accept(initial, best.score):
            return SearchResult(initial, best.score, best.path, explored)

        for depth in range(1, self.depth + 1):
            candidates: list[SearchNode[T]] = []
            for node in frontier:
                for child in expand(node.state):
                    score = evaluate(child)
                    candidates.append(
                        SearchNode(child, score, depth, node.path + (child,))
                    )
                    explored += 1

            candidates.sort(key=lambda node: node.score, reverse=True)
            frontier = candidates[: self.width]
            if not frontier:
                break

            if frontier[0].score > best.score:
                best = frontier[0]

            if accept and accept(best.state, best.score):
                break

        return SearchResult(best.state, best.score, best.path, explored)
