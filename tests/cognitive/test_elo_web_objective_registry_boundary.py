from pathlib import Path


PREFINALIZE = Path("apps/elo-web/src/app/api/elo/chat/prefinalize/route.ts").read_text(encoding="utf-8")
CONTINUITY = Path("apps/elo-web/src/lib/elo-objective-continuity.ts").read_text(encoding="utf-8")
ARCHITECTURE = Path("docs/architecture/ELO_OBJECTIVE_CONTINUITY_LOOP.md").read_text(encoding="utf-8")


def test_prefinalize_resolves_objective_from_canonical_strategic_owner() -> None:
    assert '.from("elo_strategic_objectives")' in PREFINALIZE
    assert '.eq("tenant_id", tenantId)' in PREFINALIZE
    assert '.eq("objective_id", objectiveId)' in PREFINALIZE
    assert 'code: "OBJECTIVE_NOT_REGISTERED"' in PREFINALIZE
    assert 'code: "OBJECTIVE_REGISTRY_UNAVAILABLE"' in PREFINALIZE


def test_checkpoint_cannot_be_created_before_registry_resolution() -> None:
    registry_lookup = PREFINALIZE.index('.from("elo_strategic_objectives")')
    cycle_call = PREFINALIZE.index("runObjectiveCycle({")
    assert registry_lookup < cycle_call
    assert 'if (!registeredObjective)' in PREFINALIZE
    assert 'runObjectiveCycle({' in PREFINALIZE


def test_caller_cannot_supply_canonical_objective_title() -> None:
    assert 'text(body.objective_title)' not in PREFINALIZE
    assert 'const objectiveTitle = text(registeredObjective.title);' in PREFINALIZE
    assert 'objectiveTitle,' in PREFINALIZE


def test_persistent_objective_evidence_is_carried_into_cycle() -> None:
    assert 'stringArray(registeredObjective.evidence_refs)' in PREFINALIZE
    assert 'evidenceRefs: governedEvidenceRefs' in PREFINALIZE
    assert 'authorizationEvidenceRef' in PREFINALIZE


def test_service_role_is_read_boundary_not_authorization_source() -> None:
    assert 'ELO_FORGE_SUPABASE_SERVICE_ROLE_KEY' in PREFINALIZE
    assert 'action: "check_authorization_state"' in PREFINALIZE
    assert 'authorization_state: "elo-execution-authorized"' in PREFINALIZE
    assert 'const operation = `continue_objective:${objectiveId}`' in PREFINALIZE
    assert PREFINALIZE.index('action: "check_authorization_state"') < PREFINALIZE.index('.from("elo_strategic_objectives")')


def test_continuity_store_remains_checkpoint_owner_only() -> None:
    assert 'elo_objective_continuity_checkpoints' in CONTINUITY
    assert 'elo_strategic_objectives' not in CONTINUITY
    assert 'Durable production checkpoint store: `public.elo_objective_continuity_checkpoints`' in ARCHITECTURE
    assert 'Strategic objective identity and approved targets: existing OKR contracts/repository' in ARCHITECTURE
