import websockets
import asyncio
import json

from functions.consoleColours import *
from configparser import ConfigParser

config = ConfigParser()

with open("sancus/data/api.ini") as file:
    config.read_file(file)

uri = config["WebSocket"]["uri"]
botName = "sancus"


async def startWebsocketConnection():
    "Does what is needed to start connection to the websocket"

    try:
        await ping()
        await uptime()
    except:
        pass

async def uptime():
    data = {
        "type": "09",
        "data": {
            "botName": botName
        }
    }

    async with websockets.connect(uri) as websocket:

        message = json.dumps(data)

        await websocket.send(str(message))

        greeting = await websocket.recv()


async def ping():
    async with websockets.connect(uri) as websocket:
        pinging = {
            "type": "01",
            "data": {
                "botName": botName
            }
        }

        pinging = json.dumps(pinging)

        await websocket.send(str(pinging))

        greeting = await websocket.recv()


async def heartbeat(client):
    try:
        while not client.is_closed():
            await asyncio.sleep(450)
            await ping()
    except:
        print(f"{colours.DARK_GREY}Failed to connect to websocket{colours.ENDC}")
