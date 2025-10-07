from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.core.window import Window
from scenes.hub import Hub
from utils.isnear import is_near
from ui.dialog import DialogPopup
from network.client_ws import GameClient
import asyncio, threading
import requests
import os
from dotenv import load_dotenv
from kivy.uix.screenmanager import ScreenManager, Screen

from core.player import Player
from core.otherplayer import OtherPlayer
from core.login import LoginScreen
from core.gameplay import Game
# ----------------------------
# Load .env
# ----------------------------
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")
WS_ENDPOINT = os.getenv("WS_ENDPOINT")
API_LOGIN_URL = API_BASE_URL + os.getenv("API_LOGIN_ENDPOINT", "/login")
# ----------------------------
# Cấu hình cửa sổ
# ----------------------------
Window.size = (1280, 720)
Window.minimum_width, Window.minimum_height = Window.size
Window.maximum_width, Window.maximum_height = Window.size
screen_w, screen_h = Window.system_size
# Tính toán vị trí để cửa sổ nằm giữa
Window.left = 100
Window.top = 50
# -------------------------
# GAME SCREEN
# -------------------------
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_widget = None

    def setup_player(self, player_data):
        if self.game_widget:
            self.remove_widget(self.game_widget)

        self.game_widget = Game(WS_ENDPOINT=WS_ENDPOINT, player_data=player_data)
        self.add_widget(self.game_widget)
# -------------------------
# Quản lý dữ liệu player
# -------------------------
class PlayerData:
    def __init__(self, data):
        self.id = data["id"]
        self.username = data["username"]
        self.x = data.get("x", 100)
# -------------------------
# APP
# -------------------------
class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login", API_LOGIN_URL=API_LOGIN_URL))
        sm.add_widget(GameScreen(name="game"))
        return sm

if __name__ == "__main__":
    GameApp().run()