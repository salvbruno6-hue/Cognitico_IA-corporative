"""Temporal validity metadata for knowledge used by ELO."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TemporalValidity:
    observed_at: datetime
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    last_confirmed_at: datetime | None = None

    def is_valid_at(self, moment: datetime) -> bool:
        if self.valid_from and moment < self.valid_from:
            return False
        if self.valid_until and moment > self.valid_until:
            return False
        return True
