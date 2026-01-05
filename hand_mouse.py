"""
Hand Gesture Mouse Control with Gesture Recognition
Controls: Index finger = move cursor, Pinch = click, Peace sign = right-click, etc.
"""

import cv2
import mediapipe as mp
import pyautogui
import math
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ============================================================================
# CONFIGURATION
# ============================================================================

CAMERA_SOURCE = "http://192.168.18.205:8080/video?320x240"

# Gesture thresholds
PINCH_THRESHOLD = 0.05  # Distance for pinch detection
SMOOTHING = 0.1  # Slight smoothing for stability

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0  # Remove delay between actions

# ============================================================================
# GESTURE STATE
# ============================================================================

class GestureState:
    def __init__(self):
        self.is_dragging = False
        self.last_click_time = 0
        self.last_right_click_time = 0
        self.click_cooldown = 0.5  # Seconds between clicks
        self.prev_scroll_y = 0
        
gesture_state = GestureState()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_distance(landmark1, landmark2):
    """Calculate Euclidean distance between two landmarks"""
    return math.sqrt(
        (landmark1.x - landmark2.x)**2 + 
        (landmark1.y - landmark2.y)**2 +
        (landmark1.z - landmark2.z)**2
    )

def is_pinching(hand_landmarks):
    """Detect if thumb and index finger are pinched together"""
    thumb_tip = hand_landmarks[4]
    index_tip = hand_landmarks[8]
    distance = calculate_distance(thumb_tip, index_tip)
    return distance < PINCH_THRESHOLD

def is_peace_sign(hand_landmarks):
    """Detect peace sign (index and middle extended, others closed)"""
    # Check if index and middle are extended
    index_tip = hand_landmarks[8]
    index_pip = hand_landmarks[6]
    middle_tip = hand_landmarks[12]
    middle_pip = hand_landmarks[10]
    
    # Extended if tip is higher than pip joint
    index_extended = index_tip.y < index_pip.y
    middle_extended = middle_tip.y < middle_pip.y
    
    # Check if ring and pinky are closed
    ring_tip = hand_landmarks[16]
    ring_pip = hand_landmarks[14]
    pinky_tip = hand_landmarks[20]
    pinky_pip = hand_landmarks[18]
    
    ring_closed = ring_tip.y > ring_pip.y
    pinky_closed = pinky_tip.y > pinky_pip.y
    
    return index_extended and middle_extended and ring_closed and pinky_closed

def count_extended_fingers(hand_landmarks):
    """Count how many fingers are extended"""
    fingers_extended = 0
    
    # Thumb (check x-axis for thumb)
    if hand_landmarks[4].x < hand_landmarks[3].x:
        fingers_extended += 1
    
    # Other fingers (check y-axis)
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    
    for tip, pip in zip(finger_tips, finger_pips):
        if hand_landmarks[tip].y < hand_landmarks[pip].y:
            fingers_extended += 1
    
    return fingers_extended

# ============================================================================
# MEDIAPIPE SETUP
# ============================================================================

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

landmarker = vision.HandLandmarker.create_from_options(options)

# ============================================================================
# CAMERA SETUP
# ============================================================================

print("Initializing camera...")
if isinstance(CAMERA_SOURCE, str):
    print(f"Connecting to IP camera: {CAMERA_SOURCE}")
    cap = cv2.VideoCapture(CAMERA_SOURCE)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
else:
    print(f"Opening camera index: {CAMERA_SOURCE}")
    cap = cv2.VideoCapture(CAMERA_SOURCE)

if not cap.isOpened():
    print("❌ Error: Could not connect to camera")
    exit()

print("✓ Camera connected!")
print("\n🎮 Gesture Controls:")
print("  👆 Index finger = Move cursor")
print("  🤏 Pinch (thumb + index) = Click")
print("  ✌️  Peace sign = Right-click")
print("  🖐️  Open hand (5 fingers) = Scroll mode")
print("  Press 'q' to quit\n")

