# 🎯 Face Recognition Attendance System with Advanced Anti-Spoofing

Hệ thống điểm danh tự động sử dụng công nghệ nhận diện khuôn mặt với khả năng chống giả mạo nâng cao.

## ✨ Tính năng

- ✅ **Nhận diện khuôn mặt** real-time qua webcam (DeepFace + FaceNet)
- ✅ **Advanced Liveness Detection** - Chống video replay:
  - 🎲 Random Challenge: Blink HOẶC Head Movement
  - ↔️ 4 hướng xoay đầu ngẫu nhiên (Trái/Phải/Lên/Xuống)
  - 📊 Texture Analysis tích hợp
  - 🔐 MediaPipe Face Mesh tracking
- ✅ **Hỗ trợ nhiều ảnh cho mỗi người** (user.jpg, user_1.jpg, user_2.jpg)
- ✅ **Auto-cache embeddings** - Không cần xóa cache khi thêm ảnh mới
- ✅ **Tự động ghi điểm danh** vào CSV với timestamp

## 🛡️ Bảo vệ khỏi

- ✅ Ảnh in (printed photos)
- ✅ Ảnh trên màn hình (screen display)
- ✅ **Video replay** (kể cả video có nhấp nháy mắt)
- ✅ Deep fake cơ bản

## 📋 Yêu cầu hệ thống

- Python 3.11+ (khuyến nghị)
- Webcam
- Windows/Linux/MacOS
- RAM: 4GB+
- CPU: Core i5 hoặc tương đương

## 🚀 Cài đặt

### Phương pháp 1: Setup tự động (KHUYẾN NGHỊ)

**Windows:**
```cmd
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

Script sẽ tự động:
- ✅ Kiểm tra Python 3.11+
- ✅ Tạo virtual environment (.venv)
- ✅ Cài đặt đúng phiên bản thư viện
- ✅ Xác minh cài đặt thành công

### Phương pháp 2: Setup thủ công

**Bước 1:** Clone repository
```bash
git clone https://github.com/nguyenhuuluan1702/face_attendance_system_project.git
cd face_attendance_system_project
```

**Bước 2:** Tạo môi trường ảo
```bash
python -m venv .venv
```

**Bước 3:** Kích hoạt môi trường ảo

*Windows (CMD):*
```cmd
.venv\Scripts\activate.bat
```

*Windows (PowerShell):*
```powershell
.venv\Scripts\Activate.ps1
```

*Linux/Mac:*
```bash
source .venv/bin/activate
```

**Bước 4:** Cài đặt thư viện
```bash
pip install -r requirements.txt
```

**⚠️ Lưu ý quan trọng:**
- Hệ thống yêu cầu **MediaPipe 0.10.9** và **TensorFlow 2.16.1**
- Nếu gặp lỗi protobuf, chạy:
```bash
pip install mediapipe==0.10.9 protobuf==3.20.3 tensorflow==2.16.1 tf-keras==2.16.0
```

## 💻 Sử dụng

### Thêm ảnh tham chiếu

Thêm ảnh khuôn mặt vào thư mục `known_faces/`:

**Cách 1: Một ảnh cho mỗi người**
```
known_faces/
├── NguyenVanA.jpg
├── TranThiB.jpg
└── LeVanC.jpg
```

**Cách 2: Nhiều ảnh cho mỗi người (KHUYẾN NGHỊ)**
```
known_faces/
├── NguyenVanA.jpg
├── NguyenVanA_1.jpg      # Với tóc khác
├── NguyenVanA_2.jpg      # Với kính
├── TranThiB.jpg
└── TranThiB_1.jpg
```

### Chạy hệ thống

**Cách 1: Sử dụng script (ĐƠN GIẢN NHẤT)**

*Windows:*
```cmd
run.bat
```

*Linux/Mac:*
```bash
chmod +x run.sh
./run.sh
```

**Cách 2: Chạy trực tiếp**

*Sau khi activate virtual environment:*
```bash
python face_recognition_with_blink.py
```


