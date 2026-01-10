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

        self.port_var = tk.StringVar(value="5555")
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


class GameInterface(ttk.Frame):
    """
    Giao diện game đoán số tuần 3:
    - Input để đoán số (1-100)
    - Hiển thị gợi ý (HIGH/LOW/CORRECT)
    - Số lần đoán
    - Thông báo thắng/thua
    """

    def __init__(self, master, on_guess, username: str = None):
        super().__init__(master, padding=16)
        self.on_guess = on_guess
        self.username = username
        self.guess_count = 0
        self.game_active = True
        self.last_result = None
        self._hover_job = None
        self._build_styles()
        self._build_widgets()

    def _build_styles(self):
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure(
            "Card.TFrame",
            background="#020617",
        )

        style.configure(
            "Title.TLabel",
            background="#020617",
            foreground="#e5e7eb",
            font=("Segoe UI", 16, "bold"),
        )

        style.configure(
            "Game.TEntry",
            padding=12,
            relief="flat",
            borderwidth=2,
            fieldbackground="#ffffff",
            foreground="#111827",
            font=("Segoe UI", 14, "bold"),
        )
        style.map(
            "Game.TEntry",
            fieldbackground=[("focus", "#f3f4f6")],
            bordercolor=[("focus", "#f59e0b")],
        )

        style.configure(
            "Guess.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(16, 10),
            background="#f59e0b",
            foreground="#ffffff",
            borderwidth=0,
        )
        style.map(
            "Guess.TButton",
            background=[("active", "#d97706"), ("pressed", "#b45309")],
            foreground=[("disabled", "#6b7280")],
        )

        style.configure(
            "Result.TLabel",
            background="#020617",
            foreground="#e5e7eb",
            font=("Segoe UI", 14, "bold"),
        )

    def _build_widgets(self):
        self.configure(style="Card.TFrame")

        # Header
        header = ttk.Frame(self, style="Card.TFrame")
        header.pack(fill="x", pady=(0, 12))

        title = ttk.Label(
            header,
            text="🎮 Game Đoán Số",
            style="Title.TLabel",
        )
        title.pack(anchor="w")

        # Đường kẻ phát sáng
        glow_line = tk.Canvas(
            self,
            height=2,
            bg="#020617",
            highlightthickness=0,
            bd=0,
        )
        glow_line.pack(fill="x", pady=(0, 12))
        glow_line.create_line(0, 1, 800, 1, fill="#f59e0b")

        # Game info - cải thiện với card style
        info_frame = tk.Frame(self, bg="#1f2937", relief="flat", bd=0)
        info_frame.pack(fill="x", pady=(0, 12))

        info_content = tk.Frame(info_frame, bg="#1f2937")
        info_content.pack(fill="x", padx=12, pady=10)

        self.guess_count_label = tk.Label(
            info_content,
            text="📊 Số lần đoán: 0",
            bg="#1f2937",
            fg="#e5e7eb",
            font=("Segoe UI", 11, "bold"),
        )
        self.guess_count_label.pack(anchor="w")

        self.status_label = tk.Label(
            info_content,
            text="⏳ Đang chờ game mới...",
            bg="#1f2937",
            fg="#9ca3af",
            font=("Segoe UI", 10),
        )
        self.status_label.pack(anchor="w", pady=(6, 0))

        # Result display area - làm đẹp hơn với border và shadow effect
        result_frame = tk.Frame(self, bg="#f9fafb", relief="flat", bd=1, height=100)
        result_frame.pack(fill="x", pady=(0, 16))
        result_frame.pack_propagate(False)
        result_frame.config(highlightbackground="#e5e7eb", highlightthickness=1)

        self.result_label = tk.Label(
            result_frame,
            text="✨ Nhập số từ 1-100 để bắt đầu!",
            bg="#f9fafb",
            fg="#374151",
            font=("Segoe UI", 13, "bold"),
            wraplength=300,
            justify="center",
        )
        self.result_label.pack(expand=True, fill="both", padx=16, pady=16)

        # Input area - cải thiện với label và spacing tốt hơn
        input_frame = ttk.Frame(self, style="Card.TFrame")
        input_frame.pack(fill="x", pady=(8, 0))

        # Label cho input
        input_label = ttk.Label(
            input_frame,
            text="Nhập số đoán (1-100):",
            style="Card.TFrame",
            foreground="#9ca3af",
            font=("Segoe UI", 10),
        )
        input_label.pack(anchor="w", pady=(0, 6))

        # Input container với better spacing
        input_container = ttk.Frame(input_frame, style="Card.TFrame")
        input_container.pack(fill="x")

        self.guess_var = tk.StringVar()
        self.guess_entry = ttk.Entry(
            input_container,
            textvariable=self.guess_var,
            style="Game.TEntry",
            width=15,
        )
        self.guess_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.guess_entry.bind("<Return>", self._on_enter)
        self.guess_entry.bind("<KeyRelease>", self._validate_input)

        self.guess_button = ttk.Button(
            input_container,
            text="🎯 Đoán",
            style="Guess.TButton",
            command=self._handle_guess_click,
        )
        self.guess_button.pack(side="left")
        self.guess_button.bind("<Enter>", self._on_button_hover, add="+")
        self.guess_button.bind("<Leave>", self._on_button_leave, add="+")

    def _validate_input(self, event):
        """Chỉ cho phép nhập số"""
        value = self.guess_var.get()
        if value and not value.isdigit():
            self.guess_var.set(''.join(c for c in value if c.isdigit()))

    def _on_enter(self, event):
        if self.game_active:
            self._handle_guess_click()
        return "break"

    def _handle_guess_click(self):
        if not self.game_active:
            return

        guess_text = self.guess_var.get().strip()
        if not guess_text:
            self.result_label.config(bg="#fee2e2")  # Nền đỏ nhạt cho lỗi
            self._show_result("⚠️ Vui lòng nhập số!", "#dc2626")
            return

        try:
            guess = int(guess_text)
            if not (1 <= guess <= 100):
                self.result_label.config(bg="#fee2e2")
                self._show_result("❌ Số phải từ 1-100!\nVui lòng thử lại.", "#dc2626")
                return
        except ValueError:
            self.result_label.config(bg="#fee2e2")
            self._show_result("❌ Không hợp lệ!\nVui lòng nhập SỐ.", "#dc2626")
            return

        self.guess_var.set("")
        self.guess_count += 1
        self._update_guess_count()
        self.result_label.config(bg="#f9fafb")  # Reset về nền trắng khi gửi
        self._show_result(f"⏳ Đang gửi số {guess}...", "#6b7280")

        if self.on_guess:
            self.on_guess(guess)

    def _on_button_hover(self, event):
        button = event.widget

        def pulse(step=0):
            colors = ["#f59e0b", "#fbbf24", "#f59e0b"]
            idx = step % len(colors)
            style = ttk.Style()
            style.configure("Guess.TButton", background=colors[idx])
            self._hover_job = button.after(120, pulse, step + 1)

        if self._hover_job is None:
            pulse(0)

    def _on_button_leave(self, event):
        if self._hover_job is not None:
            event.widget.after_cancel(self._hover_job)
            self._hover_job = None
        style = ttk.Style()
        style.configure("Guess.TButton", background="#f59e0b")

    def _show_result(self, text: str, color: str = "#374151"):
        """Hiển thị kết quả đoán với màu rõ ràng hơn"""
        self.result_label.config(text=text, fg=color)

    def _update_guess_count(self):
        """Cập nhật số lần đoán với format đẹp hơn"""
        self.guess_count_label.config(text=f"📊 Số lần đoán: {self.guess_count}")

    def handle_result(self, result: str, message: str = None):
        """Xử lý kết quả từ server (HIGH/LOW/CORRECT) với màu sắc rõ ràng hơn"""
        self.last_result = result

        if result == "CORRECT":
            self.game_active = False
            self.result_label.config(bg="#dcfce7")  # Nền xanh lá nhạt
            self._show_result(f"🎉🎉 CHÚC MỪNG! 🎉🎉\nBạn đã đoán đúng sau {self.guess_count} lần!", "#15803d")
            self.status_label.config(text="✅ Đã hoàn thành game! Chờ game mới...", fg="#22c55e")
            self.guess_button.config(state="disabled")
            self.guess_entry.config(state="disabled")
        elif result == "HIGH":
            self.result_label.config(bg="#fef3c7")  # Nền vàng nhạt
            self._show_result(f"⬆️ CAO HƠN!\n(Lần đoán: {self.guess_count})", "#d97706")
            self.status_label.config(text="⚠️ Số bạn đoán LỚN HƠN số bí mật", fg="#f59e0b")
        elif result == "LOW":
            self.result_label.config(bg="#fef3c7")  # Nền vàng nhạt
            self._show_result(f"⬇️ THẤP HƠN!\n(Lần đoán: {self.guess_count})", "#d97706")
            self.status_label.config(text="⚠️ Số bạn đoán NHỎ HƠN số bí mật", fg="#f59e0b")
        else:
            self.result_label.config(bg="#f9fafb")
            self._show_result(message or "Kết quả không xác định", "#6b7280")

    def start_new_game(self):
        """Bắt đầu game mới"""
        self.game_active = True
        self.guess_count = 0
        self.last_result = None
        self._update_guess_count()
        self.result_label.config(bg="#f9fafb")  # Reset về nền trắng
        self._show_result("✨ Nhập số từ 1-100 để bắt đầu!", "#374151")
        self.status_label.config(text="🎮 Đang chơi... Sẵn sàng đoán số!", fg="#22c55e")
        self.guess_button.config(state="normal")
        self.guess_entry.config(state="normal")
        self.guess_entry.focus()


