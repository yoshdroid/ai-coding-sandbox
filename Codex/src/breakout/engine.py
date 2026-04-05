"""Core game logic for a simple breakout game."""

from __future__ import annotations

from dataclasses import dataclass


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
PADDLE_WIDTH = 96
PADDLE_HEIGHT = 16
BALL_SIZE = 12
BRICK_COLUMNS = 10
BRICK_ROWS = 5
BRICK_WIDTH = 56
BRICK_HEIGHT = 20
BRICK_GAP = 8
BRICK_TOP = 72


@dataclass
class Brick:
    x: float
    y: float
    width: float
    height: float
    color: str
    alive: bool = True


@dataclass
class Paddle:
    x: float
    y: float
    width: float = PADDLE_WIDTH
    height: float = PADDLE_HEIGHT
    speed: float = 8.0

    def move(self, direction: int, screen_width: int = SCREEN_WIDTH) -> None:
        self.x += direction * self.speed
        self.x = max(0, min(self.x, screen_width - self.width))


@dataclass
class Ball:
    x: float
    y: float
    vx: float
    vy: float
    size: float = BALL_SIZE

    def step(self) -> None:
        self.x += self.vx
        self.y += self.vy


class GameState:
    """State container with deterministic update logic."""

    def __init__(self) -> None:
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.score = 0
        self.lives = 3
        self.status = "ready"
        self.message = "Press Space to launch"
        self.paddle = Paddle(x=(self.width - PADDLE_WIDTH) / 2, y=self.height - 48)
        self.ball = Ball(
            x=(self.width - BALL_SIZE) / 2,
            y=self.paddle.y - BALL_SIZE - 10,
            vx=4.0,
            vy=-4.0,
        )
        self.bricks = self._create_bricks()

    def _create_bricks(self) -> list[Brick]:
        from .palette import PALETTE

        bricks: list[Brick] = []
        total_width = BRICK_COLUMNS * BRICK_WIDTH + (BRICK_COLUMNS - 1) * BRICK_GAP
        offset_x = (self.width - total_width) / 2
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLUMNS):
                bricks.append(
                    Brick(
                        x=offset_x + col * (BRICK_WIDTH + BRICK_GAP),
                        y=BRICK_TOP + row * (BRICK_HEIGHT + BRICK_GAP),
                        width=BRICK_WIDTH,
                        height=BRICK_HEIGHT,
                        color=PALETTE["brick_rows"][row % len(PALETTE["brick_rows"])],
                    )
                )
        return bricks

    def launch(self) -> None:
        if self.status in {"ready", "serve"}:
            self.status = "running"
            self.message = ""

    def update(self, move_left: bool = False, move_right: bool = False, launch: bool = False) -> None:
        if self.status in {"won", "lost"}:
            return

        if launch:
            self.launch()

        direction = int(move_right) - int(move_left)
        self.paddle.move(direction, self.width)

        if self.status in {"ready", "serve"}:
            self.ball.x = self.paddle.x + (self.paddle.width - self.ball.size) / 2
            self.ball.y = self.paddle.y - self.ball.size - 10
            return

        self.ball.step()
        self._bounce_off_walls()
        self._bounce_off_paddle()
        self._break_bricks()
        self._check_bottom()
        self._check_win()

    def _bounce_off_walls(self) -> None:
        if self.ball.x <= 0:
            self.ball.x = 0
            self.ball.vx = abs(self.ball.vx)
        elif self.ball.x + self.ball.size >= self.width:
            self.ball.x = self.width - self.ball.size
            self.ball.vx = -abs(self.ball.vx)

        if self.ball.y <= 0:
            self.ball.y = 0
            self.ball.vy = abs(self.ball.vy)

    def _bounce_off_paddle(self) -> None:
        if self.ball.vy <= 0:
            return
        if not self._intersects(self.ball, self.paddle):
            return

        self.ball.y = self.paddle.y - self.ball.size
        self.ball.vy = -abs(self.ball.vy)
        paddle_center = self.paddle.x + self.paddle.width / 2
        ball_center = self.ball.x + self.ball.size / 2
        offset = (ball_center - paddle_center) / (self.paddle.width / 2)
        self.ball.vx = max(-6.0, min(6.0, offset * 6.0))

    def _break_bricks(self) -> None:
        for brick in self.bricks:
            if not brick.alive:
                continue
            if not self._intersects(self.ball, brick):
                continue

            brick.alive = False
            self.score += 100
            self.ball.vy *= -1
            break

    def _check_bottom(self) -> None:
        if self.ball.y <= self.height:
            return

        self.lives -= 1
        if self.lives <= 0:
            self.status = "lost"
            self.message = "Soft landing failed..."
            return

        self.status = "serve"
        self.message = "Press Space to relaunch"
        self.ball.vx = 4.0
        self.ball.vy = -4.0

    def _check_win(self) -> None:
        if all(not brick.alive for brick in self.bricks):
            self.status = "won"
            self.message = "Pastel victory!"

    @staticmethod
    def _intersects(ball: Ball, rect: Brick | Paddle) -> bool:
        return (
            ball.x < rect.x + rect.width
            and ball.x + ball.size > rect.x
            and ball.y < rect.y + rect.height
            and ball.y + ball.size > rect.y
        )
