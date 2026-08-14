from elo.core.production_flow import ProductionEvent, ProductionFlow, ProductionStage


def event(event_id, stage, **kwargs):
    return ProductionEvent(event_id=event_id, stage=stage, **kwargs)


def test_production_flow_tracks_end_to_end_lifecycle():
    flow = ProductionFlow(
        flow_id="PF-001",
        events=(
            event("1", ProductionStage.DEMAND),
            event("2", ProductionStage.PLANNING),
            event("3", ProductionStage.EXECUTION),
            event("4", ProductionStage.OUTCOME),
            event("5", ProductionStage.FEEDBACK),
        ),
    )
    assert flow.lifecycle_complete()
    assert flow.outcome_exists()
    assert flow.has_feedback()


def test_deviations_are_visible_for_systemic_analysis():
    deviation = event(
        "3",
        ProductionStage.EXECUTION,
        production_order_id="OF-001",
        deviation="material shortage",
    )
    flow = ProductionFlow(flow_id="PF-002", events=(deviation,))
    assert flow.deviations() == (deviation,)


def test_stage_queries_are_scoped():
    demand = event("1", ProductionStage.DEMAND)
    execution = event("2", ProductionStage.EXECUTION)
    flow = ProductionFlow(flow_id="PF-003", events=(demand, execution))
    assert flow.events_at(ProductionStage.DEMAND) == (demand,)
    assert flow.events_at(ProductionStage.EXECUTION) == (execution,)
