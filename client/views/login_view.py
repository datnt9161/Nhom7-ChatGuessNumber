"""Màn hình đăng nhập"""
import tkinter as tk
from tkinter import ttk, messagebox
from .styles import setup_base_styles, create_dark_entry


class LoginView(ttk.Frame):
    def __init__(self, master, on_login):
        super().__init__(master, padding=24)
        self.on_login = on_login
        setup_base_styles()
        self._build_widgets()

    def _build_widgets(self):
        self.configure(style="Card.TFrame")

        # Header
        header = ttk.Frame(self, style="Card.TFrame")
        header.pack(fill="x", pady=(0, 16))

        ttk.Label(header, text="Đăng nhập", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Nhập username để tham gia phòng chơi", style="Subtitle.TLabel").pack(anchor="w", pady=(4, 0))

        # Glow line
        glow = tk.Canvas(self, height=2, bg="#020617", highlightthickness=0, bd=0)
        glow.pack(fill="x", pady=(0, 8))
        glow.create_line(0, 1, 800, 1, fill="#22c55e")

        # Form
        card = ttk.Frame(self, style="Form.TFrame", padding=24)
        card.pack(fill="both", expand=True, pady=(8, 0))

        ttk.Label(card, text="Username", style="FormLabel.TLabel").grid(row=0, column=0, sticky="w")
        
        self.username_var = tk.StringVar()
        self.username_entry = create_dark_entry(card, self.username_var)
        self.username_entry.grid(row=1, column=0, sticky="we", pady=(4, 16), ipady=8)
        self.username_entry.focus()

        ttk.Label(card, text="Username sẽ hiển thị trong phòng chat và bảng xếp hạng.", style="FormLabel.TLabel").grid(row=2, column=0, sticky="w", pady=(0, 16))

        self.login_button = ttk.Button(card, text="Đăng nhập", style="Primary.TButton", command=self._handle_login)
        self.login_button.grid(row=3, column=0, sticky="we")

        card.columnconfigure(0, weight=1)

    def _handle_login(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showwarning("Lỗi", "Username không được để trống.")
            return
        if self.on_login:
            self.on_login(username)
