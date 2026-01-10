"""
Chat and Guess Number Game - Server
Hoàn thiện backend: multi-client chat, đoán số, điểm và bảng xếp hạng.
"""
import socket
import threading
import json
import random
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

        # Game state (single room)
        self.secret_number = random.randint(1, 100)
        self.scores = {}  # {username: points}
        self.guess_counts = {}  # {username: attempts}

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
                    args=(client_socket, address),
                )
                client_thread.daemon = True
                client_thread.start()

            except Exception as e:
                print(f"[LỖI] Lỗi kết nối: {e}")
                break

    def handle_client(self, client_socket, address):
        """Xử lý từng client trong thread riêng"""
        username = None
        buffer = b""

        try:
            while True:
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
                        # skip malformed messages
                        continue

                    msg_type = message.get('type')

                    if msg_type == 'LOGIN':
                        username = message.get('username')
                        result = self.handle_login(client_socket, username)
                        self.send_to_client(client_socket, result)

                        if result['type'] == 'LOGIN_OK':
                            # Thông báo cho tất cả (ngoại trừ người mới)
                            self.broadcast(
                                {
                                    'type': 'SYSTEM',
                                    'content': f"👋 {username} đã tham gia phòng!",
                                    'timestamp': self.get_timestamp(),
                                },
                                exclude=client_socket,
                            )

                            # Send current ranking to the newly joined user
                            self.send_ranking(client_socket)

                    elif msg_type == 'CHAT':
                        # Broadcast tin nhắn chat
                        self.broadcast(
                            {
                                'type': 'CHAT',
                                'username': username,
                                'content': message.get('content'),
                                'timestamp': self.get_timestamp(),
                            }
                        )

                    elif msg_type == 'GUESS':
                        # Handle guess
                        number = message.get('number')
                        if username is None:
                            self.send_to_client(
                                client_socket,
                                {'type': 'SYSTEM', 'content': 'Bạn phải đăng nhập trước khi đoán số.'},
                            )
                            continue

                        if not isinstance(number, int):
                            self.send_to_client(
                                client_socket,
                                {'type': 'SYSTEM', 'content': 'Số đoán không hợp lệ.'},
                            )
                            continue

                        # increment attempts
                        with self.lock:
                            self.guess_counts[username] = self.guess_counts.get(username, 0) + 1

                        if number < self.secret_number:
                            self.send_to_client(
                                client_socket,
                                {
                                    'type': 'RESULT',
                                    'result': 'LOW',
                                    'timestamp': self.get_timestamp(),
                                },
                            )
                        elif number > self.secret_number:
                            self.send_to_client(
                                client_socket,
                                {
                                    'type': 'RESULT',
                                    'result': 'HIGH',
                                    'timestamp': self.get_timestamp(),
                                },
                            )
                        else:
                            # correct guess
                            with self.lock:
                                self.scores[username] = self.scores.get(username, 0) + max(1, 10 - self.guess_counts.get(username, 0))

                            # notify all
                            self.broadcast(
                                {
                                    'type': 'SYSTEM',
                                    'content': f"🎉 {username} đã đoán đúng số {self.secret_number}!",
                                    'timestamp': self.get_timestamp(),
                                }
                            )

                            # send result to winner
                            self.send_to_client(
                                client_socket,
                                {
                                    'type': 'RESULT',
                                    'result': 'CORRECT',
                                    'timestamp': self.get_timestamp(),
                                },
                            )

                            # update and broadcast ranking
                            self.broadcast_ranking()

                            # start new game
                            with self.lock:
                                self.secret_number = random.randint(1, 100)
                                self.guess_counts = {}

                    elif msg_type == 'DISCONNECT':
                        raise ConnectionResetError()

        except json.JSONDecodeError:
            print(f"[LỖI] Dữ liệu không hợp lệ từ {address}")
        except ConnectionResetError:
            print(f"[NGẮT KẾT NỐI] Client {address} mất kết nối hoặc yêu cầu rời")
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
                    'content': 'Username phải có ít nhất 2 ký tự!',
                }

            # Kiểm tra trùng username
            if username in self.clients.values():
                return {'type': 'LOGIN_FAIL', 'content': 'Username đã được sử dụng!'}

            # Đăng nhập thành công
            self.clients[client_socket] = username
            print(f"[ĐĂNG NHẬP] {username} đã vào phòng")

            # ensure score exists
            self.scores.setdefault(username, 0)

            return {
                'type': 'LOGIN_OK',
                'content': f'Chào mừng {username}!',
                'online_users': list(self.clients.values()),
            }

    def send_to_client(self, client_socket, message: dict):
        """Gửi message đến 1 client (newline-delimited JSON)"""
        try:
            data = (json.dumps(message, ensure_ascii=False) + "\n").encode('utf-8')
            client_socket.sendall(data)
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
            self.broadcast(
                {
                    'type': 'SYSTEM',
                    'content': f"👋 {username} đã rời phòng!",
                    'timestamp': self.get_timestamp(),
                }
            )

    def get_timestamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def get_online_count(self) -> int:
        return len(self.clients)

    def get_sorted_ranking(self):
        with self.lock:
            return sorted(self.scores.items(), key=lambda kv: kv[1], reverse=True)

    def broadcast_ranking(self):
        ranking = self.get_sorted_ranking()
        payload = {'type': 'RANKING', 'ranking': ranking, 'timestamp': self.get_timestamp()}
        self.broadcast(payload)

    def send_ranking(self, client_socket):
        ranking = self.get_sorted_ranking()
        payload = {'type': 'RANKING', 'ranking': ranking, 'timestamp': self.get_timestamp()}
        self.send_to_client(client_socket, payload)


if __name__ == "__main__":
    server = GameServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[SERVER] Đang tắt server...")
