"""
レベルクラスのテスト

このテストファイルは、platformer.level モジュール内の Level クラスの
各メソッドが正しく動作することを確認します。
特に、レベル生成、プラットフォーム衝突検出、ゴール判定などを検証しています。
"""

import pytest
from platformer.level import Level
from platformer.platform import Platform


class TestLevelInitialization:
    """レベルの初期化に関するテスト"""
    
    def test_level_creation(self):
        """
        テスト: レベルが正しく初期化されることを確認
        
        Level コンストラクタで指定した値が、
        正しくプロパティに設定されることを確認します。
        """
        level = Level(stage_number=1, screen_width=256, screen_height=224)
        assert level.stage_number == 1
        assert level.screen_width == 256
        assert level.screen_height == 224
        assert level.goal is not None
    
    def test_level_has_platforms(self):
        """
        テスト: レベルにプラットフォームが生成されることを確認
        
        Level が生成されたとき、
        プラットフォームのリストが空でないことを確認します。
        """
        level = Level()
        assert len(level.platforms) > 0
    
    def test_level_has_goal(self):
        """
        テスト: レベルにゴールが配置されることを確認
        
        Level が生成されたとき、
        ゴールが画面右端に配置されていることを確認します。
        """
        level = Level()
        goal = level.get_goal()
        assert goal is not None
        assert goal.platform_type == "goal"
        assert goal.x > level.screen_width - 100


class TestLevelDifficulty:
    """レベルの難易度調整に関するテスト"""
    
    def test_difficulty_increases_with_stage(self):
        """
        テスト: ステージが進むたびに難易度がゲットされることを確認
        
        ステージ1 と ステージ2 を比較して、
        ステージ2 のプラットフォーム間隔がより広いことを確認します。
        """
        level1 = Level(stage_number=1)
        level2 = Level(stage_number=2)
        
        # ステージ2の方がプラットフォーム間隔が広い
        assert level2.platform_gap[0] >= level1.platform_gap[0]
        assert level2.platform_gap[1] >= level1.platform_gap[1]
    
    def test_difficulty_has_maximum_gap(self):
        """
        テスト: プラットフォーム間隔の最大値が制限されることを確認
        
        かなり高いステージでも、プラットフォーム間隔が
        設定した最大値を超えないことを確認します。
        """
        level = Level(stage_number=100)
        assert level.platform_gap[1] <= 100


class TestLevelPlatforms:
    """レベル内のプラットフォーム管理に関するテスト"""
    
    def test_get_platforms(self):
        """
        テスト: すべてのプラットフォームが取得できることを確認
        
        get_platforms() メソッドが、
        存在するすべてのプラットフォームを返すことを確認します。
        """
        level = Level()
        platforms = level.get_platforms()
        assert len(platforms) > 0
        assert isinstance(platforms[0], Platform)
    
    def test_start_platform_exists(self):
        """
        テスト: スタート地点のプラットフォームが存在することを確認
        
        レベルの最初の要素がプラットフォームであり、
        画面左側に配置されていることを確認します。
        """
        level = Level()
        start_platform = level.platforms[0]
        assert start_platform.x < 50  # 画面左近くに配置


class TestLevelCollisionDetection:
    """レベル内の衝突検出に関するテスト"""
    
    def test_get_colliding_platforms(self):
        """
        テスト: 衝突しているプラットフォームが検出されることを確認
        
        矩形がプラットフォームと衝突しているとき、
        get_colliding_platforms() がそのプラットフォームを含むリストを
        返すことを確認します。
        """
        level = Level()
        platforms = level.get_platforms()
        
        # 最初のプラットフォームと衝突する矩形
        first_platform = platforms[0]
        colliding_rect = (
            first_platform.x + 10,
            first_platform.y + 5,
            10,
            10
        )
        
        colliding = level.get_colliding_platforms(colliding_rect)
        assert len(colliding) > 0
        assert first_platform in colliding
    
    def test_no_collision_with_empty_space(self):
        """
        テスト: 空いているスペースではプラットフォームが検出されないことを確認
        
        矩形がどのプラットフォームとも衝突していないとき、
        get_colliding_platforms() が空のリストを返すことを確認します。
        """
        level = Level()
        
        # どのプラットフォームとも衝突しない矩形
        non_colliding_rect = (-50, -50, 10, 10)
        colliding = level.get_colliding_platforms(non_colliding_rect)
        assert len(colliding) == 0


class TestLevelStandingPlatform:
    """レベル内の着地判定に関するテスト"""
    
    def test_get_standing_platform(self):
        """
        テスト: プレイヤーが立っているプラットフォームが取得されることを確認
        
        プレイヤーがプラットフォームの上に着地したとき、
        get_standing_platform() がそのプラットフォームを返すことを確認します。
        """
        level = Level()
        platform = level.platforms[0]
        
        # プラットフォームの上から落下している矩形
        prev_y = platform.y - 20  # 前フレームで上にいた
        current_rect = (
            platform.x + 10,
            platform.y + 5,  # プラットフォーム に貫通した
            10,
            10
        )
        
        standing = level.get_standing_platform(current_rect, prev_y)
        assert standing is not None
        assert standing == platform
    
    def test_no_standing_platform_in_air(self):
        """
        テスト: 空中にいるときは立っているプラットフォームが None であることを確認
        
        プレイヤーが空中にいるとき、
        get_standing_platform() が None を返すことを確認します。
        """
        level = Level()
        
        # どのプラットフォームにも接していない矩形
        prev_y = 50
        rect = (128, 60, 10, 10)
        
        standing = level.get_standing_platform(rect, prev_y)
        assert standing is None


class TestLevelWallJump:
    """レベル内の壁ジャンプに関するテスト"""
    
    def test_get_left_wall_platform(self):
        """
        テスト: 左の壁に接しているプラットフォームが検出されることを確認
        
        プレイヤーが左の壁から壁ジャンプするとき、
        get_wall_platform() が壁のプラットフォームを返すことを確認します。
        """
        level = Level()
        platform = Platform(x=100, y=50, width=10, height=100)
        level.platforms.append(platform)
        
        # プラットフォームの左側から接近している矩形
        prev_x = 80  # 前フレームでプラットフォームの左にいた
        current_rect = (101, 75, 10, 10)
        
        wall = level.get_wall_platform(current_rect, prev_x, wall_direction=-1)
        assert wall is not None
        assert wall == platform


class TestLevelGoal:
    """レベル内のゴール判定に関するテスト"""
    
    def test_is_reaching_goal(self):
        """
        テスト: プレイヤーがゴールに到達したかが判定されることを確認
        
        プレイヤーがゴールに接したとき、
        is_reaching_goal() が True を返すことを確認します。
        """
        level = Level()
        goal = level.get_goal()
        
        # ゴールと衝突している矩形
        colliding_rect = (
            goal.x + 10,
            goal.y + 5,
            10,
            10
        )
        
        assert level.is_reaching_goal(colliding_rect) is True
    
    def test_not_reaching_goal(self):
        """
        テスト: プレイヤーがゴールに到達していないときは False が返されることを確認
        
        プレイヤーがゴールに接していないとき、
        is_reaching_goal() が False を返すことを確認します。
        """
        level = Level()
        
        # ゴールから遠い矩形
        non_goal_rect = (10, 50, 10, 10)
        assert level.is_reaching_goal(non_goal_rect) is False
