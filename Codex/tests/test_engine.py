from breakout.engine import GameState


def test_ball_bounces_from_left_wall() -> None:
    # 左端に向かったボールが壁で反射し、画面外へ出ないことを確認する。
    state = GameState()
    state.status = "running"
    state.ball.x = 1
    state.ball.vx = -4

    state.update()

    assert state.ball.vx == 4
    assert state.ball.x == 0


def test_ball_breaks_brick_and_adds_score() -> None:
    # ボールがブロックに当たると、ブロックが消えてスコアが加算されることを確認する。
    state = GameState()
    state.status = "running"
    brick = state.bricks[0]
    state.ball.x = brick.x + 10
    state.ball.y = brick.y + 10
    state.ball.vx = 0
    state.ball.vy = -4

    state.update()

    assert brick.alive is False
    assert state.score == 100
    assert state.ball.vy == 4


def test_ball_bounces_from_paddle_with_upward_velocity() -> None:
    # 落下中のボールがパドルに当たったら、上向きに跳ね返ることを確認する。
    state = GameState()
    state.status = "running"
    state.ball.x = state.paddle.x + state.paddle.width / 2
    state.ball.y = state.paddle.y - state.ball.size - 1
    state.ball.vx = 0
    state.ball.vy = 4

    state.update()

    assert state.ball.vy < 0


def test_life_is_lost_when_ball_falls_below_screen() -> None:
    # ボールが画面下へ落ちたとき、残機が減ってサーブ待ち状態になることを確認する。
    state = GameState()
    state.status = "running"
    state.ball.y = state.height + 5
    state.ball.vy = 4

    state.update()

    assert state.lives == 2
    assert state.status == "serve"
    assert state.message == "Press Space to relaunch"


def test_game_is_won_when_last_brick_is_removed() -> None:
    # 最後のブロックを壊した瞬間に、ゲームがクリア状態へ遷移することを確認する。
    state = GameState()
    for brick in state.bricks[:-1]:
        brick.alive = False
    last_brick = state.bricks[-1]
    state.status = "running"
    state.ball.x = last_brick.x + 8
    state.ball.y = last_brick.y + 8
    state.ball.vx = 0
    state.ball.vy = -4

    state.update()

    assert state.status == "won"
    assert state.message == "Pastel victory!"


def test_launch_keeps_ball_attached_until_space() -> None:
    # 発射前はボールがパドルに追従し、発射操作でゲームが進行状態になることを確認する。
    state = GameState()
    initial_y = state.ball.y

    state.update(move_right=True)

    assert state.status == "ready"
    assert state.ball.y == initial_y

    state.update(launch=True)

    assert state.status == "running"
