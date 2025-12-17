def get_hand_position(landmarks, frame_width, frame_height):
    """
    Lấy tọa độ lòng bàn tay (Landmark 9) để điều khiển robot.
    Trả về: (x, y) pixel
    """
    if not landmarks:
        return None
        
    # Dùng landmark 9 (khớp giữa ngón giữa) làm tâm
    lm = landmarks[9]
    
    x = int(lm[0] * frame_width)
    y = int(lm[1] * frame_height)
    
    # Giới hạn trong khung hình
    x = max(0, min(frame_width, x))
    y = max(0, min(frame_height, y))
    
    return x, y
