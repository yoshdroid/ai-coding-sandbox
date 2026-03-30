"""
プラットフォームクラスのテスト

このテストファイルは、platformer.platform モジュール内の Platform クラスの
各メソッドが正しく動作することを確認します。
特に、プレイヤーとプラットフォームの衝突判定パターンを検証しています。
"""

import pytest
from platformer.platform import Platform


class TestPlatformInitialization:
    """プラットフォームの初期化に関するテスト"""
    
    def test_platform_creation(self):
        """
        テスト: プラットフォームが正しく作成されることを確認
        
        Platform コンストラクタで指定した値が、
        正しくプロパティに設定されることを確認します。
        """
        platform = Platform(x=50, y=100, width=100, height=10)
        assert platform.x == 50.0
        assert platform.y == 100.0
        assert platform.width == 100
        assert platform.height == 10
        assert platform.platform_type == "normal"
    
    def test_platform_creation_with_type(self):
        """
        テスト: プラットフォームタイプが設定できることを確認
        
        プラットフォームタイプを "goal" に設定したとき、
        正しく設定されることを確認します。
        """
        platform = Platform(x=0, y=0, width=50, height=50, platform_type="goal")
        assert platform.platform_type == "goal"
    
    def test_platform_creation_with_orientation(self):
        """
        テスト: プラットフォームの向きが設定できることを確認
        
        プラットフォームの向きを "vertical" に設定したとき、
        正しく設定されることを確認します。
        """
        platform = Platform(x=0, y=0, width=50, height=50, orientation="vertical")
        assert platform.orientation == "vertical"
        # デフォルトはhorizontal
        platform_default = Platform(x=0, y=0, width=50, height=50)
        assert platform_default.orientation == "horizontal"
    
    def test_get_bounds(self):
        """
        テスト: 当たり判定矩形が正しく取得されることを確認
        
        get_bounds() メソッドが、プラットフォームの情報を
        タプルの形式で正しく返すことを確認します。
        """
        platform = Platform(x=50, y=100, width=100, height=10)
        bounds = platform.get_bounds()
        assert bounds == (50.0, 100.0, 100, 10)


class TestPlatformCollision:
    """プラットフォームの衝突判定に関するテスト"""
    
    def test_no_collision(self):
        """
        テスト: 衝突していない場合、False が返されることを確認
        
        プラットフォームと矩形が離れているとき、
        is_collision() は False を返すことを確認します。
        """
        platform = Platform(x=0, y=100, width=100, height=10)
        rect = (150, 150, 10, 10)  # プラットフォームから離れた矩形
        assert platform.is_collision(rect) is False
    
    def test_collision_overlap(self):
        """
        テスト: 矩形が重なっている場合、True が返されることを確認
        
        プラットフォームと矩形が重なっているとき、
        is_collision() は True を返すことを確認します。
        """
        platform = Platform(x=0, y=100, width=100, height=10)
        rect = (50, 105, 30, 10)  # プラットフォームと重なっている
        assert platform.is_collision(rect) is True
    
    def test_collision_touching_edge(self):
        """
        テスト: 矩形がプラットフォームの端に接している場合の判定を確認
        
        矩形がプラットフォームの端ちょうどに接しているとき、
        衝突と判定されることを確認します（実装上、端では衝突しない）。
        """
        platform = Platform(x=0, y=100, width=100, height=10)
        # 端ちょうどに接している場合は衝突しない
        rect = (100, 100, 10, 10)  # 右端に接している
        assert platform.is_collision(rect) is False
        
        # 少し重なっている場合は衝突している
        rect_overlapping = (99, 100, 10, 10)
        assert platform.is_collision(rect_overlapping) is True
    def test_collision_from_top(self):
        """
        テスト: 上からの着地判定が正しく機能することを確認
        
        矩形がプラットフォームの上から落下してきて、
        上面に衝突した場合、True が返されることを確認します。
        """
        platform = Platform(x=0, y=100, width=100, height=10)
        prev_y = 80  # 前フレームでプラットフォームの上にいた
        rect = (40, 101, 10, 10)  # 現フレームでプラットフォームに衝突
        assert platform.is_colliding_from_top(rect, prev_y) is True
    
    def test_not_collision_from_top_when_no_overlap(self):
        """
        テスト: 左右で重なっていない場合、着地判定は False を返すことを確認
        
        矩形がプラットフォームと上下で接していても、
        左右で重なっていない場合は衝突と判定されないことを確認します。
        """
        platform = Platform(x=0, y=100, width=100, height=10)
        prev_y = 80
        rect = (150, 101, 10, 10)  # 左右で重なっていない
        assert platform.is_colliding_from_top(rect, prev_y) is False
    
    def test_not_collision_from_top_when_coming_from_inside(self):
        """
        テスト: プラットフォーム内部からの衝突は着地判定にならないことを確認
        
        矩形がプラットフォーム内にいて、
        前フレームで既にプラットフォーム内にあった場合、
        着地と判定されないことを確認します。
        """
        platform = Platform(x=0, y=100, width=100, height=10)
        prev_y = 102  # 前フレームで既にプラットフォーム内
        rect = (40, 105, 10, 10)  # 現フレームも内部
        assert platform.is_colliding_from_top(rect, prev_y) is False


