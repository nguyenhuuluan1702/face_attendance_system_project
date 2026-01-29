# 📸 HƯỚNG DẪN SỬ DỤNG NHIỀU ẢNH CHO MỖI NGƯỜI

## ❓ Vấn đề đã khắc phục

**Vấn đề ban đầu:** Hệ thống không nhận diện được khi user thay đổi ngoại hình (tóc mái, râu, kính, v.v...)

**Giải pháp:** Hệ thống giờ hỗ trợ **lưu nhiều ảnh** cho cùng một người để tăng độ chính xác!

---

## 🎯 Cách đặt tên file

### ✅ ĐÚNG - Cách đặt tên để nhiều ảnh cùng 1 người:

```
known_faces/
├── user_a.jpg          ← Ảnh 1 của user_a
├── user_a_1.jpg        ← Ảnh 2 của user_a (có tóc mái)
├── user_a_2.jpg        ← Ảnh 3 của user_a (không tóc mái)
├── user_a_3.jpg        ← Ảnh 4 của user_a (đeo kính)
│
├── chi_minh.jpg        ← Ảnh 1 của chi_minh
├── chi_minh_1.jpg      ← Ảnh 2 của chi_minh
│
├── nguyen_luan.jpg     ← Ảnh 1 của nguyen_luan
└── nguyen_luan_1.jpg   ← Ảnh 2 của nguyen_luan
```

### ⚠️ QUY TẮC ĐẶT TÊN:

1. **Tên cơ bản**: `ten_nguoi.jpg` (ảnh đầu tiên)
2. **Ảnh bổ sung**: `ten_nguoi_1.jpg`, `ten_nguoi_2.jpg`, `ten_nguoi_3.jpg`, ...
3. Hệ thống sẽ tự động loại bỏ phần `_1`, `_2`, `_3` và nhóm chúng lại cùng 1 người

---

## 📋 Hướng dẫn chi tiết cho User A

### Bước 1: Chụp nhiều ảnh với các góc độ và kiểu dáng khác nhau

Chụp ít nhất **3-5 ảnh** của User A với:

- ✅ **Có tóc mái** (như ảnh hiện tại)
- ✅ **Không có tóc mái** (chải tóc ra sau hoặc cắt tóc)
- ✅ **Góc nghiêng trái**
- ✅ **Góc nghiêng phải**
- ✅ **Có/không đeo kính** (nếu có)
- ✅ **Nụ cười / Nghiêm túc**

### Bước 2: Đặt tên file theo quy tắc

Giả sử user A tên là "Nguyen Van A":

```
known_faces/
├── nguyen_van_a.jpg      ← Ảnh chính (có tóc mái)
├── nguyen_van_a_1.jpg    ← Ảnh không tóc mái
├── nguyen_van_a_2.jpg    ← Ảnh góc nghiêng
├── nguyen_van_a_3.jpg    ← Ảnh đeo kính
└── nguyen_van_a_4.jpg    ← Ảnh nụ cười
```

### Bước 3: ~~Xóa file cache cũ~~ **KHÔNG CẦN NỮA!** ✨

**🎉 TỰ ĐỘNG PHÁT HIỆN ẢNH MỚI!**

Hệ thống giờ đã thông minh hơn:
- ✅ Tự động phát hiện khi có ảnh mới
- ✅ Chỉ xử lý ảnh mới (không tốn thời gian)
- ✅ Tự động cập nhật cache
- ✅ **KHÔNG CẦN XÓA FILE PKL!**

~~Sau khi thêm ảnh mới, bạn PHẢI xóa file cache:~~

~~```bash
# Xóa file này
del face_embeddings.pkl
```~~

~~Hoặc trong PowerShell:
```powershell
Remove-Item face_embeddings.pkl
```~~

### Bước 4: Chạy lại hệ thống (chỉ thế thôi!)

```bash
python face_recognition_attendance.py
```

Hệ thống sẽ:
- **Tự động phát hiện ảnh mới** 🆕
- Chỉ xử lý các ảnh chưa có trong cache (nhanh!)
- Tự động cập nhật cache
- Hiển thị thống kê:
  ```
  🆕 Phát hiện 3 ảnh mới:
    + nguyen_van_a_1.jpg
    + nguyen_van_a_2.jpg
    + nguyen_van_a_3.jpg
  
  ⏳ Đang xử lý ảnh mới...
    ✓ nguyen_van_a_1.jpg -> nguyen_van_a
    ✓ nguyen_van_a_2.jpg -> nguyen_van_a
    ✓ nguyen_van_a_3.jpg -> nguyen_van_a
  
  📊 Tổng quan hệ thống:
    • Tổng số ảnh: 7
    • Số người: 3
      - nguyen_van_a: 5 ảnh
      - chi_minh: 1 ảnh
      - nguyen_luan: 1 ảnh
  ```