class RankingView(ttk.Frame):
    """
    Trang riêng hiển thị bảng xếp hạng tuần 3:
    - Top players
    - Điểm số
    - Số lần đoán
    - Real-time updates
    - Nút quay lại game
    """

    def __init__(self, master, on_back, username: str = None):
        super().__init__(master, padding=20)
        self.username = username
        self.on_back = on_back
        self.ranking_data = []
        self._build_styles()
        self._build_widgets()

    def _build_styles(self):
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure(
            "Card.TFrame",
            background="#020617",
        )

        style.configure(
            "Title.TLabel",
            background="#020617",
            foreground="#e5e7eb",
            font=("Segoe UI", 20, "bold"),
        )

        style.configure(
            "Back.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8),
            background="#3b82f6",
            foreground="#ffffff",
            borderwidth=0,
        )
        style.map(
            "Back.TButton",
            background=[("active", "#2563eb"), ("pressed", "#1d4ed8")],
        )

    def _build_widgets(self):
        self.configure(style="Card.TFrame")

        # Header với nút quay lại
        header = ttk.Frame(self, style="Card.TFrame")
        header.pack(fill="x", pady=(0, 16))

        title = ttk.Label(
            header,
            text="🏆 Bảng Xếp Hạng",
            style="Title.TLabel",
        )
        title.pack(side="left")

        # Nút quay lại game
        back_button = ttk.Button(
            header,
            text="◀ Quay lại Game",
            style="Back.TButton",
            command=self.on_back,
        )
        back_button.pack(side="right")

        # Đường kẻ phát sáng
        glow_line = tk.Canvas(
            self,
            height=2,
            bg="#020617",
            highlightthickness=0,
            bd=0,
        )
        glow_line.pack(fill="x", pady=(0, 16))
        glow_line.create_line(0, 1, 1200, 1, fill="#eab308")

        # Ranking area - canh giữa và có max width
        ranking_container = ttk.Frame(self, style="Card.TFrame")
        ranking_container.pack(fill="both", expand=True)

        # Center wrapper để canh giữa bảng
        center_wrapper = ttk.Frame(ranking_container, style="Card.TFrame")
        center_wrapper.pack(fill="both", expand=True)
        
        ranking_frame = tk.Frame(center_wrapper, bg="#0f172a", relief="flat", bd=0)
        ranking_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Scrollable ranking list
        self.ranking_canvas = tk.Canvas(
            ranking_frame,
            bg="#0f172a",
            highlightthickness=0,
            bd=0,
        )
        scrollbar = ttk.Scrollbar(ranking_frame, orient="vertical", command=self.ranking_canvas.yview)
        self.ranking_scrollable_frame = tk.Frame(self.ranking_canvas, bg="#0f172a")

        self.ranking_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.ranking_canvas.configure(scrollregion=self.ranking_canvas.bbox("all"))
        )

        self.ranking_canvas.create_window((0, 0), window=self.ranking_scrollable_frame, anchor="nw")
        self.ranking_canvas.configure(yscrollcommand=scrollbar.set)

        self.ranking_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Empty state
        self.empty_label = tk.Label(
            self.ranking_scrollable_frame,
            text="Chưa có dữ liệu xếp hạng\nGame sẽ bắt đầu sau khi có người chơi thắng",
            bg="#0f172a",
            fg="#9ca3af",
            font=("Segoe UI", 10),
            justify="center",
        )
        self.empty_label.pack(pady=20)

    def update_ranking(self, ranking_data: list):
        """Cập nhật bảng xếp hạng từ server"""
        self.ranking_data = ranking_data

        # Xóa các widget cũ
        for widget in self.ranking_scrollable_frame.winfo_children():
            widget.destroy()

        if not ranking_data:
            self.empty_label = tk.Label(
                self.ranking_scrollable_frame,
                text="Chưa có dữ liệu xếp hạng\nGame sẽ bắt đầu sau khi có người chơi thắng",
                bg="#0f172a",
                fg="#9ca3af",
                font=("Segoe UI", 10),
                justify="center",
            )
            self.empty_label.pack(pady=20)
            return

            # Header của bảng - làm đẹp hơn
        header_frame = tk.Frame(self.ranking_scrollable_frame, bg="#374151", relief="flat", bd=0)
        header_frame.pack(fill="x", padx=12, pady=(0, 8))

        tk.Label(header_frame, text="#", bg="#374151", fg="#ffffff", font=("Segoe UI", 11, "bold"), width=4).pack(side="left", padx=8)
        tk.Label(header_frame, text="Username", bg="#374151", fg="#ffffff", font=("Segoe UI", 11, "bold"), width=20).pack(side="left", padx=8)
        tk.Label(header_frame, text="Điểm", bg="#374151", fg="#ffffff", font=("Segoe UI", 11, "bold"), width=12).pack(side="left", padx=8)
        tk.Label(header_frame, text="Số lần đoán", bg="#374151", fg="#ffffff", font=("Segoe UI", 11, "bold"), width=12).pack(side="left", padx=8)

        # Dữ liệu ranking
        medals = ["🥇", "🥈", "🥉"]
        for idx, player in enumerate(ranking_data[:10]):  # Top 10
            username = player.get("username", "?")
            score = player.get("score", 0)
            guesses = player.get("guesses", 0)

            is_current_user = (username == self.username)

            row_frame = tk.Frame(
                self.ranking_scrollable_frame,
                bg="#1f2937" if not is_current_user else "#1e40af",
                relief="flat",
                bd=0,
            )
            row_frame.pack(fill="x", padx=12, pady=4)

            # Rank - làm to hơn
            rank_text = f"{idx + 1}" if idx >= 3 else f"{medals[idx]} {idx + 1}"
            rank_color = "#fbbf24" if idx < 3 else "#9ca3af"
            tk.Label(
                row_frame,
                text=rank_text,
                bg=row_frame.cget("bg"),
                fg=rank_color if not is_current_user else "#ffffff",
                font=("Segoe UI", 11, "bold"),
                width=4,
            ).pack(side="left", padx=8)

            # Username - font lớn hơn
            username_color = "#ffffff" if is_current_user else "#e5e7eb"
            tk.Label(
                row_frame,
                text=username[:20],
                bg=row_frame.cget("bg"),
                fg=username_color,
                font=("Segoe UI", 11, "bold" if is_current_user else "normal"),
                width=20,
                anchor="w",
            ).pack(side="left", padx=8)

            # Score - font lớn hơn
            tk.Label(
                row_frame,
                text=str(score),
                bg=row_frame.cget("bg"),
                fg=username_color,
                font=("Segoe UI", 11, "bold" if is_current_user else "normal"),
                width=12,
            ).pack(side="left", padx=8)

            # Guesses - font lớn hơn
            tk.Label(
                row_frame,
                text=str(guesses),
                bg=row_frame.cget("bg"),
                fg=username_color,
                font=("Segoe UI", 11, "bold" if is_current_user else "normal"),
                width=12,
            ).pack(side="left", padx=8)

        self.ranking_canvas.update_idletasks()
        self.ranking_canvas.configure(scrollregion=self.ranking_canvas.bbox("all"))


