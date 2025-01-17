# src/gesture/visualization.py
import cv2
import mediapipe as mp
from typing import Optional, Dict, Tuple
from .models import FingerState
from .gestures import GestureType


class GestureVisualizer:
    # Constants for visualization
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE_LARGE = 0.7
    FONT_SCALE_SMALL = 0.6
    FONT_SCALE_SMALLEST = 0.5
    THICKNESS_LARGE = 2
    THICKNESS_SMALL = 1
    TEXT_COLOR_GREEN = (0, 255, 0)
    TEXT_COLOR_WHITE = (255, 255, 255)
    LANDMARK_COLOR = (0, 121, 255)
    BACKGROUND_COLOR = (50, 50, 50)
    BACKGROUND_ALPHA = 0.5
    
    TEXT_HEIGHT = 25
    TEXT_START_X = 10
    GESTURE_START_Y = 30
    FINGER_START_Y = 60
    BOX_PADDING = 20
    BOX_WIDTH = 200

    def __init__(self):
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

    def add_background_box(self, image, start_pos: Tuple[int, int], end_pos: Tuple[int, int]):
        """Add a semi-transparent background box"""
        overlay = image.copy()
        cv2.rectangle(overlay, start_pos, end_pos, self.BACKGROUND_COLOR, -1)
        cv2.addWeighted(overlay, self.BACKGROUND_ALPHA, image, 1 - self.BACKGROUND_ALPHA, 0, image)

    def draw_landmarks(self, image, hand_landmarks, _):
        self.mp_draw.draw_landmarks(
            image,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_draw.DrawingSpec(color=self.LANDMARK_COLOR, thickness=2, circle_radius=2)
        )

    def draw_finger_states(self, image, finger_states: Dict[str, FingerState]):
        # Calculate text block size
        num_lines = len(finger_states)
        total_height = self.TEXT_HEIGHT * num_lines
        
        # Add background box for finger states
        start_position = (5, self.FINGER_START_Y - self.BOX_PADDING)
        end_position = (self.BOX_WIDTH, self.FINGER_START_Y + total_height)
        self.add_background_box(image, start_position, end_position)
        
        # Draw each finger state
        for i, (finger_name, state) in enumerate(finger_states.items()):
            y_position = self.FINGER_START_Y + (i * self.TEXT_HEIGHT)
            text = f"{finger_name:>6}: {state.description}"
            cv2.putText(
                image,
                text,
                (self.TEXT_START_X, y_position),
                self.FONT,
                self.FONT_SCALE_SMALL,
                self.TEXT_COLOR_WHITE,
                self.THICKNESS_SMALL
            )

    def draw_gesture_info(self, image, gesture_type: Optional[GestureType], finger_states: Optional[Dict[str, FingerState]] = None):
        # Draw gesture type box and text
        if gesture_type:
            # Background box for gesture type
            self.add_background_box(image, (5, 5), (300, 40))
            
            # Gesture text
            gesture_text = f"Detected Gesture: {gesture_type.value}"
            cv2.putText(
                image,
                gesture_text,
                (self.TEXT_START_X, self.GESTURE_START_Y),
                self.FONT,
                self.FONT_SCALE_LARGE,
                self.TEXT_COLOR_GREEN,
                self.THICKNESS_LARGE
            )

        # Draw finger states
        if finger_states:
            self.draw_finger_states(image, finger_states)

        # Draw quit instruction
        quit_y = image.shape[0] - 10
        quit_box_start = (5, quit_y - self.BOX_PADDING)
        quit_box_end = (150, image.shape[0] - 5)
        self.add_background_box(image, quit_box_start, quit_box_end)
        
        cv2.putText(
            image,
            "Press 'q' to quit",
            (self.TEXT_START_X, quit_y),
            self.FONT,
            self.FONT_SCALE_SMALLEST,
            self.TEXT_COLOR_WHITE,
            self.THICKNESS_SMALL
        )