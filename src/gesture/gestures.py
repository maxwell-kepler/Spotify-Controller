# src/gesture/gestures.py
from enum import Enum
from dataclasses import dataclass
from typing import Dict

class GestureType(Enum):
    UNKNOWN = "UNKNOWN"
    FIST = "FIST"
    THUMBS_UP = "THUMBS_UP"
    POINT = "POINT"
    PEACE = "PEACE"
    PALM = "PALM"

@dataclass
class Gesture:
    name: GestureType
    description: str
    finger_states: Dict[str, bool]  # finger_name: is_extended

class GestureLibrary:
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
                name=GestureType.POINT,
                description="Only index finger extended",
                finger_states={"THUMB": False, "INDEX": True, "MIDDLE": False, "RING": False, "PINKY": False}
            ),
            Gesture(
                name=GestureType.PEACE,
                description="Index and middle fingers extended",
                finger_states={"THUMB": False, "INDEX": True, "MIDDLE": True, "RING": False, "PINKY": False}
            ),
            Gesture(
                name=GestureType.PALM,
                description="All fingers extended",
                finger_states={"THUMB": True, "INDEX": True, "MIDDLE": True, "RING": True, "PINKY": True}
            )
        ]
