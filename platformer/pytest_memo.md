# pytestメモ - Platformerプロジェクトでのテスト実装方針

## 概要

このプロジェクトでは、Pythonのテストフレームワークであるpytestを使用して、プラットフォーマーゲームの各コンポーネントを徹底的にテストしています。テスト駆動開発（TDD）のアプローチを採用し、コードの品質と信頼性を確保しています。

## pytestの使用目的

### 1. ユニットテストの実施
各クラスやメソッドの機能を個別に検証し、バグの早期発見と修正を可能にします。

### 2. リファクタリングの安全性確保
コード変更時に既存機能が壊れていないことを確認します。

### 3. 仕様の明確化
テストコード自体がコードの仕様書となり、実装の意図を明確にします。

### 4. 回帰テストの自動化
継続的な開発の中で、過去のバグが再発しないことを保証します。

## 実装方針

### 1. テストファースト（TDD）
```python
# 例: Playerクラスのjumpメソッド実装前
def test_jump_on_ground(self):
    player = Player()
    player.set_on_ground(True)
    player.jump()
    assert player.vy == -player.jump_power
    assert player.is_jumping is True
```

実装前にテストを書くことで、仕様を明確にし、設計を改善します。

### 2. 各関数に対応するテスト作成
プロジェクトのルールとして、「実装していくそれぞれの関数に対応するテストを都度作成」しています。

### 3. 日本語コメントの活用
テストファイルには内容を示す日本語コメントをたくさん書いて、学習目的を果たしています。

```python
def test_wall_jump_on_left_wall(self):
    """
    テスト: 左の壁での壁ジャンプが正しく機能することを確認

    プレイヤーが左の壁に接しているときに wall_jump(-1) を呼ぶと，
    垂直速度が負になり，水平速度が正になることを確認します。
    """
```

### 4. 境界条件のテスト
正常系だけでなく、エッジケースもテストします。

```python
def test_not_collision_from_top_when_no_overlap(self):
    """
    テスト: 左右で重なっていない場合、着地判定は False を返すことを確認
    """
    platform = Platform(x=0, y=100, width=100, height=10)
    prev_y = 80
    rect = (150, 101, 10, 10)  # 左右で重なっていない
    assert platform.is_colliding_from_top(rect, prev_y) is False
```

### 5. テストの独立性
各テストは他のテストに依存せず、独立して実行可能です。

## 具体的なテスト例

### Playerクラスのテスト（test_player.py）

```python
class TestPlayerJump:
    def test_jump_on_ground(self):
        """地上でのジャンプが正しく機能することを確認"""
        player = Player()
        player.set_on_ground(True)
        player.jump()
        assert player.vy == -player.jump_power
        assert player.is_jumping is True

    def test_jump_in_air_not_possible(self):
        """空中ではジャンプできないことを確認"""
        player = Player()
        player.set_on_ground(False)
        initial_vy = player.vy
        player.jump()
        assert player.vy == initial_vy  # 変化なし
```

### Platformクラスのテスト（test_platform.py）

```python
class TestPlatformCollision:
    def test_collision_from_top(self):
        """上からの着地判定が正しく機能することを確認"""
        platform = Platform(x=0, y=100, width=100, height=10)
        prev_y = 80
        rect = (40, 101, 10, 10)
        assert platform.is_colliding_from_top(rect, prev_y) is True

    def test_not_collision_from_top_when_no_overlap(self):
        """左右で重なっていない場合、着地判定はFalse"""
        platform = Platform(x=0, y=100, width=100, height=10)
        prev_y = 80
        rect = (150, 101, 10, 10)  # 左右で重なっていない
        assert platform.is_colliding_from_top(rect, prev_y) is False
```

### Levelクラスのテスト（test_level.py）

```python
class TestLevelCollisionDetection:
    def test_get_colliding_platforms(self):
        """衝突しているプラットフォームが検出されることを確認"""
        level = Level()
        platforms = level.get_platforms()
        first_platform = platforms[0]
        colliding_rect = (
            first_platform.x + 10,
            first_platform.y + 5,
            10, 10
        )
        colliding = level.get_colliding_platforms(colliding_rect)
        assert len(colliding) > 0
```

## pytest設定（pyproject.toml）

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

## テスト実行方法

```bash
# 全テスト実行（推奨）
python -m pytest

# 特定のテストファイル実行
python -m pytest tests/test_player.py

# 特定のテストクラス実行
python -m pytest tests/test_player.py::TestPlayerJump

# 特定のテストメソッド実行
python -m pytest tests/test_player.py::TestPlayerJump::test_jump_on_ground

# 詳細出力
python -m pytest -v

# 簡易出力
python -m pytest -q
```

### 注意: CommandNotFoundExceptionが出る場合

pytestコマンドが直接見つからない場合（`CommandNotFoundException`）、以下の方法を試してください：

1. **python -m pytest を使用する**
   ```bash
   python -m pytest
   ```
   これが最も確実な方法です。

2. **pytestを明示的にインストール**
   ```bash
   pip install pytest
   ```

3. **仮想環境の確認**
   - プロジェクトの仮想環境がアクティブになっているか確認
   - `pip list` でpytestがインストールされているか確認

4. **PATH環境変数の確認**
   - PythonのScriptsフォルダがPATHに含まれているか確認
   - Windowsの場合: `C:\Users\[ユーザー名]\AppData\Local\Programs\Python\Python3x\Scripts\`

### プロジェクト固有の実行方法

このプロジェクトでは、pyproject.tomlでpytestが設定されているため：

```bash
# プロジェクトルートで実行
cd /path/to/platformer
python -m pytest
```

pytestの直接実行がうまくいかない場合は、常に `python -m pytest` を使用してください。

## テスト結果の解釈

- **PASSED**: テスト成功
- **FAILED**: テスト失敗（アサーションエラーなど）
- **ERROR**: テスト実行中の例外

## 学習効果

このプロジェクトでのpytest活用により、以下を学習できました：

1. **テスト駆動開発の流れ**
2. **境界条件の重要性**
3. **コードのモジュール化**
4. **リファクタリングの安全性**
5. **継続的インテグレーションの基礎**

## 注意点

- テストは実装コードの変更に合わせて更新する必要があります
- テストカバレッジを意識し、重要なパスを網羅する
- テストは高速に実行できるように設計する
- テストコードも保守性が高くなるよう記述する

## まとめ

pytestを活用することで、堅牢で保守性の高いコードを開発することができました。テストファーストのアプローチにより、仕様の明確化とバグの早期発見が可能になり、長期的な開発効率が向上しました。</content>
<parameter name="filePath">pytest_memo.md