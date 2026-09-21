import unittest

from POS_ORCAMENTO_RENDER import preparar_documento


class TestFronteiraDocumental(unittest.TestCase):
    def test_remove_acervo_consultivo(self):
        dados = {
            "so": "SO 001.26",
            "fontes_consultivas": [{"origem_so": "SO 157.26", "valor": 999}],
            "matriz_rastreabilidade": [
                {"n": 1, "origem_so": "SO 001.26", "item": "atual"}
            ],
        }
        saida = preparar_documento(dados)
        self.assertNotIn("fontes_consultivas", saida)
        self.assertEqual(len(saida["matriz_rastreabilidade"]), 1)

    def test_bloqueia_registro_de_outra_so(self):
        dados = {
            "so": "SO 001.26",
            "memorias_calculo": [
                {"id_mc": "MC-ATUAL", "origem_so": "SO 001.26"},
                {"id_mc": "MC-HIST", "origem_so": "SO 157.26"},
            ],
        }
        saida = preparar_documento(dados)
        self.assertEqual([m["id_mc"] for m in saida["memorias_calculo"]], ["MC-ATUAL"])

    def test_bloqueia_flag_document_safe_false(self):
        dados = {
            "so": "SO 001.26",
            "divergencias": [
                {"id": "D1", "document_safe": False},
                {"id": "D2", "document_safe": True},
            ],
        }
        saida = preparar_documento(dados)
        self.assertEqual([d["id"] for d in saida["divergencias"]], ["D2"])

    def test_historico_so_passa_somente_quando_aplicado(self):
        dados = {
            "so": "SO 001.26",
            "registro_aprendizado": [
                {
                    "contexto": "histórico não aplicado",
                    "fonte_tipo": "precedente",
                    "aplicado_na_so_atual": False,
                },
                {
                    "contexto": "aplicação atual",
                    "fonte_tipo": "precedente",
                    "aplicado_na_so_atual": True,
                    "referencia_so": "SO 001.26",
                },
            ],
        }
        saida = preparar_documento(dados)
        self.assertEqual(
            [r["contexto"] for r in saida["registro_aprendizado"]],
            ["aplicação atual"],
        )

    def test_exige_so_atual(self):
        with self.assertRaises(ValueError):
            preparar_documento({"objetivo": "sem SO"})


if __name__ == "__main__":
    unittest.main()
