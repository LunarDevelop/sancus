# Discord Imports
import discord

# General Imports
from typing import Any
from dotenv import load_dotenv
from os import getenv
import logging as pyLogging

# Local Imports
from misc.log import logging

# Local Variables
load_dotenv('.env')

TOKEN = getenv('token')

discordLogger = logging('discord')

# Bot Class


class Bot(discord.Client):

    # init the main bot with all global variables needed
    def __init__(self, *args, **options: Any):

        self.ready = False
        
        self.logger = logging('local', level=pyLogging.DEBUG, file=True)

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


bot = Bot()
