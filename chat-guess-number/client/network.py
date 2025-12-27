import socket
import threading
from typing import Callable, Optional


class NetworkClient:
    """
    Module kết nối tuần 1:
    - Chỉ tập trung vào mở / đóng kết nối TCP tới server (IP, Port).
    - Sẵn sàng mở rộng cho login, chat, game ở các tuần sau.
    """

    def __init__(self) -> None:
        self._sock: Optional[socket.socket] = None
        self._connected = False
        self._lock = threading.Lock()

        # Callback thông báo trạng thái/ lỗi cho UI
        self.on_connected: Optional[Callable[[], None]] = None
        self.on_disconnected: Optional[Callable[[str], None]] = None

    @property
    def is_connected(self) -> bool:
        return self._connected

    def connect(self, host: str, port: int, timeout: float = 5.0) -> None:
        """
        Kết nối tới server. Gọi hàm này từ thread khác nếu sợ block UI.
        """
        with self._lock:
            if self._connected:
                return

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            try:
                sock.connect((host, port))
            except OSError as exc:
                sock.close()
                raise exc

            self._sock = sock
            self._connected = True

        if self.on_connected:
            self.on_connected()

    def disconnect(self, reason: str = "Ngắt kết nối") -> None:
        with self._lock:
            if not self._connected:
                return

            try:
                if self._sock:
                    self._sock.close()
            finally:
                self._sock = None
                self._connected = False

        if self.on_disconnected:
            self.on_disconnected(reason)



