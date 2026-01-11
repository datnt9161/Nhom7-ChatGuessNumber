"""View chính với Chat + Game - Responsive với Scrollbar"""
import tkinter as tk
from tkinter import ttk
from .styles import setup_base_styles, create_button
from .chat_view import ChatView
from .game_interface import GameInterface


class MainGameView(ttk.Frame):
    def __init__(self, master, on_send_chat, on_guess, on_show_ranking, username: str = None):
        super().__init__(master)
        self.username = username
        self.on_show_ranking = on_show_ranking
        setup_base_styles()
        self._build_widgets(on_send_chat, on_guess, username)

    def _build_widgets(self, on_send_chat, on_guess, username):
        # Outer container với scrollbar
        self.configure(style="Card.TFrame")
        
        # Canvas cho scroll
        self.canvas = tk.Canvas(self, bg="#020617", highlightthickness=0)
        self.v_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        
        # Grid layout cho scrollbars
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Inner frame chứa nội dung
        self.inner_frame = tk.Frame(self.canvas, bg="#020617")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        
        # Kích thước tối thiểu cho nội dung
        self.MIN_WIDTH = 750
        self.MIN_HEIGHT = 500
        
        # === Header ===
        header = tk.Frame(self.inner_frame, bg="#020617")
        header.pack(fill="x", pady=(8, 8), padx=8)

        title_label = tk.Label(
            header, 
            text="🎮 Game Đoán Số", 
            bg="#020617",
            fg="#e5e7eb", 
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(side="left")
        
        ranking_btn = create_button(header, "🏆 Bảng Xếp Hạng", "#eab308", self.on_show_ranking, padx=12, pady=6)
        ranking_btn.pack(side="right")

        # Glow line
        glow = tk.Canvas(self.inner_frame, height=2, bg="#020617", highlightthickness=0, bd=0)
        glow.pack(fill="x", pady=(0, 8), padx=8)
        glow.create_line(0, 1, 2000, 1, fill="#3b82f6")

        # === Main content area ===
        content_frame = tk.Frame(self.inner_frame, bg="#020617")
        content_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        # 2 cột: Chat (trái) + Game (phải)
        content_frame.grid_columnconfigure(0, weight=1, minsize=380)
        content_frame.grid_columnconfigure(1, weight=1, minsize=320)
        content_frame.grid_rowconfigure(0, weight=1, minsize=400)

        # Chat (left)
        chat_frame = tk.Frame(content_frame, bg="#020617")
        chat_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.chat_view = ChatView(chat_frame, on_send=on_send_chat, username=username)
        self.chat_view.pack(fill="both", expand=True)

        # Game (right)
        game_frame = tk.Frame(content_frame, bg="#020617")
        game_frame.grid(row=0, column=1, sticky="nsew")
        self.game_interface = GameInterface(game_frame, on_guess=on_guess, username=username)
        self.game_interface.pack(fill="both", expand=True)

        # Bind events
        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Mouse wheel scroll
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)

    def _on_frame_configure(self, event=None):
        """Cập nhật scroll region khi inner_frame thay đổi"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Điều chỉnh kích thước inner_frame theo canvas"""
        canvas_width = event.width
        canvas_height = event.height
        
        # Nếu canvas nhỏ hơn min, giữ inner_frame ở kích thước min (để scroll)
        # Nếu canvas lớn hơn min, inner_frame mở rộng theo canvas
        new_width = max(canvas_width, self.MIN_WIDTH)
        new_height = max(canvas_height, self.MIN_HEIGHT)
        
        self.canvas.itemconfig(self.canvas_window, width=new_width, height=new_height)
        
        # Hiện/ẩn scrollbar tùy theo cần thiết
        if canvas_width >= self.MIN_WIDTH:
            self.h_scrollbar.grid_remove()
        else:
            self.h_scrollbar.grid()
            
        if canvas_height >= self.MIN_HEIGHT:
            self.v_scrollbar.grid_remove()
        else:
            self.v_scrollbar.grid()

    def _on_mousewheel(self, event):
        """Scroll dọc bằng mouse wheel"""
        if self.v_scrollbar.winfo_ismapped():
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_shift_mousewheel(self, event):
        """Scroll ngang bằng Shift + mouse wheel"""
        if self.h_scrollbar.winfo_ismapped():
            self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def get_chat_view(self):
        return self.chat_view

    def get_game_interface(self):
        return self.game_interface
