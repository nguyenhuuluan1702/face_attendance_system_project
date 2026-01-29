# Hệ thống Nhận diện Khuôn mặt và Điểm danh Tự động

## 📋 Mô tả
Hệ thống nhận diện khuôn mặt realtime sử dụng OpenCV và face_recognition (dlib) để tự động điểm danh.

## 🔧 Công nghệ sử dụng
- **Python 3.7+**
- **OpenCV**: Xử lý video và hình ảnh
- **face_recognition (dlib)**: Nhận diện khuôn mặt
- **numpy**: Xử lý mảng
- **datetime**: Xử lý thời gian
- **csv**: Lưu trữ dữ liệu điểm danh

## ✨ Tính năng
1. ✅ Mở webcam và phát hiện khuôn mặt theo thời gian thực
2. ✅ Nhận diện khuôn mặt dựa trên dữ liệu đã lưu
3. ✅ Hiển thị tên người trên khung hình khi nhận diện đúng
4. ✅ Ghi điểm danh vào file CSV (Tên - Thời gian)
5. ✅ Mỗi người chỉ được điểm danh 1 lần/ngày
6. ✅ Vẽ khung chữ nhật màu xanh (đã biết) hoặc đỏ (chưa biết)

## 📦 Cài đặt

### Bước 1: Cài đặt thư viện
```bash
pip install -r requirements.txt
```

**Lưu ý**: Nếu gặp lỗi khi cài dlib trên Windows:
1. Tải Visual Studio Build Tools từ: https://visualstudio.microsoft.com/downloads/
2. Hoặc cài dlib từ wheel: https://github.com/sachadee/Dlib

### Bước 2: Chuẩn bị dữ liệu khuôn mặt

1. Tạo thư mục `known_faces` (sẽ tự động tạo khi chạy lần đầu)
2. Thêm ảnh khuôn mặt vào thư mục với format:
   - `TenNguoi.jpg` (VD: `NguyenVanA.jpg`, `TranThiB.png`)
   - Mỗi file ảnh nên chỉ có 1 khuôn mặt
   - Ảnh rõ nét, khuôn mặt nhìn thẳng

**Ví dụ cấu trúc thư mục:**
```
hand_gesture_recognition/
├── face_recognition_attendance.py
├── requirements.txt
├── known_faces/
│   ├── NguyenVanA.jpg
│   ├── TranThiB.jpg
│   └── LeVanC.png
└── attendance.csv (tự động tạo)
```

## 🚀 Chạy chương trình

```bash
python face_recognition_attendance.py
```

## 🎯 Cách sử dụng

1. Chạy chương trình
2. Webcam sẽ tự động bật
3. Đưa khuôn mặt vào camera
4. Hệ thống sẽ:
   - Nhận diện và hiển thị tên
   - Vẽ khung xanh (đã biết) hoặc đỏ (chưa biết)
   - Tự động điểm danh lần đầu trong ngày
   - Hiển thị "Da diem danh" nếu đã điểm danh
5. Nhấn **'Q'** để thoát

## 📊 File điểm danh

Dữ liệu điểm danh được lưu trong `attendance.csv`:

| Tên | Thời gian |
|-----|-----------|
| NguyenVanA | 2026-01-29 08:30:15 |
| TranThiB | 2026-01-29 08:35:22 |

## ⚙️ Tùy chỉnh

### Thay đổi độ chính xác nhận diện
Trong file `face_recognition_attendance.py`, dòng 149:
```python
tolerance=0.6  # Giảm = khắt khe hơn, Tăng = dễ dàng hơn (0.4-0.8)
```

### Thay đổi tốc độ xử lý
Dòng 131:
```python
# Thay đổi scale (0.25 = 1/4, 0.5 = 1/2)
small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
```

## 🔍 Xử lý sự cố

### Không tìm thấy webcam
- Kiểm tra webcam đã được cắm và driver đã cài đặt
- Thử thay đổi `cv2.VideoCapture(0)` thành `cv2.VideoCapture(1)`

### Không nhận diện được
- Đảm bảo ảnh trong `known_faces` rõ nét
- Thử tăng `tolerance` lên 0.7 hoặc 0.8
- Kiểm tra ánh sáng khi chụp và khi sử dụng

### Lỗi cài đặt dlib
- Windows: Cài Visual C++ Build Tools
- Mac: `brew install cmake`
- Linux: `sudo apt-get install build-essential cmake`

## 📝 Ghi chú
- Hệ thống xử lý mỗi frame thứ 2 để tăng tốc độ
- Mỗi người chỉ điểm danh 1 lần/ngày
- Dữ liệu điểm danh lưu vĩnh viễn trong CSV
- Code có comment đầy đủ bằng tiếng Việt

## 📄 License
MIT License
