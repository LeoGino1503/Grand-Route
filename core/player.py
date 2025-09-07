from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock

GRAVITY = -0.5
MOVE_SPEED = 5
JUMP_FORCE = 12


class Player(Widget):
    def __init__(self, pos=(0, 0), size=(48, 48), **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.pos = pos

        # Không để Kivy tự co giãn theo widget cha
        self.size_hint = (None, None)  

        # Vẽ hình chữ nhật đại diện cho nhân vật (có thể thay bằng sprite sau)
        with self.canvas:
            self.rect = Rectangle(source="./assets/player.png", pos=self.pos, size=self.size)

        # Vận tốc
        self.vx = 0
        self.vy = 0
        self.on_ground = False

        # Cập nhật hình
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update(self, keys_pressed, platforms):
        """Cập nhật trạng thái Player"""
        # Điều khiển ngang
        if 276 in keys_pressed or 97 in keys_pressed:  # Left arrow or 'A'
            self.vx = -MOVE_SPEED
        elif 275 in keys_pressed or 100 in keys_pressed:  # Right arrow or 'D'
            self.vx = MOVE_SPEED
        else:
            self.vx = 0

        # Nhảy
        if (273 in keys_pressed or 119 in keys_pressed) and self.on_ground:  # Up arrow or 'W'
            self.vy = JUMP_FORCE
            self.on_ground = False

        # Áp dụng trọng lực
        self.vy += GRAVITY

        # Di chuyển
        new_x = self.x + self.vx
        new_y = self.y + self.vy

        # --- Va chạm theo trục X ---
        self.x = new_x
        for p in platforms:
            if self.collide_widget(p):
                if self.vx > 0:  # Va chạm phải
                    self.right = p.x
                elif self.vx < 0:  # Va chạm trái
                    self.x = p.right

        # --- Va chạm theo trục Y ---
        self.y = new_y
        self.on_ground = False
        for p in platforms:
            if self.collide_widget(p):
                if self.vy > 0:  # Đang đi lên, va trần
                    self.top = p.y
                    self.vy = 0
                elif self.vy < 0:  # Đang rơi, va đất
                    self.y = p.top
                    self.vy = 0
                    self.on_ground = True
