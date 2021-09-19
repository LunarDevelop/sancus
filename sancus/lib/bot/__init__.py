# discord imports
from asyncio.tasks import sleep
from os import read, sys, system
from discord import Intents
from discord.ext.commands import Bot as BaseBot
from discord.ext import commands

# Websocket Import
from lib.bot.websocket import *

# functions imports
from functions.mongoDbAPI import connectionDb
from functions.consoleColours import colours
import functions.exceptions as exceptions
from functions.objects import *

# general imports
from glob import glob
from configparser import ConfigParser, NoSectionError, NoOptionError
import schedule
import time
import string

COGS = [path.split("\\")[-1][:-3] for path in glob("sancus/lib/cogs/**/*.py")]
PREFIX = 's!'
OWNER_IDS = [268035643760836608, 801557845928706139]
TESTING_MODE = True

__Config__ = ConfigParser()

with open("sancus/data/config.ini", "r") as f:
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
        self.helpInstance = []

        # Footer elements for embeds
        self.embedAuthorUrl = "https://cdn.discordapp.com/attachments/789247201678327838/879862055404965938/stage_1629845776.jpeg"
        self.embedAuthorName = "Lunar Development"

        # Quick description for Sancus
        self.description = "Sancus is a multifunction bot designed and created by Solar Productions for managing their servers"

        # Intends selection
        intents = Intents.all()

        # Ensuring config classes are set
        self.config = connectionDb()
        self.config_ = self.config.get_config_config()
        self.guild_ = self.config.get_config_guilds()
        self.users_ = self.config.get_config_users()
        self.reacts_ = self.config.get_config_reacts()

        # Find and return prefix for request guilf via message object
        def get_prefix(self, message):
            try:
                return self.guild_[str(message.guild.id)]["prefix"]
            except:
                self.guild_ = self.config.get_config_guilds()

        # Finds out if should be Sancus_Testing or Sancus
        if TESTING_MODE == True:
            self.TOKEN = self.config_["testToken"]

        elif TESTING_MODE == False:
            self.TOKEN = self.config_['token']

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
        pass
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
            self.emojis()

            for guild in self.guilds:
                print(
                    f"{colours.PURPLE}Checking for guild during startup, {guild}{colours.ENDC}")
                check = False
                # Checks if guild is in the API config
                if str(guild.id) in self.guild_:
                    continue
                # If guild is not in the API it sends a post request to add to the API
                else:
                    print("Guild Not In API.... Adding now")
                    newGuild = guildObject(id=guild.id)
                    print(newGuild.__dict__)
                    self.config.post_config_guild(guild=newGuild)

            # Reloads the API config once changes have been made
            self.guild_ = self.config.get_config_guilds()
            self.users_ = self.config.get_config_users()
            self.reacts_ = self.config.get_config_reacts()
            
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

        # Post the new guild to the API and reload the bots API save
        self.config.post_config_guild(newGuild)
        self.guild_ = self.config.get_config_guilds()

    async def on_guild_remove(self, guild):
        "Remove left guild from api"
        self.config.delete_config_guild(str(guild.id))

# On Message to process commands
    async def on_message(self, message):
        # Makes sure any scheduled tasks are run on any message sent
        schedule.run_pending()

        # If message is not by a bot then process command (if it is a command)
        if not message.author.bot:
            await self.process_commands(message)

    def clientColour(self):
        self.react_colour = 0x000a8329e

    def emojis(self):
        self.addEmoji = self.get_emoji(873303876466528286)
        self.deleteEmoji = self.get_emoji(873303905008779266)
        self.adjustEmoji = self.get_emoji(873304038022713415)

        self.tickEmoji = self.get_emoji(872992713165926503)
        self.crossEmoji = self.get_emoji(872992645302075392)

    def getGuild(self, id):
        for guild in self.config.guilds:
            if guild["guildID"] == str(id):
                return guild

    async def getLogChannel(self, id):
        guild = self.getGuild(id)
        LogChannelId = guild["logChannel"]
        try:
            LogChannel = (self.get_guild(id)).get_channel(
                int(LogChannelId))

            return LogChannel

        except:
            pass

    async def getActionChannel(self, id):
        guild = self.getGuild(id)
        ActionChannelId = guild["actionChannel"]
        try:
            ActionChannel = (self.get_guild(id)).get_channel(
                int(ActionChannelId))

            return ActionChannel

        except:
            pass

    def is_hex(self, value):
        hex_string = set(string.hexdigits())

        return all(char in hex_string for char in value)


# Just to run the bot class
bot = Bot()
