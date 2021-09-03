from configparser import ConfigParser
from glob import glob

from discord import Embed
from discord.ext.commands import Cog, command, group, is_owner

from discord_slash import cog_ext, SlashContext

import asyncio
import datetime
import sys

#from tinker.ext.apps import *


class admin_slash(Cog):

    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_interaction(self, payload):
        print(payload)

    @cog_ext.cog_slash(name="test", guild_ids=[780211278614364160])
    async def _test(self,ctx):
        await ctx.send("ping, pong")