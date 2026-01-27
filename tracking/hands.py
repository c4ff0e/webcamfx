import mediapipe as mp
import logging

MODULE_NAME = "HANDS"
logging.getLogger(__name__)

def hands_init(path, hand_conf, tracking_conf):
    BaseOptions = mp.tasks.BaseOptions
    HandLandmarker = mp.tasks.vision.HandLandmarker
    HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=path),
        running_mode=VisionRunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=hand_conf,
        min_tracking_confidence=tracking_conf
    )

    hands_detector = HandLandmarker.create_from_options(options)
    
    return hands_detector

def img_preprocess(frame_rgb):
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
    return mp_image

def track(hands_detector, mp_image, timestamp):
    result = hands_detector.detect_for_video(mp_image, timestamp)
    return result