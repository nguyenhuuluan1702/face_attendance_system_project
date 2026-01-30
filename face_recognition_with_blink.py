"""
Hệ thống điểm danh nhận diện khuôn mặt với Blink Detection
Chống video replay bằng thử thách nhấp nháy mắt ngẫu nhiên
"""
import cv2
import numpy as np
import os
import pickle
from datetime import datetime
import re

# Lazy import để tránh conflict
def get_deepface():
    """Lazy import DeepFace"""
    from deepface import DeepFace
    return DeepFace

# Import module advanced liveness detection
try:
    from advanced_liveness_module import perform_advanced_liveness_challenge, MEDIAPIPE_AVAILABLE
    LIVENESS_DETECTION_ENABLED = MEDIAPIPE_AVAILABLE
except ImportError:
    LIVENESS_DETECTION_ENABLED = False
    print("⚠️ Module advanced_liveness_module không tìm thấy")


# ===========================
# CONSTANTS
# ===========================
KNOWN_FACES_DIR = "known_faces"
EMBEDDINGS_FILE = "face_embeddings.pkl"
ATTENDANCE_FILE = "attendance.csv"
THRESHOLD = 8.0  # Ngưỡng phát hiện
HAAR_CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'


# ===========================
# LOAD KNOWN FACES
# ===========================
def load_known_faces(force_reload=False):
    """
    Load embeddings của các khuôn mặt đã biết.
    Tự động phát hiện ảnh mới và cập nhật cache.
    Hỗ trợ nhiều ảnh cho mỗi người: user_a.jpg, user_a_1.jpg, user_a_2.jpg
    """
    embeddings = {}
    
    # Kiểm tra cache
    if os.path.exists(EMBEDDINGS_FILE) and not force_reload:
        with open(EMBEDDINGS_FILE, 'rb') as f:
            embeddings = pickle.load(f)
        print(f"✅ Đã load {len(embeddings)} embeddings từ cache")
    
    # Lấy danh sách file hiện tại
    current_files = {}
    if os.path.exists(KNOWN_FACES_DIR):
        for filename in os.listdir(KNOWN_FACES_DIR):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                filepath = os.path.join(KNOWN_FACES_DIR, filename)
                current_files[filename] = os.path.getmtime(filepath)
    
    # Kiểm tra file mới hoặc đã sửa
    need_update = False
    for filename, mtime in current_files.items():
        if filename not in embeddings or embeddings[filename][2] != mtime:
            need_update = True
            break
    
    # Kiểm tra file đã xóa
    for filename in list(embeddings.keys()):
        if filename not in current_files:
            del embeddings[filename]
            need_update = True
            print(f"❌ Đã xóa: {filename}")
    
    # Cập nhật nếu cần
    if need_update or force_reload:
        print("🔄 Đang cập nhật embeddings...")
        DeepFace = get_deepface()
        
        for filename, mtime in current_files.items():
            if filename not in embeddings or embeddings[filename][2] != mtime:
                filepath = os.path.join(KNOWN_FACES_DIR, filename)
                
                # Lấy tên (xóa _số và extension)
                name = os.path.splitext(filename)[0]
                name = re.sub(r'_\d+$', '', name)  # Xóa _1, _2, ...
                
                try:
                    # Tính embedding
                    result = DeepFace.represent(
                        img_path=filepath,
                        model_name="Facenet",
                        enforce_detection=False
                    )
                    embedding = result[0]["embedding"]
                    embeddings[filename] = (name, embedding, mtime)
                    print(f"✅ Đã load: {filename} -> {name}")
                except Exception as e:
                    print(f"❌ Lỗi khi load {filename}: {e}")
        
        # Lưu cache
        with open(EMBEDDINGS_FILE, 'wb') as f:
            pickle.dump(embeddings, f)
        print(f"💾 Đã lưu {len(embeddings)} embeddings vào cache")
    
    return embeddings


# ===========================
# FACE RECOGNITION
# ===========================
def recognize_face(face_embedding, known_embeddings):
    """
    So sánh embedding với database.
    Hỗ trợ nhiều ảnh cho mỗi người.
    """
    best_match = None
    min_distance = float('inf')
    
    # Group embeddings theo tên
    name_embeddings = {}
    for filename, (name, embedding, _) in known_embeddings.items():
        if name not in name_embeddings:
            name_embeddings[name] = []
        name_embeddings[name].append(embedding)
    
    # So sánh với từng người (lấy khoảng cách nhỏ nhất trong tất cả ảnh)
    for name, embeddings_list in name_embeddings.items():
        for ref_embedding in embeddings_list:
            distance = np.linalg.norm(
                np.array(face_embedding) - np.array(ref_embedding)
            )
            
            if distance < min_distance:
                min_distance = distance
                best_match = name
    
    # Kiểm tra threshold
    if min_distance < THRESHOLD:
        return best_match, min_distance
    else:
        return "Unknown", min_distance


