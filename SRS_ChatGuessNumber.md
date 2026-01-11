# Software Requirements Specification (SRS)
# Game Chat and Guess Number

## Thông tin dự án
- **Tên dự án:** Chat and Guess Number Game
- **Môn học:** Lập trình mạng
- **Loại bài tập:** Bài giữa kỳ
- **Số thành viên:** 2 người
- **Kiến trúc:** Multi Client-Server sử dụng Socket

---

## 1. Giới thiệu

### 1.1 Mục đích
Xây dựng một ứng dụng game đoán số kết hợp chat real-time, cho phép nhiều người chơi cùng tham gia qua mạng.

### 1.2 Phạm vi
- Server quản lý nhiều client đồng thời
- Người chơi có thể chat với nhau
- Người chơi đoán số do server sinh ra
- Hiển thị bảng xếp hạng

### 1.3 Công nghệ sử dụng
- **Backend:** Python/Java với Socket Programming
- **Frontend:** Python Tkinter / Java Swing / Web (HTML/CSS/JS)
- **Giao thức:** TCP Socket
- **Mô hình:** Multi-threaded Server

---

## 2. Mô tả tổng quan hệ thống

### 2.1 Kiến trúc hệ thống
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Client 1   │     │  Client 2   │     │  Client N   │
│  (Frontend) │     │  (Frontend) │     │  (Frontend) │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │ TCP Socket
                    ┌──────┴──────┐
                    │   SERVER    │
                    │  (Backend)  │
                    │             │
                    │ - Game Logic│
                    │ - Chat Room │
                    │ - Ranking   │
                    └─────────────┘
