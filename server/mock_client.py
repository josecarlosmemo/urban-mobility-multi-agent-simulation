# Web Socket Client for Mock Server

import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        map_size = input("Map Size: ")

        await websocket.send(map_size)

        lanes = input("Lanes: ")

        await websocket.send(lanes)

        cars = input("Cars: ")

        await websocket.send(cars)

        # Keep receiving messages from the server


        message = None
        while message != "Done":
            message = await websocket.recv()
            print(message)



asyncio.get_event_loop().run_until_complete(hello())
