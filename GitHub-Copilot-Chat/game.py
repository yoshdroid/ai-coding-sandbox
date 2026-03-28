import pyxel

class App:
    def __init__(self):
        # headless / MCP runtime avoids some optional args like caption
        pyxel.init(160, 120)
        self.x = 72
        self.y = 56
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 1
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 1

        self.x = max(0, min(self.x, 152))
        self.y = max(0, min(self.y, 112))

    def draw(self):
        pyxel.cls(0)
        pyxel.circ(self.x, self.y, 8, 11)
        pyxel.text(5, 5, "Pyxel MCP Demo", 7)


if __name__ == "__main__":
    App()
