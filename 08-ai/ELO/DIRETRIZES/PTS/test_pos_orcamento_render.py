import unittest

from POS_ORCAMENTO_RENDER import preparar_documento, render


def dados_base():
    return {
        "schema_version": "3.0",
        "so": "SO 001.26",
        "cliente": "Cliente",
        "objeto": "Objeto",
        "revisao": "0",
        "documentos": [],
        "matriz_principal": [
            {"n": 1, "topico": "atual", "ref_tr": "", "requisito": "", "q_prev": "", "q_orc": "", "ref_orc": "", "valor": "", "status": "", "divergencia": ""}
        ],
        "blocos_quantitativos": [{"titulo": "", "corpo": ""}],
        "conferencia_valores": {"Subtotal geral": "", "Taxa administrativa": "", "BDI": "", "Total geral": ""},
        "auditoria_reversa": [{"item": "", "ref": "", "valor": "", "base": "", "justificativa": ""}],
        "itens_premissa": [{"item": "", "origem": "", "premissa": "", "impacto": "", "tratamento": ""}],
        "logistica": [{"componente": "", "calculo": "", "valor": "", "criterio": ""}],
        "mao_de_obra": [{"titulo": "MO interna", "linhas": [{"funcao": "", "dias": "", "colab": "", "v_unit": "", "parcial": ""}], "total": ""}],
        "exclusoes": [{"item": "", "responsavel": "", "orcado": "", "status": ""}],
        "divergencias": [{"n": 1, "item": "", "tipo": "", "previsto": "", "orcado": "", "motivo": "", "impacto": "", "acao": ""}],
        "riscos": [{"risco": "", "tipo": "", "impacto": "", "condicao": "", "tratamento": ""}],
        "pendencias": [{"pendencia": "", "origem": "", "impacto": "", "acao": "", "status": ""}],
        "itens_nao_orcados": "",
        "checklist": {
            "Todos os requisitos principais possuem correspondência?": "",
            "Itens relevantes possuem origem/justificativa?": "",
            "Quantitativos confrontados?": "",
            "Áreas molhadas reavaliadas?": "",
            "Valores conferidos?": "",
            "Maiores custos justificados?": "",
            "Premissas registradas?": "",
            "Exclusões registradas?": "",
            "Pendências registradas?": "",
            "Riscos registrados?": "",
            "Responsabilidades verificadas?": "",
            "Logística conferida?": "",
            "Licenças/ART/RRT completamente confirmadas?": "",
            "BDI/taxa/total conferidos?": "",
        },
        "conclusao": "",
    }


class TestFronteiraDocumental(unittest.TestCase):
    def test_remove_acervo_consultivo(self):
        dados = dados_base()
        dados["fontes_consultivas"] = [{"origem_so": "SO 157.26", "valor": 999}]
        dados["matriz_principal"][0]["origem_so"] = "SO 001.26"
        saida = preparar_documento(dados)
        self.assertNotIn("fontes_consultivas", saida)
        self.assertEqual(len(saida["matriz_principal"]), 1)

    def test_bloqueia_registro_de_outra_so(self):
        dados = dados_base()
        dados["matriz_principal"] = [
            {"n": 1, "origem_so": "SO 001.26"},
            {"n": 2, "origem_so": "SO 157.26"},
        ]
        saida = preparar_documento(dados)
        self.assertEqual([m["n"] for m in saida["matriz_principal"]], [1])

    def test_bloqueia_flag_document_safe_false(self):
        dados = dados_base()
        dados["divergencias"] = [
            {"n": 1, "document_safe": False},
            {"n": 2, "document_safe": True},
        ]
        saida = preparar_documento(dados)
        self.assertEqual([d["n"] for d in saida["divergencias"]], [2])

    def test_historico_so_passa_somente_quando_aplicado(self):
        dados = dados_base()
        dados["pendencias"] = [
            {"pendencia": "histórico", "fonte_tipo": "precedente", "aplicado_na_so_atual": False},
            {"pendencia": "aplicação atual", "fonte_tipo": "precedente", "aplicado_na_so_atual": True, "referencia_so": "SO 001.26"},
        ]
        saida = preparar_documento(dados)
        self.assertEqual([p["pendencia"] for p in saida["pendencias"]], ["aplicação atual"])

    def test_exige_estrutura_completa(self):
        with self.assertRaises(ValueError):
            preparar_documento({"so": "SO 001.26"})

    def test_render_mantem_exatamente_17_secoes(self):
        saida = render(dados_base())
        titulos = [
            linha for linha in saida.splitlines()
            if linha.startswith("## ") and linha[3:5].isdigit()
        ]
        self.assertEqual(len(titulos), 17)
        self.assertEqual(
            [linha.split(". ", 1)[1] for linha in titulos],
            [
                "IDENTIFICAÇÃO E OBJETIVO",
                "DOCUMENTOS UTILIZADOS",
                "MATRIZ PRINCIPAL — TR × ORÇAMENTO",
                "CONFERÊNCIA DE QUANTITATIVOS",
                "CONFERÊNCIA DE VALORES",
                "AUDITORIA REVERSA — PRINCIPAIS CUSTOS",
                "ITENS ORÇADOS POR PREMISSA",
                "LOGÍSTICA",
                "MÃO DE OBRA",
                "EXCLUSÕES E RESPONSABILIDADES",
                "MATRIZ DE DIVERGÊNCIAS",
                "MATRIZ DE RISCOS",
                "PENDÊNCIAS",
                "ITENS NÃO ORÇADOS / NÃO CONFIRMADOS",
                "CHECKLIST DE COMPLETUDE",
                "CONCLUSÃO E VALIDAÇÃO",
                "REGRA DE RASTREABILIDADE",
            ],
        )

    def test_checklist_tem_14_itens(self):
        saida = render(dados_base())
        inicio = saida.index("## 15. CHECKLIST DE COMPLETUDE")
        fim = saida.index("## 16. CONCLUSÃO E VALIDAÇÃO")
        linhas = [
            linha for linha in saida[inicio:fim].splitlines()
            if linha.startswith("| ") and not linha.startswith("| Verificação")
            and not linha.startswith("|---")
        ]
        self.assertEqual(len(linhas), 14)


if __name__ == "__main__":
    unittest.main()
