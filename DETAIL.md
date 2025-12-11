# Motion-Controlled Robot Arm Project

### **Ultra-Detailed Task README (For Vibe Coding Team)**

This README is designed so that **any team member can copy their
assigned task into AI and immediately receive runnable code** without
understanding the whole project.

------------------------------------------------------------------------

# ⭐ Project Summary

A camera captures your hand → software detects landmarks → system
extracts gesture + hand position → mapping logic converts those into
servo angles → Arduino moves a 4‑servo robotic arm (base, shoulder,
elbow, gripper).

------------------------------------------------------------------------

# 🧩 Project Modules (10 Modules -- Leader does 2)

Each module is **independent** and has **extremely specific
inputs/outputs**, so team members can code individually without
conflicts.

------------------------------------------------------------------------

# 1. camera_reader.py

## 🎯 Goal

Create a module that **opens webcam**, **reads frames continuously**,
and **returns frames in 640×480 resolution**.

## 📥 Input

Nothing.

## 📤 Output

Function:

``` python
get_frame() -> numpy.ndarray | None
```

## 🔧 Detailed Work Instructions

-   Import OpenCV.
-   Initialize the default camera (ID = 0).
-   Set resolution to 640x480.
-   Write `get_frame()` that:
    -   reads a frame
    -   converts it to RGB
    -   returns the frame
    -   returns `None` if read fails.
-   Ensure FPS ≥ 20.
-   Include cleanup function if camera needs to be released.

## 📝 AI Prompt Template

"Write a Python module named `camera_reader.py` that opens webcam, reads
frames in 640×480, returns them as numpy arrays via get_frame(), returns
None on failure, and keeps FPS above 20."

------------------------------------------------------------------------

# 2. hand_detector.py

## 🎯 Goal

Use **Mediapipe Hands** to detect **21 3‑D landmarks**.

## 📥 Input

`frame` (numpy RGB image)

## 📤 Output

List of 21 points:

    [(x,y,z), (x,y,z), ...] or None

## 🔧 Detailed Work Instructions

-   Import mediapipe.
-   Initialize `mp.solutions.hands.Hands` with:
    -   `max_num_hands=1`
    -   `min_detection_confidence=0.7`
    -   `min_tracking_confidence=0.7`
-   Convert input frame to RGB.
-   Run detection.
-   If no hand: return None.
-   If hand detected:
    -   extract 21 landmark points
    -   normalize them to float values between 0--1.

## 📝 AI Prompt Template

"Write a module `hand_detector.py` that takes an RGB frame and returns
list of 21 normalized mediapipe hand landmarks or None."

------------------------------------------------------------------------

# 3. landmark_filter.py

## 🎯 Goal

Smooth the 21 landmark points to remove jitter.

## 📥 Input

`raw_landmarks: list[(x,y,z)]`

## 📤 Output

`filtered_landmarks: list[(x,y,z)]`

## 🔧 Detailed Work Instructions

-   Implement EMA smoothing:

        smoothed = alpha * new + (1-alpha) * old

-   Use `alpha = 0.35`.

-   Store previous landmark state inside the module.

-   Maintain shape exactly: 21 elements, each 3 values.

-   If previous landmarks do not exist → return input as-is.

## 📝 AI Prompt Template

"Write `landmark_filter.py` that applies EMA smoothing to 21 hand
landmarks using alpha=0.35."

------------------------------------------------------------------------

# 4. gesture_detector.py

## 🎯 Goal

Classify gesture based on finger openness.

## 📥 Input

`landmarks_filtered`

## 📤 Output

One of:

    "open" | "close" | "pinch" | "idle"

## 🔧 Detailed Work Instructions

-   Use tip positions of fingers vs their base joints.
-   Example rules:
    -   All fingertips far → "open"
    -   All fingertips near palm → "close"
    -   Thumb tip close to index tip → "pinch"
    -   Otherwise → "idle"
-   Must not modify input.

## 📝 AI Prompt Template

"Write `gesture_detector.py` that takes 21 filtered landmarks and
returns gesture string open/close/pinch/idle using fingertip distances."

------------------------------------------------------------------------

# 5. hand_position.py

## 🎯 Goal

Convert normalized coordinates → pixel coordinates in 640×480.

## 📥 Input

`landmarks_filtered`

## 📤 Output

Tuple:

    (x_pixel, y_pixel)

## 🔧 Detailed Work Instructions

-   Use landmark index 9 (center of palm) **or** combine multiple
    points.

