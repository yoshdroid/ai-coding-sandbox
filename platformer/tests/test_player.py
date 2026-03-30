"""
プレイヤークラスのテスト

このテストファイルは、platformer.player モジュール内の Player クラスの
各メソッドが正しく動作することを確認します。
テスト駆動開発（TDD）のアプローチで、各機能をテストしています。
"""

import pytest
from platformer.player import Player


class TestPlayerInitialization:
    """プレイヤーの初期化に関するテスト"""
    
    def test_player_creation_with_default_values(self):
        """
        テスト: デフォルト値でプレイヤーを作成できることを確認
        
        プレイヤーがデフォルト値で初期化されたとき，
        位置は(0, 0)，サイズは(8, 8)であることを確認します。
        """
        player = Player()
        assert player.x == 0.0
        assert player.y == 0.0
        assert player.width == 8
        assert player.height == 8
        assert player.vx == 0.0
        assert player.vy == 0.0
    
    def test_player_creation_with_custom_values(self):
        """
        テスト: カスタム値でプレイヤーを作成できることを確認
        
        プレイヤーがカスタム値で初期化されたとき，
        指定した値で初期化されることを確認します。
        """
        player = Player(x=100, y=200, width=16, height=16)
        assert player.x == 100.0
        assert player.y == 200.0
        assert player.width == 16
        assert player.height == 16
    
    def test_initial_state(self):
        """
        テスト: プレイヤーの初期状態が正しいことを確認
        
        新規作成されたプレイヤーは，地面に接していない，
        ジャンプ中でない，壁に接していない状態であることを確認します。
        """
        player = Player()
        assert player.is_on_ground is False
        assert player.is_jumping is False
        assert player.is_on_wall is False
        assert player.wall_direction == 0


class TestPlayerMovement:
    """プレイヤーの移動に関するテスト"""
    
    def test_move_left(self):
        """
        テスト: 左移動のベロシティが正しく設定されることを確認
        
        move_left() メソッドが呼ばれたとき，
        vx が負の値に設定されることを確認します。
        """
        player = Player()
        player.move_left()
        assert player.vx == -player.move_speed
    
    def test_move_right(self):
        """
        テスト: 右移動のベロシティが正しく設定されることを確認
        
        move_right() メソッドが呼ばれたとき，
        vx が正の値に設定されることを確認します。
        """
        player = Player()
        player.move_right()
        assert player.vx == player.move_speed
    
    def test_stop_horizontal_movement(self):
        """
        テスト: 水平移動の停止が正しく機能することを確認
        
        stop_horizontal_movement() メソッドが呼ばれたとき，
        vx がゼロにリセットされることを確認します。
        """
        player = Player()
        player.move_right()
        assert player.vx != 0.0
        player.stop_horizontal_movement()
        assert player.vx == 0.0
    
    def test_position_update_with_velocity(self):
        """
        テスト: ベロシティが位置に反映されることを確認
        
        プレイヤーが移動ベロシティを持つとき，
        update() メソッド呼び出し後，位置が更新されることを確認します。
        """
        player = Player(x=0, y=0)
        player.vx = 5.0
        player.vy = 0.0
        player.set_on_ground(True)
        player.update()
        assert player.x == 5.0
        assert player.y == 0.0


