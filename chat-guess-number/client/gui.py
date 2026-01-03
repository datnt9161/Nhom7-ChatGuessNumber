import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from datetime import datetime


class ConnectionView(ttk.Frame):
    """
    Màn hình kết nối tuần 1:
    - Nhập IP / Port
    - Nút Kết nối
    UI được thiết kế hiện đại, dễ nhìn, dùng ttk + style.
    """

    def __init__(self, master, on_connect):
        super().__init__(master, padding=24)
        self.on_connect = on_connect
        self._hover_job = None
        self._build_styles()
        self._build_widgets()

    def _build_styles(self):
        style = ttk.Style()
        # Sử dụng theme mặc định phù hợp hệ điều hành
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")

        # Card chính
        style.configure(
            "Card.TFrame",
            background="#020617",
        )

        # Khung form
        style.configure(
            "Form.TFrame",
            background="#020617",
        )

        # Tiêu đề
        style.configure(
            "Title.TLabel",
            background="#020617",
            foreground="#e5e7eb",
            font=("Segoe UI", 22, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background="#020617",
            foreground="#9ca3af",
            font=("Segoe UI", 10),
        )

        # Label form
        style.configure(
            "FormLabel.TLabel",
            background="#020617",
            foreground="#9ca3af",
            font=("Segoe UI", 9),
        )

        # Entry
        style.configure(
            "Modern.TEntry",
            padding=8,
            relief="flat",
            borderwidth=0,
            fieldbackground="#020617",
            foreground="#e5e7eb",
        )
        style.map(
            "Modern.TEntry",
            fieldbackground=[("focus", "#02081f")],
        )

        # Button
        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8),
            background="#22c55e",
            foreground="#020617",
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#16a34a"), ("pressed", "#15803d")],
            foreground=[("disabled", "#6b7280")],
        )

    def _build_widgets(self):
        self.configure(style="Card.TFrame")

        # Tiêu đề app
        header = ttk.Frame(self, style="Card.TFrame")
        header.pack(fill="x", pady=(0, 16))

        title = ttk.Label(
            header,
            text="Game Đoán Số",
            style="Title.TLabel",
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            header,
            text="Game đoán số multiplayer",
            style="Subtitle.TLabel",
        )
        subtitle.pack(anchor="w", pady=(4, 0))

        # Card form kết nối
        card = ttk.Frame(self, style="Form.TFrame", padding=24)
        card.pack(fill="both", expand=True)

        # IP
        ip_label = ttk.Label(card, text="Server IP", style="FormLabel.TLabel")
        ip_label.grid(row=0, column=0, sticky="w")

        self.ip_var = tk.StringVar(value="127.0.0.1")
        ip_entry = ttk.Entry(
            card,
            textvariable=self.ip_var,
            style="Modern.TEntry",
            width=32,
        )
        ip_entry.grid(row=1, column=0, sticky="we", pady=(4, 12))

        # Port
        port_label = ttk.Label(card, text="Server Port", style="FormLabel.TLabel")
        port_label.grid(row=2, column=0, sticky="w")

        self.port_var = tk.StringVar(value="5000")
        port_entry = ttk.Entry(
            card,
            textvariable=self.port_var,
            style="Modern.TEntry",
            width=32,
        )
        port_entry.grid(row=3, column=0, sticky="we", pady=(4, 16))

        # Gợi ý nhỏ
        hint = ttk.Label(
            card,
            text="Hãy đảm bảo server đã chạy trước khi kết nối.",
            style="FormLabel.TLabel",
        )
        hint.grid(row=4, column=0, sticky="w", pady=(0, 16))

        # Nút kết nối
        self.connect_button = ttk.Button(
            card,
            text="Kết nối tới server",
            style="Primary.TButton",
            command=self._handle_connect_click,
        )
        self.connect_button.grid(row=5, column=0, sticky="we")

        card.columnconfigure(0, weight=1)

    def _handle_connect_click(self):
        ip = self.ip_var.get().strip()
        port_text = self.port_var.get().strip()

        if not ip or not port_text:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ IP và Port.")
            return

        try:
            port = int(port_text)
            if not (0 < port < 65536):
                raise ValueError()
        except ValueError:
            messagebox.showerror("Port không hợp lệ", "Port phải là số trong khoảng 1-65535.")
            return

        # Callback cho client.py xử lý logic kết nối thật
        if self.on_connect:
            self.on_connect(ip, port)


