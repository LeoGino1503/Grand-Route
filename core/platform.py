from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

class Platform(Widget):
    def __init__(self, pos=(0, 0), size=(64, 64), source=None, **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.pos = pos

        with self.canvas:
            if source:
                self.rect = Rectangle(source=source, pos=pos, size=size)
            else:
                self.rect = Rectangle(pos=pos, size=size)

        # Không để Kivy tự co giãn theo widget cha
        self.size_hint = (None, None)  

        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
