# Discord Imports
import discord

# General Imports
from typing import Any
from dotenv import load_dotenv
from os import getenv
import logging as pyLogging

# Local Imports
from misc.log import logger

# Local Variables
load_dotenv('.env')

TOKEN = getenv('token')

discordLogger = logger('discord')

# Bot Class


class Bot(discord.Client):

    # init the main bot with all global variables needed
    def __init__(self, *args, **options: Any):

        # Global Variables
        self.ready = False
        self.logger = logger('local', level=pyLogging.DEBUG, file=True)
        self.guildLogger = logger(
            'guilds', level=pyLogging.DEBUG, file=True, fileName="guilds", fileMode='a')

        super().__init__(**options)

    # RUN function for the bot
    def run(self, version):
        self.bot = super().run(TOKEN, reconnect=True)

    # On Ready
    async def on_ready(self):

        # Ensures the bot knows that it is ready
        if not self.ready:
            self.ready = True

            self.logger.info(f"{self.user.name} is now up and running!!")

    # On Connect
    async def on_connect(self):
        self.logger.info(f"{self.user.name} has connected to Discord services")

    # On Disconnect
    async def on_disconnect(self):
        self.logger.error(
            f"{self.user.name} has been disconnected from Discord services")

    # On Guild Join
    async def on_guild_join(self, guild: discord.Guild):
        self.guildLogger.join(
            f"{self.user.name} has joined {guild.name} with id of {guild.id}")

    # On Guild Remove
    async def on_guild_remove(self, guild: discord.Guild):
        self.guildLogger.leave(
            f"{self.user.name} has left {guild.name} with id of {guild.id}")


bot = Bot()
