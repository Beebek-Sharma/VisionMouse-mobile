"""
Download MediaPipe Hand Landmarker model
This script downloads the required model file for MediaPipe Hands
"""

import urllib.request
import os

MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
MODEL_PATH = "hand_landmarker.task"

print("Downloading MediaPipe Hand Landmarker model...")
print(f"URL: {MODEL_URL}")
print(f"Saving to: {MODEL_PATH}")

try:
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print(f"✓ Model downloaded successfully!")
    print(f"  File size: {os.path.getsize(MODEL_PATH) / (1024*1024):.2f} MB")
except Exception as e:
    print(f"✗ Failed to download model: {e}")
    print("\nPlease download manually from:")
    print(MODEL_URL)
    exit(1)
