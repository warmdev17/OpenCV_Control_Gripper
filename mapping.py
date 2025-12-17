def map_range(x, in_min, in_max, out_min, out_max):
    """Hàm tiện ích tương đương map() trong Arduino"""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def get_servo_angles(gesture, x, y, width, height, last_gripper_angle):
    """
    Input: gesture, tọa độ x,y, kích thước khung hình
    Output: 4 góc servo (base, shoulder, elbow, gripper)
    """
    
    # --- 1. Base (Xoay ngang) ---
    # Map x (0 -> width) sang góc (ví dụ 160 -> 20)
    # Lưu ý: Nếu robot quay ngược chiều tay, đảo vị trí 160 và 20
    base = map_range(x, 0, width, 160, 20)
    
    # --- 2. Shoulder (Vươn xa/gần hoặc lên/xuống) ---
    # Map y (0 -> height) sang góc (ví dụ 140 -> 40)
    # Giả định: Y=0 (cao nhất) -> Góc nhỏ (vươn cao) hoặc ngược lại tùy cơ khí
    shoulder = map_range(y, 0, height, 140, 40)
    
    # --- 3. Elbow (Khuỷu) ---
    # Thường để giữ song song hoặc bù trừ cho shoulder
    # Công thức đơn giản: Nghịch đảo của shoulder để tay vươn ra tự nhiên
    elbow = 180 - shoulder
    
    # --- 4. Gripper (Kẹp) ---
    target_gripper = last_gripper_angle
    
    if gesture == "open":
        target_gripper = 160 # Mở rộng
    elif gesture == "close":
        target_gripper = 20  # Đóng chặt
    elif gesture == "pinch":
        target_gripper = 60  # Kẹp vừa (nhón)
    # Nếu là 'idle' hoặc 'No Hand' thì giữ nguyên giá trị cũ
    
    return int(base), int(shoulder), int(elbow), int(target_gripper)
