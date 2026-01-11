"""Bảng xếp hạng"""
import tkinter as tk
from tkinter import ttk
from .styles import setup_base_styles, create_button


class RankingView(ttk.Frame):
    def __init__(self, master, on_back, username: str = None):
        super().__init__(master, padding=20)
        self.username = username
        self.on_back = on_back
        self.ranking_data = []
        setup_base_styles()
        self._build_widgets()

    def _build_widgets(self):
        self.configure(style="Card.TFrame")

        # Header
        header = ttk.Frame(self, style="Card.TFrame")
        header.pack(fill="x", pady=(0, 16))

        ttk.Label(header, text="🏆 Bảng Xếp Hạng", style="Title.TLabel").pack(side="left")
        
        back_btn = create_button(header, "◀ Quay lại Game", "#3b82f6", self.on_back)
        back_btn.pack(side="right")

        # Glow line
        glow = tk.Canvas(self, height=2, bg="#020617", highlightthickness=0, bd=0)
        glow.pack(fill="x", pady=(0, 16))
        glow.create_line(0, 1, 1200, 1, fill="#eab308")

        # Ranking area
        ranking_container = ttk.Frame(self, style="Card.TFrame")
        ranking_container.pack(fill="both", expand=True)

        ranking_frame = tk.Frame(ranking_container, bg="#0f172a")
        ranking_frame.pack(fill="both", expand=True, padx=40, pady=20)

        self.ranking_canvas = tk.Canvas(ranking_frame, bg="#0f172a", highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(ranking_frame, orient="vertical", command=self.ranking_canvas.yview)
        self.ranking_scrollable_frame = tk.Frame(self.ranking_canvas, bg="#0f172a")

        self.ranking_scrollable_frame.bind("<Configure>", lambda e: self.ranking_canvas.configure(scrollregion=self.ranking_canvas.bbox("all")))
        self.ranking_canvas.create_window((0, 0), window=self.ranking_scrollable_frame, anchor="nw")
        self.ranking_canvas.configure(yscrollcommand=scrollbar.set)

        self.ranking_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Empty state
        self._show_empty()

    def _show_empty(self):
        tk.Label(self.ranking_scrollable_frame, text="Chưa có dữ liệu xếp hạng", bg="#0f172a", fg="#9ca3af", font=("Segoe UI", 10)).pack(pady=20)

    def update_ranking(self, ranking_data: list):
        self.ranking_data = ranking_data

        for widget in self.ranking_scrollable_frame.winfo_children():
            widget.destroy()

        if not ranking_data:
            self._show_empty()
            return

        # Header
        header = tk.Frame(self.ranking_scrollable_frame, bg="#374151")
        header.pack(fill="x", padx=12, pady=(0, 8))
        tk.Label(header, text="#", bg="#374151", fg="#fff", font=("Segoe UI", 11, "bold"), width=4).pack(side="left", padx=8)
        tk.Label(header, text="Username", bg="#374151", fg="#fff", font=("Segoe UI", 11, "bold"), width=20).pack(side="left", padx=8)
        tk.Label(header, text="Điểm", bg="#374151", fg="#fff", font=("Segoe UI", 11, "bold"), width=12).pack(side="left", padx=8)

        medals = ["🥇", "🥈", "🥉"]
        for idx, player in enumerate(ranking_data[:10]):
            username = player[0] if isinstance(player, (list, tuple)) else player.get("username", "?")
            score = player[1] if isinstance(player, (list, tuple)) else player.get("score", 0)
            is_me = (username == self.username)

            row = tk.Frame(self.ranking_scrollable_frame, bg="#1e40af" if is_me else "#1f2937")
            row.pack(fill="x", padx=12, pady=4)

            rank_text = f"{medals[idx]} {idx+1}" if idx < 3 else str(idx+1)
            rank_color = "#fbbf24" if idx < 3 else "#9ca3af"
            
            tk.Label(row, text=rank_text, bg=row.cget("bg"), fg="#fff" if is_me else rank_color, font=("Segoe UI", 11, "bold"), width=4).pack(side="left", padx=8)
            tk.Label(row, text=username[:20], bg=row.cget("bg"), fg="#fff" if is_me else "#e5e7eb", font=("Segoe UI", 11, "bold" if is_me else "normal"), width=20, anchor="w").pack(side="left", padx=8)
            tk.Label(row, text=str(score), bg=row.cget("bg"), fg="#fff" if is_me else "#e5e7eb", font=("Segoe UI", 11, "bold" if is_me else "normal"), width=12).pack(side="left", padx=8)

        self.ranking_canvas.update_idletasks()
        self.ranking_canvas.configure(scrollregion=self.ranking_canvas.bbox("all"))
