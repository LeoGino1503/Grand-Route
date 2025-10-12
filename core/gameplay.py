from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.core.window import Window
from core.player import Player
from core.otherplayer import OtherPlayer
from scenes.hub import Hub
from network.client_ws import GameClient
from utils.isnear import is_near
from ui.dialog import DialogPopup
import asyncio, threading
from kivy.uix.image import Image
from core.healthbar import HpManaBar
from core.slotbar import SlotBar
from core.inventory import InventoryWidget
import requests 
from dotenv import load_dotenv
import os
# ----------------------------
# Load .env
# ----------------------------
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")
API_LOGIN_URL = API_BASE_URL + os.getenv("API_LOGIN_ENDPOINT", "/login")
API_GET_ITEMS = API_BASE_URL + os.getenv("API_GET_ITEMS_ENDPOINT", "/get_items")

class Game(RelativeLayout):
    def __init__(self, WS_ENDPOINT, player_data, **kwargs):
        super().__init__(**kwargs)
        self.player_id = player_data.get("id")

        # Tạo hub
        self.hub = Hub()
        self.add_widget(self.hub)

        # Tạo player
        self.player = Player(pos=(100, 150))
        self.hub.add_widget(self.player)

        self.other_players = {}  # player_id -> OtherPlayer

        # Bắt sự kiện phím
        Window.bind(on_key_down=self._keydown, on_key_up=self._keyup)
        self.keys_pressed = set()
        self.dialog_open = False  

        # Game loop
        Clock.schedule_interval(self.update, 1/60)

        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.loop.run_forever, daemon=True).start()

        # 🧩 Khởi tạo client WS
        self.ws_client = GameClient(WS_ENDPOINT, self)
        asyncio.run_coroutine_threadsafe(self.ws_client.connect(), self.loop)

        self.last_sent_time = 0
        self.send_interval = 0.01

        # Health Bar
        self.healthbar = HpManaBar()
        self.add_widget(self.healthbar)

        # Slot Bar
        self.slot_bar = SlotBar(
            icons=[
                "./assets/ui/Slot_Empty_Single.png",
                "./assets/ui/Slot_Empty_Single.png",
                "./assets/ui/Slot_Empty_Single.png",
                "./assets/ui/Slot_Empty_Single.png",
                "./assets/ui/Slot_Empty_Single.png",
            ]
        )
        self.add_widget(self.slot_bar)

        self.inventory_open = False
        self.inventory_widget = InventoryWidget()
        self.add_widget(self.inventory_widget)
        self.inventory_widget.opacity = 0

    # -----------------------------
    # Input & update methods
    # -----------------------------
    def _keydown(self, window, key, scancode, codepoint, modifiers):
        if self.dialog_open:
            return
        if key == 9:
            self.toggle_inventory()
            return  # tránh xử lý tiếp phần khác

        self.keys_pressed.add(key)
        if codepoint == "e":
            for npc in self.hub.npcs:
                if is_near(self.player, npc, distance=80):
                    text = npc.interact()
                    popup = DialogPopup(npc, text, player=self.player)
                    self.dialog_open = True
                    popup.bind(on_dismiss=lambda *a: self._close_dialog())
                    popup.open()
        
    def _keyup(self, window, key, scancode):
        self.keys_pressed.discard(key)

    def update(self, dt):
        self.player.update(dt, self.hub.platforms, self.keys_pressed)
        self.last_sent_time += dt
        if self.last_sent_time >= self.send_interval and self.player.status not in ["idle", "fall", "jump"]:
            self.last_sent_time = 0
            asyncio.run_coroutine_threadsafe(
                self.ws_client.send({
                    "type": "move",
                    "player_id": self.player_id,
                    "position": {"x": self.player.x, "y": self.player.y},
                    "facing_right": self.player.facing_right,
                    "status": self.player.status
                }),
                self.loop
            )

    def on_server_message(self, data):
        if data.get("type") != "update_players":
            return

        players = data["players"]

        def process(dt):
            current_ids = set()
            for p in players:
                pid = str(p["player_id"])
                current_ids.add(pid)
                if pid == str(self.player_id):
                    continue

                if pid not in self.other_players:
                    op = OtherPlayer(pos=(p["x"], p["y"]))
                    self.other_players[pid] = op
                    self.add_widget(op)
                else:
                    op = self.other_players[pid]
                    new_x = p["x"]
                    new_y = p["y"]
                    op.pos = (new_x, new_y)
                    op.facing_right = p.get("facing_right", True)
                    op.status = p.get("status", "idle")

            for pid in list(self.other_players.keys()):
                if pid not in current_ids:
                    self.remove_widget(self.other_players[pid])
                    del self.other_players[pid]

        Clock.schedule_once(process, 0)

    def _close_dialog(self):
        self.dialog_open = False

    def toggle_inventory(self):
        self.inventory_widget.get_items(self.player_id, API_GET_ITEMS)
        self.inventory_widget.toggle()
        self.player.can_move = not self.inventory_widget.is_open
