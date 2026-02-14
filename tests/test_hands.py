from tracking.hands import pos2d, HandsPos, lm_to_2d_pos


class MockLandmark:
    #mediapipe mock
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class TestPos2d:
    def test_creation(self):
        p = pos2d(100, 200)
        assert p.x == 100
        assert p.y == 200

    def test_zero_coordinates(self):
        p = pos2d(0, 0)
        assert p.x == 0
        assert p.y == 0

    def test_negative_coordinates(self):
        p = pos2d(-10, -20)
        assert p.x == -10
        assert p.y == -20


class TestLmTo2dPos:
    def test_center_of_frame(self):
        lm = MockLandmark(0.5, 0.5)
        result = lm_to_2d_pos(lm, 800, 600)
        assert result.x == 400
        assert result.y == 300

    def test_top_left_corner(self):
        lm = MockLandmark(0.0, 0.0)
        result = lm_to_2d_pos(lm, 800, 600)
        assert result.x == 0
        assert result.y == 0

    def test_bottom_right_corner(self):
        lm = MockLandmark(1.0, 1.0)
        result = lm_to_2d_pos(lm, 800, 600)
        assert result.x == 800
        assert result.y == 600

    def test_different_resolution(self):
        lm = MockLandmark(0.25, 0.75)
        result = lm_to_2d_pos(lm, 1920, 1080)
        assert result.x == 480
        assert result.y == 810

    def test_coordinates_are_integers(self):
        lm = MockLandmark(0.333, 0.666)
        result = lm_to_2d_pos(lm, 100, 100)
        assert isinstance(result.x, int)
        assert isinstance(result.y, int)


class TestHandsPos:
    def create_hands_pos(self):
        return HandsPos(
            wrist=pos2d(0, 0),
            thumb_cmc=pos2d(1, 1),
            thumb_mcp=pos2d(2, 2),
            thumb_ip=pos2d(3, 3),
            thumb_tip=pos2d(4, 4),
            index_finger_mcp=pos2d(5, 5),
            index_finger_pip=pos2d(6, 6),
            index_finger_dip=pos2d(7, 7),
            index_finger_tip=pos2d(8, 8),
            middle_finger_mcp=pos2d(9, 9),
            middle_finger_pip=pos2d(10, 10),
            middle_finger_dip=pos2d(11, 11),
            middle_finger_tip=pos2d(12, 12),
            ring_finger_mcp=pos2d(13, 13),
            ring_finger_pip=pos2d(14, 14),
            ring_finger_dip=pos2d(15, 15),
            ring_finger_tip=pos2d(16, 16),
            pinky_mcp=pos2d(17, 17),
            pinky_pip=pos2d(18, 18),
            pinky_dip=pos2d(19, 19),
            pinky_tip=pos2d(20, 20),
        )

    def test_landmarks_returns_21_points(self):
        hands_pos = self.create_hands_pos()
        landmarks = hands_pos.landmarks()
        assert len(landmarks) == 21

    def test_landmarks_order(self):
        hands_pos = self.create_hands_pos()
        landmarks = hands_pos.landmarks()
        # first should be wrist
        assert landmarks[0].x == 0
        assert landmarks[0].y == 0
        # last should be pinky_tip
        assert landmarks[20].x == 20
        assert landmarks[20].y == 20

    def test_landmarks_contains_all_pos2d(self):
        hands_pos = self.create_hands_pos()
        landmarks = hands_pos.landmarks()
        for lm in landmarks:
            assert isinstance(lm, pos2d)

    def test_access_specific_landmarks(self):
        hands_pos = self.create_hands_pos()
        assert hands_pos.index_finger_tip.x == 8
        assert hands_pos.middle_finger_tip.x == 12
        assert hands_pos.wrist.x == 0
