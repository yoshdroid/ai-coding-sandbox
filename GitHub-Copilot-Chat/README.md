# Pyxel MCP Setup (GitHub-Copilot-Chat)

このプロジェクトは、Pyxel と Pyxel MCP を使ってゲーム開発と自動テストを行うためのサンプル構成です。

## 1. 依存関係のインストール

```bash
cd <local dir.>/ai-coding-sandbox/GitHub-Copilot-Chat
python -m pip install -r requirements.txt
```

## 2. 直接実行（Pyxelアプリ）

### オリジナルゲーム
```bash
python game.py
```
- 矢印キーで黄色（?緑色ぽくない?）の円を移動できます。

### ブロック崩しゲーム（パステルカラー版）
```bash
python breakout_game.py
```
- **矢印キー左右**: パドルを移動
- **Q キー**: ゲーム終了
- **R キー**: 再スタート（ゲームオーバー時）
- パステルカラーで統一した淡い見た目のブロック崩しゲーム
- 全ブロックを消すとゲームクリア
- ボールが画面下に落ちるとゲームオーバー

## 3. Pyxel MCP ツールの実行例

Pyxel MCP の `run_and_capture` を使ってスクリーンショットを取得:

```bash
python mcp_test.py
```

- 成功すれば `out.png` が生成されます。

## 4. pyxel_info チェック

```bash
python -c "from pyxel_mcp.server import mcp; import asyncio; print(asyncio.run(mcp.call_tool('pyxel_info', {})))"
```

## 5. 追加のPyxel MCPコマンド

- `render_audio`
- `inspect_sprite`, `inspect_screen`, `inspect_state`
- `validate_script`, `compare_frames` など

`pyxel_mcp/instructions.md` に詳細と使い方が書かれています。

## セットアップ履歴（会話ログ）

このプロジェクトのセットアップ過程を、GitHub Copilotとの会話に基づいてMarkdown形式で文書化します。後で読み返して参考にしてください。

### 初期リクエスト: Pyxel MCPセットアップ

**ユーザー:**  
このプロジェクトで Pyxel MCPを使えるようにセットアップしてください。

**対応内容:**  
- プロジェクト構造を確認（`Codex/` と `GitHub-Copilot-Chat/` が空のフォルダ）
- Pyxel と Pyxel MCP のパッケージ可用性を確認（両方インストール済み）
- `pyxel_mcp` モジュールのAPIを調査（`server.py` から `FastMCP` インスタンス `mcp` を使用）
- 必要なファイルを一括作成:
  - `requirements.txt`: `pyxel==2.8.9`, `pyxel-mcp==0.9.1`
  - `game.py`: シンプルなPyxelアプリ（矢印キーで円を移動）
  - `mcp_test.py`: `run_and_capture` ツールのテストスクリプト
  - `README.md`: 基本的な使用手順
- Windows環境での文字コード問題（`UnicodeDecodeError`）を修正:
  - `pyxel_mcp/server.py` の `instructions.md` 読み込みに `encoding="utf-8"` を追加
- 実行テスト:
  - `python mcp_test.py` でスクリーンショット取得成功（`out.png` 生成）
  - ログ: "Captured at frame 60, scale 2x"

**結果:**  
Pyxel MCP が使用可能になり、基本的なゲームアプリとテストスクリプトが動作確認済み。

### 追加リクエスト: GitHub公開リポジトリ化

**ユーザー:**  
AI-CODING-SANDBOX/ ディレクトリ以下を GitHUB上で public repositoryとして管理していきたい。何をすればよいですか？

**対応内容:**  
- Git初期化の手順説明
- `.gitignore` の作成例（Python関連、VS Code、MCP出力）
- コミットとプッシュの手順
- GitHubリポジトリ作成のガイド
- 追加アドバイス: README整備、LICENSE追加、安全運用

**結果:**  
GitHub公開リポジトリ化のための完全な手順を提供。

### ブロック崩しゲーム開発

**ユーザー:**  
新たに ブロック崩しゲームを pyxelを使って作成してください。全体的な色合いをパステルカラーで統一して淡い見た目にしてください。

**対応内容:**  
- Pyxelでブロック崩しゲームの基本実装（パドル、ボール、ブロック）
- 16色パレットを使用したパステル調の色設定
- ゲーム状態管理（ready, playing, game_over, won）
- 衝突判定とボール反射処理の実装
- エラー修正（pyxel.colorsへの直接RGB割り当て不可）
- Rキー再スタート機能の修正（_reset_gameメソッド追加）
- 耐久度機能追加（シアン色ブロックは3回耐久、50点加算）
- 起動時Rキー入力待機画面の実装
- 視覚フィードバック（フラッシュエフェクト）の追加と削除
- ボール初速の調整（遅めに設定）

**結果:**  
Pyxelを使用した完全なブロック崩しゲームが完成。パステルカラー統一の淡い見た目で、遊びやすいバランス調整済み。

