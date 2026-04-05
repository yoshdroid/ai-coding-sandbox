import pytest
from src.platformer.player import Player

class TestPlayer:
    def test_player_initialization(self):
        # プレイヤーの初期化テスト
        player = Player(10, 10)
        assert player.x == 10
        assert player.y == 10
        assert player.vx == 0
        assert player.vy == 0

    def test_player_move_right(self):
        # 右移動テスト
        player = Player(0, 0)
        player.move_right()
        assert player.vx > 0

    def test_player_move_left(self):
        # 左移動テスト
        player = Player(0, 0)
        player.move_left()
        assert player.vx < 0

    def test_player_jump(self):
        # ジャンプテスト
        player = Player(0, 0)
        player.on_ground = True
        player.jump()
        assert player.vy < 0  # 上向き

    def test_player_wall_jump(self):
        # 壁ジャンプテスト
        player = Player(0, 0)
        player.wall_jump_right()
        assert player.vx > 0
        assert player.vy < 0

    def test_player_update(self):
        # 更新テスト
        player = Player(0, 0)
        player.vx = 1
        player.vy = 1
        player.update()
        assert player.x == 1
        assert player.y == 1