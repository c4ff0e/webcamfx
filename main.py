import time
import cv2 as cv
import mediapipe as mp
import tomllib
import capture.camera as camera
import output.preview as preview
import logging

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
    logging.debug("main loop started")    
    while working:
        frame_bgr, timestamp = camera.read_frame(capture)
        if frame_bgr is None:
            print("Failed to read frame from camera")
            break
        preview.open_preview(frame_bgr)
        
        if preview.should_close():
            break
finally:
    working = False
    camera.release(capture)
    cv.destroyAllWindows()
        
        