class LoginView(ttk.Frame):
    """
    Màn hình đăng nhập tuần 2:
    - Nhập username
    - Nút Đăng nhập
    UI được thiết kế hiện đại, đẹp mắt với hiệu ứng.
    """

    def __init__(self, master, on_login):
        super().__init__(master, padding=24)
        self.on_login = on_login
        self._hover_job = None
        self._build_styles()
        self._build_widgets()

    def _build_styles(self):
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")

        # Card chính
        style.configure(
            "Card.TFrame",
            background="#020617",
        )

        # Khung form
        style.configure(
            "Form.TFrame",
            background="#020617",
        )

        # Tiêu đề
        style.configure(
            "Title.TLabel",
            background="#020617",
            foreground="#e5e7eb",
            font=("Segoe UI", 22, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background="#020617",
            foreground="#9ca3af",
            font=("Segoe UI", 10),
        )

        # Label form
        style.configure(
            "FormLabel.TLabel",
            background="#020617",
            foreground="#9ca3af",
            font=("Segoe UI", 9),
        )

        # Entry
        style.configure(
            "Modern.TEntry",
            padding=8,
            relief="flat",
            borderwidth=0,
            fieldbackground="#020617",
            foreground="#e5e7eb",
        )
        style.map(
            "Modern.TEntry",
            fieldbackground=[("focus", "#02081f")],
        )

        # Button
        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8),
            background="#22c55e",
            foreground="#020617",
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#16a34a"), ("pressed", "#15803d")],
            foreground=[("disabled", "#6b7280")],
        )

    def _build_widgets(self):
        self.configure(style="Card.TFrame")

        # Tiêu đề app
        header = ttk.Frame(self, style="Card.TFrame")
        header.pack(fill="x", pady=(0, 16))

        title = ttk.Label(
            header,
            text="Đăng nhập",
            style="Title.TLabel",
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            header,
            text="Nhập username để tham gia phòng chơi",
            style="Subtitle.TLabel",
        )
        subtitle.pack(anchor="w", pady=(4, 0))

        # Đường kẻ phát sáng nhẹ dưới header
        glow_line = tk.Canvas(
            self,
            height=2,
            bg="#020617",
            highlightthickness=0,
            bd=0,
        )
        glow_line.pack(fill="x", pady=(0, 8))
        glow_line.create_line(
            0,
            1,
            800,
            1,
            fill="#22c55e",
        )

        # Card form đăng nhập
        card = ttk.Frame(self, style="Form.TFrame", padding=24)
        card.pack(fill="both", expand=True, pady=(8, 0))

        # Username
        username_label = ttk.Label(card, text="Username", style="FormLabel.TLabel")
        username_label.grid(row=0, column=0, sticky="w")

        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(
            card,
            textvariable=self.username_var,
            style="Modern.TEntry",
            width=32,
        )
        username_entry.grid(row=1, column=0, sticky="we", pady=(4, 16))
        username_entry.focus()

        # Hiệu ứng border khi focus
        username_entry.bind("<FocusIn>", self._on_entry_focus_in, add="+")
        username_entry.bind("<FocusOut>", self._on_entry_focus_out, add="+")

        # Gợi ý nhỏ
        hint = ttk.Label(
            card,
            text="Username sẽ hiển thị trong phòng chat và bảng xếp hạng.",
            style="FormLabel.TLabel",
        )
        hint.grid(row=2, column=0, sticky="w", pady=(0, 16))

        # Nút đăng nhập
        self.login_button = ttk.Button(
            card,
            text="Đăng nhập",
            style="Primary.TButton",
            command=self._handle_login_click,
        )
        self.login_button.grid(row=3, column=0, sticky="we")

        # Hover & pulse animation cho nút đăng nhập
        self.login_button.bind("<Enter>", self._on_button_hover, add="+")
        self.login_button.bind("<Leave>", self._on_button_leave, add="+")

        card.columnconfigure(0, weight=1)

    def _on_entry_focus_in(self, event):
        event.widget.configure(style="Modern.TEntry")

    def _on_entry_focus_out(self, event):
        event.widget.configure(style="Modern.TEntry")

    def _on_button_hover(self, event):
        button = event.widget

        def pulse(step=0):
            colors = ["#22c55e", "#4ade80", "#22c55e"]
            idx = step % len(colors)
            style = ttk.Style()
            style.configure("Primary.TButton", background=colors[idx])
            self._hover_job = button.after(120, pulse, step + 1)

        if self._hover_job is None:
            pulse(0)

    def _on_button_leave(self, event):
        if self._hover_job is not None:
            event.widget.after_cancel(self._hover_job)
            self._hover_job = None
        style = ttk.Style()
        style.configure("Primary.TButton", background="#22c55e")

    def _handle_login_click(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showwarning("Lỗi", "Username không được để trống.")
            return
        if self.on_login:
            self.on_login(username)


class ChatView(ttk.Frame):
    """
    Giao diện chat tuần 2:
    - Hiển thị tin nhắn với style đẹp
    - Input box và nút gửi
    - Dark theme với message bubbles
    """

    def __init__(self, master, on_send, username: str = None):
        super().__init__(master, padding=16)
        self.on_send = on_send
        self.username = username
        self._hover_job = None
        self._build_styles()
        self._build_widgets()

    def _build_styles(self):
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")

        # Card chính
        style.configure(
            "Card.TFrame",
            background="#020617",
        )

        # Tiêu đề
        style.configure(
            "Title.TLabel",
            background="#020617",
            foreground="#e5e7eb",
            font=("Segoe UI", 18, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background="#020617",
            foreground="#9ca3af",
            font=("Segoe UI", 9),
        )

        # Entry
        style.configure(
            "Chat.TEntry",
            padding=10,
            relief="flat",
            borderwidth=0,
            fieldbackground="#1f2937",
            foreground="#e5e7eb",
        )
        style.map(
            "Chat.TEntry",
            fieldbackground=[("focus", "#374151")],
        )

        # Button
        style.configure(
            "Send.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(16, 10),
            background="#3b82f6",
            foreground="#ffffff",
            borderwidth=0,
        )
        style.map(
            "Send.TButton",
            background=[("active", "#2563eb"), ("pressed", "#1d4ed8")],
            foreground=[("disabled", "#6b7280")],
        )

    def _build_widgets(self):
        self.configure(style="Card.TFrame")

        # Header với username
        header = ttk.Frame(self, style="Card.TFrame")
        header.pack(fill="x", pady=(0, 12))

        title = ttk.Label(
            header,
            text="Phòng chat",
            style="Title.TLabel",
        )
        title.pack(anchor="w")

        if self.username:
            subtitle = ttk.Label(
                header,
                text=f"Đang chat với tên: {self.username}",
                style="Subtitle.TLabel",
            )
            subtitle.pack(anchor="w", pady=(4, 0))

        # Đường kẻ phát sáng nhẹ
        glow_line = tk.Canvas(
            self,
            height=2,
            bg="#020617",
            highlightthickness=0,
            bd=0,
        )
        glow_line.pack(fill="x", pady=(0, 12))
        glow_line.create_line(
            0,
            1,
            800,
            1,
            fill="#3b82f6",
        )

        # Chat area với dark theme
        chat_frame = ttk.Frame(self, style="Card.TFrame")
        chat_frame.pack(fill="both", expand=True, pady=(0, 12))

        self.msg_area = ScrolledText(
            chat_frame,
            state="disabled",
            wrap="word",
            bg="#0f172a",
            fg="#e5e7eb",
            font=("Segoe UI", 10),
            insertbackground="#3b82f6",
            selectbackground="#374151",
            selectforeground="#ffffff",
            relief="flat",
            borderwidth=0,
            padx=12,
            pady=12,
        )
        self.msg_area.pack(fill="both", expand=True)

        # Configure tags for message styling
        self.msg_area.tag_configure("system", foreground="#9ca3af", font=("Segoe UI", 9, "italic"))
        self.msg_area.tag_configure("timestamp", foreground="#6b7280", font=("Segoe UI", 8))
        self.msg_area.tag_configure("username", foreground="#3b82f6", font=("Segoe UI", 10, "bold"))
        self.msg_area.tag_configure("content", foreground="#e5e7eb", font=("Segoe UI", 10))
        self.msg_area.tag_configure("my_message", foreground="#22c55e", font=("Segoe UI", 10, "bold"))

        # Input area
        input_frame = ttk.Frame(self, style="Card.TFrame")
        input_frame.pack(fill="x")

        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(
            input_frame,
            textvariable=self.input_var,
            style="Chat.TEntry",
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.input_entry.bind("<Return>", self._on_enter)
        self.input_entry.focus()

        # Nút gửi với hiệu ứng
        self.send_button = ttk.Button(
            input_frame,
            text="Gửi",
            style="Send.TButton",
            command=self._on_send_click,
        )
        self.send_button.pack(side="left")
        self.send_button.bind("<Enter>", self._on_button_hover, add="+")
        self.send_button.bind("<Leave>", self._on_button_leave, add="+")

    def _on_enter(self, event):
        self._on_send_click()
        return "break"

    def _on_send_click(self):
        text = self.input_var.get().strip()
        if not text:
            return
        self.input_var.set("")
        if self.on_send:
            self.on_send(text)

    def _on_button_hover(self, event):
        button = event.widget

        def pulse(step=0):
            colors = ["#3b82f6", "#60a5fa", "#3b82f6"]
            idx = step % len(colors)
            style = ttk.Style()
            style.configure("Send.TButton", background=colors[idx])
            self._hover_job = button.after(120, pulse, step + 1)

        if self._hover_job is None:
            pulse(0)

    def _on_button_leave(self, event):
        if self._hover_job is not None:
            event.widget.after_cancel(self._hover_job)
            self._hover_job = None
        style = ttk.Style()
        style.configure("Send.TButton", background="#3b82f6")

    def add_message(self, username: str, content: str, timestamp: str = None, system: bool = False):
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.msg_area.configure(state="normal")
        
        if system:
            # System message với style đặc biệt
            self.msg_area.insert("end", f"[{timestamp}] ", "timestamp")
            self.msg_area.insert("end", "• ", "system")
            self.msg_area.insert("end", f"{content}\n", "system")
        else:
            # User message
            is_my_message = (username == self.username)
            self.msg_area.insert("end", f"[{timestamp}] ", "timestamp")
            
            if is_my_message:
                self.msg_area.insert("end", f"{username}: ", "my_message")
            else:
                self.msg_area.insert("end", f"{username}: ", "username")
            
            self.msg_area.insert("end", f"{content}\n", "content")
        
        self.msg_area.configure(state="disabled")
        # Auto-scroll to bottom
        self.msg_area.yview_moveto(1.0)


class RootWindow(tk.Tk):
    """
    Cửa sổ chính của ứng dụng với gradient background đẹp.
    Quản lý các view: Connection -> Login -> Chat
    """

    def __init__(self, on_connect):
        super().__init__()
        self.title("Game Đoán Số – Client")
        self.geometry("900x650")
        self.minsize(720, 500)

        # Nền gradient bằng Canvas
        self._bg_canvas = tk.Canvas(self, highlightthickness=0, bd=0)
        self._bg_canvas.pack(fill="both", expand=True)
        self.bind("<Configure>", self._draw_gradient)

        # Wrapper canh giữa nội dung
        self._main_frame = ttk.Frame(self._bg_canvas, padding=12)
        self._container_window = self._bg_canvas.create_window(
            0, 0, anchor="center", window=self._main_frame
        )

        def _center_container(event=None):
            w = self._bg_canvas.winfo_width()
            h = self._bg_canvas.winfo_height()
            self._bg_canvas.coords(self._container_window, w / 2, h / 2)

        self._bg_canvas.bind("<Configure>", _center_container)

        # Lưu callback để tái sử dụng
        self._on_connect_callback = on_connect
        self._current_username = None

        # Start with connection view
        self.connection_view = ConnectionView(self._main_frame, on_connect=on_connect)
        self.connection_view.pack(fill="both", expand=True)

    def _draw_gradient(self, event=None):
        """Vẽ nền gradient chéo nhẹ nhàng."""
        self._bg_canvas.delete("gradient")
        w = self.winfo_width()
        h = self.winfo_height()
        steps = 50
        for i in range(steps):
            r = int(2 + (15 - 2) * (i / steps))
            g = int(6 + (23 - 6) * (i / steps))
            b = int(23 + (42 - 23) * (i / steps))
            color = f"#{r:02x}{g:02x}{b:02x}"
            y0 = int(h * i / steps)
            y1 = int(h * (i + 1) / steps)
            self._bg_canvas.create_rectangle(
                0,
                y0,
                w,
                y1,
                outline="",
                fill=color,
                tags="gradient",
            )

    def show_login_view(self, on_login):
        """Hiển thị màn hình đăng nhập."""
        self._clear_views()
        self.login_view = LoginView(self._main_frame, on_login=on_login)
        self.login_view.pack(fill="both", expand=True)

    def show_chat_view(self, on_send, username: str = None):
        """Hiển thị màn hình chat với username."""
        self._clear_views()
        self._current_username = username
        self.chat_view = ChatView(self._main_frame, on_send=on_send, username=username)
        self.chat_view.pack(fill="both", expand=True)

    def show_connection_view(self):
        """Quay lại màn hình kết nối."""
        self._clear_views()
        self._current_username = None
        self.connection_view = ConnectionView(self._main_frame, on_connect=self._on_connect_callback)
        self.connection_view.pack(fill="both", expand=True)

    def _clear_views(self):
        """Xóa tất cả views hiện tại."""
        for child in list(self._main_frame.winfo_children()):
            child.pack_forget()

    def show_info(self, title: str, message: str):
        messagebox.showinfo(title, message)

    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message)


