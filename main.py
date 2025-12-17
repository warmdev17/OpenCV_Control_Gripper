import cv2
import sys

# Import modules
try:
    from camera_reader import CameraReader
    from hand_detector import HandDetector
    from landmark_filter import LandmarkFilter
    from gesture_detector import detect_gesture
    from hand_position import get_hand_position
    from mapping import get_servo_angles
    from pc_sender import PCSender
    from ui_debugger import UIDebugger
except ImportError as e:
    print(f"[LỖI] Thiếu file hoặc module: {e}")
    print("Hãy đảm bảo tất cả file .py nằm cùng thư mục.")
    sys.exit(1)

def main():
    print("[INIT] Đang khởi động trên Windows...")
    
    # 1. Camera
    cam = CameraReader(width=640, height=480)
    if not cam.open():
        print("[ERROR] Không mở được Camera.")
        return

    # 2. Các module xử lý
    detector = HandDetector(confidence=0.7)
    l_filter = LandmarkFilter(alpha=0.4)
    sender = PCSender() # Tự tìm COM port
    ui = UIDebugger()

    last_gripper = 90
    print("[READY] Nhấn 'q' để thoát.")

    try:
        while True:
            # --- Đọc & Xử lý ---
            frame = cam.read()
            if frame is None: break

            raw_landmarks = detector.detect(frame)
            landmarks = l_filter.filter(raw_landmarks)
            
            gesture = "No Hand"
            angles = (90, 90, 90, last_gripper)

            if landmarks:
                gesture = detect_gesture(landmarks)
                pos = get_hand_position(landmarks, cam.width, cam.height)
                
                if pos:
                    angles = get_servo_angles(gesture, pos[0], pos[1], cam.width, cam.height, last_gripper)
                    last_gripper = angles[3]
                    sender.send(*angles)

            # --- Hiển thị ---
            ui.draw(frame, landmarks, gesture, angles, cam.get_fps())

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        pass
    finally:
        cam.release()
        detector.release()
        sender.close()
        ui.close()
        print("[EXIT] Đã tắt chương trình.")

if __name__ == "__main__":
    main()
