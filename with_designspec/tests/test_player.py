from src.platformer.level import PLAYER_SIZE, Level
from src.platformer.player import Player


class TestPlayer:
    def test_player_initialization(self):
        # プレイヤーの初期位置と速度が正しく設定されることを確認する
        player = Player(10, 10)
        assert player.x == 10
        assert player.y == 10
        assert player.vx == 0
        assert player.vy == 0

    def test_player_move_right(self):
        # 右移動で正の速度になることを確認する
        player = Player(0, 0)
        player.move_right()
        assert player.vx > 0

    def test_player_move_left(self):
        # 左移動で負の速度になることを確認する
        player = Player(0, 0)
        player.move_left()
        assert player.vx < 0

    def test_player_jump(self):
        # 足場の上にいるときだけジャンプできることを確認する
        player = Player(0, 0)
        player.on_ground = True
        player.jump()
        assert player.vy < 0

    def test_player_lands_on_platform(self):
        # 落下中に足場の上へ着地できることを確認する
        level = Level(1)
        platform = level.start_platform
        player = Player(platform.x + 8, platform.y - PLAYER_SIZE - 1)
        player.vy = 2
        player.update(level)
        assert player.on_ground is True
        assert player.y == platform.y - PLAYER_SIZE

    def test_player_falls_outside_screen_and_requests_restart(self):
        # 画面下へ落ちたらリスタート要求を返すことを確認する
        level = Level(1)
        player = Player(32, 130)
        assert player.update(level) == "restart"

    def test_player_wall_jump_changes_velocity(self):
        # 壁ジャンプで壁から離れる向きに速度が付くことを確認する
        player = Player(0, 0)
        player.wall_jump_left()
        assert player.vx < 0
        assert player.vy < 0