class TestPlatformBottomCollision:
    """プラットフォームの下面衝突（天井）判定に関するテスト"""
    
    def test_collision_from_bottom(self):
        """
        テスト: 下からの天井衝突判定が正しく機能することを確認
        
        矩形がプラットフォームの下から上昇してきて、
        下面に衝突した場合、True が返されることを確認します。
        """
        platform = Platform(x=0, y=100, width=100, height=10)
        prev_y = 120  # 前フレームでプラットフォームの下にいた
        rect = (40, 99, 10, 10)  # 現フレームでプラットフォームに衝突
        assert platform.is_colliding_from_bottom(rect, prev_y) is True
    
    def test_not_collision_from_bottom_when_no_overlap(self):
        """
        テスト: 左右で重なっていない場合、天井衝突判定は False を返すことを確認
        
        矩形がプラットフォームと上下で接していても、
        左右で重なっていない場合は衝突と判定されないことを確認します。
        """
        platform = Platform(x=0, y=100, width=100, height=10)
        prev_y = 120
        rect = (150, 99, 10, 10)  # 左右で重なっていない
        assert platform.is_colliding_from_bottom(rect, prev_y) is False


class TestPlatformLeftCollision:
    """プラットフォームの左面衝突（右側の壁）判定に関するテスト"""
    
    def test_collision_from_left(self):
        """
        テスト: 左からの壁衝突判定が正しく機能することを確認
        
        矩形が左側からプラットフォームに衝突した場合、
        True が返されることを確認します。
        """
        platform = Platform(x=100, y=0, width=10, height=100)
        prev_x = 80  # 前フレームでプラットフォームの左にいた
        rect = (101, 40, 10, 10)  # 現フレームで衝突
        assert platform.is_colliding_from_left(rect, prev_x) is True
    
    def test_not_collision_from_left_when_no_overlap(self):
        """
        テスト: 上下で重なっていない場合、左衝突判定は False を返すことを確認
        
        矩形がプラットフォームと左右で接していても、
        上下で重なっていない場合は衝突と判定されないことを確認します。
        """
        platform = Platform(x=100, y=0, width=10, height=100)
        prev_x = 80
        rect = (101, 150, 10, 10)  # 上下で重なっていない
        assert platform.is_colliding_from_left(rect, prev_x) is False


class TestPlatformRightCollision:
    """プラットフォームの右面衝突（左側の壁）判定に関するテスト"""
    
    def test_collision_from_right(self):
        """
        テスト: 右からの壁衝突判定が正しく機能することを確認
        
        矩形が右側からプラットフォームに衝突した場合、
        True が返されることを確認します。
        """
        platform = Platform(x=100, y=0, width=10, height=100)
        prev_x = 120  # 前フレームでプラットフォームの右にいた
        rect = (99, 40, 10, 10)  # 現フレームで衝突
        assert platform.is_colliding_from_right(rect, prev_x) is True
    
    def test_not_collision_from_right_when_no_overlap(self):
        """
        テスト: 上下で重なっていない場合、右衝突判定は False を返すことを確認
        
        矩形がプラットフォームと左右で接していても、
        上下で重なっていない場合は衝突と判定されないことを確認します。
        """
        platform = Platform(x=100, y=0, width=10, height=100)
        prev_x = 120
        rect = (99, 150, 10, 10)  # 上下で重なっていない
        assert platform.is_colliding_from_right(rect, prev_x) is False
