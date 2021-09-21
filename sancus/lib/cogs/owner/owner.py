import asyncio
from asyncio.tasks import sleep
from datetime import datetime
from discord.client import Client

from discord.enums import ButtonStyle
from lib import bot

from functions.mongoDbAPI import *
from functions.objects import guildObject, Embeds

import discord
from discord import Embed
from discord.ext import commands
from discord.utils import utcnow
from discord.ui import button, select

from glob import glob
from configparser import ConfigParser

from discord.ext.commands import command, is_owner, Cog, group

from .mail import Mail

from lib.bot import Bot

###
COGS = [path.split("\\")[-1][:-3] for path in glob("sancus/lib/cogs/**/*.py")]

class Owner(
        Mail,
        Cog
):

    def __init__(self, client):
        self.client: Bot = client

        self.back_arrow = self.client.get_emoji(880261491587166229)
        self.forward_arrow = self.client.get_emoji(880261496167358484)


    @command()
    async def systemUpdate(self, ctx, x :str = "guilds"):
        async def guilds():
            for guild in self.client.guilds_:
                data = guildObject(**self.client.guilds_.get(guild))
                self.client.config.put_config_guild(int(guild), data.__dict__)
                
            self.client.guilds_ = self.client.config.get_config_guilds()
            await ctx.send("Guild Sys update done!")
        
        async def users():
            for user in self.client.users_:
                data = userObject(**self.client.users_.get(user))
                self.client.config.put_config_user(int(user), data.__dict__)
            self.client.guilds_ = self.client.config.get_config_guilds()
            await ctx.send("User Sys update done")
            
        if x.lower() == "all":
            await guilds()
            await users()
            
        elif x.lower() == "guilds":
            await guilds()
        
        elif x.lower() == "users":
            await users()

    @command()
    async def test(self, ctx):
        reaction, user = await self.client.wait_for("reaction_add")
        await ctx.send(embed=Embed(
            description=f"{reaction.emoji}",
            colour=0x000+int("02af02", 16)
        ))

