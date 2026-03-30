# レベル生成と管理クラス

import random
from platformer.platform import Platform


class Level:
    """
    プラットフォーマーゲームのレベル（ステージ）を管理するクラス
    
    プラットフォームをランダムに生成し、ゴールを配置します。
    プレイヤーの能力で到達可能なパスを生成します。
    
    属性:
        stage_number (int): ステージ番号
        screen_width (int): 画面幅
        screen_height (int): 画面高さ
        platforms (list): プラットフォームのリスト
        goal (Platform): ゴールプラットフォーム
    """
    
    def __init__(self, stage_number=1, screen_width=256, screen_height=224):
        """
        レベルを初期化する
        
        Args:
            stage_number (int): ステージ番号
            screen_width (int): 画面幅（ピクセル）
            screen_height (int): 画面高さ（ピクセル）
        """
        self.stage_number = stage_number
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.platforms = []
        self.goal = None
        
        # ゲーム難易度調整パラメータ
        self.platform_width_range = (40, 80)
        self.platform_height = 12
        self.platform_gap = (30, 80)  # プラットフォーム間の距離
        
        # ステージレベルに応じた難易度調整
        self._adjust_difficulty_for_stage()
        
        # レベルを生成
        self._generate_level()
    
    def _adjust_difficulty_for_stage(self):
        """
        ステージが進むにつれて難易度を上げる
        """
        # ステージが進むたびに、プラットフォーム間の距離を広げる
        difficulty_factor = 0.8 + (self.stage_number - 1) * 0.1
        gap_min, gap_max = self.platform_gap
        new_gap_min = int(gap_min * difficulty_factor)
        new_gap_max = int(gap_max * difficulty_factor)
        
        # 最大値を超えないように制限
        new_gap_max = min(new_gap_max, 100)
        # 最小値が最大値を超えないようにする
        new_gap_min = min(new_gap_min, new_gap_max)
        
        self.platform_gap = (new_gap_min, new_gap_max)
    
    def _generate_level(self):
        """
        ランダムなレベルを生成する
        """
        # 最初のプラットフォーム（スタート地点）
        start_platform = Platform(
            x=20,
            y=self.screen_height - 50,
            width=60,
            height=self.platform_height
        )
        self.platforms.append(start_platform)
        
        current_x = start_platform.x + start_platform.width + 30
        current_y = start_platform.y
        
        # プラットフォームを生成してゴールまで到達させる
        while current_x < self.screen_width - 100:
            # プラットフォームの幅をランダムに決定
            width = random.randint(self.platform_width_range[0], self.platform_width_range[1])
            
            # 高さのオフセット（上下の移動）
            # ステージが進むほど変動幅が大きくなる
            max_height_offset = 40 + (self.stage_number - 1) * 10
            height_offset = random.randint(-max_height_offset, max_height_offset)
            new_y = current_y + height_offset
            
            # 画面の上下の制限内に留まるようにクリップ
            new_y = max(50, min(new_y, self.screen_height - 80))
            
            # プラットフォームを追加
            platform = Platform(
                x=current_x,
                y=new_y,
                width=width,
                height=self.platform_height
            )
            self.platforms.append(platform)
            
            # 次のプラットフォームの位置を計算
            gap = random.randint(self.platform_gap[0], self.platform_gap[1])
            current_x += width + gap
            current_y = new_y
        
        # ゴールを画面右端に配置
        self.goal = Platform(
            x=self.screen_width - 80,
            y=self.screen_height - 50,
            width=60,
            height=self.platform_height,
            platform_type="goal"
        )
        self.platforms.append(self.goal)
    
    def get_platforms(self):
        """
        すべてのプラットフォームを取得する
        
        Returns:
            list: Platform オブジェクトのリスト
        """
        return self.platforms
    
    def get_goal(self):
        """
        ゴールプラットフォームを取得する
        
        Returns:
            Platform: ゴールプラットフォーム
        """
        return self.goal
    
    def get_colliding_platforms(self, rect):
        """
        与えられた矩形と衝突しているプラットフォームを取得する
        
        Args:
            rect (tuple): 判定する矩形 (x, y, width, height)
        
        Returns:
            list: 衝突しているプラットフォームのリスト
        """
        colliding = []
        for platform in self.platforms:
            if platform.is_collision(rect):
                colliding.append(platform)
        return colliding
    
    def get_standing_platform(self, rect, prev_y):
        """
        プレイヤーが立っているプラットフォームを取得する
        
        上からの衝突判定で実装される着地判定を使用します。
        ゴールプラットフォームは除外し、着地判定の対象にしません。
        
        Args:
            rect (tuple): プレイヤーの矩形 (x, y, width, height)
            prev_y (float): 前フレームでのプレイヤーの y 座標
        
        Returns:
            Platform: 立っているプラットフォーム、ない場合は None
        """
        for platform in self.platforms:
            # ゴールについては着地判定をしない（ゴール判定で処理）
            if platform.platform_type != "goal":
                if platform.is_colliding_from_top(rect, prev_y):
                    return platform
        return None
    
    def get_wall_platform(self, rect, prev_x, wall_direction):
        """
        プレイヤーが接している壁のプラットフォームを取得する
        
        Args:
            rect (tuple): プレイヤーの矩形 (x, y, width, height)
            prev_x (float): 前フレームでのプレイヤーの x 座標
            wall_direction (int): 確認する壁の方向（-1: 左, 1: 右）
        
        Returns:
            Platform: 接している壁のプラットフォーム、ない場合は None
        """
        for platform in self.platforms:
            if wall_direction == -1:  # 左の壁を確認
                if platform.is_colliding_from_left(rect, prev_x):
                    return platform
            elif wall_direction == 1:  # 右の壁を確認
                if platform.is_colliding_from_right(rect, prev_x):
                    return platform
        return None
    
    def is_reaching_goal(self, rect):
        """
        プレイヤーがゴールに到達したかを判定する
        
        Args:
            rect (tuple): プレイヤーの矩形 (x, y, width, height)
        
        Returns:
            bool: ゴールに到達している場合 True
        """
        return self.goal.is_collision(rect)
