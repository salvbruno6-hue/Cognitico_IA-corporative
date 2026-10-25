"""Governed dialogue projection from canonical ELO facts to ChatGPT.

This module is presentation/composition only. It does not authorize, execute,
route, persist, learn, promote, or create a new cognitive authority. All facts
must already have been produced by canonical owners before they enter here.

The response space is compositional rather than a brittle catalogue of fixed
phrases. Five canonical objective-loop decisions combined with persistence,
authorization, execution and evidence states cover hundreds of distinct
situations while preserving the ELO decision unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class PersistenceState(StrEnum):
    PERSISTED = "PERSISTED"
    EPHEMERAL = "EPHEMERAL"
    UNKNOWN = "UNKNOWN"


class AuthorizationState(StrEnum):
    VALID = "VALID"
    NOT_REQUIRED = "NOT_REQUIRED"
    MISSING = "MISSING"
    EXPIRED = "EXPIRED"


class ExecutionState(StrEnum):
    EXECUTED = "EXECUTED"
    PENDING = "PENDING"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"


class EvidenceState(StrEnum):
    OBSERVED = "OBSERVED"
    PARTIAL = "PARTIAL"
    INSUFFICIENT = "INSUFFICIENT"


CANONICAL_DECISIONS = ("CONTINUE", "CORRECT", "REPLAN", "ESCALATE", "COMPLETE")


@dataclass(frozen=True, slots=True)
class EloDialogueFacts:
    """Facts already decided by canonical ELO owners."""

    objective_id: str
    workstream_id: str
    checkpoint_version: int
    state: str
    decision: str
    next_action: str
    progress_token: str
    justification: str
    evidence_refs: tuple[str, ...] = ()
    persistence_state: PersistenceState = PersistenceState.UNKNOWN
    authorization_state: AuthorizationState = AuthorizationState.NOT_REQUIRED
    execution_state: ExecutionState = ExecutionState.PENDING
    evidence_state: EvidenceState = EvidenceState.INSUFFICIENT
    continuation_permitted: bool = False
    human_required: bool = False


@dataclass(frozen=True, slots=True)
class EloDialogueReply:
    """Bounded machine-readable and human-readable reply for ChatGPT."""

    scenario_code: str
    headline: str
    message: str
    decision: str
    next_action: str
    progress_token: str
    should_continue_automatically: bool
    human_required: bool
    evidence_refs: tuple[str, ...]


class EloDialogueResponsePolicy:
    """Project ELO facts into a deterministic GPT-facing response.

    The policy never changes ELO's decision. Automatic continuation is only
    mirrored when the canonical runtime explicitly says continuation is
    permitted and no human boundary is active.
    """

    @staticmethod
    def scenario_capacity() -> int:
        return (
            len(CANONICAL_DECISIONS)
            * len(PersistenceState)
            * len(AuthorizationState)
            * len(ExecutionState)
            * len(EvidenceState)
        )

    def compose(self, facts: EloDialogueFacts) -> EloDialogueReply:
        self._validate(facts)
        scenario_code = ".".join(
            (
                facts.decision,
                facts.persistence_state.value,
                facts.authorization_state.value,
                facts.execution_state.value,
                facts.evidence_state.value,
            )
        )
        should_continue = bool(
            facts.continuation_permitted
            and not facts.human_required
            and facts.decision in {"CONTINUE", "CORRECT", "REPLAN"}
        )
        headline = self._headline(facts.decision)
        message = self._message(facts, should_continue)
        return EloDialogueReply(
            scenario_code=scenario_code,
            headline=headline,
            message=message,
            decision=facts.decision,
            next_action=facts.next_action,
            progress_token=facts.progress_token,
            should_continue_automatically=should_continue,
            human_required=facts.human_required,
            evidence_refs=tuple(dict.fromkeys(ref for ref in facts.evidence_refs if ref)),
        )

    @staticmethod
    def _validate(facts: EloDialogueFacts) -> None:
        required = {
            "objective_id": facts.objective_id,
            "workstream_id": facts.workstream_id,
            "state": facts.state,
            "decision": facts.decision,
            "next_action": facts.next_action,
            "progress_token": facts.progress_token,
            "justification": facts.justification,
        }
        missing = [name for name, value in required.items() if not str(value).strip()]
        if missing:
            raise ValueError("missing canonical dialogue facts: " + ", ".join(missing))
        if facts.checkpoint_version < 1:
            raise ValueError("checkpoint_version must be >= 1")
        if facts.decision not in CANONICAL_DECISIONS:
            raise ValueError(f"unsupported canonical decision: {facts.decision}")
        if facts.human_required and facts.continuation_permitted:
            raise ValueError("human_required cannot coexist with continuation_permitted")

    @staticmethod
    def _headline(decision: str) -> str:
        return {
            "CONTINUE": "ELO confirmou continuidade do objetivo.",
            "CORRECT": "ELO determinou correção antes de continuar.",
            "REPLAN": "ELO determinou replanejamento governado.",
            "ESCALATE": "ELO atingiu um limite que exige escalonamento.",
            "COMPLETE": "ELO confirmou conclusão do objetivo.",
        }[decision]

    def _message(self, facts: EloDialogueFacts, should_continue: bool) -> str:
        lines = [
            self._headline(facts.decision),
            "",
            f"Objetivo: {facts.objective_id}",
            f"Workstream: {facts.workstream_id}",
            f"Checkpoint: {facts.checkpoint_version}",
            f"Estado: {facts.state}",
            f"Decisão: {facts.decision}",
            f"Progress token: {facts.progress_token}",
            f"Justificativa: {facts.justification}",
            f"Próxima ação: {facts.next_action}",
            "",
            "Controles observados:",
            f"- persistência: {facts.persistence_state.value}",
            f"- autorização: {facts.authorization_state.value}",
            f"- execução: {facts.execution_state.value}",
            f"- evidência: {facts.evidence_state.value}",
            f"- referências de evidência: {len(facts.evidence_refs)}",
        ]
        lines.extend(self._diagnostic_lines(facts))
        lines.append("")
        if facts.human_required:
            lines.append("Resultado para o GPT: apresentar o retorno do ELO e aguardar intervenção humana.")
        elif should_continue:
            lines.append(
                "Resultado para o GPT: responder com este retorno e permitir que o próximo ciclo "
                "continue do checkpoint confirmado, sem solicitar nova autorização conversacional."
            )
        elif facts.decision == "COMPLETE":
            lines.append("Resultado para o GPT: apresentar a conclusão e encerrar o ciclo do objetivo.")
        else:
            lines.append(
                "Resultado para o GPT: apresentar o retorno sem inventar continuidade; o runtime "
                "canônico ainda não declarou continuação permitida."
            )
        return "\n".join(lines)

    @staticmethod
    def _diagnostic_lines(facts: EloDialogueFacts) -> list[str]:
        lines: list[str] = []
        if facts.persistence_state is PersistenceState.EPHEMERAL:
            lines.append("- diagnóstico: checkpoint efêmero; não afirmar continuidade entre wakeups.")
        elif facts.persistence_state is PersistenceState.UNKNOWN:
            lines.append("- diagnóstico: persistência não comprovada pelo estado recebido.")
        if facts.authorization_state is AuthorizationState.MISSING:
            lines.append("- diagnóstico: autorização canônica ausente.")
        elif facts.authorization_state is AuthorizationState.EXPIRED:
            lines.append("- diagnóstico: autorização canônica expirada.")
        if facts.execution_state is ExecutionState.BLOCKED:
            lines.append("- diagnóstico: execução bloqueada pelo runtime canônico.")
        elif facts.execution_state is ExecutionState.FAILED:
            lines.append("- diagnóstico: execução falhou; não declarar efeito concluído.")
        if facts.evidence_state is EvidenceState.INSUFFICIENT:
            lines.append("- diagnóstico: evidência insuficiente; não elevar hipótese a fato.")
        elif facts.evidence_state is EvidenceState.PARTIAL:
            lines.append("- diagnóstico: evidência parcial; preservar limitações no retorno.")
        return lines
