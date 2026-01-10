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
        self._ranking_data: list = []  # Lưu ranking data để hiển thị

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
        """Tuần 3: Chuyển sang MainGameView với Chat + Game ở giữa"""
        self.username = username
        self.root.after(0, lambda: self.root.show_main_game_view(
            on_send_chat=self._send_chat_message,
            on_guess=self._send_guess_message,
            on_show_ranking=self._show_ranking_view,
            username=username
        ))
        # welcome system message
        self.root.after(50, lambda: self.root.main_game_view.get_chat_view().add_message(
            "System", f"Bạn đã đăng nhập là {username}. Chúc mừng bạn tham gia game!", system=True
        ))

    def _show_ranking_view(self) -> None:
        """Hiển thị trang bảng xếp hạng riêng"""
        self.root.after(0, lambda: self.root.show_ranking_view(
            on_back=self._back_to_main_game,
            ranking_data=self._ranking_data,
            username=self.username
        ))

    def _back_to_main_game(self) -> None:
        """Quay lại màn hình game chính"""
        self.root.after(0, lambda: self.root.show_main_game_view(
            on_send_chat=self._send_chat_message,
            on_guess=self._send_guess_message,
            on_show_ranking=self._show_ranking_view,
            username=self.username
        ))

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
            if hasattr(self.root, 'main_game_view') and self.root.main_game_view:
                self.root.after(0, lambda: self.root.main_game_view.get_chat_view().add_message(
                    username, content, timestamp=ts
                ))
            elif hasattr(self.root, 'chat_view') and self.root.chat_view:
                self.root.after(0, lambda: self.root.chat_view.add_message(username, content, timestamp=ts))
        elif mtype == "SYSTEM":
            content = msg.get("content", "")
            ts = msg.get("timestamp")
            if hasattr(self.root, 'main_game_view') and self.root.main_game_view:
                self.root.after(0, lambda: self.root.main_game_view.get_chat_view().add_message(
                    "System", content, timestamp=ts, system=True
                ))
            elif hasattr(self.root, 'chat_view') and self.root.chat_view:
                self.root.after(0, lambda: self.root.chat_view.add_message("System", content, timestamp=ts, system=True))
        elif mtype == "RESULT":
            # Xử lý kết quả đoán số (HIGH/LOW/CORRECT)
            result = msg.get("result", "")
            message = msg.get("content", "")
            if hasattr(self.root, 'main_game_view') and self.root.main_game_view:
                self.root.after(0, lambda: self.root.main_game_view.get_game_interface().handle_result(result, message))
        elif mtype == "RANKING":
            # Cập nhật bảng xếp hạng - lưu data và cập nhật cả 2 view
            ranking_data = msg.get("ranking", [])
            self._ranking_data = ranking_data
            # Cập nhật ranking view nếu đang hiển thị
            if hasattr(self.root, 'ranking_view') and self.root.ranking_view:
                self.root.after(0, lambda: self.root.ranking_view.update_ranking(ranking_data))
        elif mtype == "NEW_GAME":
            # Bắt đầu game mới
            content = msg.get("content", "Game mới đã bắt đầu!")
            if hasattr(self.root, 'main_game_view') and self.root.main_game_view:
                self.root.after(0, lambda: self.root.main_game_view.get_game_interface().start_new_game())
                self.root.after(100, lambda: self.root.main_game_view.get_chat_view().add_message(
                    "System", content, timestamp=msg.get("timestamp"), system=True
                ))

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
        if hasattr(self.root, 'main_game_view') and self.root.main_game_view:
            self.root.main_game_view.get_chat_view().add_message(self.username, text, timestamp=now)
        elif hasattr(self.root, 'chat_view') and self.root.chat_view:
            self.root.chat_view.add_message(self.username, text, timestamp=now)
        try:
            self.network.send_message(msg)
        except OSError:
            # nếu gửi thất bại, thông báo và cho phép retry trong UI
            if hasattr(self.root, 'main_game_view') and self.root.main_game_view:
                self.root.after(0, lambda: self.root.main_game_view.get_chat_view().add_message(
                    "System", "Không gửi được tin nhắn (mất kết nối).", system=True
                ))
            elif hasattr(self.root, 'chat_view') and self.root.chat_view:
                self.root.after(0, lambda: self.root.chat_view.add_message("System", "Không gửi được tin nhắn (mất kết nối).", system=True))

    def _send_guess_message(self, guess: int) -> None:
        """Gửi số đoán tới server (tuần 3)"""
        if not self.username:
            self.root.show_error("Lỗi", "Bạn cần đăng nhập trước khi chơi game.")
            return
        msg = {
            "type": "GUESS",
            "username": self.username,
            "content": str(guess),
            "timestamp": datetime.utcnow().isoformat(),
        }
        try:
            self.network.send_message(msg)
        except OSError:
            # nếu gửi thất bại, thông báo
            if hasattr(self.root, 'main_game_view') and self.root.main_game_view:
                self.root.after(0, lambda: self.root.main_game_view.get_chat_view().add_message(
                    "System", "Không gửi được số đoán (mất kết nối).", system=True
                ))
                self.root.after(100, lambda: self.root.main_game_view.get_game_interface()._show_result(
                    "Lỗi kết nối! Vui lòng kiểm tra lại.", "#ef4444"
                ))

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



