"""Bootstrap do CRL: registra os 10 handlers.

Refs: ADR-0014, ADR-0015.
"""
from __future__ import annotations
from .crl import CognitiveRuntimeLoop, Stage
from .handlers import analyze_handler, contextualize_handler, decide_handler, execute_handler, follow_up_handler, formulate_handler, learn_handler, monitor_handler, observe_handler, reassess_handler

def build_default_crl() -> CognitiveRuntimeLoop:
    crl = CognitiveRuntimeLoop()
    crl.register(Stage.OBSERVE, observe_handler)
    crl.register(Stage.CONTEXTUALIZE, contextualize_handler)
    crl.register(Stage.ANALYZE, analyze_handler)
    crl.register(Stage.FORMULATE, formulate_handler)
    crl.register(Stage.DECIDE, decide_handler)
    crl.register(Stage.EXECUTE, execute_handler)
    crl.register(Stage.MONITOR, monitor_handler)
    crl.register(Stage.LEARN, learn_handler)
    crl.register(Stage.FOLLOW_UP, follow_up_handler)
    crl.register(Stage.REASSESS, reassess_handler)
    return crl
