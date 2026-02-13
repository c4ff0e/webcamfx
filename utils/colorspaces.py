import cv2 as cv
def bgr2rgb(frame_bgr):
    frame_rgb = cv.cvtColor(frame_bgr, cv.COLOR_BGR2RGB)
    return frame_rgb

def rgb2bgr(frame_rgb):
    frame_bgr = cv.cvtColor(frame_rgb, cv.COLOR_RGB2BGR)
    return frame_bgr

def config2bgr(color_config):
    return tuple(reversed(color_config))