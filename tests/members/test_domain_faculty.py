from members.faculty.domain_faculty import (
    ComparisonKind,
    DomainFaculty,
    LogicStep,
    build_overlay,
    compare_faculty,
)


def faculty(*steps: str) -> DomainFaculty:
    return DomainFaculty(
        domain="COMERCIAL",
        version="1.0",
        objective="qualify and convert an opportunity",
        steps=tuple(LogicStep(name=step, kind="process") for step in steps),
    )


def test_same_cycle_is_compatible() -> None:
    result = compare_faculty(faculty("intake", "qualify", "proposal"), faculty("intake", "qualify", "proposal"))
    assert result.classification is ComparisonKind.COMPATIBLE
    assert result.shared_steps == frozenset({"intake", "qualify", "proposal"})


def test_new_mechanic_is_complement_and_does_not_mutate_faculty() -> None:
    canonical = faculty("intake", "qualify", "proposal")
    candidate = faculty("intake", "qualify", "risk-check", "proposal")
    result = compare_faculty(canonical, candidate)
    assert result.classification is ComparisonKind.COMPLEMENT
    assert result.added_steps == frozenset({"risk-check"})
    assert canonical.step_names == frozenset({"intake", "qualify", "proposal"})


def test_missing_and_added_steps_are_variation() -> None:
    result = compare_faculty(faculty("intake", "qualify", "proposal"), faculty("intake", "approval", "proposal"))
    assert result.classification is ComparisonKind.VARIATION
    assert result.missing_steps == frozenset({"qualify"})
    assert result.added_steps == frozenset({"approval"})


def test_overlay_is_removable_and_keeps_source_member() -> None:
    canonical = faculty("intake", "qualify", "proposal")
    candidate = faculty("intake", "qualify", "risk-check", "proposal")
    result = compare_faculty(canonical, candidate)
    overlay = build_overlay(candidate, "ELO-COMERCIAL-B", result, "commercial-b-risk-check")
    assert overlay.removable is True
    assert overlay.source_member == "ELO-COMERCIAL-B"
    assert "risk-check" in overlay.differences


def test_domain_mismatch_is_conflict() -> None:
    canonical = faculty("intake", "qualify")
    other = DomainFaculty(
        domain="PRODUCAO",
        version="1.0",
        objective="schedule production",
        steps=(LogicStep("schedule", "process"),),
    )
    result = compare_faculty(canonical, other)
    assert result.classification is ComparisonKind.CONFLICT


def test_overlay_rejects_compatible_result() -> None:
    canonical = faculty("intake", "qualify")
    result = compare_faculty(canonical, faculty("intake", "qualify"))
    try:
        build_overlay(canonical, "ELO-COMERCIAL-A", result, "invalid")
    except ValueError:
        pass
    else:
        raise AssertionError("compatible cycles must not create overlays")
