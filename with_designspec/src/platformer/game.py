from __future__ import annotations

import pyxel

from src.platformer.level import PLAYER_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, Level
from src.platformer.player import Player


class Game:
    MAX_STAGE = 10

    def __init__(self, auto_start: bool = True, pyxel_module=pyxel) -> None:
        self.pyxel = pyxel_module
        self.scene = "title"
        self.stage = 1
        self.player: Player | None = None
        self.level: Level | None = None

        if auto_start:
            self.run()

    def run(self) -> None:
        self.pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Random Platformer")
        self.pyxel.run(self.update, self.draw)

    def update(self) -> None:
        if self.scene == "title":
            self.update_title()
        elif self.scene == "game":
            self.update_game()
        elif self.scene == "ending":
            self.update_ending()

    def draw(self) -> None:
        self.pyxel.cls(0)
        if self.scene == "title":
            self.draw_title()
        elif self.scene == "game":
            self.draw_game()
        elif self.scene == "ending":
            self.draw_ending()

    def update_title(self) -> None:
        if self.pyxel.btnp(self.pyxel.KEY_SPACE):
            self.stage = 1
            self.start_stage()

    def draw_title(self) -> None:
        self.pyxel.text(78, 30, "RANDOM PLATFORMER", 7)
        self.pyxel.text(44, 52, "LEFT/RIGHT: MOVE  SPACE: JUMP", 6)
        self.pyxel.text(58, 68, "R: RESTART  S: SKIP STAGE", 6)
        self.pyxel.text(62, 92, "PRESS SPACE TO START", 10)

    def start_stage(self) -> None:
        self.scene = "game"
        self.level = Level(self.stage)
        self.player = Player(
            self.level.start_platform.x + 8,
            self.level.start_platform.y - PLAYER_SIZE,
        )
        self.player.on_ground = True

    def restart_stage(self) -> None:
        self.start_stage()

    def next_stage(self) -> None:
        if self.stage >= self.MAX_STAGE:
            self.scene = "ending"
            self.player = None
            self.level = None
            return

        self.stage += 1
        self.start_stage()

    def update_game(self) -> None:
        assert self.player is not None
        assert self.level is not None

        if self.pyxel.btn(self.pyxel.KEY_LEFT):
            self.player.move_left()
        elif self.pyxel.btn(self.pyxel.KEY_RIGHT):
            self.player.move_right()
        else:
            self.player.stop()

        if self.pyxel.btnp(self.pyxel.KEY_SPACE):
            self.player.jump()

        if self.pyxel.btnp(self.pyxel.KEY_R):
            self.restart_stage()
            return

        if self.pyxel.btnp(self.pyxel.KEY_S):
            self.next_stage()
            return

        result = self.player.update(self.level)
        if result == "restart":
            self.restart_stage()
            return

        if self.level.touches_goal(self.player.x, self.player.y):
            self.next_stage()

    def draw_game(self) -> None:
        assert self.player is not None
        assert self.level is not None

        self.pyxel.cls(1)
        for platform in self.level.platforms:
            self.pyxel.rect(platform.x, platform.y, platform.width, platform.height, 3)

        self.pyxel.rect(self.level.goal_x, self.level.goal_y, 10, 12, 11)
        self.pyxel.rect(int(self.player.x), int(self.player.y), PLAYER_SIZE, PLAYER_SIZE, 10)
        self.pyxel.text(6, 6, f"STAGE {self.stage}/{self.MAX_STAGE}", 7)
        self.pyxel.text(6, 16, "R:RESTART S:SKIP", 7)

    def update_ending(self) -> None:
        if self.pyxel.btnp(self.pyxel.KEY_SPACE):
            self.scene = "title"
            self.stage = 1

    def draw_ending(self) -> None:
        self.pyxel.text(84, 44, "ENDING", 7)
        self.pyxel.text(42, 64, "YOU CLEARED ALL 10 STAGES!", 10)
        self.pyxel.text(58, 88, "PRESS SPACE FOR TITLE", 6)