-   Convert by:

        x_pixel = x_norm * 640
        y_pixel = y_norm * 480

-   Return integers.

## 📝 AI Prompt Template

"Write `hand_position.py` that converts normalized palm landmark to
(x_pixel, y_pixel) on a 640×480 frame."

------------------------------------------------------------------------

# 6. pc_sender.py

## 🎯 Goal

Send servo angles to Arduino over Serial.

## 📥 Input

Tuple:

    (base, shoulder, elbow, gripper)

## 📤 Output

Serial transmission string:

    B:<val>;S:<val>;E:<val>;G:<val>

## 🔧 Detailed Work Instructions

-   Use pyserial.
-   Auto-detect port OR allow fixed port.
-   Reconnect if cable unplugged.
-   Convert angles to int 0--180.
-   Send formatted string.
-   Flush output.

## 📝 AI Prompt Template

"Write `pc_sender.py` that sends servo angles to Arduino using pyserial
in format B:x;S:y;E:z;G:w."

------------------------------------------------------------------------

# 7. ui_debugger.py

## 🎯 Goal

Show debug window with: - video frame\
- drawn landmarks\
- gesture text\
- servo angles\
- FPS

## 📥 Input

-   frame\
-   gesture\
-   angles

## 📤 Output

-   Debug window (OpenCV imshow)

## 🔧 Detailed Work Instructions

-   Overlay landmarks as small circles.
-   Add text in upper-left corner.
-   Add FPS counter using time.time().
-   Show servo angles clearly.

## 📝 AI Prompt Template

"Write `ui_debugger.py` that draws landmarks, gesture, angles, and FPS
on a frame and shows it via cv2.imshow."

------------------------------------------------------------------------

# 8. servo_control.ino (Arduino)

## 🎯 Goal

Parse serial input and move 4 servos.

## 📥 Input

String:

    B:val;S:val;E:val;G:val

## 📤 Output

PWM control for 4 servo motors.

## 🔧 Detailed Work Instructions

-   Use `Servo.h`.
-   Create 4 Servo objects: base, shoulder, elbow, gripper.
-   Setup correct PWM pins.
-   In loop:
    -   Read Serial line
    -   Parse values
    -   Constrain 0--180
    -   Write to each servo
-   No delay() except 1--2 ms.

## 📝 AI Prompt Template

"Write Arduino code that reads a serial command B:x;S:y;E:z;G:w and
moves 4 servos accordingly."

------------------------------------------------------------------------

# 9. mapping.py (Leader)

## 🎯 Goal

Convert gesture + (x,y) hand position → 4 servo angles.

## 📥 Input

-   gesture\
-   x_pixel\
-   y_pixel

## 📤 Output

Tuple of 4 servo angles.

## 🔧 Detailed Work Instructions

### Base

-   Rotate from left--right of frame

        base = map(x, 0→640, 20→160)

### Shoulder

-   Move based on vertical position

        shoulder = map(y, 0→480, 30→150)

### Elbow

-   Opposite of shoulder for natural motion

        elbow = 180 - shoulder

### Gripper

-   Based on gesture

        open  → 160°
        close → 20°
        pinch → 60°
        idle  → keep previous

-   Always constrain to 0--180.

## 📝 AI Prompt Template

"Write `mapping.py` that turns gesture + xy pixel into 4 servo angles
using predefined mapping rules."

------------------------------------------------------------------------

# 10. main.py (Leader)

## 🎯 Goal

Integrate all modules into one pipeline.

## 🔧 Detailed Work Instructions

-   Import all 9 modules.
-   Infinite loop:
    1.  frame = get_frame()
    2.  landmarks = detect_hand(frame)
    3.  filtered = filter_landmarks(landmarks)
    4.  gesture = detect_gesture(filtered)
    5.  x,y = calc_hand_position(filtered)
    6.  angles = mapping(gesture, x, y)
    7.  send_to_arduino(angles)
    8.  show_debug(frame, gesture, angles)
-   Maintain ≥15 FPS.
-   Handle:
    -   camera missing\
    -   serial disconnected\
    -   no landmarks

## 📝 AI Prompt Template

"Write `main.py` that connects 9 modules into a real-time loop executing
the full robot arm control pipeline."

------------------------------------------------------------------------

# 🎉 Final Notes

-   All modules are **fully independent**.\
-   Every team member can simply paste their section into ChatGPT/AI to
    get code.\
-   Leader handles mapping + main (most difficult).\
-   No need for machine learning training.
