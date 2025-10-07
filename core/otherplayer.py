from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

class OtherPlayer(Widget):
    def __init__(self, pos=(0, 0), size=(64, 64), **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = size
        self.pos = pos
        self.status = "idle"
        self.facing_right = True
        self.frame_index = 0
        self.animation_speed = 0.15

        # Tập ảnh giống player
        self.animations = {
            "idle": [
                "./assets/tiles/player/idle/1.png",
                "./assets/tiles/player/idle/2.png",
                "./assets/tiles/player/idle/3.png",
                "./assets/tiles/player/idle/4.png",
                "./assets/tiles/player/idle/5.png",
            ],
            "run": [
                "./assets/tiles/player/run/1.png",
                "./assets/tiles/player/run/2.png",
                "./assets/tiles/player/run/3.png",
                "./assets/tiles/player/run/4.png",
                "./assets/tiles/player/run/5.png",
                "./assets/tiles/player/run/6.png",
            ],
            "jump": [
                "./assets/tiles/player/jump/1.png",
                "./assets/tiles/player/jump/2.png",
                "./assets/tiles/player/jump/3.png",
            ],
            "fall": [
                "./assets/tiles/player/fall/fall.png",
            ],
        }

        with self.canvas:
            self.rect = Rectangle(source=self.animations["idle"][0], pos=self.pos, size=self.size)

        self.bind(pos=self._update_rect, size=self._update_rect)
        Clock.schedule_interval(self.animate, 1 / 60)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def animate(self, dt):
        frames = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0

        frame = frames[int(self.frame_index)]
        self.rect.source = frame

        if self.facing_right:
            self.rect.size = self.size
            self.rect.pos = self.pos
        else:
            # Flip ngang bằng cách đảo size[0]
            self.rect.size = (-self.size[0], self.size[1])
            self.rect.pos = (self.x + self.size[0], self.y)