class TestPlayerJump:
    """プレイヤーのジャンプに関するテスト"""
    
    def test_jump_on_ground(self):
        """
        テスト: 地面にいるときのジャンプが正しく機能することを確認
        
        プレイヤーが地面に接しているときに jump() を呼ぶと，
        垂直速度が負の値に設定されることを確認します。
        """
        player = Player()
        player.set_on_ground(True)
        player.jump()
        assert player.vy == -player.jump_power
        assert player.is_jumping is True
    
    def test_jump_in_air_not_possible(self):
        """
        テスト: 空中での連続ジャンプが禁止されることを確認
        
        プレイヤーが地面に接していないときに jump() を呼ぶと，
        垂直速度が変更されないことを確認します。
        """
        player = Player()
        player.set_on_ground(False)
        initial_vy = player.vy
        player.jump()
        assert player.vy == initial_vy
    
    def test_gravity_applied(self):
        """
        テスト: 重力が正しく適用されることを確認
        
        プレイヤーが地面に接していないときに update() を呼ぶと，
        垂直速度が増加することを確認します。
        """
        player = Player()
        player.set_on_ground(False)
        initial_vy = player.vy
        player.update()
        assert player.vy > initial_vy
    
    def test_max_fall_speed_limit(self):
        """
        テスト: 最大落下速度が制限されることを確認
        
        何度も update() を呼んで落下を続けるとき，
        垂直速度が max_fall_speed を超えないことを確認します。
        """
        player = Player()
        player.set_on_ground(False)
        for _ in range(100):
            player.update()
        assert player.vy <= player.max_fall_speed
    
    def test_reset_jump_flag_on_ground(self):
        """
        テスト: 地面に着地したときジャンプフラグがリセットされることを確認
        
        プレイヤーがジャンプ中に地面に着地すると，
        is_jumping フラグが False にリセットされることを確認します。
        """
        player = Player()
        player.set_on_ground(True)
        player.jump()
        assert player.is_jumping is True
        player.set_on_ground(True)
        assert player.is_jumping is False


class TestPlayerWallJump:
    """プレイヤーの壁ジャンプに関するテスト"""
    
    def test_wall_jump_on_left_wall(self):
        """
        テスト: 左の壁での壁ジャンプが正しく機能することを確認
        
        プレイヤーが左の壁に接しているときに wall_jump(-1) を呼ぶと，
        垂直速度が負になり，水平速度が正になることを確認します。
        """
        player = Player()
        player.set_on_wall(True, wall_direction=-1)
        player.wall_jump(-1)
        assert player.vy == -player.jump_power
        assert player.vx > 0
        assert player.is_on_wall is False
    
    def test_wall_jump_on_right_wall(self):
        """
        テスト: 右の壁での壁ジャンプが正しく機能することを確認
        
        プレイヤーが右の壁に接しているときに wall_jump(1) を呼ぶと，
        垂直速度が負になり，水平速度が負になることを確認します。
        """
        player = Player()
        player.set_on_wall(True, wall_direction=1)
        player.wall_jump(1)
        assert player.vy == -player.jump_power
        assert player.vx < 0
        assert player.is_on_wall is False
    
    def test_wall_jump_not_possible_without_wall(self):
        """
        テスト: 壁に接していないときの壁ジャンプが禁止されることを確認
        
        プレイヤーが壁に接していないときに wall_jump() を呼ぶと，
        何も変わらないことを確認します。
        """
        player = Player()
        player.set_on_wall(False)
        initial_vy = player.vy
        initial_vx = player.vx
        player.wall_jump(-1)
        assert player.vy == initial_vy
        assert player.vx == initial_vx
    
    def test_wall_slide_slows_fall(self):
        """
        テスト: 壁に接しているときの落下速度が低下することを確認
        
        プレイヤーが壁を滑りながら落下するときに，
        垂直速度が制限されることを確認します。
        """
        player = Player()
        player.vy = 5.0
        player.set_on_wall(True, wall_direction=-1)
        assert player.vy <= 1.0


class TestPlayerBounds:
    """プレイヤーの当たり判定に関するテスト"""
    
    def test_get_bounds(self):
        """
        テスト: 当たり判定矩形が正しく取得されることを確認
        
        get_bounds() メソッドが，プレイヤーの位置とサイズを
        正しい形式で返すことを確認します。
        """
        player = Player(x=50, y=100, width=16, height=16)
        bounds = player.get_bounds()
        assert bounds == (50.0, 100.0, 16, 16)
    
    def test_bounds_with_float_position(self):
        """
        テスト: 浮動小数点の座標でも当たり判定が正しく機能することを確認
        
        プレイヤーが浮動小数点の座標を持つとき，
        get_bounds() が正しい値を返すことを確認します。
        """
        player = Player(x=50.5, y=100.3)
        bounds = player.get_bounds()
        assert bounds[0] == 50.5
        assert bounds[1] == 100.3

