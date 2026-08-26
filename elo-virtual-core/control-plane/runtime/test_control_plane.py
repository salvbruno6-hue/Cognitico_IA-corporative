import unittest

from elo_control_plane import ELOControlPlane, PolicyError


class ControlPlaneTests(unittest.TestCase):
    def setUp(self):
        self.elo = ELOControlPlane()

    def test_supabase_routing(self):
        result = self.elo.handle("qual é a composição do M01?")
        self.assertEqual(result["decision"]["route"], "supabase_elo_forge")
        self.assertEqual(result["decision"]["operation"], "read")

    def test_local_fallback(self):
        result = self.elo.handle("explique o conceito de planejamento")
        self.assertEqual(result["decision"]["route"], "local")

    def test_write_is_denied_by_default(self):
        with self.assertRaises(PolicyError):
            self.elo.handle("atualize o kit M01", operation="write")

    def test_execute_is_denied_by_default(self):
        with self.assertRaises(PolicyError):
            self.elo.handle("execute operação", operation="execute")


if __name__ == "__main__":
    unittest.main()
