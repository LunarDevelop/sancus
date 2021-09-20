from lib import bot
from .info import Info
import discord
from discord.ext.commands import Cog

import random

from asyncio import sleep
from configparser import ConfigParser

class Meta(Info,
           Cog):

    def __init__(self, client : bot):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        self.client.loop.create_task(self.presence())

    async def presence(self):

        while not self.client.is_closed():
            
            self.version = self.client.config_["version"]

            _status = self.get_status()

            status = random.choice(_status)

            await self.client.change_presence(activity=discord.Game(name=status))

            await sleep(10)

    def get_status(self):

        return ["Default prefix is s!",  f"Version {self.version}", "s!info"]
