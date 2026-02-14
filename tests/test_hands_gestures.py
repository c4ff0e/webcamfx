from gestures.hands_gestures import check_point, check_middle, GestureState
from tracking.hands import pos2d, HandsPos


def make_hands_pos(
    index_tip_y=100, index_pip_y=200,
    middle_tip_y=200, middle_pip_y=100,
    ring_tip_y=200, ring_pip_y=100,
    pinky_tip_y=200, pinky_pip_y=100
):
    return HandsPos(
        wrist=pos2d(0, 300),
        thumb_cmc=pos2d(0, 0),
        thumb_mcp=pos2d(0, 0),
        thumb_ip=pos2d(0, 0),
        thumb_tip=pos2d(0, 0),
        index_finger_mcp=pos2d(0, 0),
        index_finger_pip=pos2d(0, index_pip_y),
        index_finger_dip=pos2d(0, 0),
        index_finger_tip=pos2d(0, index_tip_y),
        middle_finger_mcp=pos2d(0, 0),
        middle_finger_pip=pos2d(0, middle_pip_y),
        middle_finger_dip=pos2d(0, 0),
        middle_finger_tip=pos2d(0, middle_tip_y),
        ring_finger_mcp=pos2d(0, 0),
        ring_finger_pip=pos2d(0, ring_pip_y),
        ring_finger_dip=pos2d(0, 0),
        ring_finger_tip=pos2d(0, ring_tip_y),
        pinky_mcp=pos2d(0, 0),
        pinky_pip=pos2d(0, pinky_pip_y),
        pinky_dip=pos2d(0, 0),
        pinky_tip=pos2d(0, pinky_tip_y),
    )


class TestCheckPoint:
    def test_index_extended_others_folded(self):
        hands_pos = make_hands_pos(
            index_tip_y=100, index_pip_y=200,  # extended
            middle_tip_y=200, middle_pip_y=100,  # folded
            ring_tip_y=200, ring_pip_y=100,  # folded
            pinky_tip_y=200, pinky_pip_y=100,  # folded
        )
        assert check_point(hands_pos) is True

    def test_all_fingers_extended(self):
        hands_pos = make_hands_pos(
            index_tip_y=100, index_pip_y=200,
            middle_tip_y=100, middle_pip_y=200,
            ring_tip_y=100, ring_pip_y=200,
            pinky_tip_y=100, pinky_pip_y=200,
        )
        assert check_point(hands_pos) is False

    def test_all_fingers_folded(self):
        hands_pos = make_hands_pos(
            index_tip_y=200, index_pip_y=100,
            middle_tip_y=200, middle_pip_y=100,
            ring_tip_y=200, ring_pip_y=100,
            pinky_tip_y=200, pinky_pip_y=100,
        )
        assert check_point(hands_pos) is False

    def test_index_and_middle_extended(self):
        hands_pos = make_hands_pos(
            index_tip_y=100, index_pip_y=200,
            middle_tip_y=100, middle_pip_y=200,
            ring_tip_y=200, ring_pip_y=100,
            pinky_tip_y=200, pinky_pip_y=100,
        )
        assert check_point(hands_pos) is False


class TestCheckMiddle:
    def test_middle_extended_others_folded(self):
        hands_pos = make_hands_pos(
            index_tip_y=200, index_pip_y=100,  # folded
            middle_tip_y=100, middle_pip_y=200,  # extended
            ring_tip_y=200, ring_pip_y=100,  # folded
            pinky_tip_y=200, pinky_pip_y=100,  # folded
        )
        assert check_middle(hands_pos) is True

    def test_all_fingers_extended(self):
        hands_pos = make_hands_pos(
            index_tip_y=100, index_pip_y=200,
            middle_tip_y=100, middle_pip_y=200,
            ring_tip_y=100, ring_pip_y=200,
            pinky_tip_y=100, pinky_pip_y=200,
        )
        assert check_middle(hands_pos) is False

    def test_index_extended_not_middle(self):
        hands_pos = make_hands_pos(
            index_tip_y=100, index_pip_y=200,
            middle_tip_y=200, middle_pip_y=100,
            ring_tip_y=200, ring_pip_y=100,
            pinky_tip_y=200, pinky_pip_y=100,
        )
        assert check_middle(hands_pos) is False


class TestGestureState:
    def test_initial_state(self):
        state = GestureState()
        assert state.point_active is False
        assert state.middle_active is False
        assert state.active() is None

    def test_point_activates_after_confidence_threshold(self):
        state = GestureState()
        gesture_confidence = 3
        inactive_threshold = 2

        # point gesture position
        hands_pos = make_hands_pos(
            index_tip_y=100, index_pip_y=200,
            middle_tip_y=200, middle_pip_y=100,
            ring_tip_y=200, ring_pip_y=100,
            pinky_tip_y=200, pinky_pip_y=100,
        )

        # not active yet
        for _ in range(gesture_confidence):
            state.update(hands_pos, gesture_confidence, inactive_threshold)
        assert state.point_active is False

        # one more update should activate
        state.update(hands_pos, gesture_confidence, inactive_threshold)
        assert state.point_active is True
        assert state.active() == "POINT"

    def test_middle_activates_after_confidence_threshold(self):
        state = GestureState()
        gesture_confidence = 3
        inactive_threshold = 2

        # middle finger gesture position
        hands_pos = make_hands_pos(
            index_tip_y=200, index_pip_y=100,
            middle_tip_y=100, middle_pip_y=200,
            ring_tip_y=200, ring_pip_y=100,
            pinky_tip_y=200, pinky_pip_y=100,
        )

        for _ in range(gesture_confidence + 1):
            state.update(hands_pos, gesture_confidence, inactive_threshold)

        assert state.middle_active is True
        assert state.active() == "MIDDLE"

    def test_gesture_deactivates_after_inactive_threshold(self):
        state = GestureState()
        gesture_confidence = 2
        inactive_threshold = 2

        # activate point
        point_pos = make_hands_pos(
            index_tip_y=100, index_pip_y=200,
            middle_tip_y=200, middle_pip_y=100,
            ring_tip_y=200, ring_pip_y=100,
            pinky_tip_y=200, pinky_pip_y=100,
        )
        for _ in range(gesture_confidence + 1):
            state.update(point_pos, gesture_confidence, inactive_threshold)
        assert state.point_active is True

        # now show no gesture
        no_gesture_pos = make_hands_pos(
            index_tip_y=200, index_pip_y=100,
            middle_tip_y=200, middle_pip_y=100,
            ring_tip_y=200, ring_pip_y=100,
            pinky_tip_y=200, pinky_pip_y=100,
        )

        # still active during threshold
        for _ in range(inactive_threshold):
            state.update(no_gesture_pos, gesture_confidence, inactive_threshold)
        assert state.point_active is True

        # one more should deactivate
        state.update(no_gesture_pos, gesture_confidence, inactive_threshold)
        assert state.point_active is False

    def test_point_has_priority_over_middle(self):
        # if both gestures are somehow active, POINT is returned first
        state = GestureState()
        state.point_active = True
        state.middle_active = True
        assert state.active() == "POINT"
