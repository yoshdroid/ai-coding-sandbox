from src.platformer.level import PLATFORM_HEIGHT, SCREEN_WIDTH, Level


class TestLevel:
    def test_level_initialization(self):
        # ステージ番号とゴール位置が初期化されることを確認する
        level = Level(1)
        assert level.stage == 1
        assert len(level.platforms) >= 4
        assert 0 <= level.goal_x <= SCREEN_WIDTH - 10

    def test_level_random_generation_is_deterministic_per_stage(self):
        # 同じステージ番号なら同じ地形が生成されることを確認する
        level1 = Level(3)
        level2 = Level(3)
        assert level1.platforms == level2.platforms
        assert level1.goal_x == level2.goal_x

    def test_level_platforms_do_not_overlap(self):
        # 足場同士が重ならないことを確認する
        level = Level(5)
        assert level.check_overlap() is False

    def test_level_goal_is_on_screen(self):
        # ゴールが画面内に収まることを確認する
        level = Level(7)
        assert 0 <= level.goal_x <= SCREEN_WIDTH - 10
        assert level.goal_y >= 0

    def test_level_generates_vertical_platforms(self):
        # 縦方向に細長い足場が含まれることを確認する
        level = Level(2)
        assert any(platform.height > PLATFORM_HEIGHT for platform in level.platforms)
