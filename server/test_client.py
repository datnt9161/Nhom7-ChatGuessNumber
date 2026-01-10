"""
Test Client - Dùng để test server trong Tuần 1
Chạy: python test_client.py
"""
import socket
import json
import threading

HOST = '127.0.0.1'
PORT = 5555

def receive_messages(client_socket):
    """Thread nhận tin nhắn từ server"""
    buffer = b""
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            buffer += data
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                if not line:
                    continue
                try:
                    message = json.loads(line.decode('utf-8'))
                except Exception:
                    continue
                print(f"\n[SERVER] {message}")
                print(">> ", end="", flush=True)
        except:
            break

def send_message(client_socket, msg_type, **kwargs):
    """Gửi message đến server"""
    message = {"type": msg_type, **kwargs}
    data = (json.dumps(message, ensure_ascii=False) + "\n").encode('utf-8')
    client_socket.sendall(data)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((HOST, PORT))
        print(f"[CONNECTED] Đã kết nối đến {HOST}:{PORT}")
        
        # Đăng nhập
        username = input("Nhập username: ")
        send_message(client, "LOGIN", username=username)
        
        # Thread nhận tin nhắn
        recv_thread = threading.Thread(target=receive_messages, args=(client,))
        recv_thread.daemon = True
        recv_thread.start()
        
        print("\nCác lệnh:")
        print("  /chat <tin nhắn>  - Gửi tin nhắn")
        print("  /guess <số>       - Đoán số (Tuần 2)")
        print("  /quit             - Thoát")
        print("-" * 40)
        
        while True:
            msg = input(">> ")
            
            if msg.startswith("/chat "):
                content = msg[6:]
                send_message(client, "CHAT", content=content)
            elif msg.startswith("/guess "):
                number = msg[7:]
                send_message(client, "GUESS", number=int(number))
            elif msg == "/quit":
                send_message(client, "DISCONNECT")
                break
            else:
                print("Lệnh không hợp lệ!")
                
    except ConnectionRefusedError:
        print("[LỖI] Không thể kết nối đến server!")
    except Exception as e:
        print(f"[LỖI] {e}")
    finally:
        client.close()
        print("[DISCONNECTED] Đã ngắt kết nối")

if __name__ == "__main__":
    main()
