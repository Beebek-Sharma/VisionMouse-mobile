# Gesture Controls Guide

## Available Gestures

### 👆 Move Cursor
- **Gesture:** Point with index finger
- **Action:** Cursor follows your index finger tip
- **Tip:** Keep other fingers relaxed

### 🤏 Click (Left Click)
- **Gesture:** Pinch thumb and index finger together
- **Action:** Single left click
- **Cooldown:** 0.5 seconds between clicks
- **Use for:** Clicking buttons, selecting items, opening files

### ✌️ Right Click
- **Gesture:** Peace sign (index and middle finger up, others down)
- **Action:** Right click (context menu)
- **Cooldown:** 0.5 seconds between clicks
- **Use for:** Opening context menus, right-click options

### 🖐️ Scroll
- **Gesture:** Open hand (all 5 fingers extended)
- **Action:** Scroll up/down by moving hand
- **Direction:** Move hand up = scroll up, move hand down = scroll down
- **Use for:** Scrolling web pages, documents

## Tips for Best Results

### Gesture Recognition
- **Clear gestures:** Make distinct, deliberate gestures
- **Good lighting:** Ensure your hand is well-lit
- **Stable position:** Keep phone/camera steady
- **Distance:** Keep hand at comfortable distance from camera

### Click Accuracy
- **Pinch firmly:** Bring thumb and index tips close together
- **Hold briefly:** Keep pinch for a moment to ensure detection
- **Wait for cooldown:** Don't click too rapidly (0.5s cooldown)

### Scroll Control
- **Extend all fingers:** Make sure all 5 fingers are clearly extended
- **Slow movements:** Move hand slowly for smooth scrolling
- **Vertical motion:** Move hand up/down, not side to side

## Troubleshooting

### Clicks not registering
- **Issue:** Pinch not detected
- **Fix:** 
  - Bring thumb and index closer together
  - Ensure good lighting on your hand
  - Adjust `PINCH_THRESHOLD` in code (try 0.06 or 0.07)

### Too many accidental clicks
- **Issue:** Clicks triggering unintentionally
- **Fix:**
  - Reduce `PINCH_THRESHOLD` (try 0.04 or 0.03)
  - Increase `click_cooldown` to 0.7 or 1.0 seconds

### Peace sign not working
- **Issue:** Right-click not detected
- **Fix:**
  - Make sure only index and middle are up
  - Keep ring and pinky clearly down
  - Ensure fingers are well-separated

### Scroll too sensitive
- **Issue:** Scrolling too fast or erratic
- **Fix:**
  - Move hand more slowly
  - Adjust scroll multiplier in code (line with `scroll_delta`)

## Customization

### Adjust Thresholds

Edit `hand_mouse.py`:

```python
# Line 20 - Pinch sensitivity
PINCH_THRESHOLD = 0.05  # Lower = need closer pinch

# Line 21 - Cursor smoothing  
SMOOTHING = 0.1  # Higher = smoother but slower

# Line 41 - Click cooldown
self.click_cooldown = 0.5  # Seconds between clicks
```

### Modify Scroll Speed

Find this line in the code (around line 240):
```python
scroll_delta = int((norm_y - gesture_state.prev_scroll_y) * 500)
```

Change `500` to:
- `300` for slower scrolling
- `700` for faster scrolling

## Visual Feedback

The video window shows:
- **Green dots:** Hand landmarks
- **Cursor position:** Top left
- **Active gesture:** Below cursor position
- **"CLICK!"** - Yellow text when clicking
- **"RIGHT CLICK!"** - Magenta text when right-clicking
- **"SCROLL: X"** - Yellow text when scrolling

## Keyboard Shortcuts

- **'q'** - Quit the application

## Advanced: Adding Custom Gestures

You can add your own gestures by:

1. **Create detection function:**
   ```python
   def is_thumbs_up(hand_landmarks):
       # Your detection logic
       return True/False
   ```

2. **Add to main loop:**
   ```python
   if is_thumbs_up(hand_landmarks):
       # Your action
       pyautogui.doubleClick()
   ```

3. **Common gestures to try:**
   - Thumbs up = Double click
   - Fist = Pause cursor
   - Three fingers = Middle click
   - Swipe left/right = Browser back/forward
