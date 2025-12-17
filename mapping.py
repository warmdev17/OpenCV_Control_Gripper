def map_range(x, in_min, in_max, out_min, out_max):
    if (in_max - in_min) == 0: return out_min
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def get_servo_angles(gesture, x, y, width, height, last_gripper):
    # Base: Xoay ngang
    base = map_range(x, 0, width, 160, 20)
    
    # Shoulder: Vươn vai
    shoulder = map_range(y, 0, height, 140, 40)
    
    # Elbow: Khuỷu tay (nghịch đảo vai)
    elbow = 180 - shoulder
    
    # Gripper: Kẹp
    target_gripper = last_gripper
    if gesture == "open": target_gripper = 160
    elif gesture == "close": target_gripper = 20
    elif gesture == "pinch": target_gripper = 60
    
    return int(base), int(shoulder), int(elbow), int(target_gripper)
