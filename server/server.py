"""
Chat and Guess Number Game - Server
Tuần 1: Setup Server + Multi-threading
"""
import socket
import threading
import json
from datetime import datetime

# Config
HOST = '0.0.0.0'
PORT = 5555
MAX_CLIENTS = 10

class GameServer:
    def __init__(self):
        self.server_socket = None
        self.clients = {}  # {client_socket: username}
        self.lock = threading.Lock()  # Đảm bảo thread-safe
        
    def start(self):
        """Khởi động server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(MAX_CLIENTS)
        
        print(f"[SERVER] Đang chạy tại {HOST}:{PORT}")
        print(f"[SERVER] Chờ kết nối... (Tối đa {MAX_CLIENTS} clients)")
        
        self.accept_connections()
    
    def accept_connections(self):
        """Chấp nhận kết nối từ clients"""
        while True:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"[KẾT NỐI MỚI] {address}")
                
                # Tạo thread mới cho mỗi client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except Exception as e:
                print(f"[LỖI] Lỗi kết nối: {e}")
                break
    
    def handle_client(self, client_socket, address):
        """Xử lý từng client trong thread riêng"""
        username = None
        
        try:
            while True:
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                message = json.loads(data)
                msg_type = message.get('type')
                
                if msg_type == 'LOGIN':
                    username = message.get('username')
                    result = self.handle_login(client_socket, username)
                    self.send_to_client(client_socket, result)
                    
                    if result['type'] == 'LOGIN_OK':
                        # Thông báo cho tất cả
                        self.broadcast({
                            'type': 'SYSTEM',
                            'content': f"👋 {username} đã tham gia phòng!",
                            'timestamp': self.get_timestamp()
                        }, exclude=client_socket)
                
                elif msg_type == 'CHAT':
                    # Broadcast tin nhắn chat
                    self.broadcast({
                        'type': 'CHAT',
                        'username': username,
                        'content': message.get('content'),
                        'timestamp': self.get_timestamp()
                    })
                
                elif msg_type == 'GUESS':
                    # TODO: Tuần 2 - Xử lý đoán số
                    self.send_to_client(client_socket, {
                        'type': 'SYSTEM',
                        'content': '[Chức năng đoán số sẽ hoàn thành ở Tuần 2]'
                    })
                
                elif msg_type == 'DISCONNECT':
                    break
                    
        except json.JSONDecodeError:
            print(f"[LỖI] Dữ liệu không hợp lệ từ {address}")
        except ConnectionResetError:
            print(f"[NGẮT KẾT NỐI] Client {address} mất kết nối đột ngột")
        except Exception as e:
            print(f"[LỖI] {address}: {e}")
        finally:
            self.disconnect_client(client_socket, username)
    
    def handle_login(self, client_socket, username) -> dict:
        """Xử lý đăng nhập"""
        with self.lock:
            # Kiểm tra username hợp lệ
            if not username or len(username) < 2:
                return {
                    'type': 'LOGIN_FAIL',
                    'content': 'Username phải có ít nhất 2 ký tự!'
                }
            
            # Kiểm tra trùng username
            if username in self.clients.values():
                return {
                    'type': 'LOGIN_FAIL', 
                    'content': 'Username đã được sử dụng!'
                }
            
            # Đăng nhập thành công
            self.clients[client_socket] = username
            print(f"[ĐĂNG NHẬP] {username} đã vào phòng")
            
            return {
                'type': 'LOGIN_OK',
                'content': f'Chào mừng {username}!',
                'online_users': list(self.clients.values())
            }
    
    def send_to_client(self, client_socket, message: dict):
        """Gửi message đến 1 client"""
        try:
            data = json.dumps(message, ensure_ascii=False).encode('utf-8')
            client_socket.send(data)
        except Exception as e:
            print(f"[LỖI] Không thể gửi tin nhắn: {e}")
    
    def broadcast(self, message: dict, exclude=None):
        """Gửi message đến tất cả clients"""
        with self.lock:
            for client_socket in list(self.clients.keys()):
                if client_socket != exclude:
                    self.send_to_client(client_socket, message)
    
    def disconnect_client(self, client_socket, username):
        """Xử lý khi client ngắt kết nối"""
        with self.lock:
            if client_socket in self.clients:
                del self.clients[client_socket]
                print(f"[NGẮT KẾT NỐI] {username} đã rời phòng")
                
        try:
            client_socket.close()
        except:
            pass
        
        if username:
            self.broadcast({
                'type': 'SYSTEM',
                'content': f"👋 {username} đã rời phòng!",
                'timestamp': self.get_timestamp()
            })
    
    def get_timestamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")
    
    def get_online_count(self) -> int:
        return len(self.clients)


if __name__ == "__main__":
    server = GameServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[SERVER] Đang tắt server...")
