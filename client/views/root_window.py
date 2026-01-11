"""Cửa sổ chính của ứng dụng"""
import tkinter as tk
from tkinter import ttk, messagebox
from .connection_view import ConnectionView
from .login_view import LoginView
from .chat_view import ChatView
from .main_game_view import MainGameView
from .ranking_view import RankingView


class RootWindow(tk.Tk):
    def __init__(self, on_connect):
        super().__init__()
        self.title("Game Đoán Số – Client")
        self.geometry("900x650")
        self.minsize(400, 300)  # Cho phép thu nhỏ hơn
        self.main_game_view = None
        self.ranking_view = None
        self.chat_view = None
        self.login_view = None
        self._is_game_view = False  # Track nếu đang ở game view

        # Background gradient
        self._bg_canvas = tk.Canvas(self, highlightthickness=0, bd=0)
        self._bg_canvas.pack(fill="both", expand=True)
        self.bind("<Configure>", self._draw_gradient)

        # Main frame - sẽ được cấu hình khác nhau tùy view
        self._main_frame = ttk.Frame(self._bg_canvas, padding=12)
        self._container_window = self._bg_canvas.create_window(0, 0, anchor="center", window=self._main_frame)

        def _update_layout(event=None):
            w, h = self._bg_canvas.winfo_width(), self._bg_canvas.winfo_height()
            if self._is_game_view:
                # Game view: fill toàn bộ canvas
                self._bg_canvas.coords(self._container_window, 0, 0)
                self._bg_canvas.itemconfig(self._container_window, anchor="nw", width=w, height=h)
            else:
                # Các view khác: center
                self._bg_canvas.coords(self._container_window, w/2, h/2)
                self._bg_canvas.itemconfig(self._container_window, anchor="center", width=0, height=0)
        
        self._update_layout_func = _update_layout
        self._bg_canvas.bind("<Configure>", _update_layout)

        self._on_connect_callback = on_connect
        self._current_username = None

        # Start with connection view
        self.connection_view = ConnectionView(self._main_frame, on_connect=on_connect)
        self.connection_view.pack(fill="both", expand=True)

    def _draw_gradient(self, event=None):
        self._bg_canvas.delete("gradient")
        w, h = self.winfo_width(), self.winfo_height()
        for i in range(50):
            r = int(2 + 13 * (i/50))
            g = int(6 + 17 * (i/50))
            b = int(23 + 19 * (i/50))
            color = f"#{r:02x}{g:02x}{b:02x}"
            y0, y1 = int(h*i/50), int(h*(i+1)/50)
            self._bg_canvas.create_rectangle(0, y0, w, y1, outline="", fill=color, tags="gradient")

    def _clear_views(self):
        for child in list(self._main_frame.winfo_children()):
            child.pack_forget()

    def show_login_view(self, on_login):
        self._clear_views()
        self._is_game_view = False
        self.login_view = LoginView(self._main_frame, on_login=on_login)
        self.login_view.pack(fill="both", expand=True)
        self.after(10, self._update_layout_func)

    def show_chat_view(self, on_send, username: str = None):
        self._clear_views()
        self._is_game_view = False
        self._current_username = username
        self.chat_view = ChatView(self._main_frame, on_send=on_send, username=username)
        self.chat_view.pack(fill="both", expand=True)
        self.after(10, self._update_layout_func)

    def show_main_game_view(self, on_send_chat, on_guess, on_show_ranking, username: str = None):
        self._clear_views()
        self._is_game_view = True  # Bật chế độ game view
        self._current_username = username
        # Responsive: lấy kích thước màn hình
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        # Đặt kích thước 80% màn hình, tối thiểu 900x600
        win_w = max(900, int(screen_w * 0.75))
        win_h = max(600, int(screen_h * 0.8))
        self.geometry(f"{win_w}x{win_h}")
        self.minsize(400, 300)  # Cho phép thu nhỏ
        self.main_game_view = MainGameView(self._main_frame, on_send_chat=on_send_chat, on_guess=on_guess, on_show_ranking=on_show_ranking, username=username)
        self.main_game_view.pack(fill="both", expand=True)
        # Cập nhật layout ngay
        self.after(10, self._update_layout_func)

    def show_ranking_view(self, on_back, ranking_data: list = None, username: str = None):
        self._clear_views()
        self._is_game_view = False  # Tắt chế độ game view
        self._current_username = username
        self.geometry("1000x700")
        self.minsize(400, 300)
        self.ranking_view = RankingView(self._main_frame, on_back=on_back, username=username)
        self.ranking_view.pack(fill="both", expand=True)
        if ranking_data:
            self.ranking_view.update_ranking(ranking_data)
        self.after(10, self._update_layout_func)

    def show_connection_view(self):
        self._clear_views()
        self._is_game_view = False
        self._current_username = None
        self.connection_view = ConnectionView(self._main_frame, on_connect=self._on_connect_callback)
        self.connection_view.pack(fill="both", expand=True)
        self.after(10, self._update_layout_func)

    def show_info(self, title: str, message: str):
        messagebox.showinfo(title, message)

    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message)
