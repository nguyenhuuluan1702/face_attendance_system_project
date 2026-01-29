"""
Hệ thống nhận diện khuôn mặt và điểm danh tự động
Sử dụng OpenCV và DeepFace (KHÔNG CẦN DLIB)
"""

import cv2
import numpy as np
import os
from datetime import datetime
import csv
from deepface import DeepFace
import pickle

class FaceRecognitionAttendance:
    def __init__(self, known_faces_folder="known_faces", attendance_file="attendance.csv"):
        """
        Khởi tạo hệ thống nhận diện khuôn mặt
        
        Args:
            known_faces_folder: Thư mục chứa ảnh khuôn mặt đã biết
            attendance_file: File CSV lưu trữ điểm danh
        """
        self.known_faces_folder = known_faces_folder
        self.attendance_file = attendance_file
        self.embeddings_file = "face_embeddings.pkl"
        
        # Danh sách embedding và tên
        self.known_face_data = []  # [(name, embedding, image_path), ...]
        
        # Danh sách người đã điểm danh hôm nay
        self.today_attendance = set()
        
        # Model để detect face
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Tạo thư mục known_faces nếu chưa có
        if not os.path.exists(self.known_faces_folder):
            os.makedirs(self.known_faces_folder)
            print(f"Đã tạo thư mục {self.known_faces_folder}")
            print("Vui lòng thêm ảnh khuôn mặt vào thư mục này!")
        
        # Load dữ liệu điểm danh hôm nay
        self.load_today_attendance()
        
        # Load và encode khuôn mặt
        self.load_known_faces()
    
    def load_known_faces(self):
        """
        Load tất cả ảnh từ thư mục known_faces và tạo embeddings
        TỰ ĐỘNG PHÁT HIỆN ẢNH MỚI: Không cần xóa file pkl khi thêm user mới!
        HỖ TRỢ NHIỀU ẢNH CHO MỘT NGƯỜI: 
        - user_a.jpg, user_a_1.jpg, user_a_2.jpg -> cùng là "user_a"
        - Giúp nhận diện tốt hơn khi có thay đổi ngoại hình (tóc, râu, kính...)
        """
        print("Đang kiểm tra và load embeddings...")
        print("(Lần đầu sẽ tải model, có thể mất vài phút...)\n")
        
        # Lấy danh sách file ảnh hiện tại trong thư mục
        current_image_files = set([f for f in os.listdir(self.known_faces_folder) 
                                   if f.endswith(('.jpg', '.jpeg', '.png'))])
        
        if not current_image_files:
            print(f"CẢNH BÁO: Không tìm thấy ảnh nào trong thư mục {self.known_faces_folder}")
            return
        
        # Dictionary để lưu embeddings đã có: {filename: (name, embedding, path)}
        cached_embeddings = {}
        
        # Kiểm tra xem đã có file embeddings chưa
        if os.path.exists(self.embeddings_file):
            try:
                with open(self.embeddings_file, 'rb') as f:
                    data = pickle.load(f)
                    
                    # Xử lý format cũ (list) hoặc format mới (dict)
                    if isinstance(data, dict):
                        cached_embeddings = data
                    else:
                        # Chuyển đổi format cũ sang format mới
                        for name, embedding, path in data:
                            filename = os.path.basename(path)
                            cached_embeddings[filename] = (name, embedding, path)
                
                print(f"✓ Đã load {len(cached_embeddings)} embedding từ cache")
            except Exception as e:
                print(f"⚠ Không thể load cache: {str(e)}, sẽ tạo mới...")
                cached_embeddings = {}
        
        # Tìm các file mới cần xử lý
        cached_files = set(cached_embeddings.keys())
        new_files = current_image_files - cached_files
        deleted_files = cached_files - current_image_files
        
        # Báo cáo thay đổi
        if new_files:
            print(f"🆕 Phát hiện {len(new_files)} ảnh mới:")
            for f in sorted(new_files):
                print(f"  + {f}")
        
        if deleted_files:
            print(f"🗑️  Phát hiện {len(deleted_files)} ảnh đã xóa:")
            for f in sorted(deleted_files):
                print(f"  - {f}")
        
        if not new_files and not deleted_files:
            print("✓ Không có thay đổi, sử dụng cache hiện có")
        
        # Xử lý các file mới
        if new_files:
            print("\n⏳ Đang xử lý ảnh mới...")
            import re
            
            for filename in sorted(new_files):
                try:
                    image_path = os.path.join(self.known_faces_folder, filename)
                    
                    # Tạo embedding bằng DeepFace
                    embedding_objs = DeepFace.represent(
                        img_path=image_path,
                        model_name="Facenet",
                        enforce_detection=False
                    )
                    
                    if embedding_objs and len(embedding_objs) > 0:
                        embedding = embedding_objs[0]["embedding"]
                        
                        # Lấy tên từ tên file (bỏ phần extension và số phía sau)
                        name_with_ext = os.path.splitext(filename)[0]
                        name = re.sub(r'_\d+$', '', name_with_ext)
                        
                        cached_embeddings[filename] = (name, embedding, image_path)
                        print(f"  ✓ {filename} -> {name}")
                    else:
                        print(f"  ✗ Không tìm thấy khuôn mặt: {filename}")
                except Exception as e:
                    print(f"  ✗ Lỗi {filename}: {str(e)}")
        
        # Xóa các file đã bị xóa khỏi cache
        for filename in deleted_files:
            del cached_embeddings[filename]
        
        # Chuyển đổi sang format list để sử dụng
        self.known_face_data = [(name, emb, path) 
                                for name, emb, path in cached_embeddings.values()]
        
        # Lưu lại cache (format dict để dễ kiểm tra)
        if self.known_face_data:
            with open(self.embeddings_file, 'wb') as f:
                pickle.dump(cached_embeddings, f)
            if new_files or deleted_files:
                print("\n✓ Đã cập nhật cache")
        
        # Thống kê
        person_counts = {}
        for name, _, _ in self.known_face_data:
            person_counts[name] = person_counts.get(name, 0) + 1
        
        print(f"\n📊 Tổng quan hệ thống:")
        print(f"  • Tổng số ảnh: {len(self.known_face_data)}")
        print(f"  • Số người: {len(person_counts)}")
        for person, count in sorted(person_counts.items()):
            print(f"    - {person}: {count} ảnh")
        print()
    
    def load_today_attendance(self):
        """
        Load danh sách người đã điểm danh hôm nay
        """
        if not os.path.exists(self.attendance_file):
            return
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        with open(self.attendance_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    # Kiểm tra xem có phải điểm danh hôm nay không
                    timestamp = row[1]
                    if timestamp.startswith(today):
                        self.today_attendance.add(row[0])
    
    def mark_attendance(self, name):
        """
        Ghi nhận điểm danh vào file CSV
        
        Args:
            name: Tên người điểm danh
        """
        # Kiểm tra đã điểm danh hôm nay chưa
        if name in self.today_attendance:
            return False
        
        # Ghi vào file CSV
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Tạo file mới nếu chưa có
        file_exists = os.path.exists(self.attendance_file)
        
        with open(self.attendance_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Ghi header nếu file mới
            if not file_exists:
                writer.writerow(['Tên', 'Thời gian'])
            
            # Ghi dữ liệu điểm danh
            writer.writerow([name, timestamp])
        
        # Thêm vào danh sách đã điểm danh
        self.today_attendance.add(name)
        print(f"✓ Điểm danh thành công: {name} - {timestamp}")
        
        return True
    
    def recognize_face(self, face_img):
        """
        Nhận diện khuôn mặt sử dụng DeepFace
        So sánh với TẤT CẢ CÁC ẢNH của mỗi người để tìm kết quả tốt nhất
        
        Args:
            face_img: Ảnh khuôn mặt cần nhận diện
            
        Returns:
            Tên người hoặc "Unknown"
        """
        try:
            # Tạo embedding cho khuôn mặt hiện tại
            current_embedding = DeepFace.represent(
                img_path=face_img,
                model_name="Facenet",
                enforce_detection=False
            )
            
            if not current_embedding:
                return "Unknown"
            
            current_emb = np.array(current_embedding[0]["embedding"])
            
            # Dictionary lưu khoảng cách TỐT NHẤT cho mỗi người
            # {name: min_distance}
            person_best_distances = {}
            
            # So sánh với tất cả embeddings
            for name, known_emb, image_path in self.known_face_data:
                # Tính khoảng cách Euclidean
                distance = np.linalg.norm(current_emb - np.array(known_emb))
                
                # Lưu khoảng cách nhỏ nhất cho mỗi người
                if name not in person_best_distances or distance < person_best_distances[name]:
                    person_best_distances[name] = distance
            
            # Tìm người có khoảng cách nhỏ nhất
            if not person_best_distances:
                return "Unknown"
            
            best_match_name = min(person_best_distances, key=person_best_distances.get)
            min_distance = person_best_distances[best_match_name]
            
            # Ngưỡng để xác định có khớp hay không
            # Giảm xuống 8.0 vì giờ có nhiều ảnh tham chiếu hơn
            threshold = 8.0
            
            if min_distance < threshold:
                return best_match_name
            else:
                return "Unknown"
                
        except:
            return "Unknown"
    
    def run(self):
        """
        Chạy hệ thống nhận diện khuôn mặt realtime
        """
        if not self.known_face_data:
            print("Không có dữ liệu khuôn mặt để nhận diện!")
            print(f"Vui lòng thêm ảnh vào thư mục {self.known_faces_folder}")
            return
        
        print("Đang khởi động webcam...")
        print("Nhấn 'q' để thoát\n")
        
        # Mở webcam
        video_capture = cv2.VideoCapture(0)
        
        if not video_capture.isOpened():
            print("Không thể mở webcam!")
            return
        
        # Biến để tối ưu hiệu suất
        frame_count = 0
        face_names = []
        face_locations = []
        
        while True:
            # Đọc frame từ webcam
            ret, frame = video_capture.read()
            
            if not ret:
                print("Không thể đọc frame từ webcam!")
                break
            
            frame_count += 1
            
            # Xử lý mỗi 10 frame để tăng tốc độ
            if frame_count % 10 == 0:
                # Convert sang grayscale để detect face
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(60, 60)
                )
                
                face_locations = []
                face_names = []
                
                # Nhận diện từng khuôn mặt
                for (x, y, w, h) in faces:
                    # Lưu vị trí
                    face_locations.append((x, y, w, h))
                    
                    # Cắt ảnh khuôn mặt
                    face_img = frame[y:y+h, x:x+w]
                    
                    # Nhận diện
                    name = self.recognize_face(face_img)
                    face_names.append(name)
                    
                    # Ghi điểm danh nếu nhận diện được
                    if name != "Unknown":
                        self.mark_attendance(name)
            
            # Vẽ kết quả lên frame
            for (x, y, w, h), name in zip(face_locations, face_names):
                # Chọn màu: xanh lá nếu đã biết, đỏ nếu không biết
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                
                # Vẽ khung chữ nhật quanh khuôn mặt
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                
                # Vẽ nền cho tên
                cv2.rectangle(frame, (x, y+h-35), (x+w, y+h), color, cv2.FILLED)
                
                # Hiển thị tên
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (x + 6, y+h - 6), font, 0.8, (255, 255, 255), 1)
                
                # Hiển thị trạng thái điểm danh
                if name != "Unknown" and name in self.today_attendance:
                    cv2.putText(frame, "Da diem danh", (x, y - 10), 
                              font, 0.5, (0, 255, 0), 1)
            
            # Hiển thị số người đã điểm danh hôm nay
            info_text = f"Da diem danh: {len(self.today_attendance)} nguoi"
            cv2.putText(frame, info_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Hiển thị frame
            cv2.imshow('He thong nhan dien khuon mat - Nhan Q de thoat', frame)
            
            # Nhấn 'q' để thoát
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Giải phóng tài nguyên
        video_capture.release()
        cv2.destroyAllWindows()
        
        print("\n✓ Đã dừng hệ thống")
        print(f"Tổng số người đã điểm danh hôm nay: {len(self.today_attendance)}")

# Chạy chương trình
if __name__ == "__main__":
    print("=" * 60)
    print("HỆ THỐNG NHẬN DIỆN KHUÔN MẶT VÀ ĐIỂM DANH TỰ ĐỘNG")
    print("=" * 60)
    print()
    
    # Khởi tạo và chạy hệ thống
    system = FaceRecognitionAttendance()
    system.run()
