"""
GUI Module - Import tất cả views từ package views/
File này giữ lại để backward compatible với client.py
"""
from views import (
    ConnectionView,
    LoginView,
    ChatView,
    GameInterface,
    RankingView,
    MainGameView,
    RootWindow
)

__all__ = [
    'ConnectionView',
    'LoginView',
    'ChatView',
    'GameInterface',
    'RankingView',
    'MainGameView',
    'RootWindow'
]
