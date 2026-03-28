import asyncio
import os

from pyxel_mcp.server import mcp

async def main():
    script_path = os.path.abspath("game.py")
    print("Running pyxel_mcp.run_and_capture on", script_path)
    result = await mcp.call_tool(
        "run_and_capture",
        {
            "script_path": script_path,
            "frames": 60,
            "scale": 2,
            "timeout": 15,
        },
    )

    if isinstance(result, list) and result:
        first = result[0]
        print("[DEBUG] first type:", type(first), "repr:", repr(first))
        if hasattr(first, "data"):
            data = first.data
            if isinstance(data, str):
                try:
                    import base64

                    data = base64.b64decode(data)
                except Exception:
                    data = data.encode("utf-8", errors="replace")
            with open("out.png", "wb") as f:
                f.write(data)
            print("Screenshot saved to out.png")
            if len(result) > 1:
                print(result[1])
            return

    # Fallback text output
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
