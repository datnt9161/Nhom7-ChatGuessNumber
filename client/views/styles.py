"""Shared styles cho tất cả views"""
import tkinter as tk
from tkinter import ttk


def setup_base_styles():
    """Setup các style cơ bản dùng chung"""
    style = ttk.Style()
    
    if "vista" in style.theme_names():
        style.theme_use("vista")
    elif "clam" in style.theme_names():
        style.theme_use("clam")

    # Card chính
    style.configure("Card.TFrame", background="#020617")
    style.configure("Form.TFrame", background="#020617")

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

    # Button primary
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


def create_dark_entry(parent, textvariable, highlight_color="#22c55e"):
    """Tạo Entry với dark theme"""
    return tk.Entry(
        parent,
        textvariable=textvariable,
        font=("Segoe UI", 11),
        bg="#1e293b",
        fg="#f1f5f9",
        insertbackground=highlight_color,
        relief="flat",
        bd=0,
        highlightthickness=2,
        highlightbackground="#334155",
        highlightcolor=highlight_color,
    )


def create_button(parent, text, bg_color, command, **kwargs):
    """Tạo Button với style đẹp"""
    return tk.Button(
        parent,
        text=text,
        font=("Segoe UI", 10, "bold"),
        bg=bg_color,
        fg="#ffffff",
        activebackground=kwargs.get("active_bg", bg_color),
        activeforeground="#ffffff",
        relief="flat",
        bd=0,
        padx=kwargs.get("padx", 16),
        pady=kwargs.get("pady", 8),
        cursor="hand2",
        command=command,
    )
