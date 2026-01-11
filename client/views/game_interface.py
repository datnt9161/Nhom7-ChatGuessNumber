"""Giao diện game đoán số"""
import tkinter as tk
from tkinter import ttk
from .styles import setup_base_styles, create_button


class GameInterface(ttk.Frame):
    def __init__(self, master, on_guess, username: str = None):
        super().__init__(master, padding=8)
        self.on_guess = on_guess
        self.username = username
        self.guess_count = 0
        self.max_guesses = 10
        self.game_active = True
        self.last_result = None
        setup_base_styles()
        self._build_widgets()

    def _build_widgets(self):
        self.configure(style="Card.TFrame")

        # Header
        header = tk.Frame(self, bg="#020617")
        header.pack(fill="x", pady=(0, 8))
        tk.Label(header, text="🎮 Game Đoán Số", bg="#020617", fg="#e5e7eb", font=("Segoe UI", 14, "bold")).pack(anchor="w")

        # Glow line
        glow = tk.Canvas(self, height=2, bg="#020617", highlightthickness=0, bd=0)
        glow.pack(fill="x", pady=(0, 8))
        glow.create_line(0, 1, 2000, 1, fill="#f59e0b")

        # Info
        info_frame = tk.Frame(self, bg="#1f2937")
        info_frame.pack(fill="x", pady=(0, 8))
        info_content = tk.Frame(info_frame, bg="#1f2937")
        info_content.pack(fill="x", padx=10, pady=8)

        self.guess_count_label = tk.Label(info_content, text="📊 Lượt: 0/10", bg="#1f2937", fg="#e5e7eb", font=("Segoe UI", 10, "bold"))
        self.guess_count_label.pack(anchor="w")

        self.status_label = tk.Label(info_content, text="🎮 Đoán số từ 1-100", bg="#1f2937", fg="#22c55e", font=("Segoe UI", 9))
        self.status_label.pack(anchor="w", pady=(4, 0))

        # Result - responsive height
        result_frame = tk.Frame(self, bg="#f9fafb", highlightbackground="#e5e7eb", highlightthickness=1)
        result_frame.pack(fill="both", expand=True, pady=(0, 8))

        self.result_label = tk.Label(result_frame, text="✨ Nhập số 1-100\nđể bắt đầu!", bg="#f9fafb", fg="#374151", font=("Segoe UI", 12, "bold"), wraplength=250, justify="center")
        self.result_label.pack(expand=True, fill="both", padx=12, pady=12)

        # Input
        input_frame = tk.Frame(self, bg="#020617")
        input_frame.pack(fill="x")

        tk.Label(input_frame, text="Nhập số (1-100):", bg="#020617", fg="#9ca3af", font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 4))

        input_container = tk.Frame(input_frame, bg="#020617")
        input_container.pack(fill="x")

        self.guess_var = tk.StringVar()
        self.guess_entry = tk.Entry(
            input_container, textvariable=self.guess_var,
            font=("Segoe UI", 12, "bold"), bg="#1e293b", fg="#f1f5f9",
            insertbackground="#f59e0b", relief="flat", bd=0,
            highlightthickness=2, highlightbackground="#334155", highlightcolor="#f59e0b", justify="center", width=10
        )
        self.guess_entry.pack(side="left", fill="x", expand=True, padx=(0, 6), ipady=8)
        self.guess_entry.bind("<Return>", lambda e: self._handle_guess())
        self.guess_entry.bind("<KeyRelease>", self._validate_input)

        self.guess_button = create_button(input_container, "🎯 Đoán", "#f59e0b", self._handle_guess, padx=16, pady=8)
        self.guess_button.pack(side="left")

    def _validate_input(self, event):
        value = self.guess_var.get()
        if value and not value.isdigit():
            self.guess_var.set(''.join(c for c in value if c.isdigit()))

    def _handle_guess(self):
        if not self.game_active:
            return

        guess_text = self.guess_var.get().strip()
        if not guess_text:
            self._show_result("⚠️ Vui lòng nhập số!", "#dc2626", "#fee2e2")
            return

        try:
            guess = int(guess_text)
            if not (1 <= guess <= 100):
                self._show_result("❌ Số phải từ 1-100!", "#dc2626", "#fee2e2")
                return
        except ValueError:
            self._show_result("❌ Vui lòng nhập SỐ!", "#dc2626", "#fee2e2")
            return

        self.guess_var.set("")
        self.guess_count += 1
        remaining = self.max_guesses - self.guess_count
        self.guess_count_label.config(text=f"📊 Lượt đoán: {self.guess_count}/{self.max_guesses}")
        self._show_result(f"⏳ Đang gửi số {guess}...", "#6b7280")

        if self.on_guess:
            self.on_guess(guess)

    def _show_result(self, text: str, color: str, bg: str = "#f9fafb"):
        self.result_label.config(text=text, fg=color, bg=bg)

    def handle_result(self, result: str, message: str = None, **kwargs):
        self.last_result = result
        remaining = self.max_guesses - self.guess_count

        if result == "WIN" or result == "CORRECT":
            # THẮNG
            self.game_active = False
            points = kwargs.get('points', 0)
            self._show_result(f"🏆 BẠN THẮNG! 🏆\nĐoán đúng sau {self.guess_count} lần!\n+{points} điểm", "#15803d", "#dcfce7")
            self.status_label.config(text="🎉 Chúc mừng! Chờ game mới...", fg="#22c55e")
            self.guess_button.config(state="disabled")
            self.guess_entry.config(state="disabled")
        elif result == "LOSE":
            # THUA
            self.game_active = False
            secret = kwargs.get('secret', '?')
            self._show_result(f"😢 BẠN THUA!\nHết {self.max_guesses} lượt đoán\nSố bí mật là: {secret}", "#dc2626", "#fee2e2")
            self.status_label.config(text="❌ Hết lượt! Chờ game mới...", fg="#dc2626")
            self.guess_button.config(state="disabled")
            self.guess_entry.config(state="disabled")
        elif result == "HIGH":
            self._show_result(f"⬇️ Số bí mật THẤP HƠN!\nCòn {remaining} lượt", "#d97706", "#fef3c7")
            self.status_label.config(text=f"💡 Đoán số NHỎ hơn! (Còn {remaining} lượt)", fg="#f59e0b")
        elif result == "LOW":
            self._show_result(f"⬆️ Số bí mật CAO HƠN!\nCòn {remaining} lượt", "#d97706", "#fef3c7")
            self.status_label.config(text=f"💡 Đoán số LỚN hơn! (Còn {remaining} lượt)", fg="#f59e0b")

    def start_new_game(self):
        self.game_active = True
        self.guess_count = 0
        self.guess_count_label.config(text=f"📊 Lượt đoán: 0/{self.max_guesses}")
        self._show_result("✨ Game mới!\nĐoán số từ 1-100", "#374151")
        self.status_label.config(text=f"🎮 Bạn có {self.max_guesses} lượt đoán!", fg="#22c55e")
        self.guess_button.config(state="normal")
        self.guess_entry.config(state="normal")
        self.guess_entry.focus()
