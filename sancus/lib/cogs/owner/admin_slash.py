from configparser import ConfigParser
from glob import glob

from discord import Embed
from discord.ext.commands import Cog, command, group, is_owner

import asyncio
import datetime
import sys

#from tinker.ext.apps import *


COGS = [path.split("\\")[-1][:-3] for path in glob("lib/cogs/**/*.py")]

Config = ConfigParser()

with open("./data/config.ini", 'r') as f:
    Config.read_file(f)

cogsList = Config.get('DEFAULT', 'COGS')
cogsList = cogsList.strip("[] ,")
cogsList = cogsList.split(" , ")


class admin_slash(Cog):

    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_interaction(self, payload):
        print(payload)
