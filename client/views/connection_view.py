"""Màn hình kết nối server"""
import tkinter as tk
from tkinter import ttk, messagebox
from .styles import setup_base_styles, create_dark_entry


class ConnectionView(ttk.Frame):
    def __init__(self, master, on_connect):
        super().__init__(master, padding=24)
        self.on_connect = on_connect
        setup_base_styles()
        self._build_widgets()

    def _build_widgets(self):
        self.configure(style="Card.TFrame")

        # Header
        header = ttk.Frame(self, style="Card.TFrame")
        header.pack(fill="x", pady=(0, 16))

        ttk.Label(header, text="Game Đoán Số", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Game đoán số multiplayer", style="Subtitle.TLabel").pack(anchor="w", pady=(4, 0))

        # Form
        card = ttk.Frame(self, style="Form.TFrame", padding=24)
        card.pack(fill="both", expand=True)

        # IP
        ttk.Label(card, text="Server IP", style="FormLabel.TLabel").grid(row=0, column=0, sticky="w")
        self.ip_var = tk.StringVar(value="127.0.0.1")
        ip_entry = create_dark_entry(card, self.ip_var)
        ip_entry.grid(row=1, column=0, sticky="we", pady=(4, 12), ipady=8)

        # Port
        ttk.Label(card, text="Server Port", style="FormLabel.TLabel").grid(row=2, column=0, sticky="w")
        self.port_var = tk.StringVar(value="5555")
        port_entry = create_dark_entry(card, self.port_var)
        port_entry.grid(row=3, column=0, sticky="we", pady=(4, 16), ipady=8)

        # Hint
        ttk.Label(card, text="Hãy đảm bảo server đã chạy trước khi kết nối.", style="FormLabel.TLabel").grid(row=4, column=0, sticky="w", pady=(0, 16))

        # Button
        self.connect_button = ttk.Button(card, text="Kết nối tới server", style="Primary.TButton", command=self._handle_connect)
        self.connect_button.grid(row=5, column=0, sticky="we")

        card.columnconfigure(0, weight=1)

    def _handle_connect(self):
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

        if self.on_connect:
            self.on_connect(ip, port)
