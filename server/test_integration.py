#!/usr/bin/env python3
"""
Integration Test cho Chat and Guess Number Game
Tuần 4: Test kết nối server-client, chat, game logic
"""
import socket
import json
import threading
import time
import sys
from datetime import datetime


class TestClient:
    """Test client để kiểm tra server"""
    
    def __init__(self, name: str, host: str = "127.0.0.1", port: int = 5555):
        self.name = name
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.messages = []
        self.results = []
        
    def connect(self):
        """Kết nối tới server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"✅ {self.name}: Kết nối thành công")
            
            # Start receiver thread
            threading.Thread(target=self._receive_loop, daemon=True).start()
            return True
        except Exception as e:
            print(f"❌ {self.name}: Lỗi kết nối - {e}")
            return False
    
    def _receive_loop(self):
        """Nhận tin nhắn từ server"""
        buffer = b""
        try:
            while self.connected:
                data = self.socket.recv(4096)
                if not data:
                    break
                buffer += data
                
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    if not line:
                        continue
                    try:
                        message = json.loads(line.decode('utf-8'))
                        self.messages.append(message)
                        self._handle_message(message)
                    except:
                        continue
        except:
            pass
        finally:
            self.connected = False
    
    def _handle_message(self, msg):
        """Xử lý tin nhắn nhận được"""
        msg_type = msg.get('type')
        if msg_type == 'LOGIN_OK':
            print(f"✅ {self.name}: Đăng nhập thành công")
        elif msg_type == 'CHAT':
            username = msg.get('username', '?')
            content = msg.get('content', '')
            print(f"💬 {self.name} nhận chat từ {username}: {content}")
        elif msg_type == 'RESULT':
            result = msg.get('result')
            self.results.append(result)
            print(f"🎯 {self.name}: Kết quả đoán - {result}")
        elif msg_type == 'SYSTEM':
            content = msg.get('content', '')
            print(f"📢 {self.name} nhận system: {content}")
        elif msg_type == 'RANKING':
            ranking = msg.get('ranking', [])
            print(f"🏆 {self.name}: Cập nhật ranking - {len(ranking)} người chơi")
    
    def send_message(self, msg_dict):
        """Gửi tin nhắn tới server"""
        if not self.connected:
            return False
        try:
            data = (json.dumps(msg_dict, ensure_ascii=False) + "\n").encode('utf-8')
            self.socket.sendall(data)
            return True
        except Exception as e:
            print(f"❌ {self.name}: Lỗi gửi tin nhắn - {e}")
            return False
    
    def login(self, username):
        """Đăng nhập với username"""
        msg = {
            "type": "LOGIN",
            "username": username,
            "content": "",
            "timestamp": datetime.utcnow().isoformat()
        }
        return self.send_message(msg)
    
    def send_chat(self, content):
        """Gửi tin nhắn chat"""
        msg = {
            "type": "CHAT",
            "username": self.name,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }
        return self.send_message(msg)
    
    def guess_number(self, number):
        """Đoán số"""
        msg = {
            "type": "GUESS",
            "username": self.name,
            "number": number,
            "timestamp": datetime.utcnow().isoformat()
        }
        return self.send_message(msg)
    
    def disconnect(self):
        """Ngắt kết nối"""
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass


def test_basic_connection():
    """Test 1: Kết nối cơ bản"""
    print("\n🧪 TEST 1: Kết nối cơ bản")
    print("-" * 40)
    
    client = TestClient("TestClient1")
    success = client.connect()
    
    if success:
        time.sleep(0.5)
        client.disconnect()
        print("✅ Test kết nối: PASS")
        return True
    else:
        print("❌ Test kết nối: FAIL")
        return False


def test_login_system():
    """Test 2: Hệ thống đăng nhập"""
    print("\n🧪 TEST 2: Hệ thống đăng nhập")
    print("-" * 40)
    
    client1 = TestClient("TestClient1")
    client2 = TestClient("TestClient2")
    
    if not client1.connect() or not client2.connect():
        print("❌ Test login: FAIL - Không kết nối được")
        return False
    
    # Test đăng nhập thành công
    client1.login("Player1")
    time.sleep(0.5)
    
    # Test đăng nhập trùng username
    client2.login("Player1")
    time.sleep(0.5)
    
    # Test đăng nhập username khác
    client2.login("Player2")
    time.sleep(1)
    
    client1.disconnect()
    client2.disconnect()
    
    print("✅ Test login: PASS")
    return True


def test_chat_system():
    """Test 3: Hệ thống chat"""
    print("\n🧪 TEST 3: Hệ thống chat")
    print("-" * 40)
    
    client1 = TestClient("Player1")
    client2 = TestClient("Player2")
    
    if not client1.connect() or not client2.connect():
        print("❌ Test chat: FAIL - Không kết nối được")
        return False
    
    # Đăng nhập
    client1.login("Player1")
    client2.login("Player2")
    time.sleep(1)
    
    # Gửi tin nhắn
    client1.send_chat("Hello from Player1!")
    time.sleep(0.5)
    client2.send_chat("Hi Player1, this is Player2!")
    time.sleep(1)
    
    client1.disconnect()
    client2.disconnect()
    
    print("✅ Test chat: PASS")
    return True


def test_game_logic():
    """Test 4: Logic game đoán số"""
    print("\n🧪 TEST 4: Logic game đoán số")
    print("-" * 40)
    
    client = TestClient("GameTester")
    
    if not client.connect():
        print("❌ Test game: FAIL - Không kết nối được")
        return False
    
    # Đăng nhập
    client.login("GameTester")
    time.sleep(0.5)
    
    # Test đoán số (binary search để tìm nhanh)
    low, high = 1, 100
    attempts = 0
    max_attempts = 10
    
    print(f"🎯 Bắt đầu đoán số từ {low} đến {high}")
    
    while low <= high and attempts < max_attempts:
        guess = (low + high) // 2
        client.guess_number(guess)
        attempts += 1
        
        # Đợi kết quả
        time.sleep(0.5)
        
        if client.results:
            result = client.results[-1]
            print(f"   Lần {attempts}: Đoán {guess} → {result}")
            
            if result == "CORRECT":
                print(f"🎉 Đoán đúng sau {attempts} lần!")
                break
            elif result == "HIGH":
                high = guess - 1
            elif result == "LOW":
                low = guess + 1
        else:
            print(f"   Lần {attempts}: Đoán {guess} → Không nhận được kết quả")
    
    client.disconnect()
    
    if attempts <= max_attempts and client.results and client.results[-1] == "CORRECT":
        print("✅ Test game logic: PASS")
        return True
    else:
        print("❌ Test game logic: FAIL")
        return False


def test_multi_client():
    """Test 5: Nhiều client đồng thời"""
    print("\n🧪 TEST 5: Nhiều client đồng thời")
    print("-" * 40)
    
    clients = []
    num_clients = 5
    
    # Tạo và kết nối nhiều client
    for i in range(num_clients):
        client = TestClient(f"Player{i+1}")
        if client.connect():
            client.login(f"Player{i+1}")
            clients.append(client)
        else:
            print(f"❌ Không thể kết nối client {i+1}")
    
    print(f"✅ Đã kết nối {len(clients)}/{num_clients} clients")
    
    time.sleep(1)
    
    # Test chat đồng thời
    for i, client in enumerate(clients):
        client.send_chat(f"Message from {client.name}")
        time.sleep(0.1)
    
    time.sleep(2)
    
    # Ngắt kết nối tất cả
    for client in clients:
        client.disconnect()
    
    if len(clients) >= 3:  # Ít nhất 3 client kết nối được
        print("✅ Test multi-client: PASS")
        return True
    else:
        print("❌ Test multi-client: FAIL")
        return False


def run_all_tests():
    """Chạy tất cả test cases"""
    print("🚀 BẮT ĐẦU INTEGRATION TESTING")
    print("=" * 50)
    
    tests = [
        ("Kết nối cơ bản", test_basic_connection),
        ("Hệ thống đăng nhập", test_login_system),
        ("Hệ thống chat", test_chat_system),
        ("Logic game đoán số", test_game_logic),
        ("Nhiều client đồng thời", test_multi_client),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}: FAIL - Exception: {e}")
            results.append((test_name, False))
        
        time.sleep(1)  # Nghỉ giữa các test
    
    # Tổng kết
    print("\n📊 KẾT QUẢ TESTING")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print("-" * 50)
    print(f"Tổng kết: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 TẤT CẢ TESTS ĐỀU PASS!")
        return True
    else:
        print("⚠️  CÓ MỘT SỐ TESTS FAIL!")
        return False


if __name__ == "__main__":
    print("Chat and Guess Number Game - Integration Testing")
    print("Đảm bảo server đang chạy trước khi test!")
    print()
    
    # Kiểm tra server có chạy không
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(2)
        test_socket.connect(("127.0.0.1", 5555))
        test_socket.close()
        print("✅ Server đang chạy, bắt đầu testing...")
    except:
        print("❌ Server không chạy! Vui lòng khởi động server trước.")
        print("   Chạy: python server/server.py")
        sys.exit(1)
    
    success = run_all_tests()
    sys.exit(0 if success else 1)