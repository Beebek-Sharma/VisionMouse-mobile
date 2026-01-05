# Phone Camera Setup Guide

This guide shows you how to use your phone as a webcam for the hand gesture mouse control.

## Using IP Webcam (Android)

### Step 1: Install IP Webcam

1. Download **IP Webcam** from Google Play Store
2. Install and open the app

### Step 2: Start the Server

1. Scroll down in the app and tap **"Start server"**
2. The app will show you a URL like: `http://192.168.1.100:8080`
3. **Note down this IP address** - you'll need it!

### Step 3: Find the Video Stream URL

The video stream URL will be:
``

http://YOUR_PHONE_IP:8080/video
```

For example, if your phone shows `192.168.1.100:8080`, the video URL is:
```
http://192.168.1.100:8080/video
```

### Step 4: Configure hand_mouse.py

1. Open `hand_mouse.py` in your editor
2. Find the `CAMERA_SOURCE` configuration (around line 17)
3. Replace the default value with your IP Webcam URL:

```python
# Change this line:
CAMERA_SOURCE = 0

# To this (use YOUR phone's IP):
CAMERA_SOURCE = "http://192.168.1.100:8080/video"
```

### Step 5: Test the Connection

Before running the hand mouse, test if the stream works:

1. Open your web browser
2. Go to: `http://YOUR_PHONE_IP:8080/video`
3. You should see your phone's camera feed

If you see the video, you're ready to run the hand mouse!

### Step 6: Run Hand Mouse

```bash
.venv/Scripts/python.exe hand_mouse.py
```

## Troubleshooting

### "Could not connect to IP camera"

**Check WiFi Connection:**
- Make sure your phone and computer are on the **same WiFi network**
- Some public/guest WiFi networks block device-to-device communication

**Verify IP Address:**
- The IP address shown in IP Webcam app should match what you put in the code
- IP addresses can change - check the app if it stops working

**Test in Browser:**
- Open `http://YOUR_PHONE_IP:8080/video` in your browser
- If it doesn't work in browser, it won't work in the script

**Firewall:**
- Windows Firewall might block the connection
- Try temporarily disabling it to test

### Camera feed is laggy

**Reduce Resolution:**
In IP Webcam app:
1. Go to **Video preferences** → **Video resolution**
2. Select a lower resolution like `640x480` or `320x240`

**Use Specific Resolution in URL:**
```python
CAMERA_SOURCE = "http://192.168.1.100:8080/video?640x480"
```

### Camera feed is upside down

In IP Webcam app:
1. Go to **Video preferences**
2. Enable **"Flip video vertically"** or **"Flip video horizontally"**

## Alternative: DroidCam (Windows/Android/iOS)

If you prefer DroidCam:

1. Install DroidCam on phone and computer
2. DroidCam creates a **virtual webcam**
3. Use camera index instead of URL:
   ```python
   CAMERA_SOURCE = 1  # Or 2, depending on your system
   ```

## Tips for Best Performance

1. **Good Lighting:** Make sure your hand is well-lit
2. **Stable Position:** Mount your phone on a stand
3. **WiFi Quality:** Use 5GHz WiFi if available for better bandwidth
4. **Close Background Apps:** On phone to improve performance
5. **Adjust Smoothing:** Edit `SMOOTHING` value in script if cursor is jittery

## Quick Reference

**IP Webcam URLs:**
- Main page: `http://YOUR_IP:8080`
- Video stream: `http://YOUR_IP:8080/video`
- With resolution: `http://YOUR_IP:8080/video?640x480`

**Common Camera Indices:**
- `0` - Built-in laptop camera
- `1` - First USB/virtual camera
- `2` - Second USB/virtual camera
