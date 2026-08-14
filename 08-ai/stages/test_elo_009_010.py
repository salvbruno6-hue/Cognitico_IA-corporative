import unittest
from elo_009_010 import *

class Stage9010Tests(unittest.TestCase):
    def setUp(self):
        self.nodes = [
            Node("demand", "A", "pcp", "demand", 10),
            Node("capacity", "A", "pcp", "capacity", 8),
            Node("delivery", "A", "pcp", "delivery", 0),
            Node("other", "B", "pcp", "capacity", 1),
        ]
        self.edges = [Dependency("demand", "capacity", .8), Dependency("capacity", "delivery", .7), Dependency("demand", "other", 1.0)]
        self.scenario = Scenario("s1", "A", "pcp", "p1", ("demand rises",), ("demand",), ("ev1",))

    def test_impact_stays_in_tenant_domain(self):
        ids = [i.node_id for i in propagate_impact(self.nodes, self.edges, self.scenario)]
        self.assertEqual(ids, ["demand", "capacity", "delivery"])
        self.assertNotIn("other", ids)

    def test_boundary_rejects_foreign_changed_node(self):
        bad = Scenario("s2", "A", "pcp", "p1", (), ("other",))
        with self.assertRaises(ValueError):
            propagate_impact(self.nodes, self.edges, bad)

    def test_constraint_conflict_is_deterministic(self):
        self.assertEqual(validate_constraints(self.nodes, [Constraint("c1", "capacity", maximum=7)], "A", "pcp"), ("c1:maximum",))

    def test_alternative_ranking_is_explainable(self):
        impact = Impact("capacity", 1, .2, "dependency depth 1")
        a = Alternative("a", "s1", "A", (impact,), .1, .8, .9, ("ev-a",))
        b = Alternative("b", "s1", "A", (impact,), .4, .6, .8, ("ev-b",))
        self.assertEqual(rank_alternatives([b, a], "A", "s1")[0].id, "a")

    def test_conflicts_block_recommendation(self):
        result = recommend([], ["c1:maximum"], "A", "s1")
        self.assertEqual(result["status"], "PLAN WITH INCONSISTENCIES")
        self.assertIsNone(result["recommended"])

    def test_replan_requires_approval(self):
        plan = PlanVersion("p", 1, "A", "pcp", PlanState.VALID)
        proposed = propose_replan(plan, "d1", [])
        self.assertEqual(proposed.state, PlanState.PENDING_APPROVAL)
        self.assertEqual(proposed.supersedes, 1)
        approved = approve_replan(proposed, "human-1")
        self.assertEqual(approved.state, PlanState.APPROVED)
        self.assertEqual(approved.approval_principal_id, "human-1")

    def test_replan_with_conflict_does_not_advance(self):
        plan = PlanVersion("p", 1, "A", "pcp", PlanState.VALID)
        proposed = propose_replan(plan, "d1", ["capacity"])
        self.assertEqual(proposed.state, PlanState.INCONSISTENT)
        self.assertEqual(proposed.version, 1)

    def test_reject_requires_pending(self):
        plan = PlanVersion("p", 1, "A", "pcp", PlanState.VALID)
        with self.assertRaises(ValueError):
            reject_replan(plan, "human-1")

    def test_supersession_lineage_is_explicit(self):
        old = PlanVersion("p", 1, "A", "pcp", PlanState.VALID)
        new = PlanVersion("p", 2, "A", "pcp", PlanState.APPROVED, supersedes=1)
        old2, new2 = supersede(old, new)
        self.assertEqual(old2.state, PlanState.SUPERSEDED)
        self.assertEqual(new2.supersedes, old.version)

if __name__ == "__main__":
    unittest.main()
