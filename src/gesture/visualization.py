# src/gesture/visualization.py
import cv2
import mediapipe as mp
from typing import Optional

class GestureVisualizer:
    def __init__(self):
        """Initialize visualization settings"""
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.7
        self.thickness = 2
        self.text_color = (0, 255, 0)  # Green
        self.landmark_color = (0, 121, 255)  # Red
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

    def draw_landmarks(self, image, hand_landmarks, mp_hands):
        """Draw hand landmarks on the image"""
        self.mp_draw.draw_landmarks(
            image,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_draw.DrawingSpec(color=self.landmark_color, thickness=2, circle_radius=2)
        )

    def draw_gesture_info(self, image, gesture_type: Optional[str]):
        """Draw gesture information on the image"""
        if gesture_type:
            gesture_text = f"Detected Gesture: {gesture_type.name}"
            cv2.putText(
                image,
                gesture_text,
                (10, 30),
                self.font,
                self.font_scale,
                self.text_color,
                self.thickness
            )