# Guilds
    @Cog.listener()
    async def on_guild_join(self, guild):
        """Notifies Lunar Development Discord of a new guild"""

        channel = self.client.config_["guild_join_channel"]
        channel = self.client.get_channel(int(channel))

        embed = Embed(
            title="A guild has invited Sancus",
            colour=0x0007c5295
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
        """Notifies Lunar Development Discord when a guild leaves the bot"""

        channel = self.client.config_["guild_remove_channel"]
        channel = self.client.get_channel(int(channel))

        embed = Embed(
            title="A guild has removed Sancus",
            colour=0x0007c5295
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
        "Lists all servers the bot has access to"

        servers = []
        serverIDS = []

        count = 0

        def chunker_list(seq, size):
            return (seq[i::size] for i in range(size))

        """class page(discord.ui.View):

            def __init__(self):
                super.__init__()

                self.add_item(
                    button(label="Previous", custom_id="back",
                           style=ButtonStyle.danger, emoji=self.back_arrow)
                )
                self.add_item(
                    button(label="Next", custom_id="next",
                           style=ButtonStyle.green, emoji=self.forward_arrow)
                )

        for server in self.client.guilds:
            servers.append(server.name)
            serverIDS.append(server.id)

        if (len(self.client.guilds) / 10) > 1:

            size = (len(self.client.guilds) // 1) + 1

            pageServers = chunker_list(servers, size)
            pageIDs = chunker_list(serverIDS, size)

            pageNumber = 0

            embed = Embed(
                title="Servers List",
                description=f"Amount of servers = {len(self.client.guilds)}",
                colour=0x990099
            )

            for i in range(0, (len(pageServers[0])+1)):
                embed.add_field(name=pageServers[0][i], value=pageIDs[0][i], inline=True)

            def next():
                pageNumber += 1
                
                embed.remove_field(0)
                
                for i in range(0, (len(pageServers[pageNumber]))):
                    embed.add_field(
                        name=pageServers[pageNumber][i], value=pageIDs[pageNumber][i], inline=True)

        else:
            embed = Embed(
                title="Servers List",
                description=f"Amount of servers = {len(self.client.guilds)}",
                colour=0x990099
            )

            for i in range(0, (len(servers))):
                embed.add_field(
                    name=servers[i], value=serverIDS[i], inline=True)

        await ctx.send(embed=embed)"""

# Commands
    @Cog.listener()
    async def on_command(self, ctx):
        if self.client.config_["maintenance"]:
            await ctx.send(f"{self.client.user.mention} is entering maintenance mode and may go down in a little while. I appolgised for any inconvenience the bot will be sorted soon.")

        if self.client.config_["command_log"]:
            embed = Embed(
                title=f"{ctx.author.id}, {ctx.author.name} has excuted a command.",
                description=f"{ctx.command.name} was excuted in {ctx.guild.name}, {ctx.guild.id}",
                colour=0x7ccd7
            )

            channel = self.client.get_channel(self.client.config_["command_channel"])
            if channel != None:
                await channel.send(embed=embed)

# Admin work
    @group(name="set")
    @is_owner()
    async def _set(self, ctx):
        pass

    @_set.command()
    async def maintenance(self, ctx, toggle):
        data = {"maintenance": bool(int(toggle))}
        data = json.dumps(data)
        
        self.client.config.put_config_config(data)
        self.client.config_ = self.client.config.get_config_config()
        
        await ctx.send("Maintenance Mode has changed.")

    @command()
    @is_owner()
    async def shutdown(self, ctx):
        self.config.save()
        exit()

    @command()
    @is_owner()
    async def get_emojis(self, ctx, channelID=""):
        await ctx.message.delete()
        emoji_list = await ctx.guild.fetch_emojis()

        await asyncio.sleep(1)

        if channelID != "":
            channel = await self.client.fetch_channel(channelID)
            await channel.purge(limit=100, bulk=True)

        else:
            channel = ctx.channel

        for emoji in emoji_list:
            embed = Embeds(
                title=emoji.name,
                description=f"{emoji.id}\n`<:{emoji.name}:{emoji.id}>`"
            )

            embed.set_thumbnail(url=emoji.url)

            await channel.send(embed=embed)

            await asyncio.sleep(0.5)
#
# Cogs
    # Cogs Group

    @group(name="cogs")
    async def _cogs(self, ctx):
        pass

    # List Cogs and find disable/enabled ones
    @_cogs.command()
    @is_owner()
    async def List(self, ctx):
        output = ""

        for cog in COGS:
            cogs = [cog.split("/")[-1]]

            if cogs[0] == '__init__':
                pass
            else:
                for cogsA in self.client.config_["cogs"]:
                    if cogs[0] == cogsA:
                        try:
                            self.client.load_extension(f"lib.cogs.{cogs[0]}")

                        except commands.ExtensionAlreadyLoaded:
                            output += (f"{str(cogs[0]).capitalize()}\n")
                        except commands.ExtensionNotFound:
                            pass
                            # await ctx.send("Cog not found")
                        else:
                            # await ctx.send("Cog is unloaded")
                            self.client.unload_extension(f"lib.cogs.{cogs[0]}")
                            output += (f"~~{str(cogs[0]).capitalize()}~~\n")

        embed = Embed(
            title="Enabled Cogs",
            description=output,
            colour=0xbdbffa
        )

        await ctx.send(embed=embed)

    # Loading Cogs
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

    # Unloading Cogs
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

    # Reload extentions
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
                    for cogsA in self.client.config_["cogs"]:
                        if cogs[0] == cogsA:
                            try:
                                self.client.unload_extension(
                                    f'lib.cogs.{cogs[0]}')
                                self.client.load_extension(
                                    f'lib.cogs.{cogs[0]}')
                                print(f'{cogs[0]} cog has been reloaded.')

                            except commands.ExtensionAlreadyLoaded:
                                await ctx.send(f'{extention}, has already been loaded')
                                print(
                                    (f'{extention}, has already been loaded'))

                            except commands.ExtensionError as error:
                                await ctx.send(f'{extention}, has errored while loading\n{error}')
                                print(
                                    f'{extention}, has errored while loading\n{error}')

                            except commands.ExtensionFailed as error:
                                await ctx.send(f'{extention}, has failed during setup\n{error}')
                                print(
                                    f'{extention}, has failed during setup\n{error}')

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
