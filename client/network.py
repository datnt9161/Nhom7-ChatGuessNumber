import socket
import threading
import json
from typing import Callable, Optional


class NetworkClient:
    """
    Network client that supports sending/receiving JSON messages.
    Messages are newline-delimited JSON objects: each message ended by "\n".
    """

    def __init__(self) -> None:
        self._sock: Optional[socket.socket] = None
        self._connected = False
        self._lock = threading.Lock()

        # Callbacks
        self.on_connected: Optional[Callable[[], None]] = None
        self.on_disconnected: Optional[Callable[[str], None]] = None
        self.on_message: Optional[Callable[[dict], None]] = None

        self._recv_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    @property
    def is_connected(self) -> bool:
        return self._connected

    def connect(self, host: str, port: int, timeout: float = 5.0) -> None:
        with self._lock:
            if self._connected:
                return

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            try:
                sock.connect((host, port))
                # set to blocking mode for recv
                sock.settimeout(None)
            except OSError as exc:
                sock.close()
                raise exc

            self._sock = sock
            self._connected = True
            self._stop_event.clear()

            # Start receiver thread
            self._recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
            self._recv_thread.start()

        if self.on_connected:
            self.on_connected()

    def disconnect(self, reason: str = "Ngắt kết nối") -> None:
        with self._lock:
            if not self._connected:
                return

            self._stop_event.set()
            try:
                if self._sock:
                    self._sock.shutdown(socket.SHUT_RDWR)
                    self._sock.close()
            finally:
                self._sock = None
                self._connected = False

        if self.on_disconnected:
            self.on_disconnected(reason)

    def send_message(self, msg: dict) -> None:
        """
        Send a JSON-serializable message (dict). Appends newline as delimiter.
        """
        data = json.dumps(msg, ensure_ascii=False) + "\n"
        encoded = data.encode("utf-8")
        with self._lock:
            if not self._connected or not self._sock:
                raise OSError("Not connected")
            try:
                self._sock.sendall(encoded)
            except OSError as exc:
                # Treat as disconnect
                self.disconnect(f"Lỗi gửi dữ liệu: {exc}")
                raise

    def _recv_loop(self) -> None:
        """
        Receiver loop that reads from socket and emits parsed JSON messages.
        """
        buffer = b""
        try:
            while not self._stop_event.is_set():
                try:
                    data = self._sock.recv(4096)
                    if not data:
                        # connection closed
                        break
                    buffer += data
                    while b"\n" in buffer:
                        line, buffer = buffer.split(b"\n", 1)
                        if not line:
                            continue
                        try:
                            text = line.decode("utf-8")
                            msg = json.loads(text)
                        except Exception:
                            # skip malformed
                            continue
                        if self.on_message:
                            try:
                                self.on_message(msg)
                            except Exception:
                                # swallow to keep loop alive
                                pass
                except OSError:
                    break
        finally:
            # ensure state updated and notify
            self.disconnect("Server đã ngắt kết nối")



