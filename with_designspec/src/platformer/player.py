import pyxel

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.facing_right = True

    def move_right(self):
        self.vx = 2
        self.facing_right = True

    def move_left(self):
        self.vx = -2
        self.facing_right = False

    def jump(self):
        if self.on_ground:
            self.vy = -5
            self.on_ground = False

    def wall_jump_right(self):
        self.vx = 3
        self.vy = -5

    def wall_jump_left(self):
        self.vx = -3
        self.vy = -5

    def update(self, level=None):
        self.x += self.vx
        self.y += self.vy
        # 重力
        self.vy += 0.2
        # 地面判定（仮）
        if self.y >= 100:
            self.y = 100
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False
        # 減速
        self.vx *= 0.8

        # 画面下落下判定
        if self.y > 128:
            return "restart"  # リスタートフラグ

        # 衝突判定
        self.can_wall_jump_left = False
        self.can_wall_jump_right = False
        if level:
            for plat in level.platforms:
                if (self.x < plat['x'] + plat['width'] and
                    self.x + 8 > plat['x'] and
                    self.y < plat['y'] + 5 and
                    self.y + 8 > plat['y']):
                    # 衝突時、位置修正
                    if self.vy > 0:  # 下から
                        self.y = plat['y'] - 8
                        self.vy = 0
                        self.on_ground = True
                    elif self.vy < 0:  # 上から
                        self.y = plat['y'] + 5
                        self.vy = 0
                    if self.vx > 0:  # 右から
                        self.x = plat['x'] - 8
                        self.can_wall_jump_left = True
                    elif self.vx < 0:  # 左から
                        self.x = plat['x'] + plat['width']
                        self.can_wall_jump_right = True
        return None