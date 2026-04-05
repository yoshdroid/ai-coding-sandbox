from __future__ import annotations

from dataclasses import dataclass
import random


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 128
PLATFORM_HEIGHT = 6
PLAYER_SIZE = 8


@dataclass(frozen=True)
class Platform:
    x: int
    y: int
    width: int
    height: int = PLATFORM_HEIGHT


class Level:
    def __init__(self, stage: int) -> None:
        self.stage = stage
        self._rng = random.Random(stage)
        self.platforms = self.generate_platforms()
        self.start_platform = self.platforms[0]
        self.goal_platform = self.platforms[-1]
        self.goal_x = self.goal_platform.x + self.goal_platform.width - 12
        self.goal_y = self.goal_platform.y - 12

    def generate_platforms(self) -> list[Platform]:
        platforms: list[Platform] = []
        x = 0
        y = 102
        width = 52
        platforms.append(Platform(x=x, y=y, width=width))

        while x + width < SCREEN_WIDTH - 46:
            gap = self._rng.randint(14, 28)
            next_width = self._rng.randint(28, 52)
            max_x = SCREEN_WIDTH - 40 - next_width
            next_x = min(x + width + gap, max_x)

            y_shift = self._rng.randint(-18, 18)
            next_y = max(40, min(104, y + y_shift))
            if abs(next_y - y) > 20:
                next_y = y + (20 if next_y > y else -20)

            platforms.append(Platform(x=next_x, y=next_y, width=next_width))
            x = next_x
            y = next_y
            width = next_width

            if next_x >= SCREEN_WIDTH - 80:
                break

        if len(platforms) < 4:
            last = platforms[-1]
            extra_x = min(last.x + last.width + 16, SCREEN_WIDTH - 42)
            platforms.append(
                Platform(
                    x=extra_x,
                    y=max(44, min(100, last.y - 8)),
                    width=34,
                )
            )

        final = platforms[-1]
        if final.x + final.width < SCREEN_WIDTH - 34:
            platforms[-1] = Platform(
                x=SCREEN_WIDTH - 48,
                y=final.y,
                width=40,
            )

        return platforms

    def check_overlap(self) -> bool:
        for index, current in enumerate(self.platforms):
            for other in self.platforms[index + 1 :]:
                if self._platforms_overlap(current, other):
                    return True
        return False

    def find_support(self, player_x: float, player_bottom: float) -> Platform | None:
        for platform in self.platforms:
            if platform.x - PLAYER_SIZE < player_x < platform.x + platform.width:
                if abs(player_bottom - platform.y) <= 2:
                    return platform
        return None

    def touches_goal(self, player_x: float, player_y: float) -> bool:
        goal_width = 10
        goal_height = 12
        return (
            player_x < self.goal_x + goal_width
            and player_x + PLAYER_SIZE > self.goal_x
            and player_y < self.goal_y + goal_height
            and player_y + PLAYER_SIZE > self.goal_y
        )

    @staticmethod
    def _platforms_overlap(first: Platform, second: Platform) -> bool:
        return not (
            first.x + first.width <= second.x
            or second.x + second.width <= first.x
            or first.y + first.height <= second.y
            or second.y + second.height <= first.y
        )
