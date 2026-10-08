import unittest

from POS_ORCAMENTO_RENDER import preparar_documento


def _base_document() -> dict:
    return {
        "so": "SO 001.26",
        "matriz_principal": [
            {
                "n": 1,
                "ref_tecnica": "T-001",
                "topico": "teste",
                "ref_tr": "TR-001",
                "requisito": "requisito",
                "q_prev": 1,
                "q_orc": 1,
                "ref_orc": "ORC-001",
                "valor": 100,
                "status": "OK",
                "divergencia": "",
            }
        ],
        "divergencias": [],
        "riscos": [],
        "pendencias": [],
        "checklist": {},
    }


class TestFronteiraDocumental(unittest.TestCase):
    def test_remove_acervo_consultivo(self):
        dados = _base_document()
        dados.update({
            "fontes_consultivas": [{"origem_so": "SO 157.26", "valor": 999}],
            "matriz_rastreabilidade": [
                {"n": 1, "origem_so": "SO 001.26", "item": "atual"}
            ],
        })
        saida = preparar_documento(dados)
        self.assertNotIn("fontes_consultivas", saida)
        self.assertEqual(len(saida["matriz_rastreabilidade"]), 1)

    def test_bloqueia_registro_de_outra_so(self):
        dados = _base_document()
        dados["memorias_calculo"] = [
            {"id_mc": "MC-ATUAL", "origem_so": "SO 001.26"},
            {"id_mc": "MC-HIST", "origem_so": "SO 157.26"},
        ]
        saida = preparar_documento(dados)
        self.assertEqual([m["id_mc"] for m in saida["memorias_calculo"]], ["MC-ATUAL"])

    def test_aceita_representacoes_equivalentes_da_mesma_so(self):
        dados = _base_document()
        dados["memorias_calculo"] = [
            {"id_mc": "MC-ATUAL", "origem_so": "SO-001.26"},
        ]
        saida = preparar_documento(dados)
        self.assertEqual([m["id_mc"] for m in saida["memorias_calculo"]], ["MC-ATUAL"])

    def test_rejeita_so_atual_com_sequencia_zero(self):
        dados = _base_document()
        dados["so"] = "SO 000.27"
        with self.assertRaisesRegex(ValueError, "formato canônico"):
            preparar_documento(dados)

    def test_bloqueia_flag_document_safe_false(self):
        dados = _base_document()
        dados["divergencias"] = [
            {"id": "D1", "document_safe": False},
            {"id": "D2", "document_safe": True},
        ]
        saida = preparar_documento(dados)
        self.assertEqual([d["id"] for d in saida["divergencias"]], ["D2"])

    def test_historico_so_passa_somente_quando_aplicado(self):
        dados = _base_document()
        dados["registro_aprendizado"] = [
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
        ]
        saida = preparar_documento(dados)
        self.assertEqual(
            [r["contexto"] for r in saida["registro_aprendizado"]],
            ["aplicação atual"],
        )

    def test_exige_so_atual(self):
        with self.assertRaises(ValueError):
            preparar_documento({"objetivo": "sem SO"})

    def test_injects_canonical_integration(self):
        saida = preparar_documento(_base_document())
        integracao = saida["integracao"]

        self.assertEqual(integracao["competitividade"]["indicadores"][0]["abc"], "A")
        self.assertEqual(integracao["validacao"]["status_proposto"], "VALIDADO")
        self.assertEqual(
            integracao["resultado_arbitrado"]["status"],
            "AGUARDANDO_ARBITRAGEM",
        )
        self.assertEqual(integracao["elo_aprender"]["status"], "CANDIDATA")


if __name__ == "__main__":
    unittest.main()
