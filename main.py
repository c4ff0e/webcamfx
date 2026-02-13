import time
import cv2 as cv
import mediapipe as mp
import tomllib
import capture.camera as camera
import output.preview as preview
import output.hands_landmarks as hands_landmarks
import logging
import output.debug_overlay as debug_overlay
import utils.colorspaces as colorspaces
from time import perf_counter
import tracking.hands as hands
import gestures.hands_gestures as hands_gestures
import output.hands_index as hands_index
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

working = True


class Config:
    #camera
    cam_id = config["camera"]["id"]
    w = config["camera"]["w"]
    h = config["camera"]["h"]
    fps = config["camera"]["fps"]
    
    #hands
    hands_path = config["hands"]["model"]["hands_path"]
    hand_confidence = config["hands"]["confidence"]["hand_confidence"]
    tracking_confidence = config["hands"]["confidence"]["tracking_confidence"]
    gesture_confidence = config["hands"]["confidence"]["gesture_confidence"]
    inactive_threshold = config["hands"]["confidence"]["inactive_threshold"]
    
    #output
    debug = config["output"]["debug"]
    draw_lines = config["output"]["show_lines"]
    draw_landmarks = config["output"]["show_landmarks"]
    
    #hand gestures
    point_enabled = config["hands"]["gestures"]["point"]["enabled"]
    point_color = colorspaces.config2bgr(tuple(config["hands"]["gestures"]["point"]["color"])) #convert from rgb to bgr
    point_radius = config["hands"]["gestures"]["point"]["radius"]
    point_thickness = config["hands"]["gestures"]["point"]["thickness"]

logging.basicConfig(level=logging.DEBUG if Config.debug else None)
module_name = "MAIN"

# init camera and hand model
capture = camera.open_camera(Config.cam_id, Config.w, Config.h, Config.fps)
hands_detector = hands.init(Config.hands_path, Config.hand_confidence, Config.tracking_confidence)
#init gesture state
hand_state = hands_gestures.GestureState()

try: # main loop
    t_prev = perf_counter()
    fps_smooth = 0.0
    logging.debug("main loop started")    
    while working:
        
        frame_bgr, timestamp = camera.read_frame(capture)
        
        if frame_bgr is None:
            print("Failed to read frame from camera")
            break
        
        actual_w = frame_bgr.shape[1]
        actual_h = frame_bgr.shape[0]
        
        # hand tracking
        frame_rgb = colorspaces.bgr2rgb(frame_bgr) # can be used on every pass
        
        mp_image = hands.img_preprocess(frame_rgb)
        hands_result, hands_lm = hands.track(hands_detector, mp_image, timestamp)
        
        #convert to 2d pos
        hands_pos = hands.to_2d_pos(hands_lm, actual_w, actual_h) if hands_lm else None # ready to use everywhere else
        
        # draw landmarks
        if hands_pos:
            if Config.draw_landmarks:
                frame_bgr = hands_landmarks.draw_lm(frame_bgr, hands_pos)
            if Config.draw_lines:
                frame_bgr = hands_landmarks.draw_lines(frame_bgr, hands_pos)
                
        #check hand gestures
        if hands_pos:
            hands_state = hand_state.update(hands_pos, Config.gesture_confidence, Config.inactive_threshold)

            #check what is active and draw
            active_gesture = hand_state.active()
            if active_gesture == "POINT" and Config.point_enabled:
                frame_bgr = hands_index.draw_circle(frame_bgr, Config.point_color, Config.point_radius, Config.point_thickness, hands_pos.index_finger_tip)
            if active_gesture == "MIDDLE":
                pass #TODO: add middle finger gesture drawing
            
        if Config.debug:
            t = perf_counter()
            dt = t - t_prev
            t_prev = t
            fps_instant = 1.0 / dt if dt > 0 else 0
            fps_smooth = 0.9 * fps_smooth + 0.1 * fps_instant
            fps_reported = capture.get(cv.CAP_PROP_FPS)
            frame_bgr = debug_overlay.draw_dbg_frameinfo(frame_bgr, timestamp, Config.w, Config.h, Config.fps, Config.cam_id, fps_smooth, actual_w, actual_h, fps_reported)
            frame_bgr = debug_overlay.draw_dbg_gestureinfo(frame_bgr, hand_state)
        
        preview.open_preview(frame_bgr)
        if preview.should_close():
            break
        
finally:
    working = False
    camera.release(capture)
    cv.destroyAllWindows()
