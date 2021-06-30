from asyncio.tasks import sleep
from lib import bot

from functions.apiConnection import APIconfig, ApiConnection
from functions.objects import guildObject

from discord import Embed
from discord.ext import commands

from glob import glob
from configparser import ConfigParser

from discord.ext.commands import command, is_owner, Cog, group

from .mail import Mail
from .acommands import Anime

###COGS
COGS = [path.split("\\")[-1][:-3] for path in glob("lib/cogs/**/*.py")]

Config = ConfigParser()

with open("./data/config.ini", 'r') as f:
    Config.read_file(f)

cogsList = Config.get('DEFAULT', 'COGS')
cogsList = cogsList.strip("[] ,")
cogsList = cogsList.split(" , ")


class Owner(
        Mail,
        Anime,
        Cog
        ):

    def __init__(self, client):
        self.client = client

        self.Config = ConfigParser()

        with open("./data/config.ini", 'r') as configFile:

            self.Config.read_file(configFile)
            
    @command()
    async def ApiCheck(self, ctx):
        for instance in self.client.config.guilds:
            await ctx.send(instance)
            await sleep(0.5)
        
###Guilds
    @Cog.listener()
    async def on_guild_join(self, guild):

        channel = self.Config.get('DEFAULT', 'guild_join_channel')
        channel = self.client.get_channel(int(channel))

        embed = Embed(
            title = "A guild has invited Sancus",
            colour = int(self.Config.get('DEFAULT', 'guild_join_embed'),16)
        )

        totalGuilds = len(self.client.guilds)

        fields = [
            ("Name:", guild.name),
            ("ID: ", guild.id),
            ("Total Guilds: ", totalGuilds),
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
        
        embed.set_thumbnail(url=guild.icon_url)

        await channel.send(embed=embed)
    
    @Cog.listener()
    async def on_guild_remove(self, guild):
        
        ApiConnection.guild.delete(str(guild.id))

        channel = self.Config.get('DEFAULT', 'guild_remove_channel')
        channel = self.client.get_channel(int(channel))

        embed = Embed(
            title = "A guild has removed Sancus",
            colour = int(self.Config.get('DEFAULT', 'guild_remove_embed'),16)
        )

        totalGuilds = len(self.client.guilds)

        fields = [
            ("Name:", guild.name),
            ("ID: ", guild.id),
            ("Total Guilds: ", totalGuilds),
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
        
        embed.set_thumbnail(url=guild.icon_url)

        await channel.send(embed=embed)

    @command()
    @is_owner()
    async def ListServers(self, ctx):
        servers = ""
        serverIDS = ""

        count = 0

        for server in self.client.guilds:
            if count == 0:
                servers += server.name
                serverIDS += str(server.id)
                count = 1
            else:
                servers += "\n" + server.name
                serverIDS += "\n" + str(server.id)

        embed = Embed(
            title = "Servers List",
            description = f"Amount of servers = {len(self.client.guilds)}",
            colour = 0x990099
        )

        embed.add_field(name= "Names", value=servers, inline=True)
        embed.add_field(name= "ID", value=serverIDS, inline=True)

        await ctx.send(embed=embed)

###Commands
    @Cog.listener()
    async def on_command(self, ctx):
        with open("./data/config.ini", 'r') as configFile:
            Config.read_file(configFile)

        if Config.getboolean('DEFAULT', "maintenance_mode"):
            await ctx.send(f"{self.client.user.mention} is entering maintenance mode and may go down in a little while. I appolgised for any inconvenience the bot will be sorted soon.")

        if Config.getboolean('DEFAULT', 'command_logging'):
            embed = Embed(
                title = f"{ctx.author.id}, {ctx.author.name} has excuted a command.",
                description = f"{ctx.command.name} was excuted in {ctx.guild.name}, {ctx.guild.id}",
                colour = 0x7ccd7
            )

            channel = self.client.get_channel(int(Config.get('DEFAULT', 'command_logging_channel')))

            await channel.send(embed=embed)

#Admin work
    @group(name="set")
    @is_owner()
    async def _set(self, ctx):
        pass

    @_set.command()
    async def maintenance(self, ctx, toggle):
        with open("./data/config.ini", 'r') as configFile:

            Config.read_file(configFile)

        Config.set('DEFAULT', 'maintenance_mode', toggle)

        with open("./data/config.ini", 'w') as configFile:
            Config.write(configFile)

        await ctx.send("Maintenance Mode has changed.")

    @_set.command()
    async def embed(self, ctx, option, value):
        self.config.EMBEDS['DEFAULT'][option] = value
        await ctx.send(f"{option} embed changed to {value}.")

    @_set.command()
    async def timeout(self, ctx, option, value):
        self.config.TIMEOUTS['DEFAULT'][option] = value
        await ctx.send(f"{option} timeout setting changed to {value}.")

    @_set.command()
    async def default(self, ctx, option, value):
        self.config.DEFAULTS[option] = value
        await ctx.send(f"{option} embed changed to {value}.")

    @command()
    @is_owner()
    async def shutdown(self,ctx):
        self.config.save()
        exit()

###Cogs
    #Cogs Group
    @group(name="cogs")
    async def _cogs(self, ctx):
        pass
    
    #List Cogs and find disable/enabled ones
    @_cogs.command()
    @is_owner()
    async def List(self, ctx):
        output = ""

        for cog in COGS:
            cogs = [cog.split("/")[-1]]

            if cogs[0] == '__init__':
                pass
            else:
                for cogsA in cogsList:
                    if cogs[0] == cogsA:
                        try:
                            self.client.load_extension(f"lib.cogs.{cogs[0]}")
                            

                        except commands.ExtensionAlreadyLoaded:
                            output += (f"{str(cogs[0]).capitalize()}\n")
                        except commands.ExtensionNotFound:
                            pass
                            #await ctx.send("Cog not found")
                        else:
                            #await ctx.send("Cog is unloaded")
                            self.client.unload_extension(f"lib.cogs.{cogs[0]}")
                            output += (f"~~{str(cogs[0]).capitalize()}~~\n")

        embed = Embed(
            title = "Enabled Cogs",
            description = output,
            colour = 0xbdbffa
        )

        await ctx.send(embed=embed)

    #Loading Cogs
    @_cogs.command()
    @is_owner()
    async def load(self, ctx, *, extention):
        try:
            self.client.load_extension(f'lib.cogs.{extention}')
            print(f'{extention} has been loaded.')
            await ctx.send(f'{extention} has been loaded.')

        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f'{extention}, has already been loaded')
            print((f'{extention}, has already been loaded'))

        except commands.ExtensionError as error:
            await ctx.send(f'{extention}, has errored while loading\n{error}')
            print(f'{extention}, has errored while loading\n{error}')

        except commands.ExtensionFailed as error:
            await ctx.send(f'{extention}, has failed during setup\n{error}')
            print(f'{extention}, has failed during setup\n{error}')

        except commands.ExtensionNotFound:
            await ctx.send(f'{extention}, cannot be found')
            print(f'{extention}, cannot be found')

        except commands.ExtensionNotLoaded:
            await ctx.send(f'{extention}, has not been loaded')
            print(f'{extention}, has not been loaded')

    #Unloading Cogs
    @_cogs.command()
    @is_owner()
    async def unload(self, ctx, *, extention):
        try:
            self.client.unload_extension(f'lib.cogs.{extention}')
            print(f'{extention} has been unloaded.')
            await ctx.send(f'{extention} has been unloaded.')

        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f'{extention}, has already been loaded')
            print((f'{extention}, has already been loaded'))

        except commands.ExtensionError as error:
            await ctx.send(f'{extention}, has errored while loading\n{error}')
            print(f'{extention}, has errored while loading\n{error}')

        except commands.ExtensionFailed as error:
            await ctx.send(f'{extention}, has failed during setup\n{error}')
            print(f'{extention}, has failed during setup\n{error}')

        except commands.ExtensionNotFound:
            await ctx.send(f'{extention}, cannot be found')
            print(f'{extention}, cannot be found')

        except commands.ExtensionNotLoaded:
            await ctx.send(f'{extention}, has not been loaded')
            print(f'{extention}, has not been loaded')

    #Reload extentions
    @_cogs.command(name="reload")
    @is_owner()
    async def _reload(self, ctx, *, extention):
        if extention == "all":
            loaded = False
            for cog in COGS:
                cogs = [cog.split("/")[-1]]

                if cogs[0] == '__init__':
                    pass
                else:
                    for cogsA in cogsList:
                        if cogs[0] == cogsA:
                            try:
                                self.client.unload_extension(f'lib.cogs.{cogs[0]}')
                                self.client.load_extension(f'lib.cogs.{cogs[0]}')
                                print(f'{cogs[0]} cog has been reloaded.')

                            except commands.ExtensionAlreadyLoaded:
                                await ctx.send(f'{extention}, has already been loaded')
                                print((f'{extention}, has already been loaded'))

                            except commands.ExtensionError as error:
                                await ctx.send(f'{extention}, has errored while loading\n{error}')
                                print(f'{extention}, has errored while loading\n{error}')

                            except commands.ExtensionFailed as error:
                                await ctx.send(f'{extention}, has failed during setup\n{error}')
                                print(f'{extention}, has failed during setup\n{error}')

                            except commands.ExtensionNotFound:
                                await ctx.send(f'{extention}, cannot be found')
                                print(f'{extention}, cannot be found')

                            except commands.ExtensionNotLoaded:
                                await ctx.send(f'{extention}, has not been loaded')
                                print(f'{extention}, has not been loaded')


            await ctx.send(f'All cogs have been reloaded.')
                
        else:
            try:
                self.client.unload_extension(f'lib.cogs.{extention}')
                print(f'{extention} has been unloaded.')
                self.client.load_extension(f'lib.cogs.{extention}')
                print(f'{extention} has been loaded.')
                await ctx.send(f'{extention} cog has been reloaded.')

            except commands.ExtensionAlreadyLoaded:
                await ctx.send(f'{extention}, has already been loaded')
                print((f'{extention}, has already been loaded'))

            except commands.ExtensionError as error:
                await ctx.send(f'{extention}, has errored while loading\n{error}')
                print(f'{extention}, has errored while loading\n{error}')

            except commands.ExtensionFailed as error:
                await ctx.send(f'{extention}, has failed during setup\n{error}')
                print(f'{extention}, has failed during setup\n{error}')

            except commands.ExtensionNotFound:
                await ctx.send(f'{extention}, cannot be found')
                print(f'{extention}, cannot be found')

            except commands.ExtensionNotLoaded:
                await ctx.send(f'{extention}, has not been loaded')
                print(f'{extention}, has not been loaded')