from src.elo.agent_intake.hermes_checkpoint_family import checkpoint_family

def test_precompress_checkpoint_is_a_refinement_of_existing_capability():
    family = checkpoint_family()
    assert family.capability_id == "EXT-CHECKPOINT-HERMES"
    assert family.refinement_id == "EXT-CHECKPOINT-HERMES-PRECOMPRESS"
    assert family.owner == "ELO State Recovery"
    assert family.same_authority is True
    assert family.canonical_mutation_permitted is False