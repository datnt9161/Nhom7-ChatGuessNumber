# 🎮 Chat & Guess Number Game

Game đoán số kết hợp chat realtime, sử dụng Socket TCP theo mô hình Multi Client-Server.

## 📋 Mô tả

- **Server**: Xử lý nhiều client đồng thời, quản lý game và chat
- **Client**: Giao diện Tkinter với dark theme, hỗ trợ responsive

## 🎯 Tính năng

- 💬 Chat realtime giữa các người chơi
- 🔢 Game đoán số (1-100) với 10 lượt đoán
- 🏆 Bảng xếp hạng theo điểm
- 🎨 Giao diện dark theme, responsive với scrollbar

## 🚀 Cài đặt & Chạy

### Yêu cầu
- Python 3.8+

### Chạy Server
```bash
python server/server.py
```
Server chạy trên `0.0.0.0:5555`

### Chạy Client
```bash
python client/client.py
```

## 🎮 Cách chơi

1. Kết nối đến server (mặc định `localhost:5555`)
2. Đăng nhập với username
3. Gõ `!start` trong chat để bắt đầu game
4. Đoán số từ 1-100, có 10 lượt
5. Gợi ý: "Số bí mật CAO HƠN" hoặc "THẤP HƠN"

## � Tíunh điểm

- **Thắng**: `(11 - số lượt đã đoán) × 10` điểm
- **Thua**: 0 điểm

## 📁 Cấu trúc

```
├── server/
│   └── server.py           # Backend server
├── client/
│   ├── client.py           # Main client
│   ├── gui.py              # GUI wrapper
│   ├── network.py          # Socket client
│   └── views/              # UI components
│       ├── root_window.py
│       ├── main_game_view.py
│       ├── chat_view.py
│       ├── game_interface.py
│       ├── ranking_view.py
│       ├── connection_view.py
│       ├── login_view.py
│       └── styles.py
├── SRS_ChatGuessNumber.md  # Tài liệu SRS
└── README.md
```

## 📡 Protocol

JSON qua TCP, phân cách bằng newline (`\n`)

| Message | Mô tả |
|---------|-------|
| `LOGIN` | Đăng nhập |
| `CHAT` | Gửi tin nhắn |
| `GUESS` | Đoán số |
| `RANKING` | Lấy bảng xếp hạng |

## 👥 Nhóm phát triển

- **Backend**: Server, game logic, protocol
- **Frontend**: Client GUI, network handler
