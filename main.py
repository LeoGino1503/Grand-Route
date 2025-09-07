from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.core.window import Window
from core.player import Player
from scenes.hub import Hub

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

        # Game loop
        Clock.schedule_interval(self.update, 1/60)

    def _keydown(self, instance, keyboard, keycode, text, modifiers):
        self.keys_pressed.add(keycode)

    def _keyup(self, instance, keyboard, keycode):
        if keycode in self.keys_pressed:
            self.keys_pressed.remove(keycode)

    def update(self, dt):
        self.player.update(self.keys_pressed, self.hub.platforms)


class GameApp(App):
    def build(self):
        return Game()


if __name__ == "__main__":
    GameApp().run()
