import asyncio
import json
import websockets

async def test():
    uri = "ws://127.0.0.1:8000/ws/game"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"type": "hello", "msg": "test"}))
        resp = await ws.recv()
        print("Received:", resp)

asyncio.run(test())
