# src/gesture/gestures.py
from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, Optional, Callable

class GestureType(Enum):
    """Available gesture types"""
    UNKNOWN = auto()
    FIST = auto()
    THUMBS_UP = auto()
    PALM = auto()
    POINT = auto()
    PEACE = auto()

@dataclass
class Gesture:
    """Gesture definition and requirements"""
    name: GestureType
    description: str
    finger_states: Dict[str, bool]
    custom_check: Optional[Callable] = None

class GestureLibrary:
    """Collection of defined gestures"""
    @staticmethod
    def get_gestures() -> list[Gesture]:
        return [
            Gesture(
                name=GestureType.FIST,
                description="All fingers closed",
                finger_states={"THUMB": False, "INDEX": False, "MIDDLE": False, "RING": False, "PINKY": False}
            ),
            Gesture(
                name=GestureType.THUMBS_UP,
                description="Only thumb extended",
                finger_states={"THUMB": True, "INDEX": False, "MIDDLE": False, "RING": False, "PINKY": False}
            ),
            Gesture(
                name=GestureType.PALM,
                description="All fingers extended",
                finger_states={"THUMB": True, "INDEX": True, "MIDDLE": True, "RING": True, "PINKY": True}
            ),
            Gesture(
                name=GestureType.POINT,
                description="Only index finger extended",
                finger_states={"THUMB": False, "INDEX": True, "MIDDLE": False, "RING": False, "PINKY": False}
            ),
            Gesture(
                name=GestureType.PEACE,
                description="Index and middle fingers extended",
                finger_states={"THUMB": False, "INDEX": True, "MIDDLE": True, "RING": False, "PINKY": False}
            ),
        ]