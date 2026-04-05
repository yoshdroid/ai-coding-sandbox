from __future__ import annotations

from src.platformer.level import PLAYER_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, Level, Platform


class Player:
    MOVE_SPEED = 1.8
    JUMP_VELOCITY = -4.6
    WALL_JUMP_HORIZONTAL_SPEED = 2.8
    WALL_JUMP_VERTICAL_SPEED = -4.3
    GRAVITY = 0.32
    MAX_FALL_SPEED = 4.8

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.facing_right = True
        self.touch_wall_left = False
        self.touch_wall_right = False

    def move_right(self) -> None:
        self.vx = self.MOVE_SPEED
        self.facing_right = True

    def move_left(self) -> None:
        self.vx = -self.MOVE_SPEED
        self.facing_right = False

    def stop(self) -> None:
        self.vx = 0.0

    def jump(self) -> None:
        if self.on_ground:
            self.vy = self.JUMP_VELOCITY
            self.on_ground = False

    def wall_jump_left(self) -> None:
        self.vx = -self.WALL_JUMP_HORIZONTAL_SPEED
        self.vy = self.WALL_JUMP_VERTICAL_SPEED
        self.on_ground = False

    def wall_jump_right(self) -> None:
        self.vx = self.WALL_JUMP_HORIZONTAL_SPEED
        self.vy = self.WALL_JUMP_VERTICAL_SPEED
        self.on_ground = False

    def update(self, level: Level) -> str | None:
        self.touch_wall_left = False
        self.touch_wall_right = False
        self.vy = min(self.vy + self.GRAVITY, self.MAX_FALL_SPEED)
        self._move_horizontally(level)
        self._move_vertically(level)

        if self.y > SCREEN_HEIGHT:
            return "restart"
        return None

    def _move_horizontally(self, level: Level) -> None:
        next_x = self.x + self.vx
        next_x = max(0, min(SCREEN_WIDTH - PLAYER_SIZE, next_x))

        for platform in level.platforms:
            if not self._intersects_platform(next_x, self.y, platform):
                continue
            if self.vx > 0:
                next_x = platform.x - PLAYER_SIZE
                self.touch_wall_right = True
            elif self.vx < 0:
                next_x = platform.x + platform.width
                self.touch_wall_left = True

        self.x = next_x

    def _move_vertically(self, level: Level) -> None:
        self.on_ground = False
        next_y = self.y + self.vy

        for platform in level.platforms:
            if self.vy >= 0 and self._crossed_platform_top(next_y, platform):
                next_y = platform.y - PLAYER_SIZE
                self.vy = 0.0
                self.on_ground = True
                break
            if self.vy < 0 and self._crossed_platform_bottom(next_y, platform):
                next_y = platform.y + platform.height
                self.vy = 0.0
                break

        self.y = next_y

    def _crossed_platform_top(self, next_y: float, platform: Platform) -> bool:
        return (
            self.x + PLAYER_SIZE > platform.x
            and self.x < platform.x + platform.width
            and self.y + PLAYER_SIZE <= platform.y
            and next_y + PLAYER_SIZE >= platform.y
        )

    def _crossed_platform_bottom(self, next_y: float, platform: Platform) -> bool:
        return (
            self.x + PLAYER_SIZE > platform.x
            and self.x < platform.x + platform.width
            and self.y >= platform.y + platform.height
            and next_y <= platform.y + platform.height
        )

    @staticmethod
    def _intersects_platform(x: float, y: float, platform: Platform) -> bool:
        return (
            x < platform.x + platform.width
            and x + PLAYER_SIZE > platform.x
            and y < platform.y + platform.height
            and y + PLAYER_SIZE > platform.y
        )
