from elo.agent_intake.hermes_learning_graph_functional_evaluation import evaluate_learning_graph_functional_gain

def test_learning_graph_blocks_duplicate_semantic_relations():
    evidence=evaluate_learning_graph_functional_gain()
    assert evidence.baseline_duplicate_relation_block_rate == 0.0
    assert evidence.adapted_duplicate_relation_block_rate == 1.0
    assert evidence.repeatable is True
    assert evidence.boundary_integrity is True
