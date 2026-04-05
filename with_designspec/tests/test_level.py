import pytest
from src.platformer.level import Level

class TestLevel:
    def test_level_initialization(self):
        # レベルの初期化テスト
        level = Level(1)
        assert level.stage == 1
        assert len(level.platforms) > 0
        assert level.goal_x > 0

    def test_level_random_generation(self):
        # ランダム生成テスト
        level1 = Level(1)
        level2 = Level(1)
        # 同じシードでもランダムだが、テストでは異なることを確認
        # 実際にはシード固定でテスト
        pass  # 仮

    def test_level_collision(self):
        # 衝突判定テスト
        level = Level(1)
        # プレイヤーがプラットフォームに衝突するかテスト
        pass