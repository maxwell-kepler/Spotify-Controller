# src/gesture/__init__.py
"""
Gesture detection module for identifying hand gestures using computer vision
"""
from .detector import HandGestureDetector
from .gestures import GestureType

__all__ = ['HandGestureDetector', 'GestureType']