import cv2 as cv
def draw_circle(frame_bgr, color, radius, thickness, index_tip):
    center = (index_tip.x, index_tip.y)
    cv.circle(frame_bgr, center, radius, color, thickness)
    return frame_bgr