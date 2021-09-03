from discord.ext.commands import Cog
from discord.ext.commands.context import Context

import websockets
import json
from lib.bot.websocket import uri, botName
from .discordservices import DiscordServices

from datetime import datetime, timedelta


class services(
        DiscordServices,
        Cog):

    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_command(self, ctx: Context):
        """This will be used for updating websocket information when stuff changes"""
        code = "04"

        async with websockets.connect(uri) as websocket:
            data = {
                "type": f"{code}",
                "data": {
                    "botName": f"{botName}",
                    "commandName": f"{ctx.command.name}"
                }
            }
            message = json.dumps(data)

            await websocket.send(str(message))