---

## 🔧 Cải tiến kỹ thuật

### 1. **Tự động phát hiện ảnh mới** 🆕 **MỚI!**
   - Không cần xóa file pkl khi thêm user mới
   - Hệ thống tự động so sánh ảnh hiện tại với cache
   - Chỉ xử lý ảnh mới → Tiết kiệm thời gian!
   - Tự động xóa embeddings của ảnh đã bị xóa

### 2. **So sánh với nhiều ảnh tham chiếu**
   - Trước: So sánh với 1 ảnh duy nhất
   - Sau: So sánh với TẤT CẢ ảnh của người đó và chọn kết quả tốt nhất

### 3. **Tăng ngưỡng nhận diện**
   - Tăng từ `7.0` lên `8.0` để linh hoạt hơn với thay đổi ngoại hình
   - Vẫn đảm bảo độ chính xác cao

### 4. **Thống kê chi tiết**
   - Hiển thị số lượng ảnh của mỗi người
   - Báo cáo ảnh mới được thêm vào
   - Báo cáo ảnh đã bị xóa
   - Dễ dàng kiểm tra xem đã thêm đủ ảnh chưa

---

## 📝 Ví dụ thực tế

### Trước khi cải tiến:
```
known_faces/
└── user_a.jpg  ← Chỉ có ảnh có tóc mái
```
➡️ **Kết quả:** Không nhận diện được khi user_a không để tóc mái

### Sau khi cải tiến:
```
known_faces/
├── user_a.jpg       ← Ảnh có tóc mái
├── user_a_1.jpg     ← Ảnh không tóc mái
└── user_a_2.jpg     ← Ảnh góc nghiêng
```
➡️ **Kết quả:** ✅ Nhận diện THÀNH CÔNG trong cả 2 trường hợp!

---

## ⚡ Tips để nhận diện tốt hơn

1. **Chất lượng ảnh:**
   - Ảnh rõ nét, không bị mờ
   - Ánh sáng tốt (không quá tối hoặc quá sáng)
   - Khuôn mặt chiếm ít nhất 1/3 ảnh

2. **Góc độ đa dạng:**
   - Thẳng mặt (0°)
   - Nghiêng nhẹ trái/phải (±15-30°)
   - Ngẩng/cúi nhẹ (±10-20°)

3. **Biểu cảm:**
   - Nghiêm túc (mặc định)
   - Nụ cười nhẹ
   - Không nên quá khác biệt (ví dụ: cười toe toét)

4. **Số lượng ảnh khuyến nghị:**
   - Tối thiểu: **3 ảnh** / người
   - Khuyến nghị: **5-7 ảnh** / người
   - Tối đa: **10 ảnh** / người (nhiều hơn không cần thiết)

---

## 🔄 Quy trình cập nhật khi thêm ảnh mới

```bash
# 1. Thêm ảnh mới vào thư mục known_faces
#    (Copy/paste ảnh vào thư mục)

# 2. Chạy lại hệ thống - HỆ THỐNG TỰ ĐỘNG PHÁT HIỆN! ✨
python face_recognition_attendance.py
```

**Không cần làm gì thêm!** Hệ thống sẽ:
- ✅ Tự động phát hiện ảnh mới
- ✅ Chỉ xử lý ảnh mới (tiết kiệm thời gian)
- ✅ Tự động cập nhật cache

---

## ❗ Lưu ý quan trọng

- ~~⚠️ **LUÔN XÓA `face_embeddings.pkl`** sau khi thêm/sửa/xóa ảnh~~ ✨ **KHÔNG CẦN NỮA!**
- ✅ Hệ thống **TỰ ĐỘNG** phát hiện thay đổi
- ⚠️ Đặt tên file đúng quy tắc: `ten_nguoi.jpg`, `ten_nguoi_1.jpg`, ...
- ⚠️ Không dùng ký tự đặc biệt trong tên file (dấu cách, @, #, ...)
- ⚠️ Định dạng ảnh: `.jpg`, `.jpeg`, hoặc `.png`

---

## 📞 Hỗ trợ

Nếu vẫn gặp vấn đề, kiểm tra:

1. ~~✅ Đã xóa `face_embeddings.pkl` chưa?~~ (Không cần nữa!)
2. ✅ Tên file có đúng quy tắc không?
3. ✅ Ảnh có rõ nét và đủ sáng không?
4. ✅ Khuôn mặt có rõ trong ảnh không?
5. ✅ Hệ thống có hiển thị "🆕 Phát hiện X ảnh mới" không?

**Chúc bạn sử dụng hiệu quả! 🎉**
