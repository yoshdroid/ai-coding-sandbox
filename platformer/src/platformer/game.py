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

        # デバッグ用フラグ
        self.debug_wall_contact = False
        self.debug_wall_jump = False
        
        # ゲームループの開始
        pyxel.run(self.update, self.draw)
    
    def update(self):
        """
        毎フレーム実行される更新ロジック
        入力処理、物理演算、衝突判定を行う
        """
        # フレームカウンター更新
        self.frame_count += 1

        # デバッグフラグを毎フレームリセット
        self.debug_wall_contact = False
        self.debug_wall_jump = False
        
        # ゲーム終了条件（ESCキー）
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        
        # 前フレームの位置を保存
        self.prev_player_x = self.player.x
        self.prev_player_y = self.player.y

        # 横移動入力のみ処理（ジャンプは衝突判定後に実行）
        self._handle_horizontal_input()

        # プレイヤーを更新（重力など）
        self.player.update()

        # 衝突判定と物理応答
        self._handle_collisions()

        # ジャンプ入力を処理（壁接触状態を反映した後に実行）
        self._handle_jump_input()

        # ゴール判定（プラットフォームに乗っているかは関係なく、ゴール領域に到達したらOK）
        if self.current_level.is_reaching_goal(self.player.get_bounds()):
            self._next_stage()
    
    def _handle_horizontal_input(self):
        """
        横移動入力を処理する
        """
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.player.move_left()
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.player.move_right()
        else:
            self.player.stop_horizontal_movement()

    def _handle_jump_input(self):
        """
        ジャンプ入力を処理する
        """
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.player.is_on_ground:
                self.player.jump()
            elif self.player.is_on_wall:
#                if (self.player.wall_direction == -1 and pyxel.btn(pyxel.KEY_LEFT)) or \
#                   (self.player.wall_direction == 1 and pyxel.btn(pyxel.KEY_RIGHT)):
# modify input direction condition for wall jump
                if (self.player.wall_direction == 1 and pyxel.btn(pyxel.KEY_LEFT)) or \
                   (self.player.wall_direction == -1 and pyxel.btn(pyxel.KEY_RIGHT)):
                    self.player.wall_jump(self.player.wall_direction)
                    self.debug_wall_jump = True
    
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
            self.debug_wall_contact = True
            # 左の壁（プレイヤーが右に移動して衝突）に衝突したら、壁の左側に配置
            self.player.x = wall_platform_left.x - self.player.width
            # 壁衝突時に横移動を停止
            self.player.vx = 0
        elif wall_platform_right:
            self.player.set_on_wall(True, wall_direction=1)
            self.debug_wall_contact = True
            # 右の壁（プレイヤーが左に移動して衝突）に衝突したら、壁の右側に配置
            self.player.x = wall_platform_right.x + wall_platform_right.width
            # 壁衝突時に横移動を停止
            self.player.vx = 0
        
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
                if platform.orientation == "horizontal":
                    pyxel.rect(
                        platform.x,
                        platform.y,
                        platform.width,
                        platform.height,
                        2  # 緑色
                    )
                elif platform.orientation == "vertical":
                    pyxel.rect(
                        platform.x,
                        platform.y,
                        platform.width,
                        platform.height,
                        3  # 青色（壁を区別）
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

        # デバッグテキスト表示
        status_wall = "YES" if self.debug_wall_contact else "NO"
        status_jump = "YES" if self.debug_wall_jump else "NO"
        wall_direction = self.player.wall_direction
        direction_text = "-" if wall_direction == -1 else ("+" if wall_direction == 1 else "0")
        pyxel.text(5, 15, f"Wall: {status_wall}", 7)
        pyxel.text(5, 25, f"WallJump: {status_jump}", 7)
        pyxel.text(5, 35, f"WallDir: {direction_text}", 7)


def main():
    """
    ゲームのエントリーポイント
    """
    game = Game()


if __name__ == "__main__":
    main()
