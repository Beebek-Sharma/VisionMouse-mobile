# Hand Gesture Mouse Control

## Overview

This system uses your webcam to track your hand in real-time and moves the mouse cursor based on your index finger position. The camera captures your hand, MediaPipe identifies key landmarks (finger tips, knuckles, etc.), and we map the index finger tip coordinates to screen coordinates with smoothing to reduce jitter.

---

## Required Installations

**Step 1: Create and activate a virtual environment**

```bash
# Create virtual environment
uv venv --seed

# Activate it (Git Bash/MinGW on Windows)
source .venv/Scripts/activate

# Or on Windows CMD/PowerShell
.venv\Scripts\activate
```

**Step 2: Install dependencies**

```bash
uv pip install -r requirements.txt
```

**Step 3: Download the MediaPipe hand tracking model**

```bash
python download_model.py
```

This downloads the required `hand_landmarker.task` model file (~7.5 MB).

**Package purposes:**
- `opencv-python`: Webcam access and image processing
- `mediapipe`: Google's hand tracking solution
- `pyautogui`: Cross-platform mouse control
- `numpy`: Coordinate smoothing calculations
- `protobuf==3.20.3`: Required for MediaPipe compatibility

**Important:** Always run the script using the virtual environment Python:
```bash
# If venv is activated
python hand_mouse.py

# Or use the full path
.venv/Scripts/python.exe hand_mouse.py
```

---

---

## Phone Camera Setup (IP Webcam)

If your laptop camera isn't working, you can use your phone camera instead!

**Quick Setup:**

1. Install **IP Webcam** app on your Android phone (from Play Store)
2. Open the app and tap **"Start server"**
3. Note the IP address shown (e.g., `192.168.1.100:8080`)
4. Edit `hand_mouse.py` and change line 27:
   ```python
   CAMERA_SOURCE = "http://192.168.1.100:8080/video"  # Use YOUR phone's IP
   ```
5. Make sure phone and computer are on the **same WiFi network**
6. Run the script normally

**📖 Detailed Guide:** See [phone_camera_setup.md](file:///d:/Ideas/VisionMouse/phone_camera_setup.md) for complete instructions and troubleshooting.

---

---

## 🎮 Gesture Controls

The hand mouse now supports gesture-based controls!

**Available Gestures:**

| Gesture | Action | How To |
|---------|--------|--------|
| 👆 Index finger | Move cursor | Point with index finger |
| 🤏 Pinch | Click | Bring thumb & index together |
| ✌️ Peace sign | Right-click | Index & middle up, others down |
| 🖐️ Open hand (5 fingers) | Scroll | Move hand up/down to scroll |

**📖 Detailed Guide:** See [gesture_controls.md](file:///d:/Ideas/VisionMouse/gesture_controls.md) for tips, troubleshooting, and customization.

---

## Hand Landmarks Used

MediaPipe Hands detects 21 landmarks per hand (0-20). We use:

- **Landmark 8**: Index finger tip (controls cursor position)
- **Landmark 4**: Thumb tip (optional for future click gestures)

The landmarks are returned as normalized coordinates (0.0 to 1.0) relative to the image dimensions.

---

## Coordinate Mapping Logic

### Camera to Screen Mapping

1. **Capture**: Camera provides coordinates in pixels (e.g., 640x480)
2. **Normalize**: MediaPipe gives us normalized coordinates (0.0-1.0)
3. **Scale**: Multiply by screen dimensions to get screen coordinates
4. **Invert Y-axis**: Camera Y increases downward, screen Y increases downward (same direction, but we flip X for mirror effect)
5. **Smooth**: Apply exponential moving average to reduce jitter

### Smoothing Formula

```
smoothed_x = (smoothed_x * smoothing_factor) + (current_x * (1 - smoothing_factor))
```

Higher smoothing factor (0.5-0.9) = smoother but slower response
Lower smoothing factor (0.1-0.3) = faster but jittery

---

## Complete Python Script

See `hand_mouse.py` for the full implementation.

---

## Troubleshooting

### Virtual environment not activated
- **Issue**: `ModuleNotFoundError` for cv2, mediapipe, or pyautogui
- **Fix**: Make sure you're using the virtual environment Python:
  ```bash
  # Check which Python you're using
  which python
  
  # Should show: .venv/Scripts/python (or similar)
  # If not, activate the venv or use the full path
  .venv/Scripts/python.exe hand_mouse.py
  ```

### Phone camera not connecting
- **Issue**: "Could not connect to IP camera" error
- **Fix**: 
  1. Verify phone and computer are on the same WiFi network
  2. Check IP address in IP Webcam app matches the URL in code
  3. Test the URL in your web browser first: `http://YOUR_IP:8080/video`
  4. Make sure IP Webcam app is running and server is started
  5. Check firewall settings (temporarily disable to test)

### Camera not opening
- **Issue**: `cv2.VideoCapture(0)` fails
- **Fix**: Try different camera indices (1, 2) or check camera permissions

### Cursor too jittery
- **Issue**: Cursor jumps around
- **Fix**: Increase `SMOOTHING` value (try 0.7-0.8)

### Cursor too slow/laggy
- **Issue**: Cursor doesn't respond quickly
- **Fix**: Decrease `SMOOTHING` value (try 0.3-0.4)

### Hand not detected
- **Issue**: "No hand detected" message appears
- **Fix**: Ensure good lighting, hand is fully visible, and within camera frame

### Cursor moves in wrong direction
- **Issue**: Moving hand right moves cursor left
- **Fix**: Remove the X-axis flip in the code (change `screen_w - screen_x` to `screen_x`)

### High CPU usage
- **Issue**: Computer slows down
- **Fix**: Reduce camera resolution or decrease `model_complexity` to 0

---

## Usage

1. Run the script: `python hand_mouse.py` (or `.venv/Scripts/python.exe hand_mouse.py`)
2. Position your hand in front of the webcam (or phone camera)
3. Move your index finger to control the cursor
4. Press 'q' to quit

**Tips:**
- Keep hand at arm's length from camera
- Use good lighting
- Move hand slowly at first to get used to the sensitivity
- If using phone camera, mount it on a stable stand
