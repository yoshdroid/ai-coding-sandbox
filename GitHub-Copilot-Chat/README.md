# Pyxel MCP Setup (GitHub-Copilot-Chat)

このプロジェクトは、Pyxel と Pyxel MCP を使ってゲーム開発と自動テストを行うためのサンプル構成です。

## 1. 依存関係のインストール

```bash
cd c:/Users/yoshd/Documents/develop/ai-coding-sandbox/GitHub-Copilot-Chat
python -m pip install -r requirements.txt
```

## 2. 直接実行（Pyxelアプリ）

```bash
python game.py
```

- 矢印キーで黄色の円を移動できます。

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
