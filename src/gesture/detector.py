# src/gesture/detector.py
import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Dict, Tuple

from .gestures import GestureType, GestureLibrary
from .visualization import GestureVisualizer
from .models import FingerState

class HandGestureDetector:
    def __init__(self, min_detection_confidence=0.7, min_tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        self.cap = cv2.VideoCapture(0)
        self.visualizer = GestureVisualizer()
        self.gestures = GestureLibrary.get_gestures()
        
    def calculate_finger_states(self, hand_landmarks) -> Dict[str, FingerState]:
        states = {}
        
        # Get palm center for reference
        index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        pinky_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP]
        palm_center_x = (index_mcp.x + pinky_mcp.x) / 2
        palm_center_y = (index_mcp.y + pinky_mcp.y) / 2
        
        # Thumb detection using just distance ratio
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        # thumb_ip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP]
        thumb_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_MCP]
        
        tip_to_palm_dist = np.sqrt((thumb_tip.x - palm_center_x)**2 + (thumb_tip.y - palm_center_y)**2)
        mcp_to_palm_dist = np.sqrt((thumb_mcp.x - palm_center_x)**2 + (thumb_mcp.y - palm_center_y)**2)
        thumb_extended = tip_to_palm_dist / mcp_to_palm_dist > 1.1  # More lenient threshold than 1.2, causes the extension to be detected more consistently
        
        states["THUMB"] = FingerState(is_extended=thumb_extended, description="Extended" if thumb_extended else "Curled")
        
        # Handle other fingers using PIP joint
        fingers = {
            "INDEX": [self.mp_hands.HandLandmark.INDEX_FINGER_TIP, 
                     self.mp_hands.HandLandmark.INDEX_FINGER_PIP,
                     self.mp_hands.HandLandmark.INDEX_FINGER_MCP],
            "MIDDLE": [self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                      self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
                      self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP],
            "RING": [self.mp_hands.HandLandmark.RING_FINGER_TIP,
                    self.mp_hands.HandLandmark.RING_FINGER_PIP,
                    self.mp_hands.HandLandmark.RING_FINGER_MCP],
            "PINKY": [self.mp_hands.HandLandmark.PINKY_TIP,
                     self.mp_hands.HandLandmark.PINKY_PIP,
                     self.mp_hands.HandLandmark.PINKY_MCP]
        }
        
        # Calculate states for other fingers using the original thresholds
        for finger_name, landmarks in fingers.items():
            tip = hand_landmarks.landmark[landmarks[0]]
            pip = hand_landmarks.landmark[landmarks[1]]
            mcp = hand_landmarks.landmark[landmarks[2]]
            
            # Check if finger is extended
            tip_to_pip = tip.y - pip.y
            pip_to_mcp = pip.y - mcp.y
            is_extended = tip_to_pip < -0.04 and pip_to_mcp < 0.04
            
            states[finger_name] = FingerState(is_extended=is_extended, description="Extended" if is_extended else "Curled")
            
        return states

    def detect_gesture(self, hand_landmarks) -> Tuple[GestureType, Dict[str, FingerState]]:
        finger_states = self.calculate_finger_states(hand_landmarks)
        
        # Compare current states with defined gestures
        for gesture in self.gestures:
            matches = all(finger_states[finger].is_extended == required_state for finger, required_state in gesture.finger_states.items())
            if matches:
                return gesture.name, finger_states
                
        return GestureType.UNKNOWN, finger_states

    def get_gesture(self) -> Optional[GestureType]:
        success, image = self.cap.read()
        if not success:
            return None

        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_image)

        gesture_type = None
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]  # Get first hand
            gesture_type, finger_states = self.detect_gesture(hand_landmarks)
            
            # Update visualization
            self.visualizer.draw_landmarks(image, hand_landmarks, None)
            self.visualizer.draw_gesture_info(image, gesture_type, finger_states)

        cv2.imshow('Gesture Detection', image)
        cv2.waitKey(1)

        return gesture_type

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()