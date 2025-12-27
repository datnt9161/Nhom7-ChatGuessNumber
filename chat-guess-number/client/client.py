import threading
import tkinter as tk

from gui import RootWindow
from network import NetworkClient


class ChatGuessApp:
    """
    Ứng dụng client chính.
    Tuần 1:
    - Khởi động GUI đẹp, dễ nhìn.
    - Cho phép người dùng nhập IP / Port và kết nối tới server.
    - Thông báo kết quả kết nối cho người dùng.
    Các tuần sau sẽ bổ sung Login, Chat, Game, Ranking.
    """

    def __init__(self) -> None:
        self.network = NetworkClient()
        self.root = RootWindow(on_connect=self._on_connect_clicked)

        # Gán callback của network → UI
        self.network.on_connected = self._handle_connected
        self.network.on_disconnected = self._handle_disconnected

    def _on_connect_clicked(self, host: str, port: int) -> None:
        """
        Khi người dùng bấm nút Kết nối trên UI.
        Thực hiện kết nối trong thread riêng để không khóa giao diện.
        """
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
        """
        Được gọi khi kết nối thành công.
        Tuần 1 chỉ hiện thông báo; tuần sau sẽ chuyển màn hình.
        """
        self.root.after(
            0,
            lambda: self.root.show_info(
                "Kết nối thành công",
                "Đã kết nối tới server.\nCác chức năng Login/Chat/Game sẽ được bổ sung ở tuần tiếp theo.",
            ),
        )

    def _handle_disconnected(self, reason: str) -> None:
        self.root.after(0, lambda: self.root.show_error("Mất kết nối", reason))

    def _show_connect_error(self, message: str) -> None:
        self.root.show_error("Kết nối thất bại", message)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = ChatGuessApp()
    app.run()


if __name__ == "__main__":
    main()



