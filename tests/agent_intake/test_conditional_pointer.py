from elo.agent_intake.conditional_pointer import resolve_pointer, validate_pointer_matrix


def test_conditional_pointer_resolves_information_to_existing_capability():
    results = validate_pointer_matrix()

    assert len(results) == 8
    assert all(result.status == "resolved" for result in results)
    assert all(result.matched_capability for result in results)
    assert all(result.destination for result in results)
    assert all(result.learning_candidate["promotion_state"] == "candidate_only" for result in results)
    assert all(result.learning_candidate["canonical_mutation"] is False for result in results)


def test_pointer_matrix_has_no_duplicate_conditions_or_capability_identities():
    results = validate_pointer_matrix()

    conditions = [result.condition for result in results]
    capabilities = [result.matched_capability for result in results]

    assert len(conditions) == len(set(conditions))
    assert len(capabilities) == len(set(capabilities))


def test_repeated_resolution_is_idempotent_and_creates_no_state():
    information = {"condition": "semantic-recall", "source": "controlled-lab"}

    first = resolve_pointer(
        request_id="pointer-idempotent-01",
        tenant_scope="multiteiner",
        information=information,
    )
    second = resolve_pointer(
        request_id="pointer-idempotent-01",
        tenant_scope="multiteiner",
        information=information,
    )

    assert first == second
    assert information == {"condition": "semantic-recall", "source": "controlled-lab"}
    assert first.learning_candidate["canonical_mutation"] is False


def test_unknown_condition_does_not_guess_a_destination():
    result = resolve_pointer(
        request_id="pointer-unknown-01",
        tenant_scope="multiteiner",
        information={"condition": "unknown-condition", "source": "controlled-lab"},
    )

    assert result.status == "unresolved"
    assert result.matched_capability is None
    assert result.destination is None
    assert result.learning_candidate["canonical_mutation"] is False


def test_policy_requirement_is_explicit_in_pointer_evidence():
    result = resolve_pointer(
        request_id="pointer-policy-01",
        tenant_scope="multiteiner",
        information={"condition": "tool-resolution", "source": "controlled-lab"},
    )

    assert result.status == "resolved"
    assert result.matched_capability == "HERMES-TOOLSETS"
    assert result.destination == "ELO_ROUTING"
    assert result.policy_required is True
