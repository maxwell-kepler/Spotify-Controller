# src/gesture/gestures.py
from enum import Enum
from dataclasses import dataclass
from typing import Dict

class GestureType(Enum):
    UNKNOWN = "UNKNOWN"
    FIST = "FIST"
    THUMB_OUT = "THUMB_OUT"
    POINT = "POINT"
    PEACE = "PEACE"
    PALM = "PALM"
    FOUR_FORWARD = "FOUR_FORWARD"
    THREE_TO_ONE = "THREE_TO_ONE"
    GERMAN_THREE = "GERMAN_THREE"
    SPIDERMAN = "SPIDERMAN"
    GUN = "GUN"
    HEDGEHOG = "HEDGEHOG"
    W = "W"
    HANG_LOOSE = "HANG_LOOSE"
    FOUR = "FOUR"
    THREE = "THREE"
    TWO_TO_ONE = "TWO_TO_ONE"
    FLICK = "FLICK"
    I_LOVE_YOU = "I_LOVE_YOU"
    OKAY = "OKAY"
    MIDDLE_FINGER = "MIDDLE_FINGER"
    QUEENS_TEA = "QUEENS_TEA"

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
                name=GestureType.PALM,
                description="All fingers extended",
                finger_states={"THUMB": True, "INDEX": True, "MIDDLE": True, "RING": True, "PINKY": True}
            ),
            Gesture(
                name=GestureType.FOUR_FORWARD,
                description="All fingers except pinky extended",
                finger_states={"THUMB": True, "INDEX": True, "MIDDLE": True, "RING": True, "PINKY": False}
            ),
            Gesture(
                name=GestureType.THREE_TO_ONE,
                description="All fingers except ring extended",
                finger_states={"THUMB": True, "INDEX": True, "MIDDLE": True, "RING": False, "PINKY": True}
            ),
            Gesture(
                name=GestureType.GERMAN_THREE,
                description="Thumb, index, and middle extended",
                finger_states={"THUMB": True, "INDEX": True, "MIDDLE": True, "RING": False, "PINKY": False}
            ),
            Gesture(
                name=GestureType.SPIDERMAN,
                description="Thumb, index, and pinky extended",
                finger_states={"THUMB": True, "INDEX": True, "MIDDLE": False, "RING": False, "PINKY": True}
            ),
            Gesture(
                name=GestureType.GUN,
                description="Only thumb and index extended",
                finger_states={"THUMB": True, "INDEX": True, "MIDDLE": False, "RING": False, "PINKY": False}
            ),
            Gesture(
                name=GestureType.HEDGEHOG,
                description="All fingers except index extended",
                finger_states={"THUMB": True, "INDEX": False, "MIDDLE": True, "RING": True, "PINKY": True}
            ),
            Gesture(
                name=GestureType.W,
                description="Thumb, middle, and pinky extended",
                finger_states={"THUMB": True, "INDEX": False, "MIDDLE": True, "RING": False, "PINKY": True}
            ),
            Gesture(
                name=GestureType.HANG_LOOSE,
                description="Only thumb and pinky extended",
                finger_states={"THUMB": True, "INDEX": False, "MIDDLE": False, "RING": False, "PINKY": True}
            ),
            Gesture(
                name=GestureType.THUMB_OUT,
                description="Only thumb extended",
                finger_states={"THUMB": True, "INDEX": False, "MIDDLE": False, "RING": False, "PINKY": False}
            ),
            Gesture(
                name=GestureType.FOUR,
                description="All fingers except thumb extended",
                finger_states={"THUMB": False, "INDEX": True, "MIDDLE": True, "RING": True, "PINKY": True}
            ),
            Gesture(
                name=GestureType.THREE,
                description="Index, middle, and ring extended",
                finger_states={"THUMB": False, "INDEX": True, "MIDDLE": True, "RING": True, "PINKY": False}
            ),
            Gesture(
                name=GestureType.TWO_TO_ONE,
                description="Index, middle, and pinky extended",
                finger_states={"THUMB": False, "INDEX": True, "MIDDLE": True, "RING": False, "PINKY": True}
            ),
            Gesture(
                name=GestureType.PEACE,
                description="Index and middle fingers extended",
                finger_states={"THUMB": False, "INDEX": True, "MIDDLE": True, "RING": False, "PINKY": False}
            ),
            Gesture(
                name=GestureType.FLICK,
                description="Index and all fingers except middle extended",
                finger_states={"THUMB": False, "INDEX": True, "MIDDLE": False, "RING": True, "PINKY": True}
            ),
            Gesture(
                name=GestureType.I_LOVE_YOU,
                description="Index and pinky extended",
                finger_states={"THUMB": False, "INDEX": True, "MIDDLE": False, "RING": False, "PINKY": True}
            ),
            Gesture(
                name=GestureType.POINT,
                description="Only index finger extended",
                finger_states={"THUMB": False, "INDEX": True, "MIDDLE": False, "RING": False, "PINKY": False}
            ),
            Gesture(
                name=GestureType.OKAY,
                description="Middle, ring, and pinky extended",
                finger_states={"THUMB": False, "INDEX": False, "MIDDLE": True, "RING": True, "PINKY": True}
            ),
            Gesture(
                name=GestureType.MIDDLE_FINGER,
                description="Only middle finger extended",
                finger_states={"THUMB": False, "INDEX": False, "MIDDLE": True, "RING": False, "PINKY": False}
            ),
            Gesture(
                name=GestureType.QUEENS_TEA,
                description="Only pinky extended",
                finger_states={"THUMB": False, "INDEX": False, "MIDDLE": False, "RING": False, "PINKY": True}
            ),
            Gesture(
                name=GestureType.FIST,
                description="All fingers closed",
                finger_states={"THUMB": False, "INDEX": False, "MIDDLE": False, "RING": False, "PINKY": False}
            )
        ]
