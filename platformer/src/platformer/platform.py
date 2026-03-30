# プラットフォーム（足場）管理クラス

class Platform:
    """
    プラットフォーマーゲームの足場を表すクラス
    
    プレイヤーが立つことができるプラットフォームと、
    壁として使用できるプラットフォームを管理します。
    
    属性:
        x (float): プラットフォームの水平位置
        y (float): プラットフォームの垂直位置
        width (int): プラットフォームの幅
        height (int): プラットフォームの高さ
        platform_type (str): プラットフォームの種類
    """
    
    def __init__(self, x, y, width, height, platform_type="normal"):
        """
        プラットフォームを初期化する
        
        Args:
            x (float): 水平位置
            y (float): 垂直位置
            width (int): 幅
            height (int): 高さ
            platform_type (str): プラットフォームの種類
                - "normal": 通常のプラットフォーム
                - "goal": ゴール
        """
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.platform_type = platform_type
    
    def get_bounds(self):
        """
        プラットフォームの当たり判定矩形を取得する
        
        Returns:
            tuple: (x, y, width, height)
        """
        return (self.x, self.y, self.width, self.height)
    
    def is_collision(self, rect):
        """
        プラットフォームと矩形が衝突しているかを判定する
        
        Args:
            rect (tuple): 判定する矩形 (x, y, width, height)
        
        Returns:
            bool: 衝突している場合True
        """
        x1, y1, w1, h1 = self.get_bounds()
        x2, y2, w2, h2 = rect
        
        # AABB（軸並行矩形）衝突判定
        return (x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2)
    
    def is_colliding_from_top(self, rect, prev_y):
        """
        上から衝突しているかを判定する（着地判定）
        
        前フレームでの矩形の位置を使用して、
        上からプラットフォームに衝突しているかを判定します。
        
        Args:
            rect (tuple): 判定する矩形 (x, y, width, height)
            prev_y (float): 前フレームでの矩形の y 座標
        
        Returns:
            bool: 上から衝突している場合True
        """
        x1, y1, w1, h1 = self.get_bounds()
        x2, y2, w2, h2 = rect
        
        # 上下の衝突判定
        # 前フレームでは上にいて、現フレームでは下に貫通している
        return (prev_y + h2 <= y1 and  # 前フレームで上にいた
                y2 + h2 > y1 and        # 現フレームで下に來た
                x2 < x1 + w1 and        # 左右で重なっている
                x2 + w2 > x1)
    
    def is_colliding_from_bottom(self, rect, prev_y):
        """
        下から衝突しているかを判定する（天井衝突判定）
        
        前フレームでの矩形の位置を使用して、
        下からプラットフォームに衝突しているかを判定します。
        
        Args:
            rect (tuple): 判定する矩形 (x, y, width, height)
            prev_y (float): 前フレームでの矩形の y 座標
        
        Returns:
            bool: 下から衝突している場合True
        """
        x1, y1, w1, h1 = self.get_bounds()
        x2, y2, w2, h2 = rect
        
        # 前フレームでは下にいて、現フレームでは上に貫通している
        return (prev_y >= y1 + h1 and      # 前フレームで下にいた
                y2 < y1 + h1 and           # 現フレームで上に來た
                x2 < x1 + w1 and           # 左右で重なっている
                x2 + w2 > x1)
    
    def is_colliding_from_left(self, rect, prev_x):
        """
        左から衝突しているかを判定する（右側の壁衝突判定）
        
        前フレームでの矩形の位置を使用して、
        左からプラットフォームに衝突しているかを判定します。
        
        Args:
            rect (tuple): 判定する矩形 (x, y, width, height)
            prev_x (float): 前フレームでの矩形の x 座標
        
        Returns:
            bool: 左から衝突している場合True
        """
        x1, y1, w1, h1 = self.get_bounds()
        x2, y2, w2, h2 = rect
        
        # 前フレームでは左にいて、現フレームでは右に貫通している
        return (prev_x + w2 <= x1 and     # 前フレームで左にいた
                x2 + w2 > x1 and          # 現フレームで右に來た
                y2 < y1 + h1 and          # 上下で重なっている
                y2 + h2 > y1)
    
    def is_colliding_from_right(self, rect, prev_x):
        """
        右から衝突しているかを判定する（左側の壁衝突判定）
        
        前フレームでの矩形の位置を使用して、
        右からプラットフォームに衝突しているかを判定します。
        
        Args:
            rect (tuple): 判定する矩形 (x, y, width, height)
            prev_x (float): 前フレームでの矩形の x 座標
        
        Returns:
            bool: 右から衝突している場合True
        """
        x1, y1, w1, h1 = self.get_bounds()
        x2, y2, w2, h2 = rect
        
        # 前フレームでは右にいて、現フレームでは左に貫通している
        return (prev_x >= x1 + w1 and     # 前フレームで右にいた
                x2 < x1 + w1 and          # 現フレームで左に來た
                y2 < y1 + h1 and          # 上下で重なっている
                y2 + h2 > y1)
