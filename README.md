# Chat and Guess Number Game

🎮 **Game đoán số multiplayer với chat real-time**

Dự án bài giữa kỳ môn Lập trình mạng - Kiến trúc Multi Client-Server sử dụng Socket.

## 📋 Tổng quan

Game cho phép nhiều người chơi cùng tham gia:
- **Chat real-time** với tất cả người chơi
- **Đoán số bí mật** từ 1-100 với gợi ý HIGH/LOW/CORRECT  
- **Bảng xếp hạng** theo điểm số
- **Giao diện đẹp** với dark theme

## 🚀 Cách chạy nhanh

### Tự động (Khuyến nghị)
```bash
python demo.py
```

### Thủ công
```bash
# Terminal 1: Khởi động server
python server/server.py

# Terminal 2: Khởi động client 1
python chat-guess-number/client/client.py

# Terminal 3: Khởi động client 2  
python chat-guess-number/client/client.py
```

## 🧪 Testing

```bash
# Chạy integration test (server phải đang chạy)
python server/test_integration.py
```

## 📁 Cấu trúc dự án

```
chat-guess-number/
├── server/
│   ├── server.py              # Server chính
│   ├── test_integration.py    # Integration tests
│   └── test_client.py         # Test client đơn giản
├── chat-guess-number/client/
│   ├── client.py              # Client chính
│   ├── gui.py                 # Giao diện người dùng
│   └── network.py             # Module mạng
├── demo.py                    # Script demo tự động
├── README.md                  # File này
└── SRS_ChatGuessNumber.md     # Tài liệu yêu cầu
```

## 🎯 Cách chơi

1. **Kết nối**: Nhập IP server (127.0.0.1) và port (5555)
2. **Đăng nhập**: Chọn username duy nhất
3. **Chat**: Gửi tin nhắn cho tất cả người chơi
4. **Đoán số**: Nhập số từ 1-100, nhận gợi ý HIGH/LOW/CORRECT
5. **Xem ranking**: Kiểm tra bảng xếp hạng theo điểm

## 🏆 Hệ thống điểm

- **Đoán đúng**: 10 - số lần đoán (tối thiểu 1 điểm)
- **Ví dụ**: Đoán đúng sau 3 lần = 7 điểm
- **Game mới** tự động bắt đầu sau khi có người thắng

## 🔧 Yêu cầu hệ thống

- **Python 3.7+**
- **Tkinter** (thường có sẵn với Python)
- **Hệ điều hành**: Windows/Linux/macOS

## 📡 Giao thức mạng

**Format**: Newline-delimited JSON qua TCP Socket

**Các loại message**:
- `LOGIN`: Đăng nhập với username
- `CHAT`: Tin nhắn chat
- `GUESS`: Đoán số (1-100)
- `RESULT`: Kết quả đoán (HIGH/LOW/CORRECT)
- `RANKING`: Cập nhật bảng xếp hạng
- `SYSTEM`: Thông báo hệ thống

## 🎨 Tính năng UI

- **Dark theme** hiện đại
- **Message bubbles** với màu sắc phân biệt
- **Real-time updates** cho chat và ranking
- **Responsive design** thích ứng kích thước cửa sổ
- **Hover effects** và animations

## 🧪 Tuần 4: Integration Testing & Bug Fixes

### ✅ Tests đã thực hiện:
- [x] Kết nối cơ bản server-client
- [x] Hệ thống đăng nhập (username duy nhất)
- [x] Chat real-time giữa nhiều client
- [x] Logic game đoán số với binary search
- [x] Xử lý nhiều client đồng thời (5+ clients)

### 🐛 Bugs đã sửa:
- [x] Port mặc định client (5000 → 5555)
- [x] Thiếu timestamp trong SYSTEM messages
- [x] Xử lý message format consistency

### 📊 Kết quả testing:
- **5/5 test cases PASS** (100%)
- **Hỗ trợ 10+ clients đồng thời**
- **Độ trễ < 500ms** cho mọi thao tác

## 👥 Thành viên nhóm

- **Backend Developer**: Server, game logic, protocol
- **Frontend Developer**: GUI, UX/UI, client network

## 📄 License

Dự án học tập - Môn Lập trình mạng