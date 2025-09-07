from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import math


GRAVITY = -0.8
MOVE_SPEED = 8
JUMP_FORCE = 16


class Player(Widget):
    def __init__(self, pos=(0, 0), size=(64, 64), **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.pos = pos
        # Không để Kivy tự co giãn theo widget cha
        self.size_hint = (None, None) 

        # --- Animation frames ---
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

        self.status = "idle"
        self.facing_right = True
        self.frame_index = 0
        self.animation_speed = 0.15

        # Hiển thị sprite
        with self.canvas:
            self.rect = Rectangle(source=self.animations["idle"][0], pos=self.pos, size=self.size)

        # 🔗 Bind để khi Player thay đổi pos/size thì Rectangle update theo
        self.bind(pos=self._update_rect, size=self._update_rect)

        # Vận tốc
        self.vx = 0
        self.vy = 0
        self.on_ground = False

        # Invincibility
        self.invincible = False
        self.invincibility_duration = 0.5  # giây
        self.hurt_time = 0

        # Âm thanh
        self.jump_sound = SoundLoader.load("./assets/audio/jump.wav")
        self.hit_sound = SoundLoader.load("./assets/audio/hit.wav")

        # Update loop
        Clock.schedule_interval(self.animate, 1 / 60)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def set_status(self, keys_pressed):
        """Xác định trạng thái nhân vật dựa vào input và vận tốc"""
        if self.vy > 1:
            self.status = "jump"
        elif self.vy < -1:
            self.status = "fall"
        else:
            if self.vx != 0:
                self.status = "run"
            else:
                self.status = "idle"

    def move(self, keys_pressed, platforms):
        """Xử lý di chuyển + va chạm"""
        # Input trái/phải
        if 276 in keys_pressed or 97 in keys_pressed:  # left / A
            self.vx = -MOVE_SPEED
            self.facing_right = False
        elif 275 in keys_pressed or 100 in keys_pressed:  # right / D
            self.vx = MOVE_SPEED
            self.facing_right = True
        else:
            self.vx = 0

        # Nhảy
        if (273 in keys_pressed or 119 in keys_pressed) and self.on_ground:
            self.vy = JUMP_FORCE
            self.on_ground = False
            if self.jump_sound:
                self.jump_sound.play()

        # Trọng lực
        self.vy += GRAVITY

        # --- Di chuyển ---
        self.x += self.vx
        self.y += self.vy

        # Va chạm đơn giản
        self.on_ground = False
        for p in platforms:
            if self.collide_widget(p):
                # Va chạm từ trên xuống (đứng trên platform)
                if self.vy < 0:
                    self.y = p.top
                    self.vy = 0
                    self.on_ground = True
                # Va chạm khi nhảy đập đầu
                elif self.vy > 0:
                    self.top = p.y
                    self.vy = 0

        self.set_status(keys_pressed)

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


    def get_damage(self, current_time):
        """Nhận sát thương"""
        if not self.invincible:
            if self.hit_sound:
                self.hit_sound.play()
            self.invincible = True
            self.hurt_time = current_time

    def update_invincibility(self, current_time):
        if self.invincible and (current_time - self.hurt_time) > self.invincibility_duration:
            self.invincible = False

    def update(self, dt, platforms, keys_pressed=None):
        """Cập nhật toàn bộ logic Player"""
        if keys_pressed is None:
            keys_pressed = set()

        # Di chuyển + va chạm
        self.move(keys_pressed, platforms)

        # Animation
        self.animate(dt)

        # Invincibility timer
        self.update_invincibility(Clock.get_time())

