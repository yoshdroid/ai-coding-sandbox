# メインゲーム実装

import pyxel
from platformer.player import Player
from platformer.level import Level


class Game:
    """
    Pyxelを使用したプラットフォーマーゲームのメインクラス
    
    ゲームループ、入力処理、物理演算、描画を管理します。
    
    属性:
        screen_width (int): 画面幅（ピクセル）
        screen_height (int): 画面高さ（ピクセル）
        player (Player): プレイヤーキャラクター
        current_level (Level): 現在のレベル
        stage_number (int): 現在のステージ番号
        prev_player_y (float): 前フレームでのプレイヤーの y 座標
        prev_player_x (float): 前フレームでのプレイヤーの x 座標
    """
    
    def __init__(self, screen_width=256, screen_height=224):
        """
        ゲームを初期化する
        
        Args:
            screen_width (int): 画面幅
            screen_height (int): 画面高さ
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Pyxelの初期化
        pyxel.init(self.screen_width, self.screen_height, title="Platformer Game")
        
        # ゲーム状態
        self.player = Player(x=30, y=self.screen_height - 60)
        self.stage_number = 1
        self.current_level = Level(stage_number=self.stage_number,
                                   screen_width=self.screen_width,
                                   screen_height=self.screen_height)
        
        # 物理演算用の前フレーム位置
        self.prev_player_y = self.player.y
        self.prev_player_x = self.player.x
        
        # ゴール判定用のフレームカウンター
        self.frame_count = 0
        
        # ゲームループの開始
        pyxel.run(self.update, self.draw)
    
    def update(self):
        """
        毎フレーム実行される更新ロジック
        入力処理、物理演算、衝突判定を行う
        """
        # フレームカウンター更新
        self.frame_count += 1
        
        # ゲーム終了条件（ESCキー）
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        
        # 前フレームの位置を保存
        self.prev_player_x = self.player.x
        self.prev_player_y = self.player.y
        
        # 入力処理
        self._handle_input()
        
        # プレイヤーを更新（重力など）
        self.player.update()
        
        # 衝突判定と物理応答
        self._handle_collisions()
        
        # ゴール判定（プラットフォームに乗っているかは関係なく、ゴール領域に到達したらOK）
        if self.current_level.is_reaching_goal(self.player.get_bounds()):
            self._next_stage()
    
    def _handle_input(self):
        """
        ユーザー入力を処理する
        """
        # ジャンプ処理を最初に行う（優先度を上げる）
        # スペースキーが押された場合
        if pyxel.btnp(pyxel.KEY_SPACE):
            # 地面にいる場合はジャンプ
            if self.player.is_on_ground:
                self.player.jump()
            # 壁に接しているときは壁ジャンプ
            elif self.player.is_on_wall:
                self.player.wall_jump(self.player.wall_direction)
        
        # 横移動
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.player.move_left()
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.player.move_right()
        else:
            self.player.stop_horizontal_movement()
    
    def _handle_collisions(self):
        """
        プレイヤーとプラットフォームの衝突判定と応答を処理する
        """
        player_rect = self.player.get_bounds()
        
        # 初期状態：地面と壁に接していないと仮定
        self.player.set_on_ground(False)
        self.player.set_on_wall(False)
        
        # 着地判定
        standing_platform = self.current_level.get_standing_platform(
            player_rect, self.prev_player_y
        )
        if standing_platform:
            # プレイヤーをプラットフォームの上に配置
            self.player.set_on_ground(True)
            self.player.y = standing_platform.y - self.player.height
        
        # 壁判定（左と右は同時には影響を与えない）
        wall_platform_left = self.current_level.get_wall_platform(
            player_rect, self.prev_player_x, wall_direction=-1
        )
        wall_platform_right = self.current_level.get_wall_platform(
            player_rect, self.prev_player_x, wall_direction=1
        )
        
        # 左の壁が優先される
        if wall_platform_left:
            self.player.set_on_wall(True, wall_direction=-1)
            # 左の壁右側に配置：壁から右に押し出す
            self.player.x = wall_platform_left.x + wall_platform_left.width
        elif wall_platform_right:
            self.player.set_on_wall(True, wall_direction=1)
            # 右の壁左側に配置：壁から左に押し出す
            self.player.x = wall_platform_right.x - self.player.width
        
        # 天井判定
        ceiling_platforms = [p for p in self.current_level.get_platforms()
                            if p.is_colliding_from_bottom(player_rect, self.prev_player_y)]
        if ceiling_platforms:
            self.player.vy = 0
            self.player.y = ceiling_platforms[0].y + ceiling_platforms[0].height
        
        # 画面外に落ちたらステージをリセット
        if self.player.y > self.screen_height:
            self._reset_stage()
    
    def _next_stage(self):
        """
        次のステージに進む
        """
        self.stage_number += 1
        self.current_level = Level(
            stage_number=self.stage_number,
            screen_width=self.screen_width,
            screen_height=self.screen_height
        )
        self.player.x = 30
        self.player.y = self.screen_height - 60
        self.player.vx = 0
        self.player.vy = 0
    
    def _reset_stage(self):
        """
        現在のステージをリセット
        """
        self.player.x = 30
        self.player.y = self.screen_height - 60
        self.player.vx = 0
        self.player.vy = 0
    
    def draw(self):
        """
        毎フレーム実行される描画ロジック
        """
        # 画面をクリア
        pyxel.cls(0)
        
        # ステージ番号を表示
        pyxel.text(5, 5, f"Stage: {self.stage_number}", 7)
        
        # プラットフォームを描画
        self._draw_platforms()
        
        # ゴールを描画
        self._draw_goal()
        
        # プレイヤーを描画
        self._draw_player()
    
    def _draw_platforms(self):
        """
        すべてのプラットフォームを描画する
        """
        for platform in self.current_level.get_platforms():
            if platform.platform_type != "goal":
                pyxel.rect(
                    platform.x,
                    platform.y,
                    platform.width,
                    platform.height,
                    2  # 緑色
                )
    
    def _draw_goal(self):
        """
        ゴールを描画する
        ゴールを目立たせるため、点滅させたり、テキストを表示したりする
        """
        goal = self.current_level.get_goal()
        
        # ゴールを点滅させる（10フレームごと）
        blink = (self.frame_count // 10) % 2
        if blink:
            # 黄色で描画
            pyxel.rect(
                int(goal.x),
                int(goal.y),
                goal.width,
                goal.height,
                10  # 黄色
            )
        else:
            # 白色で描画
            pyxel.rect(
                int(goal.x),
                int(goal.y),
                goal.width,
                goal.height,
                7  # 白色
            )
        
        # ゴール目印の矢印を描画
        arrow_x = int(goal.x + goal.width // 2 - 2)
        arrow_y = int(goal.y - 10)
        pyxel.text(arrow_x, arrow_y, "Goal!", 10)
    
    def _draw_player(self):
        """
        プレイヤーを描画する
        """
        pyxel.rect(
            self.player.x,
            self.player.y,
            self.player.width,
            self.player.height,
            8  # 赤色
        )


def main():
    """
    ゲームのエントリーポイント
    """
    game = Game()


if __name__ == "__main__":
    main()
