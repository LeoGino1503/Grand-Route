from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from ui.inventory import InventoryPopup

class DialogPopup(Popup):
    def __init__(self, npc, text, player, **kwargs):
        # gán các biến custom trước
        self.npc = npc
        self.text = text
        self.player_ref = player

        super().__init__(**kwargs)
        self.title = npc.name.capitalize()
        self.size_hint = (0.6, 0.4)   # 60% width, 40% height
        self.auto_dismiss = False

        layout = BoxLayout(orientation="horizontal", spacing=10, padding=10)

        # Avatar (ảnh đại diện NPC)
        avatar = Image(
            source=f"./assets/tiles/npc/{npc.name}/avatar/{npc.name}_avatar.png", 
            size_hint=(0.3, 1)
        )

        # Nội dung thoại + nút
        right = BoxLayout(orientation="vertical", spacing=5)

        dialog_label = Label(
            text=text,
            size_hint=(1, 0.6),
            halign="left",
            valign="top"
        )
        dialog_label.bind(size=dialog_label.setter("text_size"))

        # Các button
        btns = BoxLayout(orientation="horizontal", size_hint=(1, 0.4), spacing=5)

        btn_talk = Button(text="Trò chuyện")
        btn_buy = Button(text="Mua đồ")
        btn_buy.bind(on_release=lambda *a: self.open_inventory(npc))
        btn_exit = Button(text="Rời đi")
        btn_exit.bind(on_release=lambda *a: self.dismiss())

        btns.add_widget(btn_buy)
        btns.add_widget(btn_talk)
        btns.add_widget(btn_exit)

        right.add_widget(dialog_label)
        right.add_widget(btns)

        layout.add_widget(avatar)
        layout.add_widget(right)

        self.content = layout
    
    def open_inventory(self, npc):
        from core.player import Player
        popup = InventoryPopup(player=self.player_ref, npc=npc)  
        popup.open()
