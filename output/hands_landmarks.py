import cv2 as cv
def draw(frame_bgr, hands_pos):
    for landmark in hands_pos.landmarks():
        cv.circle(frame_bgr, (landmark.x, landmark.y), 5, (0, 255, 0), -1)
        cv.putText(frame_bgr, f"{landmark.x},{landmark.y}", (landmark.x + 5, landmark.y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    return frame_bgr