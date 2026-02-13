from playsound3 import playsound
from playsound3 import AVAILABLE_BACKENDS, DEFAULT_BACKEND
import logging
module_name = "HANDS_MIDDLE"
logging.getLogger(__name__)

def play_sfx():
    playsound("sfx/faaah.mp3", block=False)
    logging.debug(f"{module_name}: middle finger sfx")
    logging.debug(f"{module_name}: available backends: {AVAILABLE_BACKENDS}")
    logging.debug(f"{module_name}: default backend: {DEFAULT_BACKEND}")
