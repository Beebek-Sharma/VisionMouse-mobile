"""
Ultra-fast hand mouse - Optimized for IP camera with minimal lag
This version removes all visual feedback to maximize performance
"""

import cv2
import mediapipe as mp
import pyautogui
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ============================================================================
# CONFIGURATION
# ============================================================================

# Camera source
CAMERA_SOURCE = "http://192.168.18.205:8080/video?320x240"

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Disable PyAutoGUI failsafe
pyautogui.FAILSAFE = False

# ============================================================================
# MEDIAPIPE SETUP
# ============================================================================

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.3,  # Very low for fastest detection
    min_hand_presence_confidence=0.3,
    min_tracking_confidence=0.3
)

landmarker = vision.HandLandmarker.create_from_options(options)

# ============================================================================
# CAMERA SETUP
# ============================================================================

print("Connecting to IP camera...")
cap = cv2.VideoCapture(CAMERA_SOURCE)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap.isOpened():
    print("❌ Could not connect to camera")
    exit()

print("✓ Connected! Press 'q' to quit")
print("Note: No video window for maximum speed")

# ============================================================================
# MAIN LOOP - OPTIMIZED FOR SPEED
# ============================================================================

frame_count = 0

while True:
    # Clear buffer - get latest frame only
    for _ in range(5):
        cap.grab()
    
    success, frame = cap.read()
    if not success:
        continue
    
    # Convert to RGB (required by MediaPipe)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    
    # Process frame
    frame_count += 1
    timestamp_ms = int(frame_count * 33.33)
    
    try:
        detection_result = landmarker.detect_for_video(mp_image, timestamp_ms)
        
        # Move cursor if hand detected
        if detection_result.hand_landmarks:
            hand_landmarks = detection_result.hand_landmarks[0]
            index_finger_tip = hand_landmarks[8]
            
            # Direct cursor movement - no smoothing
            screen_x = int(index_finger_tip.x * SCREEN_WIDTH)
            screen_y = int(index_finger_tip.y * SCREEN_HEIGHT)
            
            pyautogui.moveTo(screen_x, screen_y, _pause=False)
    
    except Exception:
        pass  # Skip errors for speed
    
    # Check for quit (minimal overhead)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ============================================================================
# CLEANUP
# ============================================================================

cap.release()
cv2.destroyAllWindows()
landmarker.close()
print("Stopped")
