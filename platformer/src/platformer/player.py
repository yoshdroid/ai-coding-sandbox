# プレイヤーキャラクター管理クラス

class Player:
    """
    プラットフォーマーゲームのプレイヤーキャラクターを管理するクラス
    
    属性:
        x (float): プレイヤーの水平位置
        y (float): プレイヤーの垂直位置
        vx (float): 水平速度
        vy (float): 垂直速度
        width (int): プレイヤーの幅
        height (int): プレイヤーの高さ
        is_jumping (bool): ジャンプ中かどうか
        is_on_ground (bool): 地面に接しているかどうか
        is_on_wall (bool): 壁に接しているかどうか
    """
    
    def __init__(self, x=0, y=0, width=8, height=8):
        """
        プレイヤーを初期化する
        
        Args:
            x (float): 初期水平位置
            y (float): 初期垂直位置
            width (int): プレイヤーの幅
            height (int): プレイヤーの高さ
        """
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0  # 水平速度
        self.vy = 0.0  # 垂直速度
        self.width = width
        self.height = height
        
        # ジャンプと壁ジャンプの状態管理
        self.is_jumping = False
        self.is_on_ground = False
        self.is_on_wall = False
        self.wall_direction = 0  # 壁の方向（-1: 左, 1: 右）
        
        # 物理パラメータ
        self.gravity = 0.4
        self.max_fall_speed = 8.0
        self.jump_power = 5.0  # ジャンプ力
        self.move_speed = 3.0
        
    def update(self):
        """
        プレイヤーの状態を更新する（物理演算）
        毎フレーム呼び出される
        """
        # 重力を適用
        if not self.is_on_ground:
            self.vy += self.gravity
            # 落下速度の最大値を制限
            if self.vy > self.max_fall_speed:
                self.vy = self.max_fall_speed
        
        # 位置を更新
        self.x += self.vx
        self.y += self.vy
    
    def move_left(self):
        """左に移動する"""
        self.vx = -self.move_speed
    
    def move_right(self):
        """右に移動する"""
        self.vx = self.move_speed
    
    def stop_horizontal_movement(self):
        """水平方向の移動を停止する"""
        self.vx = 0.0
    
    def jump(self):
        """
        通常のジャンプを行う
        地面に接しているときのみジャンプ可能
        """
        if self.is_on_ground and not self.is_jumping:
            self.vy = -self.jump_power
            self.is_jumping = True
            self.is_on_ground = False
    
    def wall_jump(self, wall_direction):
        """
        壁ジャンプを行う
        壁に接しているときのみ壁ジャンプ可能
        
        Args:
            wall_direction (int): 壁の方向（-1: 左の壁, 1: 右の壁）
        """
        if self.is_on_wall and wall_direction == self.wall_direction:
            self.vy = -self.jump_power
            # 壁に接している場合、反対方向に飛び出す
            self.vx = -wall_direction * self.move_speed
            self.is_jumping = True
            self.is_on_wall = False
    
    def set_on_ground(self, on_ground):
        """
        プレイヤーが地面に接しているかを設定する
        
        Args:
            on_ground (bool): 地面に接しているかどうか
        """
        self.is_on_ground = on_ground
        if on_ground:
            self.vy = 0.0
            self.is_jumping = False
    
    def set_on_wall(self, on_wall, wall_direction=0):
        """
        プレイヤーが壁に接しているかを設定する
        
        Args:
            on_wall (bool): 壁に接しているかどうか
            wall_direction (int): 壁の方向（-1: 左, 1: 右）
        """
        self.is_on_wall = on_wall
        self.wall_direction = wall_direction if on_wall else 0
        if on_wall and self.vy > 0:
            # 壁を滑りながら落下する速度を低下させる
            self.vy = min(self.vy, 1.0)
    
    def get_bounds(self):
        """
        プレイヤーの当たり判定矩形を取得する
        
        Returns:
            tuple: (x, y, width, height)
        """
        return (self.x, self.y, self.width, self.height)
