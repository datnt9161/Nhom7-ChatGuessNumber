import tkinter as tk
from tkinter import ttk, messagebox


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
            text="Chat & Guess Number",
            style="Title.TLabel",
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            header,
            text="Multiplayer chat & guessing game • Week 1 – Connection UI",
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

        # Card form kết nối
        # Bọc bởi canvas để tạo viền bo góc & đổ bóng
        card_wrapper = tk.Canvas(
            self,
            bg="#020617",
            highlightthickness=0,
            bd=0,
        )
        card_wrapper.pack(fill="both", expand=True, pady=(8, 0))

        # Vẽ nền bo góc với hiệu ứng glow
        def _draw_card_bg(event=None):
            card_wrapper.delete("all")
            w = card_wrapper.winfo_width()
            h = card_wrapper.winfo_height()
            radius = 18
            x0, y0, x1, y1 = 4, 4, w - 4, h - 4

            # Bóng mờ
            card_wrapper.create_rectangle(
                x0 + 2,
                y0 + 6,
                x1 + 2,
                y1 + 10,
                outline="",
                fill="#020617",
            )
            # Viền sáng nhạt
            card_wrapper.create_rectangle(
                x0,
                y0,
                x1,
                y1,
                outline="#1f2937",
                width=1,
                fill="#020617",
            )

        card_wrapper.bind("<Configure>", _draw_card_bg)

        card = ttk.Frame(card_wrapper, style="Form.TFrame", padding=24)
        # Đặt card ở giữa canvas
        card_window = card_wrapper.create_window(
            0, 0, anchor="nw", window=card
        )

        def _reposition_card(event=None):
            w = card_wrapper.winfo_width()
            h = card_wrapper.winfo_height()
            cw = card.winfo_reqwidth()
            ch = card.winfo_reqheight()
            x = max((w - cw) // 2, 16)
            y = max((h - ch) // 2, 8)
            card_wrapper.coords(card_window, x, y)

        card_wrapper.bind("<Configure>", _reposition_card)

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

        # Hiệu ứng border khi focus
        for entry in (ip_entry, port_entry):
            entry.bind("<FocusIn>", self._on_entry_focus_in, add="+")
            entry.bind("<FocusOut>", self._on_entry_focus_out, add="+")

        # Gợi ý nhỏ
        hint = ttk.Label(
            card,
            text="Hãy đảm bảo server đã chạy trước khi kết nối.\n"
            "Tuần 1: mới thực hiện kết nối, chưa cần login & chat.",
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

        # Hover & pulse animation cho nút kết nối
        self.connect_button.bind("<Enter>", self._on_button_hover, add="+")
        self.connect_button.bind("<Leave>", self._on_button_leave, add="+")

        card.columnconfigure(0, weight=1)

    def _on_entry_focus_in(self, event):
        event.widget.configure(style="Modern.TEntry")

    def _on_entry_focus_out(self, event):
        event.widget.configure(style="Modern.TEntry")

    def _on_button_hover(self, event):
        button = event.widget

        def pulse(step=0):
            # step: 0 → 1 → 2 → 3 rồi quay lại
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


class RootWindow(tk.Tk):
    """
    Cửa sổ chính của ứng dụng.
    Tuần 1 chỉ hiển thị màn hình kết nối, nhưng khung layout đã sẵn sàng
    để thêm Login, Chat, Game, Ranking ở các tuần sau.
    """

    def __init__(self, on_connect):
        super().__init__()
        self.title("Chat & Guess Number – Client")
        self.geometry("720x420")
        self.minsize(640, 380)

        # Nền gradient bằng Canvas để mềm mại hơn
        self._bg_canvas = tk.Canvas(self, highlightthickness=0, bd=0)
        self._bg_canvas.pack(fill="both", expand=True)
        self.bind("<Configure>", self._draw_gradient)

        # Wrapper canh giữa nội dung
        container = ttk.Frame(self._bg_canvas, style="Card.TFrame", padding=24)
        self._container_window = self._bg_canvas.create_window(
            0, 0, anchor="center", window=container
        )

        def _center_container(event=None):
            w = self._bg_canvas.winfo_width()
            h = self._bg_canvas.winfo_height()
            self._bg_canvas.coords(self._container_window, w / 2, h / 2)

        self._bg_canvas.bind("<Configure>", _center_container)

        self.connection_view = ConnectionView(container, on_connect=on_connect)
        self.connection_view.pack(fill="both", expand=True)

    def _draw_gradient(self, event=None):
        """Vẽ nền gradient chéo nhẹ nhàng phía sau card."""
        self._bg_canvas.delete("gradient")
        w = self.winfo_width()
        h = self.winfo_height()
        steps = 40
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

    def show_info(self, title: str, message: str):
        messagebox.showinfo(title, message)

    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message)


