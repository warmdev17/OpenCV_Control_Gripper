import cv2

class UIDebugger:
    def __init__(self, window_name="Robot View"):
        self.window_name = window_name

    def draw(self, frame, landmarks, gesture, angles, fps):
        if frame is None:
            return

        h, w, _ = frame.shape

        # Vẽ các điểm landmarks
        if landmarks:
            for lm in landmarks:
                cx, cy = int(lm[0] * w), int(lm[1] * h)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        # Vẽ khung thông tin
        cv2.rectangle(frame, (0, 0), (250, 160), (0, 0, 0), -1) # Nền đen góc trái
        
        # Hiển thị chữ
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, f"Gesture: {gesture}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        y_start = 90
        if angles:
            cv2.putText(frame, f"Base: {angles[0]}", (10, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(frame, f"Shoulder: {angles[1]}", (10, y_start+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(frame, f"Elbow: {angles[2]}", (10, y_start+40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(frame, f"Gripper: {angles[3]}", (10, y_start+60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        cv2.imshow(self.window_name, frame)

    def close(self):
        cv2.destroyAllWindows()
