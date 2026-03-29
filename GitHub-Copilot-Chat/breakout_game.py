import pyxel
import math

# Pyxelの標準16色パレット（インデックス）を使用
# 0=黒, 1=紺, 2=暗赤, 3=暗紫, 4=暗緑, 5=暗スレートグレー, 6=暗オリーブ, 7=ライトグレー
# 8=グレー, 9=青, 10=赤, 11=マゼンタ, 12=緑, 13=シアン, 14=ライトグレー, 15=白

COLOR_BG = 0          # 黒（背景）
COLOR_PADDLE = 9      # 青（パドル）
COLOR_BALL = 11       # マゼンタ（ボール）
COLOR_BLOCKS = [10, 12, 13, 2]  # 赤、緑、シアン、暗赤（ブロック）
COLOR_TEXT = 15       # 白（テキスト）
COLOR_BORDER = 7      # ライトグレー（枠線）

class Ball:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = 4
        self.wall_collided = False
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.wall_collided = False
        
        # 壁との衝突
        if self.x - self.radius < 0 or self.x + self.radius > pyxel.width:
            self.speed_x = -self.speed_x
            self.x = max(self.radius, min(pyxel.width - self.radius, self.x))
            self.wall_collided = True
        
        if self.y - self.radius < 0:
            self.speed_y = -self.speed_y
            self.y = max(self.radius, self.y)
            self.wall_collided = True
    
    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, COLOR_BALL)
    
    def is_out_of_bounds(self):
        return self.y - self.radius > pyxel.height

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
    
    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(0, self.x - self.speed)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(pyxel.width - self.width, self.x + self.speed)
    
    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, COLOR_PADDLE)
    
    def get_rect(self):
        return (self.x, self.y, self.width, self.height)

