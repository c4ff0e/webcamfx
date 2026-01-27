import cv2 as cv
import logging
module_name = "PREVIEW"
logging.getLogger(__name__)

def open_preview(frame_bgr):
    cv.imshow("Camera Feed", frame_bgr)

def should_close():
    if cv.waitKey(1) & 0xFF == ord('q'):
        logging.debug(f"{module_name}: Preview window closed by user")
        return True
    else:
        return False