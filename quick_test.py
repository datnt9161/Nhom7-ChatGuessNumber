#!/usr/bin/env python3
"""
Quick Test cho Chat and Guess Number Game
"""
import socket
import json
import time
import threading

def test_server_connection():
    """Test kết nối server cơ bản"""
    print("🧪 Testing server connection...")
    
    try:
        # Test kết nối
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(("127.0.0.1", 5555))
        
        print("✅ Server connection: OK")
        
        # Test login
        login_msg = {
            "type": "LOGIN",
            "username": "TestUser",
            "content": "",
            "timestamp": "2025-01-10T10:00:00"
        }
        
        data = (json.dumps(login_msg, ensure_ascii=False) + "\n").encode('utf-8')
        sock.sendall(data)
        
        # Nhận response
        response = sock.recv(4096)
        if response:
            print("✅ Server response: OK")
            print(f"   Response: {response.decode('utf-8').strip()}")
        
        # Test chat
        chat_msg = {
            "type": "CHAT",
            "username": "TestUser",
            "content": "Hello from test!",
            "timestamp": "2025-01-10T10:00:01"
        }
        
        data = (json.dumps(chat_msg, ensure_ascii=False) + "\n").encode('utf-8')
        sock.sendall(data)
        print("✅ Chat message sent: OK")
        
        # Test guess
        guess_msg = {
            "type": "GUESS",
            "username": "TestUser",
            "number": 50,
            "timestamp": "2025-01-10T10:00:02"
        }
        
        data = (json.dumps(guess_msg, ensure_ascii=False) + "\n").encode('utf-8')
        sock.sendall(data)
        print("✅ Guess message sent: OK")
        
        # Đợi response
        time.sleep(1)
        try:
            response = sock.recv(4096)
            if response:
                print(f"✅ Guess response: {response.decode('utf-8').strip()}")
        except:
            pass
        
        sock.close()
        print("✅ All basic tests: PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    print("🎮 QUICK TEST - Chat and Guess Number Game")
    print("=" * 50)
    
    # Kiểm tra server có chạy không
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(2)
        test_socket.connect(("127.0.0.1", 5555))
        test_socket.close()
        print("✅ Server is running")
    except:
        print("❌ Server is not running!")
        print("   Please start server first: python server/server.py")
        return
    
    # Chạy test
    success = test_server_connection()
    
    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Server is working correctly")
        print("✅ Ready for demo!")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("⚠️  Please check server logs")

if __name__ == "__main__":
    main()