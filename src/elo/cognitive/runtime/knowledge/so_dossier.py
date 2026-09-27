"""Índice governado de referências de uma Solicitação de Orçamento (SO).

O SODossier não persiste nem copia conteúdo das fontes canônicas. Ele
descreve a identidade da SO, o escopo conhecido e as localizações das fontes.

Refs: ELO-SO-DOSSIER-PROTOCOL, ELO_CONTEXT_ASSEMBLY_CONTRACT.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping


BUDGET_LEARNING_ROOT = Path(
    "08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS"
)
OPERATIONAL_MEMORY_ROOT = Path("memory/solicitations")
SUPABASE_EXPERIENCE_TABLE = "elo_aprendizado_experiencias"


@dataclass(frozen=True)
class DossierSourceRef:
    """Referência para uma fonte existente; nunca contém seu conteúdo."""

    source_type: str
    authority: str
    path: str | None = None
    table: str | None = None
    exists: bool | None = None
    applicability: str = "CONSULTIVE"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SODossier:
    """Índice governado de uma SO."""

    so_id: str
    canonical_key: str
    mask: str = "SO NNN.AA"
    tenant_id: str | None = None
    domain: str | None = None
    scope_state: str = "UNKNOWN"
    maturation_state: str = "IDENTIFIED"
    context_keys: tuple[str, ...] = ()
    source_refs: tuple[DossierSourceRef, ...] = ()
    provenance: Mapping[str, Any] = field(
        default_factory=lambda: {"resolver": "ELO SOResolver"}
    )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["context_keys"] = list(self.context_keys)
        payload["source_refs"] = [ref.to_dict() for ref in self.source_refs]
        payload["provenance"] = dict(self.provenance)
        return payload

    @classmethod
    def from_disk(
        cls,
        canonical_key: str,
        repository_root: Path | None = None,
    ) -> "SODossier | None":
        """Carrega dossiê físico de forge/dossiers/<canonical_key>/.

        Retorna None se o dossiê não existir.
        Não copia conteúdo de context.md — apenas verifica presença.
        """
        import json

        root = repository_root or Path(".")
        base = root / "forge" / "dossiers" / canonical_key

        if not base.exists():
            return None

        identity_path = base / "identity.json"
        if not identity_path.exists():
            return None

        identity = json.loads(
            identity_path.read_text(encoding="utf-8")
        )

        provenance_path = base / "provenance.json"
        provenance: dict[str, Any] = {"resolver": "ELO SOResolver"}
        source_refs: list[DossierSourceRef] = []

        if provenance_path.exists():
            prov_payload = json.loads(
                provenance_path.read_text(encoding="utf-8")
            )
            provenance = prov_payload.get("provenance", provenance)
            for entry in prov_payload.get("source_refs", []):
                source_refs.append(
                    DossierSourceRef(
                        source_type=entry.get("source_type", "unknown"),
                        authority=entry.get("authority", ""),
                        path=entry.get("path"),
                        table=entry.get("table"),
                        exists=entry.get("exists"),
                        applicability=entry.get(
                            "applicability", "CONSULTIVE"
                        ),
                    )
                )

        status_path = base / "status.json"
        maturation_state = identity.get(
            "maturation_state", "IDENTIFIED"
        )
        if status_path.exists():
            status_payload = json.loads(
                status_path.read_text(encoding="utf-8")
            )
            maturation_state = status_payload.get(
                "maturation_state", maturation_state
            )

        return cls(
            so_id=identity.get("instance", canonical_key),
            canonical_key=identity.get(
                "canonical_key", canonical_key
            ),
            mask=identity.get("mask", "SO NNN.AA"),
            tenant_id=identity.get("tenant_id"),
            domain=identity.get("domain"),
            scope_state=identity.get("scope_state", "UNKNOWN"),
            maturation_state=maturation_state,
            context_keys=tuple(identity.get("context_keys", ())),
            source_refs=tuple(source_refs),
            provenance=provenance,
        )

    def has_context_file(
        self, repository_root: Path | None = None
    ) -> bool:
        """Verifica se context.md existe, sem ler o conteúdo."""
        root = repository_root or Path(".")
        return (
            root / "forge" / "dossiers" / self.canonical_key
            / "context.md"
        ).exists()

    @classmethod
    def from_resolved_context(
        cls,
        *,
        so_id: str,
        canonical_key: str,
        learning: Mapping[str, Any] | None,
        handbook: list[Mapping[str, Any]],
        context_keys: tuple[str, ...] = (),
        repository_root: Path | None = None,
        tenant_id: str | None = None,
        domain: str | None = None,
    ) -> "SODossier":
        """Build only references from already resolved metadata."""

        root = repository_root or Path(".")
        refs: list[DossierSourceRef] = []

        if learning:
            candidate = learning.get("path")
            if candidate:
                learning_path = str(candidate)
                refs.append(
                    DossierSourceRef(
                        source_type="solicitations_learning",
                        authority="memory/solicitations_learning",
                        path=learning_path,
                        exists=(root / learning_path).exists(),
                    )
                )

        # A canonical learning index is authoritative for discovery. Filename
        # globbing is only a compatibility fallback for legacy budget records.
        indexed_budget_paths: set[str] = set()
        learning_index = root / "memory/solicitations_learning/INDEX.json"
        if learning_index.exists():
            import json

            payload = json.loads(learning_index.read_text(encoding="utf-8"))
            for entry in payload.get("solicitations", []):
                if (
                    entry.get("canonical_key") == canonical_key
                    or entry.get("so_id") == so_id
                ):
                    candidate = entry.get("budget_learning_paths", [])
                    if isinstance(candidate, str):
                        candidate = [candidate]
                    for path in candidate:
                        indexed_budget_paths.add(str(path))

        for path_str in sorted(indexed_budget_paths):
            path = root / path_str
            refs.append(
                DossierSourceRef(
                    source_type="budget_learning",
                    authority="08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS",
                    path=path.as_posix(),
                    exists=path.exists(),
                )
            )

        if not indexed_budget_paths:
            for path in sorted(
                root.joinpath(BUDGET_LEARNING_ROOT).glob(f"{canonical_key}*.md")
            ):
                refs.append(
                    DossierSourceRef(
                        source_type="budget_learning",
                        authority="08-ai/ELO/ESPECIALISTAS/ORCAMENTO/APRENDIZADOS",
                        path=path.relative_to(root).as_posix(),
                        exists=True,
                    )
                )

        for document in handbook:
            path = document.get("path")
            if not path:
                continue
            path_str = str(path)
            refs.append(
                DossierSourceRef(
                    source_type="knowledge_handbook",
                    authority="04-knowledge-handbook",
                    path=path_str,
                    exists=(root / path_str).exists(),
                )
            )

        refs.append(
            DossierSourceRef(
                source_type="supabase_experience",
                authority="Supabase",
                table=SUPABASE_EXPERIENCE_TABLE,
                exists=None,
            )
        )

        operational_path = (
            OPERATIONAL_MEMORY_ROOT / canonical_key / "index.json"
        )
        refs.append(
            DossierSourceRef(
                source_type="operational_memory",
                authority="memory/solicitations",
                path=operational_path.as_posix(),
                exists=(root / operational_path).exists(),
            )
        )

        observed_refs = [
            ref
            for ref in refs
            if ref.source_type != "supabase_experience"
            and ref.exists is True
        ]
        resolved_metadata = learning is not None or bool(handbook)
        state = (
            "REFERENCED"
            if observed_refs or resolved_metadata
            else "IDENTIFIED"
        )
        scope_state = (
            "SCOPED"
            if tenant_id and domain
            else "PARTIAL"
            if tenant_id or domain
            else "UNKNOWN"
        )

        return cls(
            so_id=so_id,
            canonical_key=canonical_key,
            tenant_id=tenant_id,
            domain=domain,
            scope_state=scope_state,
            context_keys=tuple(context_keys),
            maturation_state=state,
            source_refs=tuple(refs),
        )
