import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parent
RENDERER = ROOT / "PTS_TECNICA_RENDER.py"


class PtsTecnicaRenderCliTests(unittest.TestCase):
    def test_cli_reports_rejected_legacy_contract_without_traceback(self):
        legacy = {
            "identificacao": {"so_resolvida": "SO 001.27"},
            "objetivo": "teste",
            "escopo": [],
            "matriz_tecnica": [],
            "consultas": [],
            "resumo_executivo": [],
            "legenda": {},
            "rastreabilidade": [],
        }
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "legacy.json"
            source.write_text(json.dumps(legacy, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(RENDERER), str(source)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("[ERRO]", result.stderr)
        self.assertIn("contrato_maturidade=1.0", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
