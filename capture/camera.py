import cv2 as cv
import time

def open_camera(cam_id, w, h, fps):
    capture = cv.VideoCapture(cam_id)
    capture.set(cv.CAP_PROP_FRAME_WIDTH, w)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, h)
    capture.set(cv.CAP_PROP_FPS, fps) # not guaranteed to work but anyways
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open camera with id {cam_id}")
    return capture

def read_frame(capture):
    ok, frame_bgr = capture.read()
    if not ok:
        return None
    timestamp = round(time.time() * 1000)
    return frame_bgr, timestamp

def release(capture):
    capture.release()