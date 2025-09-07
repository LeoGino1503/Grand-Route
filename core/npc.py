from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.clock import Clock


class NPC(Widget):
    def __init__(self, name="villager", pos=(0, 0), size=(64, 64), dialog=None, patrol_range=100, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.size = size
        self.pos = pos
        self.size_hint = (None, None)

        # --- Animation frames ---
        self.animations = {
            "idle": [
                f"./assets/tiles/npc/{name}/idle/{name}1.png",
                f"./assets/tiles/npc/{name}/idle/{name}2.png",
                f"./assets/tiles/npc/{name}/idle/{name}3.png",
                f"./assets/tiles/npc/{name}/idle/{name}4.png",
                f"./assets/tiles/npc/{name}/idle/{name}5.png",
            ],
            "walk": [
                f"./assets/tiles/npc/{name}/walk/{name}1.png",
                f"./assets/tiles/npc/{name}/walk/{name}2.png",
                f"./assets/tiles/npc/{name}/walk/{name}3.png",
                f"./assets/tiles/npc/{name}/walk/{name}4.png",
                f"./assets/tiles/npc/{name}/walk/{name}5.png"
            ],
        }

        self.status = "idle"
        self.facing_right = True
        self.frame_index = 0
        self.animation_speed = 0.1

        # Sprite hiển thị
        with self.canvas:
            self.rect = Rectangle(source=self.animations["idle"][0], pos=self.pos, size=self.size)

        self.bind(pos=self._update_rect, size=self._update_rect)

        # --- NPC logic ---
        self.dialog = dialog or ["Xin chào!", "Bạn có khỏe không?"]
        self.dialog_index = 0

        # Patrol logic
        self.vx = 0
        self.direction = 1
        self.patrol_range = patrol_range
        if self.patrol_range is not None:
            self.walk_range = (self.x - patrol_range, self.x + patrol_range)
        else:
            self.walk_range = None

        Clock.schedule_interval(self.update, 1 / 60)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def set_status(self):
        if self.vx != 0:
            self.status = "walk"
        else:
            self.status = "idle"

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
            self.rect.size = (-self.size[0], self.size[1])
            self.rect.pos = (self.x + self.size[0], self.y)

    def patrol(self):
        """NPC tự đi qua lại (nếu có patrol_range)"""
        if self.walk_range is None:
            self.vx = 0
            return

        self.vx = 1 * self.direction
        self.x += self.vx

        if self.x < self.walk_range[0]:
            self.direction = 1
            self.facing_right = True
        elif self.x > self.walk_range[1]:
            self.direction = -1
            self.facing_right = False

    def talk(self):
        """Trả về 1 câu thoại"""
        text = self.dialog[self.dialog_index]
        self.dialog_index = (self.dialog_index + 1) % len(self.dialog)
        return text

    def interact(self):
        """Khi player tương tác (ví dụ nhấn E) thì trả về câu thoại"""
        return self.talk()

    def update(self, dt):
        self.patrol()
        self.set_status()
        self.animate(dt)
