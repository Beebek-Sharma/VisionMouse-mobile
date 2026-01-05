"""
Test script to diagnose import issues
"""

print("Testing imports...")

try:
    import sys
    print(f"✓ Python version: {sys.version}")
except Exception as e:
    print(f"✗ Python import failed: {e}")

try:
    import numpy as np
    print(f"✓ NumPy version: {np.__version__}")
except Exception as e:
    print(f"✗ NumPy import failed: {e}")

try:
    import cv2
    print(f"✓ OpenCV version: {cv2.__version__}")
except Exception as e:
    print(f"✗ OpenCV import failed: {e}")
    print(f"   Error details: {type(e).__name__}: {e}")

try:
    import mediapipe as mp
    print(f"✓ MediaPipe version: {mp.__version__}")
except Exception as e:
    print(f"✗ MediaPipe import failed: {e}")

try:
    import pyautogui
    print(f"✓ PyAutoGUI version: {pyautogui.__version__}")
except Exception as e:
    print(f"✗ PyAutoGUI import failed: {e}")

print("\nAll imports successful!" if all else "Some imports failed - see errors above")
