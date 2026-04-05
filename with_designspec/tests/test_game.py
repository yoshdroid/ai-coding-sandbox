from src.platformer.game import Game


class DummyPyxel:
    KEY_LEFT = 1
    KEY_RIGHT = 2
    KEY_SPACE = 3
    KEY_R = 4
    KEY_S = 5

    def __init__(self):
        self._pressed = set()
        self._pressed_once = set()

    def init(self, *_args, **_kwargs):
        return None

    def run(self, *_args, **_kwargs):
        return None

    def cls(self, *_args, **_kwargs):
        return None

    def text(self, *_args, **_kwargs):
        return None

    def rect(self, *_args, **_kwargs):
        return None

    def btn(self, key):
        return key in self._pressed

    def btnp(self, key):
        return key in self._pressed_once


class TestGame:
    def test_game_initialization(self):
        # ゲーム起動直後はタイトル画面になることを確認する
        game = Game(auto_start=False, pyxel_module=DummyPyxel())
        assert game.scene == "title"
        assert game.stage == 1

    def test_start_stage_changes_scene(self):
        # ステージ開始時にゲーム画面へ遷移することを確認する
        game = Game(auto_start=False, pyxel_module=DummyPyxel())
        game.start_stage()
        assert game.scene == "game"
        assert game.player is not None
        assert game.level is not None

    def test_restart_stage_keeps_same_stage_number(self):
        # リスタートしても同じステージ番号のままであることを確認する
        game = Game(auto_start=False, pyxel_module=DummyPyxel())
        game.stage = 4
        game.start_stage()
        game.restart_stage()
        assert game.stage == 4

    def test_next_stage_advances_until_ending(self):
        # 10面クリア後にエンディングへ遷移することを確認する
        game = Game(auto_start=False, pyxel_module=DummyPyxel())
        game.stage = 9
        game.start_stage()
        game.next_stage()
        assert game.stage == 10
        assert game.scene == "game"
        game.next_stage()
        assert game.scene == "ending"

    def test_wall_jump_uses_directional_input_toward_wall(self):
        # 壁方向の入力とジャンプ入力で壁ジャンプできることを確認する
        pyxel = DummyPyxel()
        game = Game(auto_start=False, pyxel_module=pyxel)
        game.start_stage()
        game.player.on_ground = False
        game.player.touch_wall_right = True
        pyxel._pressed = {pyxel.KEY_RIGHT}
        pyxel._pressed_once = {pyxel.KEY_SPACE}
        game.update_game()
        assert game.player.vx < 0
        assert game.player.vy < 0
