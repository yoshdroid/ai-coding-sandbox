import os
import pyxel

AUTO_PLAY = os.path.exists("autoplay.txt")
current_frame = 0

def auto_control(frame):
    # 左右移動とジャンプを簡易的にシーケンスで指定
    wx = 0
    jump = False
    if frame < 80:
        wx = 2
    elif frame < 140:
        wx = -2
    elif frame < 220:
        wx = 2
    else:
        wx = 0
    if frame in [24, 84, 144, 204]:
        jump = True
    return wx, jump

class Player:
    def __init__(self):
        self.x = 10
        self.y = 100
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.wall_left = False
        self.wall_right = False

    def update(self):
        global current_frame
        # 入力処理
        if AUTO_PLAY:
            self.vx, jump = auto_control(current_frame)
            if jump:
                if self.on_ground:
                    self.vy = -5
                elif self.wall_left:
                    self.vy = -5
                    self.vx = 2
                elif self.wall_right:
                    self.vy = -5
                    self.vx = -2
        else:
            if pyxel.btn(pyxel.KEY_LEFT):
                self.vx = -2
            elif pyxel.btn(pyxel.KEY_RIGHT):
                self.vx = 2
            else:
                self.vx = 0

            # ジャンプと壁ジャンプ
            if pyxel.btnp(pyxel.KEY_SPACE):
                if self.on_ground:
                    self.vy = -5
                elif self.wall_left:
                    self.vy = -5
                    self.vx = 2  # 右にジャンプ
                elif self.wall_right:
                    self.vy = -5
                    self.vx = -2  # 左にジャンプ

        # 重力
        self.vy += 0.5

        # 位置更新
        self.x += self.vx
        self.y += self.vy

        # 初期化
        self.on_ground = False
        self.wall_left = False
        self.wall_right = False

        # フレームカウンタ更新 (自動プレイ用)
        current_frame += 1

class Platform:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class Spike:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

# ゴール位置
goals = [
    (140, 20),  # Stage 1
    (140, 10),  # Stage 2
    (140, 5),   # Stage 3
    (140, 0),   # Stage 4
]

def generate_platforms(goal_x, goal_y, stage):
    platforms = [Platform(0, 120-8, 160, 8)]  # 地面
    # 壁：通れないが壁ジャンプなし
    platforms.append(Platform(0, 0, 8, 120))  # 左壁
    platforms.append(Platform(152, 0, 8, 120))  # 右壁
    # 足場生成：スタートからゴールへ到達可能なパス
    current_x = 10
    current_y = 100
    step = 0
    while current_y > goal_y + 10 and step < 8:
        next_x = current_x + 25 + (step % 2) * 15
        next_y = current_y - 12 - (step % 3) * 3
        if next_x > goal_x - 20: next_x = goal_x - 20
        if next_y < goal_y + 10: next_y = goal_y + 10
        platforms.append(Platform(next_x, next_y, 20, 8))
        current_x = next_x
        current_y = next_y
        step += 1
    return platforms

def generate_spikes(stage):
    if stage < 2:
        return []
    spikes = []
    import random
    random.seed(stage)
    for i in range(stage):
        x = 40 + i * 25 + random.randint(0, 20)
        y = 90 - i * 15 + random.randint(0, 10)
        if y < 10: y = 10
        spikes.append(Spike(x, y, 10, 10))
    return spikes

# ステージ生成
stages = [generate_platforms(goals[i][0], goals[i][1], i) for i in range(4)]
spikes_list = [generate_spikes(i) for i in range(4)]

current_stage = 0
platforms = stages[current_stage]
goal_x, goal_y = goals[current_stage]
current_spikes = spikes_list[current_stage]
player = Player()

def check_collision(player, platform):
    px, py, pw, ph = player.x, player.y, 8, 8
    bx, by, bw, bh = platform.x, platform.y, platform.w, platform.h

    if px < bx + bw and px + pw > bx and py < by + bh and py + ph > by:
        # 衝突方向判定
        overlap_left = (px + pw) - bx
        overlap_right = (bx + bw) - px
        overlap_top = (py + ph) - by
        overlap_bottom = (by + bh) - py

        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_overlap == overlap_top and player.vy > 0:  # 上から着地
            player.y = by - ph
            player.vy = 0
            player.on_ground = True
        elif min_overlap == overlap_bottom and player.vy < 0:  # 下から頭突き
            player.y = by + bh
            player.vy = 0
        elif min_overlap == overlap_left and player.vx > 0 and bx != 0 and bx != 152:  # 右から左壁（壁以外）
            player.x = bx - pw
            player.vx = 0
            player.wall_left = True
        elif min_overlap == overlap_right and player.vx < 0 and bx != 0 and bx != 152:  # 左から右壁（壁以外）
            player.x = bx + bw
            player.vx = 0
            player.wall_right = True

def update():
    global current_stage, platforms, goal_x, goal_y, current_spikes, player
    # リトライ
    if pyxel.btnp(pyxel.KEY_R):
        player.x = 10
        player.y = 100
        player.vx = 0
        player.vy = 0

    player.update()

    # プラットフォームとの衝突
    for p in platforms:
        check_collision(player, p)

    # スパイクとの衝突
    for s in current_spikes:
        if (player.x < s.x + s.w and player.x + 8 > s.x and
            player.y < s.y + s.h and player.y + 8 > s.y):
            # リトライ
            player.x = 10
            player.y = 100
            player.vx = 0
            player.vy = 0

    # ゴールチェック
    if (player.x < goal_x + 10 and player.x + 8 > goal_x and
        player.y < goal_y + 10 and player.y + 8 > goal_y):
        # 次のステージへ
        current_stage += 1
        if current_stage < len(stages):
            platforms = stages[current_stage]
            goal_x, goal_y = goals[current_stage]
            current_spikes = spikes_list[current_stage]
            player.x = 10
            player.y = 100
            player.vx = 0
            player.vy = 0
        # 全クリアしたら何もしない

def draw():
    pyxel.cls(0)
    # プラットフォーム描画
    for p in platforms:
        pyxel.rect(p.x, p.y, p.w, p.h, 7)
    # スパイク描画
    for s in current_spikes:
        pyxel.rect(s.x, s.y, s.w, s.h, 8)  # 赤
    # ゴール描画
    pyxel.rect(goal_x, goal_y, 10, 10, 10)
    # プレイヤー描画
    pyxel.rect(player.x, player.y, 8, 8, 11)
    # ステージ表示
    pyxel.text(5, 5, f"Stage {current_stage + 1}", 7)
    if current_stage >= len(stages):
        pyxel.text(50, 50, "All Clear!", 7)

pyxel.init(160, 120)
pyxel.run(update, draw)