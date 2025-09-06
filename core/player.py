from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color


class Player(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (40, 60)
        self.vel_y = 0
        self.gravity = -0.5
        self.jump_force = 12
        self.speed = 5
        self.on_ground = False

        with self.canvas:
            Color(0, 1, 0)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(pos=self.update_graphics)

    def update_graphics(self, *args):
        self.rect.pos = self.pos

    def update(self, keys, platforms=None):
        # di chuyển ngang
        if "a" in keys:  # left
            self.x -= self.speed
        if "d" in keys:  # right
            self.x += self.speed
        if "w" in keys and self.on_ground:  # jump
            self.vel_y = self.jump_force
            self.on_ground = False

        # gravity
        self.vel_y += self.gravity
        self.y += self.vel_y

        # kiểm tra va chạm
        self.on_ground = False
        if platforms:
            for plat in platforms:
                if self.collide_widget(plat) and self.vel_y <= 0:
                    self.y = plat.top
                    self.vel_y = 0
                    self.on_ground = True
                    break

        self.update_graphics()
