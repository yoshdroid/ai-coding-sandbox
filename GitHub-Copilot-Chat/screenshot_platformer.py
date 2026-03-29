import asyncio
import os
import base64

from pyxel_mcp.server import mcp

async def main():
    script_path = os.path.abspath("platformer_game.py")
    print("Running pyxel_mcp.run_and_capture on", script_path)

    # 自動プレイモード用のファイルを作成
    with open("autoplay.txt", "w"):
        pass

    result = await mcp.call_tool(
        "run_and_capture",
        {
            "script_path": script_path,
            "frames": 60,
            "scale": 2,
            "timeout": 15,
        },
    )

    if os.path.exists("autoplay.txt"):
        os.remove("autoplay.txt")

    if isinstance(result, list) and result:
        first = result[0]
        print("First result type:", first.type)
        if hasattr(first, 'data'):
            image_data = base64.b64decode(first.data)
            with open("platformer_screenshot_1.png", "wb") as f:
                f.write(image_data)
            print("Saved platformer_screenshot_1.png")

    # もう一回、異なるフレームで
    # 2回目は自動プレイでより進めて、移動・ジャンプしている状態を取得
    with open("autoplay.txt", "w"):
        pass

    result2 = await mcp.call_tool(
        "run_and_capture",
        {
            "script_path": script_path,
            "frames": 300,
            "scale": 2,
            "timeout": 30,
        },
    )

    if os.path.exists("autoplay.txt"):
        os.remove("autoplay.txt")

    if isinstance(result2, list) and result2:
        second = result2[0]
        if hasattr(second, 'data'):
            image_data2 = base64.b64decode(second.data)
            with open("platformer_screenshot_2.png", "wb") as f:
                f.write(image_data2)
            print("Saved platformer_screenshot_2.png")

if __name__ == "__main__":
    asyncio.run(main())