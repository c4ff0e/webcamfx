import mediapipe as mp
import logging
from dataclasses import dataclass

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
    hands_result = hands_detector.detect_for_video(mp_image, timestamp)
    hands_lm = hands_result.hand_landmarks[0] if hands_result.hand_landmarks else None
    return hands_result, hands_lm

@dataclass
class pos2d:
    x: int
    y: int

@dataclass
class HandsPos:
    wrist: pos2d
    thumb_cmc: pos2d
    thumb_mcp: pos2d
    thumb_ip: pos2d
    thumb_tip: pos2d
    index_finger_mcp: pos2d
    index_finger_pip: pos2d
    index_finger_dip: pos2d
    index_finger_tip: pos2d
    middle_finger_mcp: pos2d
    middle_finger_pip: pos2d
    middle_finger_dip: pos2d
    middle_finger_tip: pos2d
    ring_finger_mcp: pos2d
    ring_finger_pip: pos2d
    ring_finger_dip: pos2d
    ring_finger_tip: pos2d
    pinky_mcp: pos2d
    pinky_pip: pos2d
    pinky_dip: pos2d
    pinky_tip: pos2d
    
    def landmarks(self):
        return [
            self.wrist,
            self.thumb_cmc,
            self.thumb_mcp,
            self.thumb_ip,
            self.thumb_tip,
            self.index_finger_mcp,
            self.index_finger_pip,
            self.index_finger_dip,
            self.index_finger_tip,
            self.middle_finger_mcp,
            self.middle_finger_pip,
            self.middle_finger_dip,
            self.middle_finger_tip,
            self.ring_finger_mcp,
            self.ring_finger_pip,
            self.ring_finger_dip,
            self.ring_finger_tip,
            self.pinky_mcp,
            self.pinky_pip,
            self.pinky_dip,
            self.pinky_tip
        ]

WRIST = 0
THUMB_CMC = 1
THUMB_MCP = 2
THUMB_IP = 3
THUMB_TIP = 4
INDEX_FINGER_MCP = 5
INDEX_FINGER_PIP = 6
INDEX_FINGER_DIP = 7
INDEX_FINGER_TIP = 8
MIDDLE_FINGER_MCP = 9
MIDDLE_FINGER_PIP = 10
MIDDLE_FINGER_DIP = 11
MIDDLE_FINGER_TIP = 12
RING_FINGER_MCP = 13
RING_FINGER_PIP = 14
RING_FINGER_DIP = 15
RING_FINGER_TIP = 16
PINKY_MCP = 17
PINKY_PIP = 18
PINKY_DIP = 19
PINKY_TIP = 20

def lm_to_pos2d(lm, actual_w, actual_h):
    return pos2d(int(lm.x * actual_w), int(lm.y * actual_h))

def to_hands_pos(hands_lm, actual_w, actual_h):
    return HandsPos(
        wrist=lm_to_pos2d(hands_lm[WRIST], actual_w, actual_h),
        thumb_cmc=lm_to_pos2d(hands_lm[THUMB_CMC], actual_w, actual_h),
        thumb_mcp=lm_to_pos2d(hands_lm[THUMB_MCP], actual_w, actual_h),
        thumb_ip=lm_to_pos2d(hands_lm[THUMB_IP], actual_w, actual_h),
        thumb_tip=lm_to_pos2d(hands_lm[THUMB_TIP], actual_w, actual_h),
        index_finger_mcp=lm_to_pos2d(hands_lm[INDEX_FINGER_MCP], actual_w, actual_h),
        index_finger_pip=lm_to_pos2d(hands_lm[INDEX_FINGER_PIP], actual_w, actual_h),
        index_finger_dip=lm_to_pos2d(hands_lm[INDEX_FINGER_DIP], actual_w, actual_h),
        index_finger_tip=lm_to_pos2d(hands_lm[INDEX_FINGER_TIP], actual_w, actual_h),
        middle_finger_mcp=lm_to_pos2d(hands_lm[MIDDLE_FINGER_MCP], actual_w, actual_h),
        middle_finger_pip=lm_to_pos2d(hands_lm[MIDDLE_FINGER_PIP], actual_w, actual_h),
        middle_finger_dip=lm_to_pos2d(hands_lm[MIDDLE_FINGER_DIP], actual_w, actual_h),
        middle_finger_tip=lm_to_pos2d(hands_lm[MIDDLE_FINGER_TIP], actual_w, actual_h),
        ring_finger_mcp=lm_to_pos2d(hands_lm[RING_FINGER_MCP], actual_w, actual_h),
        ring_finger_pip=lm_to_pos2d(hands_lm[RING_FINGER_PIP], actual_w, actual_h),
        ring_finger_dip=lm_to_pos2d(hands_lm[RING_FINGER_DIP], actual_w, actual_h),
        ring_finger_tip=lm_to_pos2d(hands_lm[RING_FINGER_TIP], actual_w, actual_h),
        pinky_mcp=lm_to_pos2d(hands_lm[PINKY_MCP], actual_w, actual_h),
        pinky_pip=lm_to_pos2d(hands_lm[PINKY_PIP], actual_w, actual_h),
        pinky_dip=lm_to_pos2d(hands_lm[PINKY_DIP], actual_w, actual_h),
        pinky_tip=lm_to_pos2d(hands_lm[PINKY_TIP], actual_w, actual_h)
    )
