import cv2 as cv
from dataclasses import fields
def draw_lm(frame_bgr, hands_pos):
    for field in fields(hands_pos):
        landmark = getattr(hands_pos, field.name)
        cv.circle(frame_bgr, (landmark.x, landmark.y), 5, (0, 255, 0), -1)
        cv.putText(frame_bgr, field.name, (landmark.x + 5, landmark.y + 15), cv.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
        cv.putText(frame_bgr, f"{landmark.x},{landmark.y}", (landmark.x + 5, landmark.y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    return frame_bgr

def draw_lines(frame_bgr, hands_pos):
    for field in fields(hands_pos):
        landmark = getattr(hands_pos, field.name)
        cv.line(frame_bgr, (hands_pos.wrist.x, hands_pos.wrist.y), (landmark.x, landmark.y), (255, 0, 0), 2)
    return frame_bgr