from pathlib import Path


RECOVERY = Path(
    "docs/implementation/sql/ELO_AUTHZ_CANONICAL_ADMIN_BASELINE_RECOVERY_CANDIDATE.sql"
).read_text(encoding="utf-8")
SEQUENCE = Path(
    "docs/architecture/ELO_OBJECTIVE_CONTINUITY_ACTIVATION_SEQUENCE_20261102.md"
).read_text(encoding="utf-8")
BASELINE = Path(
    "supabase/migrations/20260912195000_elo_authorization_schema_baseline.sql"
).read_text(encoding="utf-8")


def test_recovery_is_non_live_and_bound_to_canonical_baseline() -> None:
    assert "CANDIDATE ONLY" in RECOVERY
    assert "NOT AUTHORIZED FOR LIVE DML/DDL" in RECOVERY
    assert "20260912195000_elo_authorization_schema_baseline.sql" in RECOVERY
    assert "r.code = 'CANONICAL_ADMIN'" in BASELINE


def test_recovery_restores_only_material_baseline_capabilities() -> None:
    for code in ("READ", "ADMIN", "CANONICAL_WRITE", "APPROVE"):
        assert f"'{code}'" in RECOVERY
    assert "v_required_count <> 4" in RECOVERY
    assert "v_existing_count <> 0" in RECOVERY
    assert "INSERT INTO public.elo_role_capabilities" in RECOVERY
    assert "INSERT INTO public.elo_capabilities" not in RECOVERY
    assert "INSERT INTO public.elo_roles" not in RECOVERY


def test_recovery_does_not_auto_delegate_strategic_capabilities() -> None:
    assert "c.code IN ('PROPOSE', 'REVIEW')" in RECOVERY
    assert "Delegable strategic capability was unexpectedly assigned" in RECOVERY
    assert "PROPOSE and REVIEW are intentionally NOT assigned" in RECOVERY


def test_activation_order_preserves_all_authority_boundaries() -> None:
    gates = [
        "Gate 1 — Deploy canonical `elo-authz`",
        "Gate 2 — Recover the canonical administrative baseline",
        "Gate 3 — Apply authorization drift remediation",
        "Gate 4 — Provision the strategic owner schema",
        "Gate 5 — Explicitly assign delegated strategic capability",
        "Gate 6 — Materialize the first operational Objective",
        "Gate 7 — Bootstrap Objective Continuity",
        "Gate 8 — Run the first real replay",
    ]
    positions = [SEQUENCE.index(gate) for gate in gates]
    assert positions == sorted(positions)


def test_sequence_forbids_checkpoint_first_bootstrap() -> None:
    assert "It must not be created in the continuity checkpoint table first." in SEQUENCE
    assert "No automation text or conversational memory is a checkpoint." in SEQUENCE
    assert "No checkpoint should be fabricated" in SEQUENCE


def test_runtime_activation_requires_explicit_governance() -> None:
    assert "A conversational instruction is not substituted for that control." in SEQUENCE
    assert "Technical service-role/database access is not authorization evidence." in SEQUENCE
    assert "does not choose recipients or assign them automatically" in SEQUENCE


def test_live_operational_completion_requires_runtime_evidence() -> None:
    assert "live-operational" in SEQUENCE
    assert "all eight gates have runtime evidence" in SEQUENCE
