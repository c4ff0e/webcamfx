import time
import cv2
import mediapipe as mp

# путь к скачанному hand_landmarker.task
MODEL_PATH = "hand_landmarker.task"

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.6,
    min_tracking_confidence=0.6,
)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Не удалось открыть камеру (VideoCapture(0)).")

with HandLandmarker.create_from_options(options) as landmarker:
    while True:
        ok, frame_bgr = cap.read()
        if not ok:
            break

        # MediaPipe ожидает SRGB
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        timestamp_ms = int(time.time() * 1000)
        result = landmarker.detect_for_video(mp_image, timestamp_ms)

        # result.hand_landmarks: список рук; каждая рука = список landmark'ов (x,y,z в нормализованных координатах)
        h, w = frame_bgr.shape[:2]
        if result.hand_landmarks:
            for hand in result.hand_landmarks:
                for lm in hand:
                    x, y = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame_bgr, (x, y), 2, (0, 255, 0), -1)
                    cv2.putText(frame_bgr, f"{lm.z:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)


        cv2.imshow("HandLandmarker (MediaPipe Tasks)", frame_bgr)
        if cv2.waitKey(1) & 0xFF == 27:  # Esc
            break

cap.release()
cv2.destroyAllWindows()
