# test_gesture.py
from src.gesture import HandGestureDetector
import cv2

def main():
    detector = HandGestureDetector()
    print("Starting gesture detection...")
    print("Press 'q' to quit")
    
    try:
        while True:
            gesture = detector.get_gesture()
            if gesture:
                print(f"Detected: {gesture.value}")
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        detector.cleanup()

if __name__ == "__main__":
    main()