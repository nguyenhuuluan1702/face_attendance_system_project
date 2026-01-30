"""
Advanced Liveness Detection Module
- Random Blink Detection
- Random Head Movement (Left/Right/Up/Down)
- Multi-Challenge System
- Texture Analysis
"""
import cv2
import numpy as np
import time
import random

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("⚠️ MediaPipe không có. Cài: pip install mediapipe")


class AdvancedLivenessDetector:
    """Phát hiện liveness với nhiều phương pháp kết hợp"""
    
    def __init__(self):
        if not MEDIAPIPE_AVAILABLE:
            raise ImportError("MediaPipe không được cài đặt")
        
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Landmark indices
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        self.NOSE_TIP = 1
        self.FOREHEAD = 10
        self.CHIN = 152
        self.LEFT_CHEEK = 234
        self.RIGHT_CHEEK = 454
        
        # Thresholds
        self.EAR_THRESHOLD = 0.22
        self.MOVEMENT_THRESHOLD = 0.15  # Tỷ lệ di chuyển so với kích thước khuôn mặt
        
        # State tracking
        self.initial_face_position = None
        
    def calculate_ear(self, eye_landmarks):
        """Tính Eye Aspect Ratio"""
        v1 = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
        v2 = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
        h = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])
        return (v1 + v2) / (2.0 * h)
    
    def detect_blink(self, frame):
        """Phát hiện nhấp nháy mắt"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return False, 0, 0
        
        face_landmarks = results.multi_face_landmarks[0]
        h, w = frame.shape[:2]
        
        # Lấy EAR
        left_eye = np.array([
            [face_landmarks.landmark[i].x * w, face_landmarks.landmark[i].y * h]
            for i in self.LEFT_EYE
        ])
        left_ear = self.calculate_ear(left_eye)
        
        right_eye = np.array([
            [face_landmarks.landmark[i].x * w, face_landmarks.landmark[i].y * h]
            for i in self.RIGHT_EYE
        ])
        right_ear = self.calculate_ear(right_eye)
        
        avg_ear = (left_ear + right_ear) / 2.0
        blink_detected = avg_ear < self.EAR_THRESHOLD
        
        return blink_detected, left_ear, right_ear
    
    def get_face_position(self, frame):
        """Lấy vị trí khuôn mặt (nose tip)"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return None
        
        face_landmarks = results.multi_face_landmarks[0]
        h, w = frame.shape[:2]
        
        nose = face_landmarks.landmark[self.NOSE_TIP]
        forehead = face_landmarks.landmark[self.FOREHEAD]
        chin = face_landmarks.landmark[self.CHIN]
        left_cheek = face_landmarks.landmark[self.LEFT_CHEEK]
        right_cheek = face_landmarks.landmark[self.RIGHT_CHEEK]
        
        # Normalize bằng kích thước khuôn mặt
        face_width = abs(right_cheek.x - left_cheek.x)
        face_height = abs(chin.y - forehead.y)
        
        return {
            'nose': (nose.x, nose.y),
            'forehead': (forehead.x, forehead.y),
            'chin': (chin.x, chin.y),
            'left_cheek': (left_cheek.x, left_cheek.y),
            'right_cheek': (right_cheek.x, right_cheek.y),
            'face_width': face_width,
            'face_height': face_height
        }
    
    def check_head_movement(self, current_pos, initial_pos, direction):
        """
        Kiểm tra xem đầu có di chuyển theo hướng yêu cầu không
        direction: 'left', 'right', 'up', 'down'
        """
        if current_pos is None or initial_pos is None:
            return False, 0
        
        nose_delta_x = current_pos['nose'][0] - initial_pos['nose'][0]
        nose_delta_y = current_pos['nose'][1] - initial_pos['nose'][1]
        
        # Normalize bằng kích thước khuôn mặt
        face_width = initial_pos['face_width']
        face_height = initial_pos['face_height']
        
        normalized_x = nose_delta_x / face_width if face_width > 0 else 0
        normalized_y = nose_delta_y / face_height if face_height > 0 else 0
        
        # Kiểm tra hướng
        if direction == 'left':
            movement = -normalized_x  # Di chuyển sang trái = x giảm
            return movement > self.MOVEMENT_THRESHOLD, movement
        elif direction == 'right':
            movement = normalized_x  # Di chuyển sang phải = x tăng
            return movement > self.MOVEMENT_THRESHOLD, movement
        elif direction == 'up':
            movement = -normalized_y  # Di chuyển lên = y giảm
            return movement > self.MOVEMENT_THRESHOLD, movement
        elif direction == 'down':
            movement = normalized_y  # Di chuyển xuống = y tăng
            return movement > self.MOVEMENT_THRESHOLD, movement
        
        return False, 0
    
    def detect_texture_quality(self, frame):
        """Phát hiện texture không tự nhiên (video/ảnh in)"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Laplacian variance
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = laplacian.var()
        
        # High frequency analysis
        f = np.fft.fft2(gray)
        fshift = np.fft.fftshift(f)
        magnitude = np.abs(fshift)
        high_freq = np.mean(magnitude[magnitude.shape[0]//4:3*magnitude.shape[0]//4,
                                     magnitude.shape[1]//4:3*magnitude.shape[1]//4])
        
        # Kiểm tra threshold
        texture_score = 0
        if variance > 100:
            texture_score += 0.5
        if high_freq > 1e6:
            texture_score += 0.5
        
        return texture_score >= 0.5, variance, high_freq
    
    def close(self):
        """Đóng face mesh"""
        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()


def perform_advanced_liveness_challenge(video_capture):
    """
    Thực hiện thử thách liveness nâng cao
    - Random challenge: Blink hoặc Head Movement
    - Texture analysis
    Returns: (success, message)
    """
    if not MEDIAPIPE_AVAILABLE:
        return False, "MediaPipe không có"
    
    try:
        detector = AdvancedLivenessDetector()
    except Exception as e:
        return False, f"Không thể khởi tạo detector: {e}"
    
    print("\n" + "="*60)
    print("🔐 THÔNG BÁO: Đang chuẩn bị thử thách liveness nâng cao...")
    print("="*60)
    
    # Random chọn loại challenge
    challenge_type = random.choice(['blink', 'head_movement'])
    if challenge_type == 'head_movement':
        direction = random.choice(['left', 'right', 'up', 'down'])
    
    # Chờ ngẫu nhiên 2-4 giây
    wait_time = random.uniform(2, 4)
    start_wait = time.time()
    
    # Lấy vị trí ban đầu
    initial_position = None
    
    while time.time() - start_wait < wait_time:
        ret, frame = video_capture.read()
        if not ret:
            detector.close()
            return False, "Không đọc được frame"
        
        # Lấy vị trí ban đầu cho head movement
        if challenge_type == 'head_movement' and initial_position is None:
            initial_position = detector.get_face_position(frame)
        
        cv2.putText(frame, "Chuyen bi...", (50, 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
        cv2.imshow('Face Recognition', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            detector.close()
            return False, "Người dùng hủy"
    
    # Hiển thị yêu cầu
    if challenge_type == 'blink':
        challenge_text = "NHAP NHAY MAT!"
        print("\n" + "="*60)
        print("👁️  YÊU CẦU: NHẤP NHÁY MẮT NGAY BÂY GIỜ!")
        print("="*60)
    else:
        direction_text = {
            'left': 'TRAI',
            'right': 'PHAI',
            'up': 'LEN',
            'down': 'XUONG'
        }
        challenge_text = f"XOAY DAU {direction_text[direction]}!"
        print("\n" + "="*60)
        print(f"🔄 YÊU CẦU: XOAY ĐẦU SANG {direction_text[direction]} NGAY!")
        print("="*60)
    
    start_challenge = time.time()
    timeout = 5
    success_frames = 0
    required_frames = 3  # Cần 3 frame liên tiếp
    
    # Texture check
    texture_passes = 0
    texture_checks = 0
    
    while time.time() - start_challenge < timeout:
        ret, frame = video_capture.read()
        if not ret:
            detector.close()
            return False, "Không đọc được frame"
        
        # Texture analysis
        texture_ok, variance, high_freq = detector.detect_texture_quality(frame)
        texture_checks += 1
        if texture_ok:
            texture_passes += 1
        
        # Challenge check
        challenge_passed = False
        debug_value = 0
        
        if challenge_type == 'blink':
            blink_detected, left_ear, right_ear = detector.detect_blink(frame)
            challenge_passed = blink_detected
            debug_value = (left_ear + right_ear) / 2
        else:
            current_position = detector.get_face_position(frame)
            if current_position and initial_position:
                movement_ok, movement_value = detector.check_head_movement(
                    current_position, initial_position, direction
                )
                challenge_passed = movement_ok
                debug_value = movement_value
        
        if challenge_passed:
            success_frames += 1
            color = (0, 255, 0)
            text = f"THANH CONG! ({success_frames}/{required_frames})"
        else:
            success_frames = 0
            color = (0, 165, 255)
            text = challenge_text
        
        # Hiển thị
        remaining = int(timeout - (time.time() - start_challenge))
        cv2.putText(frame, text, (50, 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        cv2.putText(frame, f"Con: {remaining}s", (50, 150),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"Value: {debug_value:.3f}", (50, 190),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Texture: {variance:.0f}", (50, 220),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('Face Recognition', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            detector.close()
            return False, "Người dùng hủy"
        
        # Kiểm tra thành công
        if success_frames >= required_frames:
            # Kiểm tra texture
            texture_ratio = texture_passes / texture_checks if texture_checks > 0 else 0
            if texture_ratio < 0.5:
                detector.close()
                print("\n❌ THẤT BẠI: Texture không tự nhiên (có thể là video/ảnh in)!")
                print(f"   Texture pass rate: {texture_ratio*100:.1f}%")
                return False, "Texture không tự nhiên"
            
            detector.close()
            print(f"\n✅ THÀNH CÔNG: Đã hoàn thành thử thách {challenge_type}!")
            return True, f"{challenge_type} challenge passed"
    
    # Timeout
    detector.close()
    print(f"\n❌ THẤT BẠI: Không hoàn thành thử thách trong thời gian quy định!")
    return False, f"Timeout - {challenge_type} challenge failed"


# Test độc lập
if __name__ == "__main__":
    if not MEDIAPIPE_AVAILABLE:
        print("❌ MediaPipe không được cài đặt!")
        print("Chạy: pip install mediapipe")
        exit(1)
    
    print("🎯 Test Advanced Liveness Detection")
    print("Nhấn 'q' để thoát\n")
    
    video = cv2.VideoCapture(0)
    
    try:
        success, message = perform_advanced_liveness_challenge(video)
        print(f"\nKết quả: {'✅ PASS' if success else '❌ FAIL'}")
        print(f"Message: {message}")
    finally:
        video.release()
        cv2.destroyAllWindows()
