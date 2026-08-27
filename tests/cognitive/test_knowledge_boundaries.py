from elo.cognitive.knowledge import KnowledgeRecord, KnowledgeScope


def test_tenant_knowledge_is_not_portable():
    record = KnowledgeRecord(
        key="budget.loss.material_x",
        value=0.03,
        scope=KnowledgeScope.TENANT,
        tenant_id="tenant-a",
    )
    record.validate()
    assert not record.is_portable()
    assert not record.can_promote_to_canonical()


def test_canonical_knowledge_is_portable():
    record = KnowledgeRecord(
        key="governance.canonical_immutability",
        value=True,
        scope=KnowledgeScope.CANONICAL,
    )
    record.validate()
    assert record.is_portable()


def test_private_learned_knowledge_cannot_cross_tenant_boundary():
    record = KnowledgeRecord(
        key="observed.parameter",
        value=0.075,
        scope=KnowledgeScope.LEARNED,
        tenant_id="tenant-a",
    )
    record.validate()
    assert not record.can_promote_to_canonical()
