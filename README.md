# Face Recognition Attendance System

Hệ thống điểm danh tự động sử dụng công nghệ nhận diện khuôn mặt.

## Tính năng

- ✅ Nhận diện khuôn mặt real-time qua webcam
- ✅ Tự động ghi điểm danh vào file CSV
- ✅ Hỗ trợ nhiều ảnh cho mỗi người
- ✅ Giao diện đơn giản, dễ sử dụng

## Yêu cầu hệ thống

- Python 3.7+
- Webcam
- Windows/Linux/MacOS

## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/nguyenhuuluan1702/face_attendance_system_project.git
cd face_attendance_system_project
```

2. Tạo môi trường ảo:
```bash
python -m venv .venv
```

3. Kích hoạt môi trường ảo:
- Windows:
```bash
.venv\Scripts\activate
```
- Linux/Mac:
```bash
source .venv/bin/activate
```

4. Cài đặt thư viện:
```bash
pip install -r requirements.txt
```

## Sử dụng

1. Thêm ảnh khuôn mặt vào thư mục `known_faces/`:
   - Tạo thư mục con theo tên người: `known_faces/TenNguoi/`
   - Thêm ảnh: `known_faces/TenNguoi/anh1.jpg`, `anh2.jpg`, ...

2. Chạy chương trình:
```bash
python face_recognition_attendance.py
```

3. Nhấn `q` để thoát

## Cấu trúc thư mục

```
face_attendance_system/
├── face_recognition_attendance.py  # File chính
├── requirements.txt                # Thư viện cần thiết
├── known_faces/                    # Thư mục chứa ảnh
│   ├── Person1/
│   │   ├── image1.jpg
│   │   └── image2.jpg
│   └── Person2/
│       └── image1.jpg
├── attendance.csv                  # File điểm danh (tự động tạo)
└── face_embeddings.pkl            # Cache dữ liệu (tự động tạo)
```

## Lưu ý

- Ảnh nên rõ nét, ánh sáng đủ
- Mỗi người nên có 2-5 ảnh từ nhiều góc độ
- File `attendance.csv` sẽ tự động tạo khi có người được nhận diện

## License

MIT License
