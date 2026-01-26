import cv2 as cv
import numpy as np
import mediapipe as mp

feed = cv.VideoCapture(0)
if not feed.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    ret, frame = feed.read()
    
    if not ret:
        print("Error: Could not read frame.")
        break
    cv.imshow("Webcam Feed", frame)
    if cv.waitKey(1) == ord('q'):
        break
feed.release()
cv.destroyAllWindows()