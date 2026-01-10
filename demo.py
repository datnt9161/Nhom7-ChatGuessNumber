#!/usr/bin/env python3
"""
Demo Script cho Chat and Guess Number Game
Tuần 4: Tự động demo các tính năng chính
"""
import subprocess
import time
import sys
import os
import threading
from pathlib import Path


class GameDemo:
    """Class quản lý demo game"""
    
    def __init__(self):
        self.server_process = None
        self.client_processes = []
        
    def start_server(self):
        """Khởi động server"""
        print("🚀 Đang khởi động server...")
        try:
            self.server_process = subprocess.Popen(
                [sys.executable, "server/server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            time.sleep(2)  # Đợi server khởi động
            
            if self.server_process.poll() is None:
                print("✅ Server đã khởi động thành công!")
                return True
            else:
                print("❌ Server không khởi động được!")
                return False
        except Exception as e:
            print(f"❌ Lỗi khởi động server: {e}")
            return False
    
    def start_client(self, client_name="Client"):
        """Khởi động client GUI"""
        print(f"🖥️  Đang khởi động {client_name}...")
        try:
            client_process = subprocess.Popen(
                [sys.executable, "chat-guess-number/client/client.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.client_processes.append(client_process)
            print(f"✅ {client_name} đã khởi động!")
            return client_process
        except Exception as e:
            print(f"❌ Lỗi khởi động {client_name}: {e}")
            return None
    
    def run_integration_test(self):
        """Chạy integration test"""
        print("🧪 Đang chạy integration test...")
        try:
            result = subprocess.run(
                [sys.executable, "server/test_integration.py"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            print("📊 KẾT QUẢ INTEGRATION TEST:")
            print("-" * 40)
            print(result.stdout)
            
            if result.stderr:
                print("⚠️  STDERR:")
                print(result.stderr)
            
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print("❌ Integration test timeout!")
            return False
        except Exception as e:
            print(f"❌ Lỗi chạy integration test: {e}")
            return False
    
    def cleanup(self):
        """Dọn dẹp các process"""
        print("\n🧹 Đang dọn dẹp...")
        
        # Tắt client processes
        for client_process in self.client_processes:
            try:
                client_process.terminate()
                client_process.wait(timeout=5)
            except:
                try:
                    client_process.kill()
                except:
                    pass
        
        # Tắt server process
        if self.server_process:
            try:
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
            except:
                try:
                    self.server_process.kill()
                except:
                    pass
        
        print("✅ Dọn dẹp hoàn tất!")
    
    def show_menu(self):
        """Hiển thị menu demo"""
        print("\n" + "="*50)
        print("🎮 CHAT AND GUESS NUMBER GAME - DEMO")
        print("="*50)
        print("1. 🚀 Demo đầy đủ (Server + 2 Clients)")
        print("2. 🧪 Chạy Integration Test")
        print("3. 🖥️  Chỉ khởi động Server")
        print("4. 👥 Chỉ khởi động Client")
        print("5. 📖 Hướng dẫn sử dụng")
        print("6. ❌ Thoát")
        print("-"*50)
    
    def show_instructions(self):
        """Hiển thị hướng dẫn sử dụng"""
        print("\n📖 HƯỚNG DẪN SỬ DỤNG")
        print("="*50)
        print("""
🎯 CÁCH CHƠI:
1. Khởi động server trước
2. Mở client và kết nối tới server (127.0.0.1:5555)
3. Đăng nhập với username
4. Chat với người chơi khác
5. Đoán số từ 1-100
6. Xem bảng xếp hạng

🔧 CHẠY THỦ CÔNG:
• Server: python server/server.py
• Client: python chat-guess-number/client/client.py
• Test: python server/test_integration.py

🎮 TÍNH NĂNG:
✅ Multi-client chat real-time
✅ Game đoán số với gợi ý HIGH/LOW/CORRECT
✅ Bảng xếp hạng theo điểm
✅ Giao diện đẹp với dark theme
✅ Tự động bắt đầu game mới sau khi có người thắng

🏆 ĐIỂM SỐ:
• Đoán đúng = 10 - số lần đoán (tối thiểu 1 điểm)
• Càng ít lần đoán, càng nhiều điểm
        """)
    
    def run_full_demo(self):
        """Demo đầy đủ với server + 2 clients"""
        print("\n🚀 DEMO ĐẦY ĐỦ")
        print("="*30)
        
        # Khởi động server
        if not self.start_server():
            return False
        
        print("\n⏳ Đợi 3 giây để server ổn định...")
        time.sleep(3)
        
        # Khởi động 2 clients
        client1 = self.start_client("Client 1")
        time.sleep(1)
        client2 = self.start_client("Client 2")
        
        if client1 and client2:
            print("\n🎉 Demo đã sẵn sàng!")
            print("📝 HƯỚNG DẪN:")
            print("1. Trong mỗi client, nhập IP: 127.0.0.1, Port: 5555")
            print("2. Đăng nhập với username khác nhau")
            print("3. Thử chat và đoán số!")
            print("4. Nhấn Enter để tắt demo...")
            
            input()  # Đợi user nhấn Enter
            return True
        else:
            print("❌ Không thể khởi động clients!")
            return False


def main():
    """Hàm main"""
    demo = GameDemo()
    
    try:
        while True:
            demo.show_menu()
            choice = input("Chọn tùy chọn (1-6): ").strip()
            
            if choice == "1":
                demo.run_full_demo()
            
            elif choice == "2":
                if demo.start_server():
                    time.sleep(2)
                    demo.run_integration_test()
                else:
                    print("❌ Không thể khởi động server để test!")
            
            elif choice == "3":
                if demo.start_server():
                    print("✅ Server đang chạy. Nhấn Enter để tắt...")
                    input()
                
            elif choice == "4":
                demo.start_client("Manual Client")
                print("✅ Client đã khởi động. Nhấn Enter để tiếp tục...")
                input()
            
            elif choice == "5":
                demo.show_instructions()
                input("\nNhấn Enter để quay lại menu...")
            
            elif choice == "6":
                print("👋 Tạm biệt!")
                break
            
            else:
                print("❌ Lựa chọn không hợp lệ!")
            
            demo.cleanup()
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Nhận Ctrl+C, đang thoát...")
    
    finally:
        demo.cleanup()


if __name__ == "__main__":
    # Kiểm tra các file cần thiết
    required_files = [
        "server/server.py",
        "chat-guess-number/client/client.py",
        "server/test_integration.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Thiếu các file sau:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\nVui lòng đảm bảo cấu trúc thư mục đúng!")
        sys.exit(1)
    
    main()