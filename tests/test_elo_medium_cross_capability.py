from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

COGNITIVE_CONTRACT = ROOT / "01-meta-architecture/cognitive-architecture/ELO_COGNITIVE_EXECUTION_CONTRACT.md"
ACCEPTANCE = ROOT / "01-meta-architecture/cognitive-architecture/ELO_022_ACCEPTANCE_TESTS.md"
MT001 = ROOT / "04-knowledge-handbook/MT001_COGNITIVE_CYCLE_TEST.md"
PCP = ROOT / "docs/forge/skills/PCP_SKILL_UDEMY_APPLIED_KNOWLEDGE.md"
AUDIT = ROOT / "docs/governance/ELO_CAPABILITY_IMPLEMENTATION_AUDIT_2026-08-17.md"


def _text(path: Path) -> str:
    assert path.exists(), f"Canonical validation artifact missing: {path}"
    return path.read_text(encoding="utf-8")


def test_cognitive_core_forge_application_infrastructure_boundaries_remain_distinct():
    text = _text(COGNITIVE_CONTRACT)
    assert "ELO Cognitivo       = supervises, reasons, decides" in text
    assert "ELO Core            = materializes canonical capabilities" in text
    assert "ELO Forge           = constructs, tests and corrects" in text
    assert "Validation/Governance = verifies and can block promotion" in text
    assert "GitHub/main         = canonical repository state" in text
    assert "without introducing a separate Supervisor, Orchestrator, Core or memory authority" in text


def test_provenance_gap_and_evidence_lifecycle_is_governed():
    contract = _text(COGNITIVE_CONTRACT)
    mt001 = _text(MT001)
    pcp = _text(PCP)
    assert "Evidence MUST retain provenance and type" in contract
    assert "Evidence, inference, hypothesis, recommendation and decision MUST NOT be stored as interchangeable facts" in contract
    assert "FACT | COMMITTED | AVAILABLE | ASSUMPTION | ESTIMATE | HYPOTHESIS | GAP | CONFLICT" in pcp
    assert "WAITING_FEEDBACK" in mt001
    assert "GAP" in mt001
    assert "New feedback creates a new evidence/result state" in mt001


def test_governed_cognitive_execution_lifecycle_has_no_gate_bypass():
    contract = _text(COGNITIVE_CONTRACT)
    acceptance = _text(ACCEPTANCE)
    for state in (
        "CREATED",
        "UNDERSTANDING",
        "PLANNING",
        "EXECUTING",
        "VALIDATING",
        "SPECIALIST_REVIEW",
        "ELO_ARCHITECTURAL_REVIEW",
        "APPROVED",
        "MERGING",
        "POST_MERGE_VERIFY",
        "COMPLETED",
    ):
        assert state in contract
    assert "No transition may bypass required repository gates." in contract
    assert "Merge followed by completion without post-merge verification" in acceptance


def test_specialist_technical_ownership_stays_in_forge():
    pcp = _text(PCP)
    assert "Forge PCP Specialist" in pcp
    assert "The PCP specialist may use the course as a learning aid" in pcp
    assert "The original experience remains in Forge." in pcp
    assert "promote to Core only after generalization, validation and Evolution Gate approval" in pcp


def test_budgeting_consumes_governed_inputs_and_keeps_missing_authority_as_a_gap():
    audit = _text(AUDIT)
    assert "ELO-024" in audit
    assert "Source adapters, price authority, demand/forecast ingestion, resource planning, quotation" in audit
    assert "actual authorized source retrieval" in audit
    assert "stale-input/temporal-validity enforcement" in audit
    assert "The next maturity transition requires reproducible test evidence tied to a commit/run." in audit


def test_no_second_cognitive_authority_is_accepted():
    contract = _text(COGNITIVE_CONTRACT)
    acceptance = _text(ACCEPTANCE)
    assert "parallel Supervisor/Core/Orchestrator authority" in contract
    assert "Creation of a parallel Supervisor/Orchestrator/Core authority" in acceptance
    assert "Reject" in acceptance
