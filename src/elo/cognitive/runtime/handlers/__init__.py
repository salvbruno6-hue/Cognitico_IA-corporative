"""Handlers do CRL. Cada handler adapta um estágio do ciclo canônico à API pública do Core.

Refs: ADR-0014, ADR-0015.
"""
from .observe import observe_handler
from .contextualize import contextualize_handler
from .analyze import analyze_handler
from .formulate import formulate_handler
from .decide import decide_handler
from .execute import execute_handler
from .monitor import monitor_handler
from .learn import learn_handler
from .follow_up import follow_up_handler
from .reassess import reassess_handler

__all__ = ["observe_handler","contextualize_handler","analyze_handler","formulate_handler","decide_handler","execute_handler","monitor_handler","learn_handler","follow_up_handler","reassess_handler"]
