from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.core.window import Window
from core.player import Player
from scenes.hub import Hub
from utils.isnear import is_near
from ui.dialog import DialogPopup

Window.size = (1280, 720)
Window.minimum_width, Window.minimum_height = Window.size
Window.maximum_width, Window.maximum_height = Window.size

class Game(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Tạo hub
        self.hub = Hub()
        self.add_widget(self.hub)

        # Tạo player
        self.player = Player(pos=(100, 150))
        self.hub.add_widget(self.player)

        # Bắt sự kiện phím
        Window.bind(on_key_down=self._keydown, on_key_up=self._keyup)
        self.keys_pressed = set()

        # Cờ trạng thái dialog
        self.dialog_open = False  

        # Game loop
        Clock.schedule_interval(self.update, 1/60)

    def _keydown(self, window, key, scancode, codepoint, modifiers):
        print("Key down:", key)
        if self.dialog_open:
            return # Nếu đang mở dialog thì không nhận input di chuyển
        self.keys_pressed.add(key)
        if codepoint == "e":  # dùng codepoint để bắt chữ
            for npc in self.hub.npcs:
                if is_near(self.player, npc, distance=80):
                    text = npc.interact()
                    popup = DialogPopup(npc, text, player=self.player)

                    # Khi mở dialog thì khóa di chuyển
                    self.dialog_open = True
                    popup.bind(on_dismiss=lambda *a: self._close_dialog())
                    popup.open()

    def _keyup(self, window, key, scancode):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def update(self, dt):
        self.player.update(dt, self.hub.platforms, self.keys_pressed)

class GameApp(App):
    def build(self):
        return Game()

if __name__ == "__main__":
    GameApp().run()
