import serial
import serial.tools.list_ports
import time

class PCSender:
    def __init__(self, baudrate=115200):
        self.serial = None
        self.baudrate = baudrate
        self.simulation_mode = False
        self.connect()

    def connect(self):
        print("[SERIAL] Đang quét thiết bị...")
        ports = list(serial.tools.list_ports.comports())
        target_port = None
        
        # Tìm Arduino hoặc CH340
        for p in ports:
            if "Arduino" in p.description or "CH340" in p.description or "ttyUSB" in p.device or "ttyACM" in p.device:
                target_port = p.device
                break
        
        # Nếu có thiết bị thì kết nối
        if target_port:
            try:
                print(f"[SERIAL] Tìm thấy thiết bị tại {target_port}. Đang kết nối...")
                self.serial = serial.Serial(target_port, self.baudrate, timeout=1)
                time.sleep(2) 
                print("[SERIAL] Đã kết nối thành công!")
                self.simulation_mode = False
            except Exception as e:
                print(f"[SERIAL] Lỗi kết nối: {e}. Chuyển sang chế độ GIẢ LẬP.")
                self.serial = None
                self.simulation_mode = True
        else:
            # Không có thiết bị -> Chế độ giả lập
            print("[SERIAL] Không tìm thấy Arduino. Đang chạy chế độ GIẢ LẬP (Simulation Mode).")
            print("[SERIAL] Các lệnh sẽ được in ra màn hình thay vì gửi đi.")
            self.simulation_mode = True

    def send(self, base, shoulder, elbow, gripper):
        # Format lệnh: B:xx;S:xx;E:xx;G:xx
        cmd = f"B:{base};S:{shoulder};E:{elbow};G:{gripper}\n"
        
        # --- LOGGING TÍN HIỆU ---
        # Dòng này sẽ in tín hiệu ra console để bạn debug
        # end='\r' giúp dòng chữ cập nhật tại chỗ
        print(f"[DATA] >> {cmd.strip()}" + " " * 10, end='\r')

        if self.serial and self.serial.is_open:
            try:
                self.serial.write(cmd.encode('utf-8'))
            except Exception:
                print("\n[SERIAL] Mất kết nối! Chuyển sang chế độ GIẢ LẬP.")
                self.serial = None
                self.simulation_mode = True
        
        elif self.simulation_mode:
            # Trong chế độ giả lập, chỉ cần in log là đủ
            pass
    
    def close(self):
        if self.serial:
            self.serial.close()
