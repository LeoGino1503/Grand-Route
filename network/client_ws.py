# network/client_ws.py
import asyncio
import json
import threading
import websockets

class GameClient:
    def __init__(self, uri, game):
        self.uri = uri
        self.ws = None
        self.game = game
        self.loop = None

    async def connect(self):
        try:
            self.ws = await websockets.connect(self.uri)
            print("✅ Connected to server")
            # Chạy nhận message liên tục
            asyncio.create_task(self.receive())
        except Exception as e:
            print("❌ Connection error:", e)

    async def receive(self):
        while True:
            try:
                msg = await self.ws.recv()
                data = json.loads(msg)
                # Gọi hàm của Game (UI thread)
                self.game.on_server_message(data)
            except Exception as e:
                print("⚠️ Connection lost:", e)
                break

    async def send(self, data):
        await self.ws.send(json.dumps(data))

    async def start(self):
        """Chạy WebSocket trong thread riêng"""
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self._run_loop, daemon=True).start()

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect())

    def send_sync(self, data: dict):
        """Gửi dữ liệu từ thread Kivy"""
        if self.loop and self.ws:
            asyncio.run_coroutine_threadsafe(self.send(data), self.loop)
