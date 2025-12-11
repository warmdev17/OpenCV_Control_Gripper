# Motion-Controlled Robot Arm Project

## Overview

This project uses computer vision to detect human hand movement and map
it to a 4-servo robotic arm with a gripper. The system processes camera
input, identifies hand landmarks, detects gestures, calculates hand
position, maps this to servo angles, and sends control signals to an
Arduino that drives the servos.

## Module Structure (10 Modules)

The project is divided into 10 modules. Each module is handled by one
team member, except the leader who handles 2 modules.

---

## 1. camera_reader.py

### Responsibilities

- Access system webcam.
- Continuously capture frames (minimum 20 FPS).
- Provide frames in 640×480 resolution.

### Input

- None.

### Output

- `numpy array` frame or `None` if failed.

---

## 2. hand_detector.py

### Responsibilities

- Use MediaPipe Hands to detect a human hand.
- Extract 21 hand landmarks in normalized coordinates.
- Ensure confidence ≥ 0.7.

### Input

- Frame from camera_reader.

### Output

- List of 21 `(x,y,z)` normalized points or `None`.

---

## 3. landmark_filter.py

### Responsibilities

- Apply EMA or moving average smoothing to reduce jitter.
- Maintain consistent landmark structure.

### Input

- Raw landmarks list.

### Output

- Smoothed landmarks list.

---

## 4. gesture_detector.py

### Responsibilities

- Identify gesture type based on finger openness/tightness.
- Classify gestures:
  - `"open"`
  - `"close"`
  - `"pinch"`
  - `"idle"`

### Input

- Filtered landmarks.

### Output

- Gesture string.

---

## 5. hand_position.py

### Responsibilities

- Convert normalized landmarks to pixel coordinates.
- Use index finger tip + palm center for control reference.

### Input

- Landmarks.

### Output

- `(x_pixel, y_pixel)` hand position.

---

## 6. pc_sender.py

### Responsibilities

- Send servo commands to Arduino via Serial.

- Format:

      B:<val>;S:<val>;E:<val>;G:<val>

### Input

- Tuple angles.

### Output

- Serial transmission.

---

## 7. ui_debugger.py

### Responsibilities

- Display debug interface showing:
  - Landmarks overlay
  - Gesture text
  - Servo angles
  - FPS
- Maintain real-time update.

### Input

- Frame, gesture, angles.

### Output

- Debug window.

---

## 8. servo_control.ino (Arduino)

### Responsibilities

- Parse incoming serial formatted angles.
- Drive 4 servos:
  - Base
  - Shoulder
  - Elbow
  - Gripper
- Enforce angle limits.

### Input

- Serial string.

### Output

- PWM servo control.

---

## 9. mapping.py (Leader)

### Responsibilities

- Convert gesture + hand position into 4 servo angles.
- Logic includes:
  - Base rotates with x-position.
  - Shoulder + elbow map from y-position.
  - Gripper opens/closes from gesture.
- Ensure angle bounds (0--180°).

### Input

- Gesture + hand position.

### Output

- Tuple `(base, shoulder, elbow, gripper)`.

---

## 10. main.py (Leader)

### Responsibilities

- Integrate all modules into a single pipeline:

      frame → detect → filter → gesture → position → mapping → send → debug

- Ensure system stability.

- Manage FPS loop (≥15 FPS).

- Handle module errors gracefully.

---

## Final Notes

- The team can work independently without conflict.
- The leader handles core logic + final integration.
- No model training required (MediaPipe provides landmarks).
