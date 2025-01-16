# src/gesture/detector.py
import cv2
import mediapipe as mp
from typing import Optional, Dict

from .gestures import GestureType, GestureLibrary
from .visualization import GestureVisualizer

class HandGestureDetector:
    def __init__(self, min_detection_confidence=0.7, min_tracking_confidence=0.7):
        """Initialize the hand gesture detector"""
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
        
    def calculate_finger_states(self, hand_landmarks) -> Dict[str, bool]:
        """Calculate which fingers are extended"""
        states = {}
        
        # Thumb calculation
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        thumb_ip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP]
        states["THUMB"] = thumb_tip.y < thumb_ip.y
        
        # Other fingers
        fingers = {
            "INDEX": [self.mp_hands.HandLandmark.INDEX_FINGER_TIP, self.mp_hands.HandLandmark.INDEX_FINGER_PIP],
            "MIDDLE": [self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP, self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP],
            "RING": [self.mp_hands.HandLandmark.RING_FINGER_TIP, self.mp_hands.HandLandmark.RING_FINGER_PIP],
            "PINKY": [self.mp_hands.HandLandmark.PINKY_TIP, self.mp_hands.HandLandmark.PINKY_PIP]
        }
        
        for finger_name, (tip_id, pip_id) in fingers.items():
            tip = hand_landmarks.landmark[tip_id]
            pip = hand_landmarks.landmark[pip_id]
            states[finger_name] = tip.y < pip.y

        return states

    def detect_gesture(self, hand_landmarks) -> GestureType:
        """Detect the gesture from hand landmarks"""
        finger_states = self.calculate_finger_states(hand_landmarks)
        
        # Compare against known gestures
        for gesture in self.gestures:
            matches = all(
                finger_states[finger] == state 
                for finger, state in gesture.finger_states.items()
            )
            
            if matches:
                if gesture.custom_check:
                    matches = gesture.custom_check(hand_landmarks)
                    
                if matches:
                    return gesture.name
                    
        return GestureType.UNKNOWN

    def get_gesture(self) -> Optional[GestureType]:
        """Get the current gesture from the camera feed"""
        success, image = self.cap.read()
        if not success:
            return None

        # Process image
        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_image)

        gesture_type = None
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]  # Get first hand
            gesture_type = self.detect_gesture(hand_landmarks)
            
            # Update visualization
            self.visualizer.draw_landmarks(image, hand_landmarks, None)
            self.visualizer.draw_gesture_info(image, gesture_type)

        # Display feed
        cv2.imshow('Spotify Gesture Controller', image)
        cv2.waitKey(1)

        return gesture_type

    def cleanup(self):
        """Release resources"""
        self.cap.release()
        cv2.destroyAllWindows()