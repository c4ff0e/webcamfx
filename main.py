import time
import cv2 as cv
import mediapipe as mp
import tomllib
import capture.camera as camera
import output.preview as preview
import logging
import output.debug_overlay as debug_overlay
import utils.colorspaces as colorspaces
from time import perf_counter

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

working = True

logging.basicConfig(level=logging.DEBUG if config["output"]["debug"] else None)
module_name = "MAIN"

cam_id = config["camera"]["id"]
w = config["camera"]["w"]
h = config["camera"]["h"]
fps = config["camera"]["fps"]
debug = config["output"]["debug"]

capture = camera.open_camera(cam_id, w, h, fps)
try: # main loop
    t_prev = perf_counter()
    fps_smooth = 0.0
    logging.debug("main loop started")    
    while working:
        
        frame_bgr, timestamp = camera.read_frame(capture)
        
        if frame_bgr is None:
            print("Failed to read frame from camera")
            break
        
        if debug:
            t = perf_counter()
            dt = t - t_prev
            t_prev = t
            fps_instant = 1.0 / dt if dt > 0 else 0
            fps_smooth = 0.9 * fps_smooth + 0.1 * fps_instant
            
            actual_w = capture.get(cv.CAP_PROP_FRAME_WIDTH)
            actual_h = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
            fps_reported = capture.get(cv.CAP_PROP_FPS)
            frame_bgr = debug_overlay.draw_dbg_frameinfo(frame_bgr, timestamp, w, h, fps, cam_id, fps_smooth, actual_w, actual_h, fps_reported)

        preview.open_preview(frame_bgr)
        
        if preview.should_close():
            break
        
finally:
    working = False
    camera.release(capture)
    cv.destroyAllWindows()
