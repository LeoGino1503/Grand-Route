from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.animation import Animation
import requests
import os
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
class InventoryWidget(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (384, 448)
        self.pos_hint = {'center_x':-0.5,'center_y':0.5}  # ẩn dưới
        self.opacity = 0

        self.bg = Image(source="./assets/ui/Inventory_Empty.png", allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bg)

        self.add_widget(Label(text="[b]Inventory[/b]", markup=True, font_size=24,
                              pos_hint={"center_x": 0.5, "center_y": 0.9}))
        
        # --- lưới item ---
        self.grid = GridLayout(cols=4, rows=5, spacing=0, padding=0,
                               size_hint=(None, None), size=(256, 320),
                               pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.add_widget(self.grid)
        self.is_open = False

        self.is_open = False

    def open(self):
        self.is_open = True
        anim = Animation(pos_hint={'center_x':0.25,'center_y':0.5}, opacity=1, duration=0.3, t='out_cubic')
        anim.start(self)

    def close(self):
        self.is_open = False
        anim = Animation(pos_hint={'center_x':-0.5,'center_y':0.5}, opacity=0, duration=0.3, t='in_cubic')
        anim.start(self)

    def get_items(self, player_id, API_GET_ITEMS):
        try:
            response = requests.post(API_GET_ITEMS, json={
                "player_id": player_id
            })
            if response.status_code == 200:
                data = response.json()
                print(data)
                self.display_items(data["items"])
        except Exception as e:
            print("Error:", str(e))

    def toggle(self):
        if self.is_open:
            self.close()
        else:
            self.open()

    # -------------------------------
    # Hiển thị item trong grid
    # -------------------------------
    def display_items(self, items):
        # Xóa widget cũ (nếu có)
        self.grid.clear_widgets()

        total_slots = self.grid.cols * self.grid.rows
        slots = [None] * total_slots  # tạo danh sách trống cho tất cả ô

        # Gán item vào đúng vị trí slot_index (1-based)
        for item in items:
            slot_index = item.get("slot_index", 1)
            if 1 <= slot_index <= total_slots:
                slots[slot_index - 1] = item  # -1 để chuyển về 0-based index

        # Lặp qua toàn bộ slot để hiển thị
        for i in range(total_slots):
            item = slots[i]
            if item is None:
                # ô trống
                empty_slot = RelativeLayout(size_hint=(None, None), size=(64, 64))
                with empty_slot.canvas.before:
                    Color(0.2, 0.2, 0.2, 0.3)  # màu nền mờ
                    Rectangle(pos=empty_slot.pos, size=empty_slot.size)
                self.grid.add_widget(empty_slot)
                continue

            # Có item
            icon_path = item.get("icon_path", "")
            quantity = item.get("quantity", 1)
            name = item.get("name", "")
            desc = item.get("description", "Không có mô tả.")
            price = item.get("price", 0)
            effects = item.get("description", "Không có hiệu ứng.")

            if not os.path.exists(icon_path):
                icon_path = "./assets/ui/unknown.png"

            item_slot = RelativeLayout(size_hint=(None, None), size=(64, 64))

            # Icon
            icon = Image(source=icon_path, allow_stretch=True, keep_ratio=False)
            item_slot.add_widget(icon)

            # Số lượng (hiển thị góc phải dưới)
            qty_label = Label(
                text=str(quantity),
                font_size=14,
                color=(1, 1, 1, 1),
                pos_hint={"right": 0.95, "y": 0},
                size_hint=(None, None),
                size=(20, 20)
            )
            item_slot.add_widget(qty_label)
            item_slot.bind(on_touch_down=partial(
                self.show_item_info, name=name, desc=desc, price=price, effects=effects
            ))

            self.grid.add_widget(item_slot)


    def show_item_info(self, instance, touch, name, desc, price, effects):
        if instance.collide_point(*touch.pos):
            # Tính toạ độ thực của item trên màn hình
            abs_x, abs_y = instance.to_window(*instance.pos)
            print(f"Item position: ({abs_x}, {abs_y})")
            win_width, win_height = self.get_parent_window().size
            print(f"Window size: ({win_width}, {win_height})")
            popup_width, popup_height = 220, 280

            print(f"Item position: ({instance.width}, {instance.height})")

            # # Mặc định popup mở bên phải item
            popup_x = abs_x + instance.width
            popup_y = abs_y - popup_height + instance.height

            # # Nếu sát mép phải thì hiển thị sang bên trái
            # if popup_x + popup_width > win_width:
            #     popup_x = abs_x - popup_width - 10
            # # Nếu vượt mép dưới
            # if popup_y < 0:
            #     popup_y = 0
            # # Nếu vượt mép trên
            # if popup_y + popup_height > win_height:
            #     popup_y = win_height - popup_height

            # Popup container
            popup_layout = FloatLayout(
                size_hint=(None, None),
                size=(220, 280),
                pos=(0, 0))
            popup_layout.opacity = 0
            local_x, local_y = self.to_widget(popup_x, popup_y)
            popup_layout.pos = (local_x, local_y)
            self.add_widget(popup_layout)

            with popup_layout.canvas.before:
                from kivy.graphics import Color, Rectangle
                Color(1, 0, 0, 0.5)  # đỏ, alpha 0.5
                rect = Rectangle(pos=popup_layout.pos, size=popup_layout.size)

            # Ảnh nền popup
            bg_image = Image(
                source="./assets/ui/description_bg.png",
                size_hint=(1, 1),
                pos=(local_x, local_y),
                allow_stretch=True
            )
            popup_layout.add_widget(bg_image)

            # Tên item
            title_label = Label(
                text=f"[b]{name}[/b]",
                markup=True,
                font_size=18,
                color=(1, 0.9, 0.3, 1),
                pos_hint={"center_x": 0.5, "y": 0.4}
            )
            popup_layout.add_widget(title_label)

            # Mô tả
            desc_label = Label(
                text=f"[i]{desc}[/i]",
                markup=True,
                font_size=12,
                color=(1, 1, 1, 1),
                text_size=(popup_width * 0.75, None),
                halign="center",
                valign="middle",
                pos_hint={"center_x": 0.5, "y": 0.3}
            )
            popup_layout.add_widget(desc_label)

            # Hiệu ứng
            effect_label = Label(
                text=f"Effect: [color=00ffff]{effects}[/color]",
                markup=True,
                font_size=12,
                text_size=(popup_width * 0.75, None),
                halign="center",
                valign="middle",
                pos_hint={"center_x": 0.5, "y": 0.15}
            )
            popup_layout.add_widget(effect_label)

            # Giá
            price_label = Label(
                text=f"Giá: [color=ffcc00]{price} vàng[/color]",
                markup=True,
                font_size=14,
                pos_hint={"right": 0.9, "bottom": 0.8}
            )
            popup_layout.add_widget(price_label)

            # Nút đóng
            close_btn = Button(
                text="X",
                size_hint=(None, None),
                size=(32, 32),
                pos_hint={"right": 0.98, "top": 0.8},
                background_color=(0, 0, 0, 0),
                color=(1, 1, 1, 1)
            )
            popup_layout.add_widget(close_btn)
            # Hiệu ứng fade-in
            Animation(opacity=1, d=0.25, t='out_quad').start(popup_layout)

            # Hàm đóng popup
            def close_popup(*_):
                anim = Animation(opacity=0, d=0.2)
                def remove_anim(*_):
                    if popup_layout.parent:
                        popup_layout.parent.remove_widget(popup_layout)
                anim.bind(on_complete=remove_anim)
                anim.start(popup_layout)

            close_btn.bind(on_release=close_popup)
            return True

        return False
