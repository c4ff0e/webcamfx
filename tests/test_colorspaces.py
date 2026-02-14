from utils.colorspaces import config2bgr


class TestConfig2Bgr:
    def test_red_rgb_to_bgr(self):
        assert config2bgr((255, 0, 0)) == (0, 0, 255)

    def test_green_stays_same(self):
        assert config2bgr((0, 255, 0)) == (0, 255, 0)

    def test_blue_rgb_to_bgr(self):
        assert config2bgr((0, 0, 255)) == (255, 0, 0)

    def test_mixed_color(self):
        assert config2bgr((100, 150, 200)) == (200, 150, 100)

    def test_white(self):
        assert config2bgr((255, 255, 255)) == (255, 255, 255)

    def test_black(self):
        assert config2bgr((0, 0, 0)) == (0, 0, 0)
