"""Giao diện chat"""
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
from .styles import setup_base_styles, create_dark_entry, create_button


class ChatView(ttk.Frame):
    def __init__(self, master, on_send, username: str = None):
        super().__init__(master, padding=8)
        self.on_send = on_send
        self.username = username
        setup_base_styles()
        self._build_widgets()

    def _build_widgets(self):
        self.configure(style="Card.TFrame")

        # Header
        header = tk.Frame(self, bg="#020617")
        header.pack(fill="x", pady=(0, 8))

        tk.Label(header, text="💬 Phòng Chat", bg="#020617", fg="#e5e7eb", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        if self.username:
            tk.Label(header, text=f"Tên: {self.username}", bg="#020617", fg="#9ca3af", font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 0))

        # Glow line
        glow = tk.Canvas(self, height=2, bg="#020617", highlightthickness=0, bd=0)
        glow.pack(fill="x", pady=(0, 8))
        glow.create_line(0, 1, 2000, 1, fill="#3b82f6")

        # Chat area - responsive
        chat_frame = tk.Frame(self, bg="#020617")
        chat_frame.pack(fill="both", expand=True, pady=(0, 8))

        self.msg_area = ScrolledText(
            chat_frame, state="disabled", wrap="word",
            bg="#0f172a", fg="#e5e7eb", font=("Segoe UI", 10),
            insertbackground="#3b82f6", selectbackground="#374151",
            relief="flat", borderwidth=0, padx=10, pady=10,
        )
        self.msg_area.pack(fill="both", expand=True)

        # Tags
        self.msg_area.tag_configure("system", foreground="#9ca3af", font=("Segoe UI", 9, "italic"))
        self.msg_area.tag_configure("timestamp", foreground="#6b7280", font=("Segoe UI", 8))
        self.msg_area.tag_configure("username", foreground="#3b82f6", font=("Segoe UI", 10, "bold"))
        self.msg_area.tag_configure("content", foreground="#e5e7eb", font=("Segoe UI", 10))
        self.msg_area.tag_configure("my_message", foreground="#22c55e", font=("Segoe UI", 10, "bold"))

        # Input
        input_frame = tk.Frame(self, bg="#020617")
        input_frame.pack(fill="x")

        self.input_var = tk.StringVar()
        self.input_entry = create_dark_entry(input_frame, self.input_var, "#3b82f6")
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 6), ipady=6)
        self.input_entry.bind("<Return>", lambda e: self._on_send())
        self.input_entry.focus()

        self.send_button = create_button(input_frame, "Gửi", "#3b82f6", self._on_send, padx=16, pady=6)
        self.send_button.pack(side="left")

    def _on_send(self):
        text = self.input_var.get().strip()
        if text and self.on_send:
            self.input_var.set("")
            self.on_send(text)

    def add_message(self, username: str, content: str, timestamp: str = None, system: bool = False):
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.msg_area.configure(state="normal")
        
        if system:
            self.msg_area.insert("end", f"[{timestamp}] ", "timestamp")
            self.msg_area.insert("end", "• ", "system")
            self.msg_area.insert("end", f"{content}\n", "system")
        else:
            is_mine = (username == self.username)
            self.msg_area.insert("end", f"[{timestamp}] ", "timestamp")
            self.msg_area.insert("end", f"{username}: ", "my_message" if is_mine else "username")
            self.msg_area.insert("end", f"{content}\n", "content")
        
        self.msg_area.configure(state="disabled")
        self.msg_area.yview_moveto(1.0)
