"""Build an evidence-based capability report for ELO budget learning.

This script discovers acquired semantic learning in Git and calculation-memory
references that are explicitly represented in repository artifacts. It does
not promote learning, write Supabase, or commit learning autonomously.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(".")
SOURCES = (
    Path("04-knowledge-handbook"),
    Path("memory/solicitations"),
    Path("memory/solicitations_learning"),
    Path("memory/evolution"),
)
OUTPUT = Path("memory/solicitations_learning/ELO_BUDGET_CAPABILITY_REPORT.md")

SO_RE = re.compile(r"\bSO\s*[_-]?\s*\d{1,4}[./_-]?\s*\d{2}\b", re.I)


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _source_label(path: Path) -> str:
    text = _read(path)
    matches = sorted(set(m.group(0).upper().replace(" ", "") for m in SO_RE.finditer(text)))
    if matches:
        return ", ".join(matches)
    return "SO NÃO IDENTIFICADA"


def main() -> int:
    files: list[Path] = []
    for source in SOURCES:
        if source.exists():
            files.extend(p for p in source.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".json", ".txt"})

    files = sorted(set(files))
    lines = [
        "# ELO APRENDER — Capacidade Atual de Orçamento",
        "",
        "> Relatório de descoberta de conhecimento adquirido. Evidência consultiva; não é autorização de promoção.",
        "",
        f"Arquivos de conhecimento localizados: **{len(files)}**.",
        "",
        "## Capacidades/evidências encontradas",
        "",
    ]

    for path in files:
        text = _read(path)
        if not text.strip():
            continue
        compact = " ".join(line.strip() for line in text.splitlines() if line.strip())
        if len(compact) > 320:
            compact = compact[:317] + "..."
        lines.extend([
            f"### `{path.as_posix()}`",
            f"- Fonte/SO identificável: `{_source_label(path)}`",
            f"- Evidência: {compact}",
            "- Status: **CONSULTIVO — ELO deve interpretar e validar aplicabilidade.**",
            "",
        ])

    lines.extend([
        "## Regra de proveniência",
        "",
        "Informação de outra SO nunca é tratada como origem da SO corrente. ELO deve registrar fonte, contexto original, motivo da recuperação, motivo da possível aplicação, premissas/equivalência e validações pendentes.",
        "",
        "## Memória de cálculo",
        "",
        "Cálculos estruturados devem ser consultados no Supabase quando disponíveis e apresentados como:",
        "",
        "`entrada → fonte → premissa → fórmula → subcálculo → resultado → validação`",
        "",
        "## Governança",
        "",
        "`VALIDATED_LEARNING` é reutilizado/enriquecido; `PRECEDENT` não vira `RULE` automaticamente; fonte inacessível deve ser registrada como `FONTE NÃO ACESSÍVEL`.",
        "",
    ])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"files={len(files)} output={OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
