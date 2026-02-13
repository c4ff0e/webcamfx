import cv2 as cv
import logging

module_name = "DEBUG"
logging.getLogger(__name__)

DEBUG_FONT = cv.FONT_HERSHEY_SIMPLEX
DEBUG_FONT_SCALE = 0.6
DEBUG_FONT_COLOR = (0, 255, 0)
DEBUG_FONT_THICKNESS = 1

def draw_dbg_frameinfo(frame_bgr, timestamp, w, h, fps, cam_id, fps_smooth, actual_w, actual_h, fps_reported):
    config_info = f"Config:{w}x{h}, fps:{fps}, cam_id:{cam_id}"
    actual_info = f"Actual:{int(actual_w)}x{int(actual_h)}, FPS reported:{fps_reported:.2f}"
    fps_info = f"FPS calculated:{fps_smooth:.2f}"
    timestamp_info = f"Timestamp:{timestamp}ms"
    lines = [config_info, actual_info, fps_info, timestamp_info]
    y0, dy = 20, 25
    for i, line in enumerate(lines):
        y = y0 + i * dy
        cv.putText(frame_bgr, line, (10, y), DEBUG_FONT, DEBUG_FONT_SCALE, DEBUG_FONT_COLOR, DEBUG_FONT_THICKNESS, cv.LINE_AA)
    
    return frame_bgr

def draw_dbg_gestureinfo(frame_bgr, hand_state):
    if hand_state.point_active:
        cv.putText(frame_bgr, "Point gesture detected", (10, 150), DEBUG_FONT, DEBUG_FONT_SCALE, (0, 255, 255), DEBUG_FONT_THICKNESS, cv.LINE_AA)
    if hand_state.middle_active:
        cv.putText(frame_bgr, "Middle gesture detected", (10, 180), DEBUG_FONT, DEBUG_FONT_SCALE, (0, 255, 255), DEBUG_FONT_THICKNESS, cv.LINE_AA)
    return frame_bgr