```

### 2.2 Luồng hoạt động chính
1. Client kết nối đến Server
2. Client đăng nhập với username
3. Client tham gia phòng chơi
4. Server sinh số ngẫu nhiên (1-100)
5. Các client đoán số và chat
6. Server phản hồi "Cao hơn" / "Thấp hơn" / "Chính xác"
7. Cập nhật điểm và bảng xếp hạng

---

## 3. Yêu cầu chức năng

### 3.1 Chức năng Server (Backend)
| ID | Chức năng | Mô tả |
|----|-----------|-------|
| S1 | Quản lý kết nối | Chấp nhận nhiều client kết nối đồng thời |
| S2 | Xác thực người dùng | Kiểm tra username hợp lệ, không trùng |
| S3 | Sinh số ngẫu nhiên | Tạo số bí mật từ 1-100 cho mỗi game |
| S4 | Xử lý đoán số | Nhận số từ client, so sánh và trả kết quả |
| S5 | Broadcast chat | Gửi tin nhắn đến tất cả client trong phòng |
| S6 | Quản lý điểm | Tính điểm dựa trên số lần đoán |
| S7 | Bảng xếp hạng | Lưu và gửi top người chơi |
| S8 | Quản lý phòng | Tạo/xóa phòng chơi, giới hạn người chơi |

### 3.2 Chức năng Client (Frontend)
| ID | Chức năng | Mô tả |
|----|-----------|-------|
| C1 | Kết nối server | Nhập IP/Port để kết nối |
| C2 | Đăng nhập | Nhập username để tham gia |
| C3 | Giao diện chat | Hiển thị và gửi tin nhắn |
| C4 | Giao diện đoán số | Input số và nút gửi |
| C5 | Hiển thị gợi ý | Hiện "Cao hơn"/"Thấp hơn" |
| C6 | Hiển thị ranking | Bảng xếp hạng real-time |
| C7 | Thông báo | Hiện thông báo thắng/thua |

---

## 4. Yêu cầu phi chức năng

| ID | Yêu cầu | Mô tả |
|----|---------|-------|
| NF1 | Hiệu năng | Server xử lý tối thiểu 10 client đồng thời |
| NF2 | Độ trễ | Thời gian phản hồi < 500ms |
| NF3 | Ổn định | Không crash khi client disconnect đột ngột |
| NF4 | Giao diện | UI thân thiện, dễ sử dụng |

---

## 5. Giao thức truyền thông

### 5.1 Định dạng message
```
{
    "type": "LOGIN|CHAT|GUESS|RESULT|RANKING|SYSTEM",
    "username": "player1",
    "content": "...",
    "timestamp": "2025-12-22T10:30:00"
}
```

### 5.2 Các loại message
| Type | Hướng | Mô tả |
|------|-------|-------|
| LOGIN | Client → Server | Đăng nhập với username |
| LOGIN_OK | Server → Client | Đăng nhập thành công |
| CHAT | Cả hai chiều | Tin nhắn chat |
| GUESS | Client → Server | Gửi số đoán |
| RESULT | Server → Client | Kết quả (HIGH/LOW/CORRECT) |
| RANKING | Server → Client | Cập nhật bảng xếp hạng |
| NEW_GAME | Server → All | Bắt đầu game mới |

---

## 6. Phân chia công việc

### 👤 Thành viên 1: Backend Developer

**Nhiệm vụ chính:**
| STT | Task | Mô tả | Thời gian |
|-----|------|-------|-----------|
| 1 | Setup Server | Tạo socket server, lắng nghe kết nối | 1 ngày |
| 2 | Multi-threading | Xử lý nhiều client đồng thời | 1 ngày |
| 3 | Game Logic | Sinh số, so sánh, tính điểm | 1 ngày |
| 4 | Chat System | Broadcast tin nhắn đến các client | 0.5 ngày |
| 5 | Ranking System | Lưu trữ và cập nhật điểm | 0.5 ngày |
| 6 | Protocol Design | Định nghĩa format message JSON | 0.5 ngày |
| 7 | Error Handling | Xử lý disconnect, lỗi kết nối | 0.5 ngày |
| 8 | Testing & Debug | Test với nhiều client | 1 ngày |

**Deliverables:**
- `server.py` hoặc `Server.java` - File server chính
- `game_logic.py` - Logic game đoán số
- `client_handler.py` - Xử lý từng client
- Documentation API

---

### 👤 Thành viên 2: Frontend Developer

**Nhiệm vụ chính:**
| STT | Task | Mô tả | Thời gian |
|-----|------|-------|-----------|
| 1 | UI Design | Thiết kế giao diện người dùng | 1 ngày |
| 2 | Connection Module | Kết nối đến server | 0.5 ngày |
| 3 | Login Screen | Màn hình nhập username, IP, Port | 0.5 ngày |
| 4 | Chat Interface | Khung chat, input, hiển thị tin nhắn | 1 ngày |
| 5 | Game Interface | Input đoán số, hiển thị gợi ý | 1 ngày |
| 6 | Ranking Display | Bảng xếp hạng real-time | 0.5 ngày |
| 7 | Notifications | Thông báo thắng/thua, lỗi | 0.5 ngày |
| 8 | Testing & Polish | Test UX, fix bugs | 1 ngày |

**Deliverables:**
- `client.py` hoặc `Client.java` - File client chính
- `gui.py` - Giao diện người dùng
- `network.py` - Module xử lý kết nối
- User Guide

---

## 7. Timeline dự kiến

```
Tuần 1: ████████████████████████████████
        Backend: Setup Server + Multi-threading
        Frontend: UI Design + Connection Module

Tuần 2: ████████████████████████████████
        Backend: Game Logic + Chat System
        Frontend: Login + Chat Interface

Tuần 3: ████████████████████████████████
        Backend: Ranking + Error Handling
        Frontend: Game Interface + Ranking Display

Tuần 4: ████████████████████████████████
        Cả hai: Integration Testing + Bug Fixes + Demo
```

---

## 8. Cấu trúc thư mục dự án

```
chat-guess-number/
├── server/
│   ├── server.py
│   ├── game_logic.py
│   ├── client_handler.py
│   └── config.py
├── client/
│   ├── client.py
│   ├── gui.py
│   ├── network.py
│   └── assets/
│       └── (images, icons)
├── docs/
│   ├── SRS.md
│   ├── API.md
│   └── UserGuide.md
└── README.md
```

---

## 9. Tiêu chí đánh giá

| Tiêu chí | Trọng số |
|----------|----------|
| Kết nối Multi-client hoạt động | 25% |
| Chức năng đoán số chính xác | 25% |
| Chat real-time hoạt động | 20% |
| Giao diện người dùng | 15% |
| Code quality & Documentation | 15% |

---

## 10. Rủi ro và giải pháp

| Rủi ro | Giải pháp |
|--------|-----------|
| Xung đột khi merge code | Sử dụng Git, chia branch rõ ràng |
| Không đồng bộ protocol | Thống nhất JSON format từ đầu |
| Client crash khi mất kết nối | Implement reconnect mechanism |
| Server quá tải | Giới hạn số client, optimize code |

---
