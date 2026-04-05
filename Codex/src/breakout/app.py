"""Tkinter front end for the breakout game."""

from __future__ import annotations

import tkinter as tk

from .engine import GameState
from .palette import PALETTE


class BreakoutApp:
    def __init__(self) -> None:
        self.state = GameState()
        self.root = tk.Tk()
        self.root.title("Pastel Breakout")
        self.root.configure(bg=PALETTE["background"])
        self.canvas = tk.Canvas(
            self.root,
            width=self.state.width,
            height=self.state.height,
            bg=PALETTE["background"],
            highlightthickness=0,
        )
        self.canvas.pack(padx=16, pady=16)
        self.keys: set[str] = set()
        self.root.bind("<KeyPress>", self._on_keypress)
        self.root.bind("<KeyRelease>", self._on_keyrelease)

    def _on_keypress(self, event: tk.Event) -> None:
        self.keys.add(event.keysym)
        if event.keysym == "space":
            self.state.launch()

    def _on_keyrelease(self, event: tk.Event) -> None:
        self.keys.discard(event.keysym)

    def run(self) -> None:
        self._tick()
        self.root.mainloop()

    def _tick(self) -> None:
        self.state.update(
            move_left="Left" in self.keys,
            move_right="Right" in self.keys,
        )
        self._draw()
        self.root.after(16, self._tick)

    def _draw(self) -> None:
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            12,
            12,
            self.state.width - 12,
            self.state.height - 12,
            fill=PALETTE["panel"],
            outline=PALETTE["outline"],
            width=2,
        )
        self.canvas.create_text(
            32,
            28,
            anchor="w",
            text=f"Score {self.state.score}",
            fill=PALETTE["text"],
            font=("Yu Gothic UI", 14, "bold"),
        )
        self.canvas.create_text(
            self.state.width - 32,
            28,
            anchor="e",
            text=f"Lives {self.state.lives}",
            fill=PALETTE["text"],
            font=("Yu Gothic UI", 14, "bold"),
        )

        for brick in self.state.bricks:
            if not brick.alive:
                continue
            self.canvas.create_rectangle(
                brick.x,
                brick.y,
                brick.x + brick.width,
                brick.y + brick.height,
                fill=brick.color,
                outline=PALETTE["outline"],
                width=2,
            )

        paddle = self.state.paddle
        self.canvas.create_rectangle(
            paddle.x,
            paddle.y,
            paddle.x + paddle.width,
            paddle.y + paddle.height,
            fill=PALETTE["paddle"],
            outline=PALETTE["outline"],
            width=2,
        )

        ball = self.state.ball
        self.canvas.create_oval(
            ball.x,
            ball.y,
            ball.x + ball.size,
            ball.y + ball.size,
            fill=PALETTE["ball"],
            outline=PALETTE["outline"],
            width=2,
        )

        if self.state.message:
            message_color = PALETTE["text"]
            if self.state.status == "won":
                message_color = PALETTE["victory"]
            elif self.state.status == "lost":
                message_color = PALETTE["game_over"]
            self.canvas.create_text(
                self.state.width / 2,
                self.state.height - 28,
                text=self.state.message,
                fill=message_color,
                font=("Yu Gothic UI", 16, "bold"),
            )

