import threading
import tkinter as tk
import json
from datetime import datetime

from gui import RootWindow
from network import NetworkClient


class ChatGuessApp:
    """
    Ứng dụng client chính.
    - Connection -> Login -> Chat
    """

    def __init__(self) -> None:
        self.network = NetworkClient()
        self.root = RootWindow(on_connect=self._on_connect_clicked)

        # Gán callback của network → UI
        self.network.on_connected = self._handle_connected
        self.network.on_disconnected = self._handle_disconnected
        self.network.on_message = self._on_network_message

        self.username: str | None = None
        self._pending_login_username: str | None = None
        self._login_fallback_timer: threading.Timer | None = None

    def _on_connect_clicked(self, host: str, port: int) -> None:
        # Khóa nút để tránh bấm nhiều lần
        self.root.connection_view.connect_button.config(state="disabled")

        def worker():
            try:
                self.network.connect(host, port)
            except OSError as exc:
                # Quay về main thread để show dialog
                self.root.after(
                    0,
                    lambda: self._show_connect_error(
                        f"Không thể kết nối tới server {host}:{port}\nLỗi: {exc}"
                    ),
                )
            finally:
                # Dù thành công hay thất bại cũng mở lại nút
                self.root.after(
                    0,
                    lambda: self.root.connection_view.connect_button.config(
                        state="normal"
                    ),
                )

        threading.Thread(target=worker, daemon=True).start()

    def _handle_connected(self) -> None:
        # Khi kết nối thành công, chuyển sang màn hình login
        self.root.after(0, lambda: self.root.show_login_view(on_login=self._on_login))

    def _on_login(self, username: str) -> None:
        # Gửi message LOGIN tới server
        self._pending_login_username = username
        msg = {
            "type": "LOGIN",
            "username": username,
            "content": "",
            "timestamp": datetime.utcnow().isoformat(),
        }

        try:
            self.network.send_message(msg)
        except OSError:
            # nếu không gửi được, hiện lỗi
            self.root.after(0, lambda: self.root.show_error("Lỗi", "Không thể gửi yêu cầu login."))
            return

        # đặt timeout fallback: nếu server không trả lời trong 3s, cho phép vào chế độ offline/chat local
        def fallback():
            if self._pending_login_username:
                self.root.after(0, lambda: self._proceed_to_chat(self._pending_login_username))
                self._pending_login_username = None

        self._login_fallback_timer = threading.Timer(3.0, fallback)
        self._login_fallback_timer.start()

    def _proceed_to_chat(self, username: str) -> None:
        self.username = username
        self.root.after(0, lambda: self.root.show_chat_view(on_send=self._send_chat_message, username=username))
        # welcome system message
        self.root.after(50, lambda: self.root.chat_view.add_message("System", f"Bạn đã đăng nhập là {username}", system=True))

    def _on_network_message(self, msg: dict) -> None:
        # Runs in network thread; schedule UI updates via root.after
        mtype = msg.get("type")
        if mtype == "LOGIN_OK":
            username = msg.get("username")
            if self._login_fallback_timer:
                self._login_fallback_timer.cancel()
                self._login_fallback_timer = None
            self._pending_login_username = None
            # proceed to chat
            self._proceed_to_chat(username)
        elif mtype == "CHAT":
            username = msg.get("username", "?")
            content = msg.get("content", "")
            ts = msg.get("timestamp")
            self.root.after(0, lambda: self.root.chat_view.add_message(username, content, timestamp=ts))
        elif mtype == "SYSTEM":
            content = msg.get("content", "")
            ts = msg.get("timestamp")
            self.root.after(0, lambda: self.root.chat_view.add_message("System", content, timestamp=ts, system=True))
        # ignore other types for now

    def _send_chat_message(self, text: str) -> None:
        if not self.username:
            self.root.show_error("Lỗi", "Bạn cần đăng nhập trước khi gửi tin nhắn.")
            return
        msg = {
            "type": "CHAT",
            "username": self.username,
            "content": text,
            "timestamp": datetime.utcnow().isoformat(),
        }
        # optimistic update
        now = datetime.now().strftime("%H:%M:%S")
        self.root.chat_view.add_message(self.username, text, timestamp=now)
        try:
            self.network.send_message(msg)
        except OSError:
            # nếu gửi thất bại, thông báo và cho phép retry trong UI
            self.root.after(0, lambda: self.root.chat_view.add_message("System", "Không gửi được tin nhắn (mất kết nối).", system=True))

    def _handle_disconnected(self, reason: str) -> None:
        # show error and revert to connection view
        self.root.after(0, lambda: self.root.show_error("Mất kết nối", reason))
        self.root.after(0, lambda: self.root.show_connection_view())

    def _show_connect_error(self, message: str) -> None:
        self.root.show_error("Kết nối thất bại", message)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = ChatGuessApp()
    app.run()


if __name__ == "__main__":
    main()



