"""RUN-06 operational resilience evidence over the existing ELO boundary.

The transport harness is test-only and provider-independent. It uses a real
localhost HTTP server to produce an actual socket timeout, an HTTP 503, and a
successful response. No production provider, credential, or second executor
is introduced.
"""

from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import socket
import threading
import urllib.error
import urllib.request

from elo.core.context_resolution import ContextEvidence, ContextQuery, ContextResolutionEngine, ContextSource
from elo.core.core_loop import CoreLoopEngine, CoreLoopRequest
from elo.core.diagnostic_scenarios import DiagnosticLens, DiagnosticObservation, DiagnosticScenario, DiagnosticStatus


@dataclass(frozen=True)
class TransportEvidence:
    attempt: int
    status: str
    provenance: str
    historical_id: str


class _SequenceHandler(BaseHTTPRequestHandler):
    sequence = []
    attempts = 0
    lock = threading.Lock()

    def do_GET(self):
        with self.lock:
            index = self.attempts
            self.__class__.attempts += 1
            outcome = self.sequence[index] if index < len(self.sequence) else "success"

        if outcome == "timeout":
            self.connection.settimeout(0.1)
            try:
                import time
                time.sleep(0.08)
            except Exception:
                pass
            return

        if outcome == "unavailable":
            self.send_response(503)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        body = b"ok"
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):
        return


class LocalResilienceHarness:
    """Real localhost transport fixture; intentionally scoped to tests."""

    def __init__(self, sequence):
        self.sequence = tuple(sequence)
        self.server = None
        self.thread = None

    def __enter__(self):
        _SequenceHandler.sequence = list(self.sequence)
        _SequenceHandler.attempts = 0
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), _SequenceHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return self

    def __exit__(self, *_args):
        if self.server is not None:
            self.server.shutdown()
            self.server.server_close()
        if self.thread is not None:
            self.thread.join(timeout=2)

    @property
    def url(self):
        assert self.server is not None
        return f"http://127.0.0.1:{self.server.server_port}/health"


def run_transport(sequence, max_retries=2, timeout=0.01):
    evidence = []
    with LocalResilienceHarness(sequence) as harness:
        for attempt in range(1, max_retries + 2):
            try:
                with urllib.request.urlopen(harness.url, timeout=timeout) as response:
                    response.read()
                evidence.append(TransportEvidence(attempt, "SUCCESS", "local-http-lab", "RUN06-H001"))
                return evidence, "RECOVERED", _SequenceHandler.attempts
            except urllib.error.HTTPError as exc:
                if exc.code != 503:
                    raise
                evidence.append(TransportEvidence(attempt, "UNAVAILABLE", "local-http-lab", "RUN06-H001"))
            except (socket.timeout, TimeoutError, urllib.error.URLError) as exc:
                reason = getattr(exc, "reason", None)
                if not isinstance(exc, (socket.timeout, TimeoutError)) and not isinstance(reason, (socket.timeout, TimeoutError)):
                    raise
                evidence.append(TransportEvidence(attempt, "TIMEOUT", "local-http-lab", "RUN06-H001"))
        return evidence, "DEGRADED", _SequenceHandler.attempts


def _source_id(item: TransportEvidence) -> str:
    # Attempt-specific IDs retain the same historical transport identity.
    return f"{item.historical_id}-attempt-{item.attempt}"


def build_context(transport_evidence: tuple[TransportEvidence, ...] | list[TransportEvidence]):
    """Feed real HTTP attempt outcomes into existing governed Core context."""
    if not transport_evidence:
        raise ValueError("RUN-06 transport evidence is required")
    engine = ContextResolutionEngine()
    pack = engine.resolve(ContextQuery(
        "recuperar capacidade apos falha",
        tenant_id="tenant-mt",
        domain="PCP",
    ))
    sources = tuple(
        ContextSource(
            _source_id(item), "localhost-http-transport", "observed-test",
            tenant_id="tenant-mt", domain="PCP",
            provenance={
                "historical_id": item.historical_id,
                "origin": item.provenance,
                "attempt": str(item.attempt),
                "transport_status": item.status,
            },
        )
        for item in transport_evidence
    )
    facts = tuple(
        ContextEvidence(
            _source_id(item),
            f"real HTTP attempt {item.attempt}: {item.status}",
            0.9,
            tenant_id="tenant-mt", domain="PCP",
            provenance={
                "historical_id": item.historical_id,
                "origin": item.provenance,
                "attempt": str(item.attempt),
                "transport_status": item.status,
            },
        )
        for item in transport_evidence
    )
    exhausted = transport_evidence[-1].status != "SUCCESS"
    return engine.enrich(
        pack, sources=sources, evidence=facts,
        gaps=("transport retry budget exhausted",) if exhausted else (),
    )


