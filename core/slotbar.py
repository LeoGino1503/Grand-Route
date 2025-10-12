from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty

class SlotBar(BoxLayout):
    icons = ListProperty([])  # danh sách đường dẫn icon

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.size_hint = (None, None)
        self.pos_hint = {'center_x': 0.5, 'y': 0.05}
        self.create_slots()

    def create_slots(self):
        """Tạo 5 ô slot (64x64)"""
        self.clear_widgets()
        slot_size = 64
        num_slots = 5
        self.width = num_slots * slot_size + self.spacing * (num_slots - 1)
        self.height = slot_size

        for i in range(num_slots):
            icon_path = self.icons[i] if i < len(self.icons) else "./assets/ui/Slot_Empty_Single.png"
            slot = SlotIcon(source=icon_path)
            self.add_widget(slot)

    def update_icons(self, new_icons):
        """Cập nhật icon trong thanh slot"""
        self.icons = new_icons
        self.create_slots()


class SlotIcon(Widget):
    """Một ô trong slot bar (nền trong suốt)"""
    def __init__(self, source=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (64, 64)

        with self.canvas:
            # Nền trong suốt
            Color(1, 1, 1, 0)  
            self.bg = Rectangle(size=self.size, pos=self.pos)
            # Icon (chỉ vẽ nếu có)
            Color(1, 1, 1, 1)
            self.icon = Rectangle(source=source, size=self.size, pos=self.pos) if source else None

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        if self.icon:
            self.icon.pos = self.pos
            self.icon.size = self.size
