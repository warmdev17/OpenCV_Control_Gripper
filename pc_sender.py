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
        print("[SERIAL] Đang quét cổng COM...")
        ports = list(serial.tools.list_ports.comports())
        target_port = None
        
        # Windows thường đặt tên cổng là COM3, COM4...
        # Arduino thường có chữ 'Arduino' hoặc 'USB Serial' trong description
        for p in ports:
            desc = p.description.lower()
            print(f"  - Tìm thấy: {p.device} ({p.description})")
            if "arduino" in desc or "serial" in desc or "ch340" in desc:
                target_port = p.device
                break
        
        if target_port:
            try:
                print(f"[SERIAL] Kết nối tới {target_port}...")
                self.serial = serial.Serial(target_port, self.baudrate, timeout=1)
                time.sleep(2) # Đợi Arduino reset
                print("[SERIAL] Đã kết nối!")
                self.simulation_mode = False
            except Exception as e:
                print(f"[SERIAL] Lỗi kết nối: {e}")
                self.simulation_mode = True
        else:
            print("[SERIAL] Không tìm thấy Arduino. Chạy GIẢ LẬP.")
            self.simulation_mode = True

    def send(self, base, shoulder, elbow, gripper):
        cmd = f"B:{base};S:{shoulder};E:{elbow};G:{gripper}\n"
        
        # In log ra màn hình CMD/PowerShell
        print(f"[DATA] >> {cmd.strip()}" + " " * 10, end='\r')

        if self.serial and self.serial.is_open:
            try:
                self.serial.write(cmd.encode('utf-8'))
            except:
                self.serial = None
                self.simulation_mode = True
    
    def close(self):
        if self.serial:
            self.serial.close()
