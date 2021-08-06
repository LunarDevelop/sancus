
#discord imports
from asyncio.tasks import sleep
from os import read, sys, system
from discord import Intents
from discord.ext.commands import Bot as BaseBot
from discord.ext import commands

from discord_components import DiscordComponents, Button, Select, SelectOption

#functions imports
from functions.apiConnection import APIconfig, ApiConnection
from functions.consoleColours import colours
import functions.exceptions as exceptions
from functions.objects import *
from functions.config import config #This is temporary while I add stuff to the api

#general imports
from glob import glob
from configparser import ConfigParser, NoSectionError, NoOptionError
import schedule, time

COGS = [path.split("\\")[-1][:-3] for path in glob("lib/cogs/**/*.py")]
PREFIX = 's!'
OWNER_IDS = [268035643760836608, 801557845928706139]
TESTING_MODE = True

__Config__ = ConfigParser()

with open("./data/config.ini", "r") as f:
    __Config__.read_file(f)
    
class Bot(BaseBot):

###Init which set the start of the bot and all the objects with in the bot
    def __init__(self):
        self.Prefix = PREFIX
        self.ready = False
        self.Version = BaseBot
        self.exceptions = exceptions
        
        self.embedAuthorUrl = "https://images-ext-2.discordapp.net/external/PR2dRBWGoEAaqJ44iktdKFKAw4-rgZPbsp9B7zxO0YQ/%3Fsize%3D1024/https/cdn.discordapp.com/icons/789941733998854176/c9938e932be5bb6ee2ba6eed81d8c6f7.webp"
        self.embedAuthorName = "Solar Productions"
        
        self.help_instance = []

        self.description = "Sancus is a multifunction bot designed and created by Solar Productions for managing their servers"
        
        intents = Intents.all()

        self.config = APIconfig()
        self.oldConfig = config()

        def get_prefix(self, message):
            for guild in self.config.guilds:
                if guild["guildID"] == str(message.guild.id):
                    return str(guild["prefix"])

        if TESTING_MODE == True:
            self.TOKEN = __Config__.get('DEFAULT', 'testingtoken')
        
        elif TESTING_MODE == False:
            self.TOKEN = __Config__.get('DEFAULT', 'token')

        print(colours.GREEN,"STARTING BOT",colours.ENDC)

        super().__init__(get_prefix, help_command=None, description=self.description, owner_ids=OWNER_IDS, intents=intents)

###RUN function for the bot
    def run(self,version):
        self.Version = version

        print(f"{colours.GREEN}STARTING SETUP...{colours.ENDC}")
        self.setup()

        print(f"{colours.GREEN}Running Bot...{colours.ENDC}")
        
        self.bot = super().run(self.TOKEN, reconnect=True)

###Setup for the bot
    def setup(self):
        
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
                            print(f'{colours.OKCYAN}{cogs[0]} cog is loaded.{colours.ENDC}')

                        except commands.ExtensionAlreadyLoaded:
                            print(f"{colours.WARNING}FAIL COG LOADING\n {cogs[0]}, has already been loaded{colours.ENDC}")
                            

                        except commands.ExtensionError as error:
                            print(f"{colours.WARNING}FAIL COG LOADING\n {cogs[0]}, has errored while loading\n   {error}{colours.ENDC}")
                            

                        except commands.ExtensionFailed as error:
                            print(f"{colours.WARNING}FAIL COG LOADING\n {cogs[0]}, has failed during setup\n  {error}{colours.ENDC}")
                            

                        except commands.ExtensionNotFound:
                            print(f"{colours.WARNING}FAIL COG LOADING\n {cogs[0]}, cannot be found{colours.ENDC}")
                            
                        except commands.ExtensionNotLoaded:
                            print(f"{colours.WARNING}FAIL COG LOADING\n {cogs[0]}, has not been loaded{colours.ENDC}")

                        except:
                            print(f"{colours.WARNING}FAIL COG LOADING\n {cogs[0]} Failed{colours.ENDC}")
                    
                    else:
                        pass

###Connect/Disconnections
    async def on_connect(self):
        print(f"{colours.GREEN}{self.user.name} has connected{colours.ENDC}")

    async def on_disconnect(self):
        print(f"{colours.WARNING} Bot has disconnected{colours.ENDC}")

###On Ready
    async def on_ready(self):
        if not self.ready:
            self.ready = True

            for guild in self.guilds:
                print(f"{colours.PURPLE}Checking for guild during startup, {guild}{colours.ENDC}")
                check = False
                for Cguilds in self.config.guilds:
                    if Cguilds["guildID"] == str(guild.id):
                        print("Guild In API")
                        check = True
                        break
                
                if check == False:
                    print("Guild Not In API.... Adding now")
                    newGuild = guildObject(str(guild.id))
                    newGuild.prefix = "s!"
                    ApiConnection.guild.post(newGuild)
                        
            self.config = APIconfig()
    
            self.load_extension("lib.cogs.help")
            print(f"{colours.OKCYAN}Help command has been loaded.{colours.ENDC}")

            #schedule.every().hour.do(self.config.save)
            #print("Scheduler for saving config started....")

            print(f"{colours.OKGREEN}{self.user.name} Ready{colours.ENDC}")
            
            self.DiscordComponents = DiscordComponents(bot)
            
    async def on_guild_join(self, guild):
        
        newGuild = guildObject(str(guild.id))
        newGuild.prefix = "s!"
        
        ApiConnection.guild.post(newGuild)
        self.config = APIconfig()
            
        
###On Message to process commands
    async def on_message(self, message):
        schedule.run_pending()

        if not message.author.bot:
            await self.process_commands(message)

bot = Bot()