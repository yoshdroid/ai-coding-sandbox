import random

class Level:
    def __init__(self, stage):
        self.stage = stage
        random.seed(stage)  # ステージごとに同じランダム
        self.platforms = self.generate_platforms()
        self.goal_x = 200 + stage * 50  # 目的地

    def generate_platforms(self):
        platforms = []
        used_positions = []
        for i in range(10):
            attempts = 0
            while attempts < 100:  # 最大試行回数
                x = random.randint(0, 200)
                y = random.randint(50, 100)
                width = random.randint(20, 50)
                # 重なりチェック
                overlap = False
                for px, py, pw in used_positions:
                    if not (x + width < px or px + pw < x or y + 5 < py or py + 5 < y):
                        overlap = True
                        break
                if not overlap:
                    platforms.append({'x': x, 'y': y, 'width': width})
                    used_positions.append((x, y, width))
                    break
                attempts += 1
        return platforms

    def check_collision(self, player):
        # 簡易衝突判定
        for plat in self.platforms:
            if (player.x < plat['x'] + plat['width'] and
                player.x + 8 > plat['x'] and  # プレイヤー幅8仮定
                player.y < plat['y'] + 5 and
                player.y + 8 > plat['y']):
                return True
        return False