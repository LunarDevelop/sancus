
from discord import interactions
from discord.enums import ButtonStyle
from discord.message import Message
from lib.bot import Bot
from functions.objects import Embeds
from functions.objects import guildObject
from discord.ui import button, Button
from discord.interactions import Interaction
from discord.ui.view import View

import discord
from discord import Embed
from asyncio import sleep

import validators

from discord.ext.commands import context, has_permissions, command, Cog, group

class main():
    class menu(View):
        
            def __init__(self, bot):
                super().__init__()
                self.bot = bot

            @button(
                label="Prefix",
                style=ButtonStyle.blurple)
            async def prefix(self, button: Button, interaction: Interaction):

                """Change your server's prefix to use the bot.

                        Prefix cannot be more then 5 charcters in length
                        """
                cur_prefix = self.bot.client.guilds_[
                    str(interaction.guild_id)]["prefix"]
                menu = self.bot.Prefix(self.bot)

                embed = Embeds(
                    title="Prefix Menu",
                    description=f"If you would like to change the prefix please select **Change** below and type the new prefix in this channel. Otherwise click main menu.\n\n`Current Prefix:` **{cur_prefix}**"
                )

                await interaction.response.edit_message(embed=embed, view=menu)
            
            @button(
                label="Filter",
                style=ButtonStyle.blurple
            )
            async def filter(self, button:Button, interaction:Interaction):
                cur_filter = self.bot.client.bot.guilds_[
                    str(interaction.guild_id)]["filter"]
                cur_type = self.bot.client.guilds_[
                    str(interaction.guild_id)]["filterDelete"]
                
                embed = Embeds(
                    title="Filter Menu",
                    description=f"""Change the settings of your filter and custom filter.
                    
                    Filter: {cur_filter}
                    Delete Messages: {cur_type}
                    """
                )

                await interaction.response.edit_message(embed=embed, view=self.bot.Filter(self.bot))
            
            @button(
                label="Log Channel",
                style=ButtonStyle.blurple
            )
            async def log(self, button: Button, interaction: Interaction):
                pass
            
            @button(
                label="Action Channel",
                style=ButtonStyle.blurple
            )
            async def action(self, button: Button, interaction: Interaction):
                pass
            
            @button(
                label="Manage Welcoming",
                style=ButtonStyle.blurple
            )
            async def welcome(self, button: Button, interaction: Interaction):
                pass
            
            @button(
                label="Close!",
                style=ButtonStyle.red
            )
            async def close(self, button: Button, interaction: Interaction):
                embed = Embeds(
                    title=f"{interaction.guild.name}'s Guild Settings",
                    description=f"""Prefix: **{self.bot.client.guilds_[str(interaction.guild.id)]["prefix"]}**
                    Filter On: **{self.bot.client.guilds_[str(interaction.guild.id)]["filter"]}**
                    Filter Delete Messages: **{self.bot.client.guilds_[str(interaction.guild.id)]["filterDelete"]}**
                    """,
                    colour=0x000e8a302
                )
                
                await interaction.response.edit_message(embed=embed, view=None)

    class Prefix(View):
    
        def __init__(self, bot):
            super().__init__()
            self.bot = bot

        @button(
            label="Change Prefix",
            custom_id="change",
            style=ButtonStyle.green,
            row=0)
        async def recieve(self, button: Button, interaction: Interaction):
            while True:
                cur_prefix = self.bot.guilds_[
                    str(interaction.guild.id)]["prefix"]
                embed = Embeds(
                    title="Change Prefix",
                    description="Type your new prefix below"
                )

                msg = await interaction.response.edit_message(embed=embed, view=None)

                valueObj: Message = await self.bot.client.wait_for("message", timeout=120, check=lambda i: i.author.id == interaction.user.id)

                value = valueObj.content

                if len(value) < 1 or len(value) > 5:
                    embed.description = "Prefix needs to be between 1 and 5 characters long"

                elif value != None and value != cur_prefix:
                    self.bot.client.config.put_config_guild(
                        interaction.guild.id, {"prefix": value})
                    self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()

                await valueObj.delete()
                break
            msg = interaction.message
            cur_prefix = self.bot.client.guilds_[
                str(interaction.guild_id)]["prefix"]
            value = None
            menu = self.bot.Prefix(self.bot)

            embed = Embeds(
                title="Prefix Menu",
                description=f"If you would like to change the prefix please select **Change** below and type the new prefix in this channel. Otherwise click main menu.\n\n`Current Prefix:` **{cur_prefix}**"
            )

            await msg.edit(embed=embed, view=menu)

        @button(
            label="Main Menu",
            custom_id="menu",
            style=ButtonStyle.blurple)
        async def receive(self, button:Button, interaction:Interaction):
            embed = Embeds(
                title=f"{interaction.guild.name}'s Settings",
                colour=0x000e8a302)

            fields = [
                ("Changing Comand Prefix",
                f"Change how users on your server use commands on {self.bot.client.user.name}"),
                ("Filter setting",
                f"Change how the filter reacts, if its on and the custom filter"),
                ("LogChannel",
                f"Change the log channel that your server uses."),
                ("Action Channel",
                 f"Change the action channel for {interaction.guild.name}."),
                ("Welcome User Message",
                f"Open the welcome message editor"),
            ]

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

            msg: Message = await interaction.response.edit_message(embed=embed, view=self.bot.menu(self.bot))

    class Filter(View):
        pass
