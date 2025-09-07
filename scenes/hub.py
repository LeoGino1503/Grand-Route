from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle
from core.platform import Platform
from utils.load_map import load_map_csv
from utils.texture import make_vertical_gradient
from core.animation import AnimatedPlatform
from core.npc import NPC

# Tileset mapping: id trong CSV -> file ảnh
TILESET = {
    1: "./assets/tiles/block/terrain_tiles1.png",
    2: "./assets/tiles/block/terrain_tiles2.png",
    3: "./assets/tiles/block/terrain_tiles3.png",
    4: "./assets/tiles/block/terrain_tiles4.png",
    5: "./assets/tiles/block/terrain_tiles5.png",
    6: "./assets/tiles/block/terrain_tiles6.png",
    7: "./assets/tiles/block/terrain_tiles7.png",
    8: "./assets/tiles/block/terrain_tiles8.png",
    9: "./assets/tiles/block/terrain_tiles9.png",
    10: "./assets/tiles/block/terrain_tiles10.png",
    11: "./assets/tiles/block/terrain_tiles11.png",
    12: "./assets/tiles/block/terrain_tiles12.png",
    13: "./assets/tiles/block/terrain_tiles13.png",
    14: "./assets/tiles/block/terrain_tiles14.png",
    15: "./assets/tiles/block/terrain_tiles15.png",
    16: "./assets/tiles/block/terrain_tiles16.png",
    1000: [
        "./assets/tiles/water/water1.png",
        "./assets/tiles/water/water2.png",
        "./assets/tiles/water/water3.png",
        "./assets/tiles/water/water4.png",
    ], # animated water
}
# NPC mapping: id trong CSV -> config NPC
NPCSET = {
    100: {
        "name": "goblin",
        "dialog": ["Chào bạn!", "Tôi là goblin."],
        "patrol_range": None
    },
    101: {
        "name": "goblin",
        "dialog": ["Tôi đi tuần đây!", "Đừng lại gần!"],
        "patrol_range": 120
    }
}

# Load các layer từ CSV
grid_back = load_map_csv("./assets/maps/hub_0.csv")   # background
grid_main = load_map_csv("./assets/maps/hub_1.csv")   # main (platform có va chạm)
grid_front = load_map_csv("./assets/maps/hub_2.csv")  # foreground (trang trí)

class Hub(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # # Background
        # with self.canvas.before:
        #     self.bg = Rectangle(source="./assets/bg_hub.png", size=self.size, pos=(0, 0))
        # self.bind(size=self._update_bg)
        with self.canvas.before:
            self.bg = Rectangle(size=self.size, pos=(0, 0))
        self.bind(size=self._update_bg)

        # Platforms
        self.platforms = []
        self.npcs = []

        # --- Thêm NPC vào Hub ---
        # goblin = NPC(
        #     name="goblin",
        #     pos=(400, 150),
        #     dialog=["Chào bạn!", "Tôi là goblin."],
        #     patrol_range=None
        # )
        # self.add_widget(goblin)
        # self.npcs.append(goblin)

        tile_size = 64
        layers = [
            (grid_back, 0),   # background
            (grid_main, 1),   # main gameplay
            (grid_front, 2),  # foreground
        ]

        for grid, z_index in layers:
            rows = len(grid)
            for y, row in enumerate(grid):
                for x, cell in enumerate(row):
                    if cell != -1:
                        pos_x = x * tile_size
                        pos_y = (rows - y - 1) * tile_size

                        # --- Check NPC ---
                        npc_config = NPCSET.get(cell)
                        if npc_config:
                            npc = NPC(
                                name=npc_config["name"],
                                pos=(pos_x, pos_y),
                                dialog=npc_config["dialog"],
                                patrol_range=npc_config["patrol_range"]
                            )
                            self.add_widget(npc)
                            self.npcs.append(npc)
                            continue

                        # --- Check tile ---
                        tex = TILESET.get(cell)
                        if tex:
                            if isinstance(tex, list):
                                block = AnimatedPlatform(
                                    pos=(pos_x, pos_y),
                                    size=(tile_size, tile_size),
                                    sources=tex,
                                    fps=5
                                )
                            else:
                                block = Platform(
                                    pos=(pos_x, pos_y),
                                    size=(tile_size, tile_size),
                                    source=tex
                                )

                            if z_index == 0:
                                self.add_widget(block, index=0)
                            elif z_index == 2:
                                self.add_widget(block, index=0)
                            else:
                                self.add_widget(block)
                                self.platforms.append(block)


    def _update_bg(self, *args):
        # self.bg.size = (self.width, self.height)
        # self.bg.pos = (0, 0)
        """Cập nhật gradient nền khi đổi size."""
        gradient_tex = make_vertical_gradient(
            color_top=(0.4, 0.7, 1, 1),   # xanh trời
            color_bottom=(0.0, 0.2, 0.5, 1),  # xanh biển
            size=self.size
        )
        self.bg.texture = gradient_tex
        self.bg.size = self.size
        self.bg.pos = (0, 0)