class Block:
    def __init__(self, x, y, width, height, color_index, durability=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_index = color_index
        self.durability = durability
        self.alive = True
    
    def draw(self):
        if self.alive:
            color = COLOR_BLOCKS[self.color_index % 4]
            pyxel.rect(self.x, self.y, self.width, self.height, color)
            # ブロックの枠線
            pyxel.rectb(self.x, self.y, self.width, self.height, COLOR_BORDER)
            
            # 耐久度が3以上の場合、耐久度の数字を表示
            if self.durability > 1:
                pyxel.text(self.x + 10, self.y + 4, str(self.durability), COLOR_TEXT)
    
    def get_rect(self):
        return (self.x, self.y, self.width, self.height)
    
    def take_damage(self):
        """ダメージを受ける"""
        self.durability -= 1
        if self.durability <= 0:
            self.alive = False

class BreakoutGame:
    def __init__(self):
        # Pyxel初期化
        pyxel.init(256, 192, "Pastel Breakout Game", 60)
        
        # ゲーム状態
        self.game_state = "ready"  # "ready", "playing", "game_over", "won"
        self.score = 0
        self.level = 1
        self.flash_timer = 0  # 画面フラッシュタイマー
        
        # パドル
        self.paddle = Paddle(256 // 2 - 25, 176, 50, 8)
        
        # ボール（初速を遅く）
        self.ball = Ball(128, 100, 1, -1)
        
        # ブロック
        self.blocks = self._create_blocks()
        
        pyxel.run(self.update, self.draw)
    
    def _reset_game(self):
        """ゲームをリセット"""
        self.game_state = "ready"
        self.score = 0
        self.level = 1
        self.paddle = Paddle(256 // 2 - 25, 176, 50, 8)
        self.ball = Ball(128, 100, 1, -1)
        self.blocks = self._create_blocks()
    
    def _create_blocks(self):
        blocks = []
        block_width = 28
        block_height = 12
        spacing_x = 2
        spacing_y = 2
        start_x = 10
        start_y = 20
        cols = 8
        rows = 4
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (block_width + spacing_x)
                y = start_y + row * (block_height + spacing_y)
                color_index = (row + col) % 4
                # シアン色（color_index=2）のブロックは耐久度3
                durability = 3 if color_index == 2 else 1
                blocks.append(Block(x, y, block_width, block_height, color_index, durability))
        
        return blocks
    
    def _check_collision(self, rect1, rect2):
        """矩形同士の衝突判定"""
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)
    
    def _check_ball_rect_collision(self, ball, rect):
        """ボールと矩形の衝突判定と反射方向の判定"""
        bx, by = ball.x, ball.y
        rx, ry, rw, rh = rect
        
        # 最も近い点を求める
        closest_x = max(rx, min(bx, rx + rw))
        closest_y = max(ry, min(by, ry + rh))
        
        distance = math.sqrt((bx - closest_x)**2 + (by - closest_y)**2)
        
        if distance < ball.radius:
            # 衝突した側を判定
            if closest_x == bx:
                # 上下の面に衝突
                ball.speed_y = -ball.speed_y
            else:
                # 左右の面に衝突
                ball.speed_x = -ball.speed_x
            return True
        return False
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        if self.game_state == "ready":
            if pyxel.btnp(pyxel.KEY_R):
                self.game_state = "playing"
        
        elif self.game_state == "playing":
            self.paddle.update()
            self.ball.update()
            
            # パドルとの衝突
            if self._check_ball_rect_collision(self.ball, self.paddle.get_rect()):
                # パドルの位置に応じてボールの水平速度を調整
                paddle_rect = self.paddle.get_rect()
                paddle_center = paddle_rect[0] + paddle_rect[2] // 2
                hit_position = (self.ball.x - paddle_center) / (paddle_rect[2] // 2)
                self.ball.speed_x += hit_position * 2
            
            # ブロックとの衝突
            for block in self.blocks:
                if block.alive and self._check_ball_rect_collision(self.ball, block.get_rect()):
                    is_cyan = (block.color_index == 2)  # シアン色判定
                    block.take_damage()
                    if not block.alive:
                        # シアン色は50点、その他は10点
                        score_gained = 50 if is_cyan else 10
                        self.score += score_gained
            
            # ゲームオーバー判定
            if self.ball.is_out_of_bounds():
                self.game_state = "game_over"
            
            # ゲームクリア判定
            if all(not block.alive for block in self.blocks):
                self.game_state = "won"
        
        elif self.game_state in ("game_over", "won"):
            if pyxel.btnp(pyxel.KEY_R):
                self._reset_game()
    
    def draw(self):
        pyxel.cls(COLOR_BG)  # 背景色で塗りつぶし
        
        # ゲーム描画
        self.paddle.draw()
        self.ball.draw()
        
        for block in self.blocks:
            block.draw()
        
        # ボーダー
        pyxel.rectb(0, 0, pyxel.width, pyxel.height, COLOR_BORDER)
        
        # スコア表示
        pyxel.text(5, 5, f"Score: {self.score}", COLOR_TEXT)
        
        # ゲーム状態表示
        if self.game_state == "ready":
            pyxel.text(256 // 2 - 50, 192 // 2 - 20, "PASTEL BREAKOUT", COLOR_TEXT)
            pyxel.text(256 // 2 - 60, 192 // 2 + 10, "Press R to start", COLOR_TEXT)
        elif self.game_state == "game_over":
            pyxel.text(256 // 2 - 40, 192 // 2 - 10, "GAME OVER", COLOR_TEXT)
            pyxel.text(256 // 2 - 50, 192 // 2 + 10, "Press R to restart", COLOR_TEXT)
        elif self.game_state == "won":
            pyxel.text(256 // 2 - 20, 192 // 2 - 10, "YOU WIN!", COLOR_TEXT)
            pyxel.text(256 // 2 - 50, 192 // 2 + 10, "Press R to restart", COLOR_TEXT)

if __name__ == "__main__":
    BreakoutGame()
