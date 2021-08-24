import websockets
import asyncio
import json

from functions.consoleColours import *

uri = "ws://localhost:8765"


async def startWebsocketConnection():
    "Does what is needed to start connection to the websocket"

    try:
        await ping()
        await uptime()
    except:
        print(f"{colours.DARK_GREY}Failed to connect to websocket{colours.ENDC}")

async def uptime():
    data = {
        "type": "09",
        "data": {
            "botName": "sancus"
        }
    }

    async with websockets.connect(uri) as websocket:

        message = json.dumps(data)

        await websocket.send(str(message))
        print(f"{colours.DARK_GREY}> {message}{colours.ENDC}")

        greeting = await websocket.recv()
        print(f"{colours.DARK_GREY}< {greeting}{colours.ENDC}")


async def ping():
    async with websockets.connect(uri) as websocket:
        pinging = {
            "type": "01",
            "data": {
                "botName": "sancus"
            }
        }

        pinging = json.dumps(pinging)

        await websocket.send(str(pinging))
        print(f"{colours.DARK_GREY}> {pinging}{colours.ENDC}")

        greeting = await websocket.recv()
        print(f"{colours.DARK_GREY}< {greeting}{colours.ENDC}")


async def heartbeat(client):
    try:
        while not client.is_closed():
            await asyncio.sleep(450)
            await ping()
    except:
        print(f"{colours.DARK_GREY}Failed to connect to websocket{colours.ENDC}")
