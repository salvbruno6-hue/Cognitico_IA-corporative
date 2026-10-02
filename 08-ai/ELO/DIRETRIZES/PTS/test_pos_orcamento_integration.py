import unittest

from POS_ORCAMENTO_INTEGRATION import integrate


class IntegrationTests(unittest.TestCase):
    def base_pos(self):
        return {
            "so": "SO 001.26",
            "matriz_principal": [
                {"n": 1, "ref_tecnica": "T-1", "ref_orc": "O-1", "valor": 800},
                {"n": 2, "ref_tecnica": "T-2", "ref_orc": "O-2", "valor": 150},
                {"n": 3, "ref_tecnica": "T-3", "ref_orc": "O-3", "valor": 50},
            ],
            "divergencias": [],
            "riscos": [],
            "pendencias": [],
            "checklist": {"valores": "sim"},
        }

    def test_competitiveness_consumes_audit_and_builds_abc(self):
        result = integrate(self.base_pos())
        indicators = result.competitividade["indicadores"]
        self.assertEqual(indicators[0]["ref_orc"], "O-1")
        self.assertEqual(indicators[0]["abc"], "A")
        self.assertEqual(indicators[-1]["abc"], "C")
        self.assertEqual(result.arbitrado["status"], "AGUARDANDO_ARBITRAGEM")

    def test_audit_divergence_is_preserved_in_validation(self):
        pos = self.base_pos()
        pos["divergencias"] = [{"item": "O-1", "tipo": "quantitativo"}]
        result = integrate(pos)
        self.assertEqual(result.validacao["status_proposto"], "VALIDADO_COM_PENDENCIAS")
        self.assertEqual(result.validacao["divergencias"], 1)

    def test_arbitration_requires_explicit_actor_and_reason(self):
        result = integrate(
            self.base_pos(),
            resultado="VALIDADO",
            responsavel="ENG",
            justificativa="Conferência concluída com evidências.",
        )
        self.assertEqual(result.arbitrado["status"], "VALIDADO")
        self.assertTrue(result.arbitrado["arbitragem_explicita"])
        self.assertEqual(result.elo_aprender["status"], "CANDIDATA")

    def test_no_automatic_decision_or_learning(self):
        result = integrate(self.base_pos())
        self.assertEqual(result.arbitrado["status"], "AGUARDANDO_ARBITRAGEM")
        self.assertEqual(result.elo_aprender["status"], "CANDIDATA")
        self.assertIn("não promove conhecimento ao Core", result.elo_aprender["limitacoes"])


if __name__ == "__main__":
    unittest.main()
