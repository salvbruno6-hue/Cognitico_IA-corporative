import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parent
PIPELINE = ROOT / "pipeline.py"

TECHNICA = {
    "identificacao": {"so": "SO-TESTE"},
    "objetivo": "validar vínculo",
    "escopo": [],
    "matriz_tecnica": [{
        "id": "T-001", "item_tr": "TR-1", "trecho_tr": "trecho de teste",
        "exigencia": "requisito de teste", "tipo": "PAD", "adequacao": "adequada",
        "status": "🟢", "curva": "A", "motivo": "teste",
        "responsavel": "PLA", "consulta_id": "C-001"
    }],
    "consultas": [{"id": "C-001", "texto": "consulta de teste", "item_ids": ["T-001"]}],
    "resumo_executivo": [], "legenda": {}, "rastreabilidade": []
}

POS = {
    "so": "SO-TESTE",
    "pts_tecnica_ref": "PTS-TESTE",
    "itens_herdados": ["T-001"],
    "consultas_abertas": ["C-001"],
    "documentos": [],
    "objetivo_texto": "auditoria de teste",
    "matriz_principal": [{
        "n": 1, "ref_tecnica": "T-001", "topico": "teste", "ref_tr": "TR-1",
        "requisito": "solução de teste", "q_prev": 1, "q_orc": 1,
        "ref_orc": "ORC-001", "valor": 0, "status": "VALIDAR", "divergencia": "—"
    }],
    "blocos_quantitativos": [{"titulo": "teste", "corpo": "teste"}],
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
        "BDI/taxa/total conferidos?": ""
    },
    "conclusao": ""
}


class PipelineTests(unittest.TestCase):
    def run_pipeline(self, pos):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            tecnica = root / "tecnica.json"
            pos_file = root / "pos.json"
            tecnica.write_text(json.dumps(TECHNICA, ensure_ascii=False), encoding="utf-8")
            pos_file.write_text(json.dumps(pos, ensure_ascii=False), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(PIPELINE), str(tecnica), str(pos_file)],
                capture_output=True, text=True, encoding="utf-8"
            )

    def test_valid_link(self):
        result = self.run_pipeline(POS)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("validação cruzada", result.stdout)

    def test_orphan_ref_fails(self):
        pos = json.loads(json.dumps(POS))
        pos["matriz_principal"][0]["ref_tecnica"] = "T-999"
        result = self.run_pipeline(pos)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("referências técnicas", result.stderr)

    def test_open_query_must_exist(self):
        pos = json.loads(json.dumps(POS))
        pos["consultas_abertas"] = ["C-999"]
        result = self.run_pipeline(pos)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("consultas_abertas", result.stderr)


if __name__ == "__main__":
    unittest.main()
