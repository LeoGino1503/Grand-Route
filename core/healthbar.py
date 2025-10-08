import kivy
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout

class HpManaBar(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.hp_bg = Image(source="./assets/ui/HealthBar_Empty.png",
                           size_hint=(None,None), size=(256,64),
                           pos_hint={'x':0.01,'top':0.99}, allow_stretch=True)
        self.hp_fill = Image(source="./assets/ui/HP.png",
                             size_hint=(None,None), size=(183,12), allow_stretch=True)
        self.mana_fill = Image(source="./assets/ui/Mana.png",
                               size_hint=(None,None), size=(184,6), allow_stretch=True)

        self.add_widget(self.hp_bg)
        self.add_widget(self.hp_fill)
        self.add_widget(self.mana_fill)

        self.hp_bg.bind(pos=self.update_fill_pos)

    def update_fill_pos(self, instance, value):
        self.hp_fill.pos = (self.hp_bg.x + 66, self.hp_bg.y + 26)
        self.mana_fill.pos = (self.hp_bg.x + 62, self.hp_bg.y + 16)

    def update_hp(self, current, max_hp):
        ratio = max(0, min(1, current/max_hp))
        self.hp_fill.size = (183 * ratio, self.hp_fill.height)

    def update_mana(self, current, max_mana):
        ratio = max(0, min(1, current/max_mana))
        self.mana_fill.size = (184 * ratio, self.mana_fill.height)
