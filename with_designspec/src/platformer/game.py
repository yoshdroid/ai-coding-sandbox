import pyxel
from src.platformer.player import Player
from src.platformer.level import Level

class Game:
    def __init__(self):
        pyxel.init(256, 128, title="Platformer")
        self.scene = "title"  # title, game, ending
        self.stage = 1
        self.player = None
        self.level = None
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.scene == "title":
            self.update_title()
        elif self.scene == "game":
            self.update_game()
        elif self.scene == "ending":
            self.update_ending()

    def draw(self):
        pyxel.cls(0)
        if self.scene == "title":
            self.draw_title()
        elif self.scene == "game":
            self.draw_game()
        elif self.scene == "ending":
            self.draw_ending()

    def update_title(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.start_game()

    def draw_title(self):
        pyxel.text(80, 50, "PLATFORMER", 7)
        pyxel.text(70, 70, "Press SPACE to start", 7)

    def start_game(self):
        self.scene = "game"
        self.player = Player(10, 100)
        self.level = Level(self.stage)

    def update_game(self):
        # 入力処理
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player.move_left()
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.player.move_right()
        else:
            self.player.vx = 0

        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.player.can_wall_jump_left:
                self.player.wall_jump_left()
            elif self.player.can_wall_jump_right:
                self.player.wall_jump_right()
            else:
                self.player.jump()

        if pyxel.btnp(pyxel.KEY_R):
            self.restart_stage()
        if pyxel.btnp(pyxel.KEY_S):
            self.next_stage()

        # 更新
        result = self.player.update(self.level)
        if result == "restart":
            self.restart_stage()

        # 衝突判定
        if self.level.check_collision(self.player):
            # 壁ジャンプなど
            pass

        # クリア判定
        if self.player.x >= self.level.goal_x:
            self.stage += 1
            if self.stage > 10:
                self.scene = "ending"
            else:
                self.next_stage()

    def draw_game(self):
        # プレイヤー描画
        pyxel.rect(self.player.x, self.player.y, 8, 8, 11)
        # プラットフォーム描画
        for plat in self.level.platforms:
            pyxel.rect(plat['x'], plat['y'], plat['width'], 5, 3)
        # ゴール描画
        pyxel.rect(self.level.goal_x, 100, 10, 10, 8)

    def restart_stage(self):
        self.player = Player(10, 100)
        self.level = Level(self.stage)

    def next_stage(self):
        self.stage += 1
        self.restart_stage()

    def update_ending(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.scene = "title"
            self.stage = 1

    def draw_ending(self):
        pyxel.text(80, 50, "CONGRATULATIONS!", 7)
        pyxel.text(70, 70, "Press SPACE to restart", 7)