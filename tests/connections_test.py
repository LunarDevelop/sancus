import json
import sys, os, unittest, configparser, asyncio

import requests

sys.path.insert(0, os.getcwd())

from sancus.functions.mongoDbAPI import connectionDb
from sancus.lib.bot.websocket import *

class Connections(unittest.TestCase):

    def test_mongodb_Config(self):
        client = connectionDb()

        config = client.get_config_config()

        self.assertEqual(0, config["id"], "Should be 0")

    def test_mongodb_Guilds(self):
        client = connectionDb()

        data = client.get_config_guilds()

        self.assertIs(dict, type(data))

    def test_mongodb_Users(self):
        client = connectionDb()

        data = client.get_config_guilds()

        self.assertIs(dict, type(data))

    def test_websocket_Ping(self):
        async def ping_connect():
            async with websockets.connect(uri) as websocket:

                message = json.dumps({
                    "type":"ping"
                })

                await websocket.send(str(message))

                return await websocket.recv()
        
        ping_loop = asyncio.new_event_loop()
        result = ping_loop.run_until_complete(ping_connect())
        ping_loop.close()

        data = json.loads(result)

        self.assertEqual("pong", data["type"], "Should have return 'pong'!")

    def test_websocket_Error(self):
        async def connect():
            async with websockets.connect(uri) as websocket:

                message = json.dumps({
                    "type":"ErrorTESTING"
                })

                await websocket.send(str(message))

                return await websocket.recv()
        
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(connect())
        loop.close()

        data = json.loads(result)
        

        self.assertEqual("404", data["type"], "Should have return 'pong'!")


    def test_fluxpoint_Auth(self):
        """
        FluxPoint API connection, Provided by BuilderB#0001 on Discord
        """

        data = configparser.ConfigParser()
        with open("./sancus/data/api.ini") as f:
            data.read_file(f)
        
        headers = {
        "Authorization":data["FluxPoint"]["api_token"]}

        request = requests.get("https://api.fluxpoint.dev/me", headers=headers)

        self.assertEqual(200, request.status_code, "Unable to connect to FluxPoint Api")

    def test_fluxpoint_Connection(self):
        """
        FluxPoint API connection, Provided by BuilderB#0001 on Discord
        """

        data = configparser.ConfigParser()
        with open("./sancus/data/api.ini") as f:
            data.read_file(f)
        
        headers = {
        "Authorization": None}

        request = requests.get("https://api.fluxpoint.dev/me", headers=headers)

        self.assertEqual(401, request.status_code, "Unable to connect to FluxPoint Api")


if __name__ == "__main__":
    unittest.main()