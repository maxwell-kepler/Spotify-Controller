# src/gesture/visualization.py
import cv2
import mediapipe as mp
from typing import Optional, Dict, Tuple
from .models import FingerState
from .gestures import GestureType


class GestureVisualizer:
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.7
        self.thickness = 2
        self.text_color = (0, 255, 0)  # Green
        self.landmark_color = (0, 121, 255)  # Red
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

    def add_background_box(self, image, start_pos: Tuple[int, int], end_pos: Tuple[int, int], alpha: float = 0.5):
        """Add a semi-transparent background box"""
        overlay = image.copy()
        cv2.rectangle(overlay, start_pos, end_pos, (50, 50, 50), -1)
        cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

    def draw_landmarks(self, image, hand_landmarks, _):
        self.mp_draw.draw_landmarks(
            image,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_draw.DrawingSpec(color=self.landmark_color, thickness=2, circle_radius=2)
        )

    def draw_finger_states(self, image, finger_states: Dict[str, FingerState]):
        # Calculate text block size
        text_height = 25
        num_lines = len(finger_states)
        total_height = text_height * num_lines
        
        # Add background box for finger states
        start_y = 60  # Start below gesture text
        start_position = (5, start_y - 20)
        end_position = (200, start_y + total_height)
        alpha = 0.5
        self.add_background_box(image, start_position, end_position, alpha) 
        
        y_offset = start_y
        origin = (10, y_offset)
        font_scale = 0.6
        white_text = (255, 255, 255) 
        font_thickness = 1
        for finger_name, state in finger_states.items():
            text = f"{finger_name:>6}: {state.description}"
            cv2.putText(image, text, origin, self.font, font_scale, white_text, font_thickness)
            y_offset += text_height

    def draw_gesture_info(self, image, gesture_type: Optional[GestureType], finger_states: Optional[Dict[str, FingerState]] = None):
        # Add background box for gesture type
        alpha = 0.5
        if gesture_type:
            start_position = (5, 5)
            end_position = (300, 40)
            self.add_background_box(image, start_position, end_position, alpha)
            gesture_text = f"Detected Gesture: {gesture_type.value}"

            origin = (10, 30)
            cv2.putText(
                image,
                gesture_text,
                origin,
                self.font,
                self.font_scale,
                self.text_color,
                self.thickness
            )

        if finger_states:
            self.draw_finger_states(image, finger_states)

        # Add background for quit instruction
        quit_box_start_position = (5, image.shape[0] - 30)
        quit_box_end_position = (150, image.shape[0] - 5)
        self.add_background_box(image, quit_box_start_position, quit_box_end_position, alpha)
        
        quit_box_text = "Press 'q' to quit"
        quit_box_origin = (10, image.shape[0] - 10)
        font_scale = 0.5
        white_text = (255, 255, 255) 
        font_thickness = 1
        cv2.putText(image, quit_box_text, quit_box_origin, self.font, font_scale, white_text, font_thickness)