def run_core(transport_evidence: tuple[TransportEvidence, ...] | list[TransportEvidence]):
    """Core receives the actual final attempt, not a synthetic capacity fact."""
    if not transport_evidence:
        raise ValueError("RUN-06 transport evidence is required")
    last = transport_evidence[-1]
    recovered = last.status == "SUCCESS"
    diagnostic = DiagnosticObservation(
        evidence_id=_source_id(last),
        dimension=DiagnosticLens.OPERATIONAL.value,
        value=1.0 if recovered else 0.0,
        statement=f"transport-final-{last.status.lower()}",
        confidence=0.9,
        lens=DiagnosticLens.OPERATIONAL,
        status=DiagnosticStatus.SUPPORTED if recovered else DiagnosticStatus.BLOCKED,
        metadata={
            "historical_id": last.historical_id,
            "origin": last.provenance,
            "attempt": str(last.attempt),
            "transport_status": last.status,
        },
    )
    scenario = DiagnosticScenario(
        f"run06-{last.historical_id.lower()}-{last.status.lower()}",
        "avaliar capacidade apos evento de resiliencia",
        observations=(diagnostic,),
    )
    return CoreLoopEngine().run(CoreLoopRequest(
        build_context(transport_evidence), scenario, (diagnostic,),
    ))


def test_run06_real_timeout_then_recovery_preserves_attempt_history():
    evidence, resilience_state, attempts = run_transport(["timeout", "success"])
    result = run_core(evidence)
    assert resilience_state == "RECOVERED"
    assert [item.status for item in evidence] == ["TIMEOUT", "SUCCESS"]
    assert [item.attempt for item in evidence] == [1, 2]
    assert attempts == 2
    assert result.status == "RECOMMENDATION"
    assert result.handoff_required is False
    assert result.can_execute is False
    assert result.evidence_ids == tuple(_source_id(item) for item in evidence)
    assert result.gaps == ()
    pack = build_context(evidence)
    assert all(
        item.provenance["historical_id"] == "RUN06-H001"
        and item.provenance["origin"] == "local-http-lab"
        and item.provenance["transport_status"] == original.status
        for item, original in zip(pack.scoped_evidence(), evidence)
    )


def test_run06_real_503_is_bounded_and_governed_handoff():
    evidence, resilience_state, attempts = run_transport(
        ["unavailable", "unavailable", "unavailable"]
    )
    result = run_core(evidence)
    assert resilience_state == "DEGRADED"
    assert [item.status for item in evidence] == ["UNAVAILABLE"] * 3
    assert [item.attempt for item in evidence] == [1, 2, 3]
    assert attempts == 3
    assert result.evidence_ids == tuple(_source_id(item) for item in evidence)
    assert result.status == "HANDOFF"
    assert result.handoff_required is True
    assert result.can_execute is False
    assert "transport retry budget exhausted" in result.gaps
    assert "blocked evidence or governance condition" in result.gaps
    assert result.recommendation is None


def test_run06_timeout_503_then_recovery_reaches_core_and_is_reproducible():
    first = run_transport(["timeout", "unavailable", "success"])
    second = run_transport(["timeout", "unavailable", "success"])
    assert first[1] == second[1] == "RECOVERED"
    assert [item.status for item in first[0]] == ["TIMEOUT", "UNAVAILABLE", "SUCCESS"]
    assert [item.attempt for item in first[0]] == [1, 2, 3]
    assert [item.provenance for item in first[0]] == ["local-http-lab"] * 3
    assert [item.historical_id for item in first[0]] == ["RUN06-H001"] * 3
    assert first[0] == second[0]
    assert first[2] == second[2] == 3
    first_core = run_core(first[0])
    second_core = run_core(second[0])
    assert first_core == second_core
    assert first_core.status == "RECOMMENDATION"
    assert first_core.handoff_required is False
    assert first_core.evidence_ids == tuple(_source_id(item) for item in first[0])
    assert set(first_core.evidence_ids) != {"src-capacity"}


def test_run06_does_not_promote_empty_or_synthetic_evidence_to_core():
    import pytest

    with pytest.raises(ValueError, match="transport evidence is required"):
        run_core(())
    with pytest.raises(ValueError, match="transport evidence is required"):
        build_context(())
