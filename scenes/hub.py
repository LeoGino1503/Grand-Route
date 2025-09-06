from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color


class Platform(Widget):
    def __init__(self, pos, size, **kwargs):
        super().__init__(**kwargs)
        self.pos = pos
        self.size = size
        with self.canvas:
            Color(0.5, 0.3, 0.1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class Hub(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.platforms = []

        # nền đất
        ground = Platform(pos=(0, 0), size=(800, 40))
        self.add_widget(ground)
        self.platforms.append(ground)

        # vài platform giữa màn
        plat1 = Platform(pos=(200, 150), size=(120, 20))
        plat2 = Platform(pos=(400, 300), size=(150, 20))
        self.add_widget(plat1)
        self.add_widget(plat2)
        self.platforms.extend([plat1, plat2])
