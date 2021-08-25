from configparser import ConfigParser
from glob import glob

from discord import Embed
from discord.ext import commands
from discord.ext.commands import Cog, command, group, is_owner
from discord_slash import cog_ext
from discord_slash.context import SlashContext
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import (create_choice, create_option,
                                                 create_permission)

import asyncio, datetime

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
    
    @cog_ext.cog_slash(
        name="list",
        description="List cogs in Sancus",
        guild_ids=[789941733998854176, 780211278614364160],
        permissions={
            789941733998854176 : [
                create_permission(268035643760836608, SlashCommandPermissionType.USER, True)
            ]
        }
    )
    async def List__(self, ctx):
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
    
    @cog_ext.cog_subcommand(
        base="cog",
        name="reload",
        description="Reload cogs in Sancus",
        guild_ids=[789941733998854176, 780211278614364160],
        options=[
            create_option(
                 name="extention",
                 description="Which cogs to reload?",
                 option_type=3,
                 required=True,
                 choices=[
                  create_choice(
                    name="All",
                    value="all"
                  ),
                  create_choice(
                    name="Owner",
                    value="owner"
                  ),
                  create_choice(
                    name="Mod",
                    value="mod"
                  ),
                  create_choice(
                    name="Economy",
                    value="economy"
                  ),
                  create_choice(
                    name="Errors",
                    value="errors"
                  ),
                  create_choice(
                    name="Filter",
                    value="filter"
                  ),
                  create_choice(
                    name="Games",
                    value="games"
                  ),
                  create_choice(
                    name="Help",
                    value="help"
                  ),
                  create_choice(
                    name="Logging",
                    value="logging"
                  ),
                  create_choice(
                    name="Meta",
                    value="meta"
                  ),
                  create_choice(
                    name="Misc",
                    value="misc"
                  ),
                  create_choice(
                    name="Services",
                    value="services"
                  ),
                  create_choice(
                    name="Stats",
                    value="stats"
                  )
                 ]
            )
        ],
        base_permissions={
            789941733998854176 : [
                create_permission(268035643760836608, SlashCommandPermissionType.USER, True)
            ]
        }
    )
    async def reload(self, ctx, extention):
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
                
    """@cog_ext.cog_slash(
        name="get_emoji",
        description="Get Emojis from guild",
        guild_ids=[789941733998854176, 780211278614364160, 861331674876608533],
        permissions={
            789941733998854176 : [
                create_permission(268035643760836608, SlashCommandPermissionType.USER, True)
            ]
        }
    )"""
    async def get_emojis(self, ctx, channelID = ""):
        await ctx.message.delete()
        emoji_list = await ctx.guild.fetch_emojis()
        
        time = datetime.utcnow()
        await asyncio.sleep(1)
        
        for emoji in emoji_list:
            embed = Embed(
                title=emoji.name,
                description = f"{emoji.id}\n`<:{emoji.name}:{emoji.id}>`"
            )
            
            embed.set_thumbnail(url=emoji.url)
            
            if channelID == "":
                await ctx.send(embed=embed)
            
            else:
                channel = await self.client.fetch_channel(channelID)
                await channel.purge(limit=100, bulk=True, before=time)
                await ctx.send(embed=embed)
                
            await asyncio.sleep(0.5)

    @cog_ext.cog_slash(
            name="list",
            description="List cogs in Sancus",
            guild_ids=[789941733998854176, 780211278614364160],
            options=[
            create_option(
                 name="toggle",
                 description="Which cogs to reload?",
                 option_type=3,
                 required=True,
                 choices=[
                  create_choice(
                    name="On",
                    value="1"
                  ),
                  create_choice(
                    name="Off",
                    value="0"
                  )
                 ]
            )],
            permissions={
                789941733998854176 : [
                    create_permission(268035643760836608, SlashCommandPermissionType.USER, True)
                ]
            }
        )
    async def maintenance(self, ctx, toggle):
        with open("./data/config.ini", 'r') as configFile:

            Config.read_file(configFile)

        Config.set('DEFAULT', 'maintenance_mode', toggle)

        with open("./data/config.ini", 'w') as configFile:
            Config.write(configFile)

        await ctx.send("Maintenance Mode has changed.")
    