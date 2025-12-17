import cv2
import sys

# Import các module (đảm bảo file nằm cùng thư mục)
from camera_reader import CameraReader
from hand_detector import HandDetector
from landmark_filter import LandmarkFilter
from gesture_detector import detect_gesture
from hand_position import get_hand_position
from mapping import get_servo_angles
from pc_sender import PCSender
from ui_debugger import UIDebugger

def main():
    # 1. Setup
    print("[INIT] Starting system...")
    cam = CameraReader(width=640, height=480)
    if not cam.open():
        print("[ERROR] Could not open camera.")
        return

    # Khởi tạo các module
    detector = HandDetector(confidence=0.7)
    l_filter = LandmarkFilter(alpha=0.4)
    sender = PCSender()
    ui = UIDebugger()

    # Trạng thái ban đầu
    last_gripper = 90
    
    print("[INIT] System Ready. Press 'q' to exit.")

    try:
        while True:
            # 2. Read Frame
            frame = cam.read()
            if frame is None:
                break

            # 3. Detect Hand
            raw_landmarks = detector.detect(frame)
            
            # 4. Filter Landmarks
            landmarks = l_filter.filter(raw_landmarks)
            
            gesture = "No Hand"
            angles = (90, 90, 90, last_gripper)

            # 5. Process logic if hand found
            if landmarks:
                # Detect gesture
                gesture = detect_gesture(landmarks)
                
                # Get position
                pos = get_hand_position(landmarks, cam.width, cam.height)
                
                if pos:
                    x, y = pos
                    # Map to angles
                    angles = get_servo_angles(gesture, x, y, cam.width, cam.height, last_gripper)
                    
                    # Cập nhật last_gripper
                    last_gripper = angles[3]
                    
                    # Send to Arduino
                    sender.send(*angles)

            # 6. Display
            fps = cam.get_fps()
            ui.draw(frame, landmarks, gesture, angles, fps)

            # 7. Exit condition
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        cam.release()
        detector.release()
        sender.close()
        ui.close()
        print("[EXIT] Cleanup done.")

if __name__ == "__main__":
    main()
