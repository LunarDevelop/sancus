# discord imports
from asyncio.tasks import sleep
from os import read, sys, system
from discord import Intents
from discord.ext.commands import Bot as BaseBot
from discord.ext import commands

from discord_components import DiscordComponents, Button, Select, SelectOption
from discord_slash import SlashCommand

# Websocket Import
from lib.bot.websocket import *

# functions imports
from functions.apiConnection import APIconfig, ApiConnection
from functions.consoleColours import colours
import functions.exceptions as exceptions
from functions.objects import *
# This is temporary while I add stuff to the api
from functions.config import config

# general imports
from glob import glob
from configparser import ConfigParser, NoSectionError, NoOptionError
import schedule
import time

COGS = [path.split("\\")[-1][:-3] for path in glob("lib/cogs/**/*.py")]
PREFIX = 's!'
OWNER_IDS = [268035643760836608, 801557845928706139]
TESTING_MODE = True

__Config__ = ConfigParser()

with open("./data/config.ini", "r") as f:
    __Config__.read_file(f)


class Bot(BaseBot):

    # Init which set the start of the bot and all the objects with in the bot
    def __init__(self):
        """Bot Class for Sancus"""

        # Basic variables used across all of Sancus
        self.Prefix = PREFIX
        self.ready = False
        self.Version = BaseBot
        self.exceptions = exceptions

        # Footer elements for embeds
        self.embedAuthorUrl = "https://cdn.discordapp.com/attachments/789247201678327838/879862055404965938/stage_1629845776.jpeg"
        self.embedAuthorName = "Lunar Development"

        # Quick description for Sancus
        self.description = "Sancus is a multifunction bot designed and created by Solar Productions for managing their servers"

        # Intends selection
        intents = Intents.all()

        # Ensuring config classes are set
        self.config = APIconfig()
        self.oldConfig = config()

        # Find and return prefix for request guilf via message object
        def get_prefix(self, message):
            try:
                for guild in self.config.guilds:
                    if guild["guildID"] == str(message.guild.id):
                        return str(guild["prefix"])
            except:
                self.config = APIconfig()

        # Finds out if should be Sancus_Testing or Sancus
        if TESTING_MODE == True:
            self.TOKEN = __Config__.get('DEFAULT', 'testingtoken')

        elif TESTING_MODE == False:
            self.TOKEN = __Config__.get('DEFAULT', 'token')

        print(colours.GREEN, "STARTING BOT", colours.ENDC)

        # Begins connection to discord
        super().__init__(get_prefix, help_command=None,
                         description=self.description, owner_ids=OWNER_IDS, intents=intents)

# RUN function for the bot
    def run(self, version):
        self.Version = version

        print(f"{colours.GREEN}STARTING SETUP...{colours.ENDC}")
        self.setup()

        print(f"{colours.GREEN}Running Bot...{colours.ENDC}")

        self.bot = super().run(self.TOKEN, reconnect=True)

# Setup for the bot
    def setup(self):
        # Enables slash commands for Sancus
        self.slash_commands = SlashCommand(bot, sync_commands=True)

# COGS system to load all cogs aside from help (loaded separately)
        for cog in COGS:
            cogs = [cog.split("/")[-1]]
            cogsList = __Config__.get('DEFAULT', 'COGS')
            cogsList = cogsList.strip("[] ,")
            cogsList = cogsList.split(" , ")

            if cogs[0] == '__init__':
                pass

            else:
                for cogsA in cogsList:
                    if cogs[0] == cogsA:
                        try:
                            self.load_extension(f'lib.cogs.{cogs[0]}')
                            print(
                                f'{colours.OKCYAN}{cogs[0]} cog is loaded.{colours.ENDC}')

                        except commands.ExtensionAlreadyLoaded:
                            print(
                                f"{colours.WARNING}FAIL COG LOADING\n {cogs[0]}, has already been loaded{colours.ENDC}")

                        except commands.ExtensionError as error:
                            print(
                                f"{colours.WARNING}FAIL COG LOADING\n {cogs[0]}, has errored while loading\n   {error}{colours.ENDC}")

                        except commands.ExtensionFailed as error:
                            print(
                                f"{colours.WARNING}FAIL COG LOADING\n {cogs[0]}, has failed during setup\n  {error}{colours.ENDC}")

                        except commands.ExtensionNotFound:
                            print(
                                f"{colours.WARNING}FAIL COG LOADING\n {cogs[0]}, cannot be found{colours.ENDC}")

                        except commands.ExtensionNotLoaded:
                            print(
                                f"{colours.WARNING}FAIL COG LOADING\n {cogs[0]}, has not been loaded{colours.ENDC}")

                        except:
                            print(
                                f"{colours.WARNING}FAIL COG LOADING\n {cogs[0]} Failed{colours.ENDC}")

                    else:
                        pass

# Connect/Disconnections
    async def on_connect(self):
        print(f"{colours.GREEN}{self.user.name} has connected{colours.ENDC}")

    async def on_disconnect(self):
        print(f"{colours.WARNING} Bot has disconnected{colours.ENDC}")

# On Ready
    async def on_ready(self):
        # Just doubles checks if bot is ready
        if not self.ready:
            self.ready = True

            # Loads the discordComponents module
            self.DiscordComponents = DiscordComponents(bot)

            for guild in self.guilds:
                print(
                    f"{colours.PURPLE}Checking for guild during startup, {guild}{colours.ENDC}")
                check = False
                # Checks if guild is in the API config
                for configGuild in self.config.guilds:
                    if configGuild["guildID"] == str(guild.id):
                        print("Guild In API")
                        check = True
                        break
                # If guild is not in the API it sends a post request to add to the API
                if check == False:
                    print("Guild Not In API.... Adding now")
                    newGuild = guildObject(str(guild.id))
                    newGuild.prefix = "s!"
                    ApiConnection.guild.post(newGuild)

            # Reloads the API config once changes have been made
            self.config = APIconfig()

            # Loads the help command
            self.load_extension("lib.cogs.help")
            print(f"{colours.OKCYAN}Help command has been loaded.{colours.ENDC}")

            # (Feature will be removed once API takes over fully)
            schedule.every().hour.do(self.oldConfig.save)
            print("Scheduler for saving old config system started....")

            # Starting Websocket Requests
            print(f"{colours.OKCYAN}Starting Websocket Connection{colours.ENDC}")
            await startWebsocketConnection()
            print(f"{colours.OKCYAN}Connect to Websocket{colours.ENDC}")
            self.loop.create_task(heartbeat(self))

            print(f"{colours.OKGREEN}{self.user.name} Ready{colours.ENDC}")

    async def on_guild_join(self, guild):
        """When a new guild joins do these things
        This is one of many fuctions throughout the bot that activates with new guild joining"""

        # Makes a new guild object to make it easier to upload to the API
        newGuild = guildObject(str(guild.id))
        newGuild.prefix = "s!"

        # Post the new guild to the API and reload the bots API save
        ApiConnection.guild.post(newGuild)
        self.config = APIconfig()


# On Message to process commands
    async def on_message(self, message):
        # Makes sure any scheduled tasks are run on any message sent
        schedule.run_pending()

        # If message is not by a bot then process command (if it is a command)
        if not message.author.bot:
            await self.process_commands(message)


# Just to run the bot class
bot = Bot()
