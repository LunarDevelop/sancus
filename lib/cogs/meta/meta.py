import discord
from discord.ext.commands import Cog

import random

from asyncio import sleep
from configparser import ConfigParser

config = ConfigParser()
with open("./data/config.ini", 'r') as configFile:
    config.read_file(configFile)

from .info import Info

class Meta(Info,
            Cog):

    def __init__(self, client):
        self.client = client


    @Cog.listener()
    async def on_ready(self):
        self.client.loop.create_task(self.presence())
    
    async def presence(self):

        while not self.client.is_closed():

            _status = self.get_status()

            status = random.choice(_status)

            await self.client.change_presence(activity=discord.Game(name=status))

            await sleep(10)

    def get_status(self):
        self.version = config.get('DEFAULT', 'version')

        return ["Default prefix is s!",  f"Version {self.version}"]

    

