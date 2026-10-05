"""Orchestration orientation — camada consultiva read-only do ELO.

Este pacote produz orientação estruturada a partir de estados canônicos já
produzidos. Não é autoridade de execução, autorização, roteamento, seleção,
aprendizado ou promoção.
"""

from .orchestration_orientation_builder import (
    OrchestrationOrientationBuilder,
    Orientation,
    OrientationConfidence,
    OrientationFact,
    OrientationRequest,
)

__all__ = [
    "OrchestrationOrientationBuilder",
    "Orientation",
    "OrientationConfidence",
    "OrientationFact",
    "OrientationRequest",
]