# ============================================================================
# MAIN LOOP
# ============================================================================

frame_count = 0
prev_x, prev_y = 0, 0
first_frame = True

while True:
    # Read frame
    success, frame = cap.read()
    if not success:
        continue
    
    # Clear buffer for IP cameras
    if isinstance(CAMERA_SOURCE, str):
        for _ in range(3):
            cap.grab()
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    
    frame_count += 1
    timestamp_ms = int(frame_count * 33.33)
    
    detection_result = landmarker.detect_for_video(mp_image, timestamp_ms)
    
    if detection_result.hand_landmarks:
        hand_landmarks = detection_result.hand_landmarks[0]
        h, w, _ = frame.shape
        
        # Draw hand landmarks
        for landmark in hand_landmarks:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
        
        # Get index finger position for cursor
        index_tip = hand_landmarks[8]
        norm_x = index_tip.x
        norm_y = index_tip.y
        
        screen_x = int(norm_x * SCREEN_WIDTH)
        screen_y = int(norm_y * SCREEN_HEIGHT)
        
        # Apply smoothing
        if first_frame:
            smooth_x, smooth_y = screen_x, screen_y
            first_frame = False
        else:
            smooth_x = int(prev_x * SMOOTHING + screen_x * (1 - SMOOTHING))
            smooth_y = int(prev_y * SMOOTHING + screen_y * (1 - SMOOTHING))
        
        prev_x, prev_y = smooth_x, smooth_y
        
        # Move cursor
        pyautogui.moveTo(smooth_x, smooth_y, _pause=False)
        
        # ====================================================================
        # GESTURE DETECTION
        # ====================================================================
        
        current_time = time.time()
        pinching = is_pinching(hand_landmarks)
        peace = is_peace_sign(hand_landmarks)
        extended_fingers = count_extended_fingers(hand_landmarks)
        
        # PINCH = CLICK / DRAG
        if pinching:
            if not gesture_state.is_dragging:
                # Check cooldown
                if current_time - gesture_state.last_click_time > gesture_state.click_cooldown:
                    pyautogui.click()
                    gesture_state.last_click_time = current_time
                    cv2.putText(frame, "CLICK!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                               1, (0, 255, 255), 2)
                    print("🖱️ Click!")
        
        # PEACE SIGN = RIGHT CLICK
        elif peace:
            if current_time - gesture_state.last_right_click_time > gesture_state.click_cooldown:
                pyautogui.rightClick()
                gesture_state.last_right_click_time = current_time
                cv2.putText(frame, "RIGHT CLICK!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                           1, (255, 0, 255), 2)
                print("🖱️ Right-click!")
        
        # OPEN HAND (5 FINGERS) = SCROLL
        elif extended_fingers == 5:
            if gesture_state.prev_scroll_y != 0:
                scroll_delta = int((norm_y - gesture_state.prev_scroll_y) * 500)
                if abs(scroll_delta) > 10:
                    pyautogui.scroll(-scroll_delta)
                    cv2.putText(frame, f"SCROLL: {scroll_delta}", (10, 60), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            gesture_state.prev_scroll_y = norm_y
        else:
            gesture_state.prev_scroll_y = 0
        
        # Display cursor position
        cv2.putText(frame, f"Cursor: ({smooth_x}, {smooth_y})", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Display active gesture
        if pinching:
            cv2.putText(frame, "Pinch", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 255, 255), 2)
        elif peace:
            cv2.putText(frame, "Peace", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (255, 0, 255), 2)
        elif extended_fingers == 5:
            cv2.putText(frame, "Scroll", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (255, 255, 0), 2)
    
    else:
        cv2.putText(frame, "No hand detected", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        gesture_state.prev_scroll_y = 0
    
    cv2.imshow("Hand Gesture Control", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ============================================================================
# CLEANUP
# ============================================================================

cap.release()
cv2.destroyAllWindows()
landmarker.close()
print("✓ Stopped")
