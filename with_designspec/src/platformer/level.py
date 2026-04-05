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
        self.goal_platform = self._find_goal_platform()
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

        platforms.extend(self._generate_vertical_platforms(platforms))
        platforms.sort(key=lambda platform: (platform.x, platform.y, platform.width, platform.height))
        return platforms

    def _generate_vertical_platforms(self, base_platforms: list[Platform]) -> list[Platform]:
        verticals: list[Platform] = []

        for index, platform in enumerate(base_platforms[:-1]):
            next_platform = base_platforms[index + 1]
            gap_left = platform.x + platform.width
            gap_right = next_platform.x
            gap_width = gap_right - gap_left
            if gap_width < 14:
                continue

            pillar_width = 8
            pillar_height = self._rng.randint(24, 40)
            pillar_x = gap_left + gap_width // 2 - pillar_width // 2
            pillar_top = max(24, min(platform.y, next_platform.y) - pillar_height + 12)
            candidate = Platform(
                x=pillar_x,
                y=pillar_top,
                width=pillar_width,
                height=pillar_height,
            )
            if any(self._platforms_overlap(candidate, other) for other in [*base_platforms, *verticals]):
                continue
            verticals.append(candidate)

            if len(verticals) >= 2:
                break

        if not verticals:
            support = base_platforms[1]
            verticals.append(
                Platform(
                    x=max(60, support.x - 18),
                    y=max(28, support.y - 32),
                    width=8,
                    height=32,
                )
            )

        return verticals

    def _find_goal_platform(self) -> Platform:
        horizontal_platforms = [
            platform for platform in self.platforms if platform.width >= platform.height
        ]
        return max(horizontal_platforms, key=lambda platform: platform.x)

    def check_overlap(self) -> bool:
        for index, current in enumerate(self.platforms):
            for other in self.platforms[index + 1 :]:
                if self._platforms_overlap(current, other):
                    return True
        return False

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
