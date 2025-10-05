from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
import requests

class InventorySlot(FloatLayout):
    def __init__(self, icon_path=None, quantity=0, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (128, 128)  # mỗi ô 64x64 px

        # background viền xám
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)  # màu nền slot
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        # icon
        if icon_path:
            self.icon = Image(source=icon_path, size_hint=(1, 1))
            self.add_widget(self.icon)

        # số lượng (nếu có)
        if quantity > 1:
            self.qty_label = Label(
                text=str(quantity),
                size_hint=(None, None),
                size=(self.width, 20),
                pos_hint={"x": 0, "y": 0},  # góc dưới
                halign="right",
                valign="bottom"
            )
            self.qty_label.bind(size=self._update_text_size)
            self.add_widget(self.qty_label)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def _update_text_size(self, instance, value):
        instance.text_size = value


class InventoryPopup(Popup):
    def __init__(self, player, npc, **kwargs):
        super().__init__(**kwargs)
        self.title = f"Giao dịch với {npc.name}"
        self.size_hint = (0.95, 0.9)
        self.auto_dismiss = False

        root = BoxLayout(orientation="horizontal", spacing=20, padding=20)

        # Inventory NPC (5x5)
        self.npc_inv = GridLayout(cols=5, spacing=5, size_hint=(0.45, 1))
        for i in range(25):  # 25 slot
            # demo: vài slot có icon, còn lại trống
            if i < 5:
                self.npc_inv.add_widget(InventorySlot(icon_path="./assets/icons/potion.png", quantity=i+1))
            else:
                self.npc_inv.add_widget(InventorySlot())

        # Inventory Player (5x5)
        self.player_inv = GridLayout(cols=5, spacing=5, size_hint=(0.45, 1))
        for i in range(25):
            if i == 0:
                self.player_inv.add_widget(InventorySlot(icon_path="./assets/icons/sword.png", quantity=1))
            else:
                self.player_inv.add_widget(InventorySlot())

        root.add_widget(self.npc_inv)
        root.add_widget(self.player_inv)
        self.content = root

    def open(self, *largs):
        super().open(*largs)

        # ban đầu để ngoài màn hình
        self.npc_inv.x = -self.npc_inv.width
        self.player_inv.x = self.width + self.player_inv.width

        # trượt vào
        anim_npc = Animation(x=50, d=0.5, t="out_back")
        anim_player = Animation(x=self.width - self.player_inv.width - 50, d=0.5, t="out_back")
        anim_npc.start(self.npc_inv)
        anim_player.start(self.player_inv)