class MainGameView(ttk.Frame):
    """
    View chính với Chat và Game ở giữa, dễ thao tác:
    - Layout 2 cột: Chat (bên trái) + Game (bên phải)
    - Nút mở bảng xếp hạng
    """

    def __init__(self, master, on_send_chat, on_guess, on_show_ranking, username: str = None):
        super().__init__(master, padding=16)
        self.username = username
        self.on_show_ranking = on_show_ranking
        self._build_styles()
        self._build_widgets(on_send_chat, on_guess, username)

    def _build_styles(self):
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure("Card.TFrame", background="#020617")
        
        style.configure(
            "Ranking.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8),
            background="#eab308",
            foreground="#ffffff",
            borderwidth=0,
        )
        style.map(
            "Ranking.TButton",
            background=[("active", "#ca8a04"), ("pressed", "#a16207")],
        )

    def _build_widgets(self, on_send_chat, on_guess, username):
        self.configure(style="Card.TFrame")

        # Header với nút xem ranking
        header = ttk.Frame(self, style="Card.TFrame")
        header.pack(fill="x", pady=(0, 12))

        title = ttk.Label(
            header,
            text="🎮 Game Đoán Số",
            style="Card.TFrame",
            foreground="#e5e7eb",
            font=("Segoe UI", 18, "bold"),
        )
        title.pack(side="left")

        # Nút xem bảng xếp hạng
        ranking_button = ttk.Button(
            header,
            text="🏆 Xem Bảng Xếp Hạng",
            style="Ranking.TButton",
            command=self.on_show_ranking,
        )
        ranking_button.pack(side="right")

        # Đường kẻ phát sáng
        glow_line = tk.Canvas(
            self,
            height=2,
            bg="#020617",
            highlightthickness=0,
            bd=0,
        )
        glow_line.pack(fill="x", pady=(0, 16))
        glow_line.create_line(0, 1, 800, 1, fill="#3b82f6")

        # Main container với 2 cột canh giữa
        main_container = ttk.Frame(self, style="Card.TFrame")
        main_container.pack(fill="both", expand=True)

        # Center wrapper để canh giữa nội dung
        center_wrapper = ttk.Frame(main_container, style="Card.TFrame")
        center_wrapper.pack(expand=True, fill="both", padx=40, pady=20)

        # Layout 2 cột với grid để control tốt hơn
        center_wrapper.grid_columnconfigure(0, weight=5, uniform="col")
        center_wrapper.grid_columnconfigure(1, weight=4, uniform="col")

        # Cột 1: Chat (55%)
        chat_frame = ttk.Frame(center_wrapper, style="Card.TFrame")
        chat_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 16))

        self.chat_view = ChatView(chat_frame, on_send=on_send_chat, username=username)
        self.chat_view.pack(fill="both", expand=True)

        # Cột 2: Game Interface (45%)
        game_frame = ttk.Frame(center_wrapper, style="Card.TFrame")
        game_frame.grid(row=0, column=1, sticky="nsew")

        self.game_interface = GameInterface(game_frame, on_guess=on_guess, username=username)
        self.game_interface.pack(fill="both", expand=True)

    def get_chat_view(self):
        return self.chat_view

    def get_game_interface(self):
        return self.game_interface


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
        self.main_game_view = None  # Tuần 3 view

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
        """Hiển thị màn hình chat với username (tuần 2 - legacy)."""
        self._clear_views()
        self._current_username = username
        self.chat_view = ChatView(self._main_frame, on_send=on_send, username=username)
        self.chat_view.pack(fill="both", expand=True)

    def show_main_game_view(self, on_send_chat, on_guess, on_show_ranking, username: str = None):
        """Hiển thị màn hình chính với Chat + Game ở giữa (tuần 3)."""
        self._clear_views()
        self._current_username = username
        self.geometry("1200x700")  # Cỡ cửa sổ phù hợp với 2 cột
        self.minsize(1000, 600)
        self.main_game_view = MainGameView(
            self._main_frame,
            on_send_chat=on_send_chat,
            on_guess=on_guess,
            on_show_ranking=on_show_ranking,
            username=username
        )
        self.main_game_view.pack(fill="both", expand=True)

    def show_ranking_view(self, on_back, ranking_data: list = None, username: str = None):
        """Hiển thị trang bảng xếp hạng riêng (tuần 3)."""
        self._clear_views()
        self._current_username = username
        self.geometry("1000x700")  # Cỡ cửa sổ phù hợp với ranking
        self.minsize(900, 600)
        self.ranking_view = RankingView(
            self._main_frame,
            on_back=on_back,
            username=username
        )
        self.ranking_view.pack(fill="both", expand=True)
        # Cập nhật ranking nếu có data
        if ranking_data is not None:
            self.ranking_view.update_ranking(ranking_data)

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


