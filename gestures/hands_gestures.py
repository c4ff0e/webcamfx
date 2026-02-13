
from dataclasses import dataclass
import cv2 as cv

@dataclass
class GestureState: #this class can be used everywhere
    point_count:int = 0
    point_count_inactive: int = 0
    point_active: bool = False

    middle_count: int = 0
    middle_count_inactive: int = 0
    middle_active: bool = False

    def update(self, hands_pos, gesture_confidence, inactive_threshold):
        if check_point(hands_pos):
            self.point_count += 1
            if self.point_count > gesture_confidence:
                self.point_active = True
                self.point_count_inactive = 0 # reset inactive count when gesture is active
        else:
            self.point_count = 0
            self.point_count_inactive += 1
            if self.point_count_inactive > inactive_threshold:
                self.point_active = False
        
        if check_middle(hands_pos):
            self.middle_count += 1
            if self.middle_count > gesture_confidence:
                self.middle_active = True
                self.middle_count_inactive = 0 # reset inactive count when gesture is active
        else:
            self.middle_count = 0
            self.middle_count_inactive += 1
            if self.middle_count_inactive > inactive_threshold:
                self.middle_active = False
            
    def active(self):
        if self.point_active:
            return "POINT"
        if self.middle_active:
            return "MIDDLE"
        return None
    
def check_point(hands_pos): 
    # check if index finger is extended and other fingers are not
    index_extended = hands_pos.index_finger_tip.y < hands_pos.index_finger_pip.y
    middle_extended = hands_pos.middle_finger_tip.y < hands_pos.middle_finger_pip.y
    ring_extended = hands_pos.ring_finger_tip.y < hands_pos.ring_finger_pip.y
    pinky_extended = hands_pos.pinky_tip.y < hands_pos.pinky_pip.y
    if index_extended and not middle_extended and not ring_extended and not pinky_extended:
        return True
    else:
        return False

def check_middle(hands_pos):
    # check if middle finger is extended and other fingers are not
    index_extended = hands_pos.index_finger_tip.y < hands_pos.index_finger_pip.y
    middle_extended = hands_pos.middle_finger_tip.y < hands_pos.middle_finger_pip.y
    ring_extended = hands_pos.ring_finger_tip.y < hands_pos.ring_finger_pip.y
    pinky_extended = hands_pos.pinky_tip.y < hands_pos.pinky_pip.y
    if middle_extended and not index_extended and not ring_extended and not pinky_extended:
        return True
    else:
        return False

