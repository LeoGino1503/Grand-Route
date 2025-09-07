from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.clock import Clock

class AnimatedPlatform(Widget):
    def __init__(self, pos=(0, 0), size=(64, 64), sources=None, fps=30, **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.pos = pos
        self.sources = sources or []
        self.frame = 0
        self.fps = fps

        # Không để Kivy tự co giãn theo widget cha
        self.size_hint = (None, None)

        with self.canvas:
            if self.sources:
                self.rect = Rectangle(source=self.sources[0], pos=self.pos, size=self.size)
            else:
                self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_rect, size=self._update_rect)

        if self.sources and len(self.sources) > 1:
            Clock.schedule_interval(self._next_frame, 1.0 / self.fps)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _next_frame(self, dt):
        self.frame = (self.frame + 1) % len(self.sources)
        self.rect.source = self.sources[self.frame]
