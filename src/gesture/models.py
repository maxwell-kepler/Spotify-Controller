# src/gesture/models.py
from dataclasses import dataclass

@dataclass
class FingerState:
    is_extended: bool
    description: str  # 'Extended' or 'Curled'