# ===========================
# ATTENDANCE LOGGING
# ===========================
def log_attendance(name):
    """Ghi nhận điểm danh vào CSV"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    # Kiểm tra đã điểm danh hôm nay chưa
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if name in line and date_str in line:
                    print(f"ℹ️  {name} đã điểm danh hôm nay")
                    return False
    
    # Ghi attendance
    with open(ATTENDANCE_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{name},{date_str},{time_str}\n")
    
    print(f"✅ Đã ghi nhận điểm danh: {name} - {date_str} {time_str}")
    return True


# ===========================
# MAIN
# ===========================
def main():
    print("="*60)
    print("   HỆ THỐNG ĐIỂM DANH NHẬN DIỆN KHUÔN MẶT")
    print("   Advanced Liveness Detection - Chống Video Replay")
    print("="*60)
    
    # Kiểm tra MediaPipe
    if not LIVENESS_DETECTION_ENABLED:
        print("\n⚠️ CẢNH BÁO: Advanced Liveness Detection không khả dụng!")
        print("   Hệ thống sẽ chạy KHÔNG CÓ anti-spoofing")
        print("   Cài đặt: pip install mediapipe")
        response = input("\nTiếp tục không có liveness detection? (y/n): ")
        if response.lower() != 'y':
            print("❌ Đã hủy")
            return
    else:
        print("\n✅ Advanced Liveness Detection: Đã kích hoạt")
        print("   - Random Blink Challenge")
        print("   - Random Head Movement Challenge")
        print("   - Texture Analysis")
    
    # Load known faces
    print(f"\n📂 Đang load khuôn mặt từ: {KNOWN_FACES_DIR}")
    known_embeddings = load_known_faces()
    
    if not known_embeddings:
        print(f"❌ Không có khuôn mặt nào trong {KNOWN_FACES_DIR}")
        return
    
    # Hiển thị danh sách
    names = set()
    for filename, (name, _, _) in known_embeddings.items():
        names.add(name)
    print(f"\n👥 Có {len(names)} người: {', '.join(sorted(names))}")
    print(f"📷 Tổng {len(known_embeddings)} ảnh tham chiếu")
    
    # Khởi tạo camera và face detector
    print("\n📹 Đang khởi động camera...")
    video_capture = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    
    print("\n" + "="*60)
    print("HƯỚNG DẪN SỬ DỤNG:")
    print("- Đưa khuôn mặt vào trước camera")
    print("- Nhấn SPACE để bắt đầu nhận diện")
    if LIVENESS_DETECTION_ENABLED:
        print("- Làm theo hướng dẫn: Nhấp nháy mắt HOẶC Xoay đầu")
        print("  (Hệ thống sẽ chọn ngẫu nhiên)")
    print("- Nhấn 'q' để thoát")
    print("="*60 + "\n")
    
    DeepFace = get_deepface()
    
    try:
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("❌ Không đọc được frame từ camera")
                break
            
            # Detect faces
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100)
            )
            
            # Vẽ khung
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Nhan SPACE de nhan dien", 
                           (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (0, 255, 0), 2)
            
            # Hiển thị
            cv2.putText(frame, "Nhan SPACE: Nhan dien | Q: Thoat",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (255, 255, 255), 2)
            
            cv2.imshow('Face Recognition', frame)
            
            # Xử lý phím
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\n👋 Đã thoát")
                break
            
            elif key == ord(' '):  # SPACE
                if len(faces) == 0:
                    print("❌ Không phát hiện khuôn mặt!")
                    continue
                
                print("\n" + "="*60)
                print("🔍 BẮT ĐẦU NHẬN DIỆN...")
                print("="*60)
                
                # Liveness Detection (nếu có)
                if LIVENESS_DETECTION_ENABLED:
                    print("\n🔐 Thực hiện Advanced Liveness Detection...")
                    success, message = perform_advanced_liveness_challenge(video_capture)
                    
                    if not success:
                        print(f"\n❌ THẤT BẠI: {message}")
                        print("⚠️  Có thể là video replay hoặc ảnh in!")
                        continue
                    
                    print(f"\n✅ Liveness Check: PASSED")
                
                # Nhận diện
                print("\n🔍 Đang nhận diện khuôn mặt...")
                try:
                    # Lấy embedding
                    result = DeepFace.represent(
                        img_path=frame,
                        model_name="Facenet",
                        enforce_detection=False
                    )
                    
                    if not result:
                        print("❌ Không detect được khuôn mặt")
                        continue
                    
                    face_embedding = result[0]["embedding"]
                    
                    # So sánh
                    name, distance = recognize_face(face_embedding, known_embeddings)
                    
                    print(f"\n📊 Kết quả:")
                    print(f"   Người: {name}")
                    print(f"   Distance: {distance:.2f}")
                    print(f"   Threshold: {THRESHOLD}")
                    
                    if name != "Unknown":
                        print(f"\n✅ XIN CHÀO, {name.upper()}!")
                        log_attendance(name)
                    else:
                        print(f"\n❌ KHÔNG NHẬN DIỆN ĐƯỢC")
                        print(f"   (Distance {distance:.2f} > Threshold {THRESHOLD})")
                
                except Exception as e:
                    print(f"❌ Lỗi khi nhận diện: {e}")
                
                print("="*60)
    
    finally:
        video_capture.release()
        cv2.destroyAllWindows()
        print("\n✅ Đã đóng camera")


if __name__ == "__main__":
    main()
