from configparser import ConfigParser
import io
import json
import discord
from discord import reaction
from discord.enums import ButtonStyle
from discord.errors import NotFound
from discord.message import Attachment, Message
from functions.objects import Embeds
from discord.ui import button, Button
from discord.interactions import Interaction
from discord.ui.view import View

import requests


async def welcomeEmbed(self, button: Button, interaction: Interaction):
    if self.bot.client.guilds_[
            str(interaction.guild_id)]["welcomeType"]:
        cur_toggle = self.bot.client.guilds_[
            str(interaction.guild_id)]["welcomeMessage"]
        cur_type = "Banner Message"
        if self.bot.client.guilds_[str(interaction.guild_id)]["welcomeChannel"] != None:
            cur_channel = await self.bot.client.fetch_channel(self.bot.client.guilds_[
                str(interaction.guild_id)]["welcomeChannel"])
            cur_channel = cur_channel.mention
        else:
            cur_channel = None
        cur_bg = self.bot.client.guilds_[
            str(interaction.guild_id)]["welcomeBack"]
        cur_banner = self.bot.client.guilds_[
            str(interaction.guild_id)]["welcomeBanner"]
        cur_icon = self.bot.client.guilds_[
            str(interaction.guild_id)]["welcomeIcon"]
        cur_colour_txt = self.bot.client.guilds_[
            str(interaction.guild_id)]["welcomeTxtColor"]
        cur_colour_user = self.bot.client.guilds_[
            str(interaction.guild_id)]["welcomeUserColor"]
        cur_colour_members = self.bot.client.guilds_[
            str(interaction.guild_id)]["welcomeMembersColor"]

        embed = Embeds(
            title="Welcome Message Menu",
            description=f"""Change the settings of your welcome message.

                **On or Off** : {cur_toggle}
                **Welcome Type** : {cur_type}
                **Channel** : {cur_channel}
                
                **Background** : {cur_bg}
                **Banner** : {cur_banner}
                **Icon** : {cur_icon}
                **Text Color** : {cur_colour_txt}
                **User Text Color** : {cur_colour_user}
                **Member Count Text Color** : {cur_colour_members}
                """
        )

        await interaction.message.edit(embed=embed, view=self.bot.welcomeBanner(self.bot))
    else:
        cur_type = "Text Based Message"
        cur_toggle = self.bot.client.guilds_[
            str(interaction.guild_id)]["welcomeMessage"]
        cur_text = self.bot.client.guilds_[
            str(interaction.guild_id)]["welcomeText"]

        if self.bot.client.guilds_[str(interaction.guild_id)]["welcomeChannel"] != None:
            cur_channel = await self.bot.client.fetch_channel(self.bot.client.guilds_[
                str(interaction.guild_id)]["welcomeChannel"])
            cur_channel = cur_channel.mention
        else:
            cur_channel = None

        embed = Embeds(
            title="Welcome Message Menu",
            description=f"""Change the settings of your welcome message.
                
                **On or Off** : {cur_toggle}
                **Welcome Type** : {cur_type}
                **Channel** : {cur_channel}
                **Text** : {cur_text}
                """
        )
        await interaction.message.edit(embed=embed, view=self.bot.welcomeText(self.bot))


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
        async def filter(self, button: Button, interaction: Interaction):
            cur_filter = self.bot.client.guilds_[
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
            if self.bot.client.guilds_[
                    str(interaction.guild_id)]["logChannel"] != None:
                cur_channel = await self.bot.client.fetch_channel(int(self.bot.client.guilds_[
                    str(interaction.guild_id)]["logChannel"]))
            else:
                cur_channel = None

            embed = Embeds(
                title="Log Channel Menu",
                description=f"""Change the settings of your log channel.
                    
                    Log Channel: {cur_channel}
                    """
            )

            await interaction.response.edit_message(embed=embed, view=self.bot.log(self.bot))

        @button(
            label="Action Channel",
            style=ButtonStyle.blurple
        )
        async def action(self, button: Button, interaction: Interaction):
            if self.bot.client.guilds_[
                    str(interaction.guild_id)]["actionChannel"] != None:
                cur_channel = await self.bot.client.fetch_channel(int(self.bot.client.guilds_[
                    str(interaction.guild_id)]["actionChannel"]))
            else:
                cur_channel = None

            embed = Embeds(
                title="Action Log Channel Menu",
                description=f"""Change the settings of your action log channel.
                    
                    Action Log Channel: {cur_channel}
                    """
            )

            await interaction.response.edit_message(embed=embed, view=self.bot.action(self.bot))

        @button(
            label="Manage Welcoming",
            style=ButtonStyle.blurple
        )
        async def welcome(self, button: Button, interaction: Interaction):
            await welcomeEmbed(self, button, interaction)

        @button(
            label="Close!",
            style=ButtonStyle.red
        )
        async def close(self, button: Button, interaction: Interaction):
            if self.bot.client.guilds_[
                    str(interaction.guild_id)]["logChannel"] != None:
                log = await self.bot.client.fetch_channel(int(self.bot.client.guilds_[
                    str(interaction.guild_id)]["logChannel"]))
            else:
                log = None

            if self.bot.client.guilds_[
                    str(interaction.guild_id)]["actionChannel"] != None:
                action = await self.bot.client.fetch_channel(int(self.bot.client.guilds_[
                    str(interaction.guild_id)]["actionChannel"]))
            else:
                action = None

            embed = Embeds(
                title=f"{interaction.guild.name}'s Guild Settings",
                description=f"""Prefix: **{self.bot.client.guilds_[str(interaction.guild.id)]["prefix"]}**
                    Filter On: **{self.bot.client.guilds_[str(interaction.guild.id)]["filter"]}**
                    Filter Delete Messages: **{self.bot.client.guilds_[str(interaction.guild.id)]["filterDelete"]}**
                    Custom Filter: **{self.bot.client.guilds_[str(interaction.guild.id)]["filterWords"]}**
                    Log Channel: **{log}**
                    Action Channel: **{action}**
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
                cur_prefix = self.bot.client.guilds_[
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
        async def receive(self, button: Button, interaction: Interaction):
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
        def __init__(self, bot):
            super().__init__()
            self.bot = bot

        @button(
            label="Toggle Filter",
            style=ButtonStyle.blurple
        )
        async def toggle(self, button: Button, interaction: Interaction):

            if self.bot.client.guilds_[str(interaction.guild_id)]["filter"]:
                self.bot.client.config.put_config_guild(
                    interaction.guild.id, {"filter": False})
                self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()
            else:
                self.bot.client.config.put_config_guild(
                    interaction.guild.id, {"filter": True})
                self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()

            cur_filter = self.bot.client.guilds_[
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
            label="Toggle Filter Delete",
            style=ButtonStyle.red
        )
        async def delete(self, button: Button, interaction: Interaction):
            if self.bot.client.guilds_[str(interaction.guild_id)]["filterDelete"]:
                self.bot.client.config.put_config_guild(
                    interaction.guild.id, {"filterDelete": False})
                self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()
            else:
                self.bot.client.config.put_config_guild(
                    interaction.guild.id, {"filterDelete": True})
                self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()

            cur_filter = self.bot.client.guilds_[
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
            label="Custom Filter",
            style=ButtonStyle.green
        )
        async def custom(self, button: Button, interaction: Interaction):
            cur_words = self.bot.client.guilds_[
                str(interaction.guild_id)]["filterWords"]

            embed = Embeds(
                title="Filter Menu",
                description=f"""Change the settings of your custom filter.
                    
                    Custom Filter Words: {cur_words}
                    """
            )
            await interaction.response.edit_message(embed=embed, view=self.bot.custom(self.bot))

        @button(
            label="Main Menu",
            row=1,
            style=ButtonStyle.blurple)
        async def receive(self, button: Button, interaction: Interaction):
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

    class custom(View):
        def __init__(self, bot):
            super().__init__()
            self.bot = bot

        @button(
            label="Add a Word",
            style=ButtonStyle.blurple
        )
        async def add(self, button: Button, interaction: Interaction):
            message = interaction.message
            await interaction.message.edit(view=None)
            cur_list = self.bot.client.guilds_[
                str(interaction.guild_id)]["filterWords"]

            if cur_list == None:
                cur_list = []

            await interaction.response.send_message("What word do you want to add to the filter?")

            msg = await self.bot.client.wait_for("message", check=lambda u: u.author.id == interaction.user.id)

            cur_list.append(msg.content.lower())

            self.bot.client.config.put_config_guild(
                interaction.guild.id, {"filterWords": cur_list})
            self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()

            cur_words = self.bot.client.guilds_[
                str(interaction.guild_id)]["filterWords"]

            embed = Embeds(
                title="Filter Menu",
                description=f"""Change the settings of your custom filter.
                    
                    Custom Filter Words: {cur_words}
                    """
            )
            await interaction.delete_original_message()
            try:
                await msg.delete()
            except NotFound:
                pass
            await message.edit(embed=embed, view=self.bot.custom(self.bot))

        @button(
            label="Remove a Word",
            style=ButtonStyle.red
        )
        async def remove(self, button: Button, interaction: Interaction):
            message = interaction.message
            await interaction.message.edit(view=None)
            cur_list: list = self.bot.client.guilds_[
                str(interaction.guild_id)]["filterWords"]

            if cur_list == None:
                cur_list = []

            await interaction.response.send_message("What word do you want to remove from the filter?")

            msg = await self.bot.client.wait_for("message", check=lambda u: u.author.id == interaction.user.id)

            cur_list.remove(msg.content.lower())

            self.bot.client.config.put_config_guild(
                interaction.guild.id, {"filterWords": cur_list})
            self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()

            cur_words = self.bot.client.guilds_[
                str(interaction.guild_id)]["filterWords"]

            embed = Embeds(
                title="Filter Menu",
                description=f"""Change the settings of your custom filter.
                    
                    Custom Filter Words: {cur_words}
                    """
            )
            await interaction.delete_original_message()
            try:
                await msg.delete()
            except NotFound:
                pass
            await message.edit(embed=embed, view=self.bot.custom(self.bot))

        @button(
            label="Remove All",
            style=ButtonStyle.red
        )
        async def all(self, button: Button, interaction: Interaction):
            self.bot.client.config.put_config_guild(
                interaction.guild.id, {"filterWords": None})
            self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()

            cur_words = self.bot.client.guilds_[
                str(interaction.guild_id)]["filterWords"]

            embed = Embeds(
                title="Filter Menu",
                description=f"""Change the settings of your custom filter.
                    
                    Custom Filter Words: {cur_words}
                    """
            )
            await interaction.response.edit_message(embed=embed, view=self.bot.custom(self.bot))

        @button(
            label="Return to Filter Menu",
            style=ButtonStyle.grey
        )
        async def mainmenu(self, button: Button, interaction: Interaction):
            cur_filter = self.bot.client.guilds_[
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

    class log(View):

        def __init__(self, bot):
            super().__init__()
            self.bot = bot

        @button(
            label="Change Log Channel",
            custom_id="change",
            style=ButtonStyle.green,
            row=0)
        async def recieve(self, button: Button, interaction: Interaction):
            await interaction.response.defer()
            embed = Embeds(
                title="Change Log Channel",
                description="Type your new log channel below, either #ChannelName or channel id"
            )
            while True:
                cur_log = self.bot.client.guilds_[
                    str(interaction.guild.id)]["logChannel"]

                message: Message = interaction.message
                await message.edit(embed=embed, view=None)

                valueObj: Message = await self.bot.client.wait_for("message", timeout=120, check=lambda i: i.author.id == interaction.user.id)

                await valueObj.delete()

                if len(valueObj.channel_mentions) != 0:
                    self.bot.client.config.put_config_guild(
                        interaction.guild.id, {"logChannel": valueObj.channel_mentions[0].id})
                    self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()

                else:
                    try:
                        msg = int(valueObj.content)
                        channel = self.bot.client.fetch_channel(msg)
                        self.bot.client.config.put_config_guild(
                            interaction.guild.id, {"logChannel": channel.id})
                        self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()
                    except:
                        embed.add_field(
                            name="Error", value="Make sure you are entering either the id of the channel or mention the channel by typing # then the channel name")
                        await message.edit(embed=embed)
                        continue

                break

            msg = interaction.message
            menu = self.bot.Prefix(self.bot)

            if self.bot.client.guilds_[
                    str(interaction.guild_id)]["logChannel"] != None:
                cur_channel = await self.bot.client.fetch_channel(int(self.bot.client.guilds_[
                    str(interaction.guild_id)]["logChannel"]))
            else:
                cur_channel = None

            embed = Embeds(
                title="Log Channel Menu",
                description=f"""Change the settings of your log channel.
                
                Log Channel: {cur_channel}
                """
            )

            await message.edit(embed=embed, view=self.bot.log(self.bot))

        @button(
            label="Main Menu",
            custom_id="menu",
            style=ButtonStyle.blurple)
        async def receive(self, button: Button, interaction: Interaction):
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

    class action(View):

        def __init__(self, bot):
            super().__init__()
            self.bot = bot

        @button(
            label="Change Action Log Channel",
            custom_id="change",
            style=ButtonStyle.green,
            row=0)
        async def recieve(self, button: Button, interaction: Interaction):
            await interaction.response.defer()
            embed = Embeds(
                title="Change Action Log Channel",
                description="Type your new action log channel below, either #ChannelName or channel id"
            )
            while True:
                cur_log = self.bot.client.guilds_[
                    str(interaction.guild.id)]["actionChannel"]

                message: Message = interaction.message
                await message.edit(embed=embed, view=None)

                valueObj: Message = await self.bot.client.wait_for("message", timeout=120, check=lambda i: i.author.id == interaction.user.id)

                await valueObj.delete()

                if len(valueObj.channel_mentions) != 0:
                    self.bot.client.config.put_config_guild(
                        interaction.guild.id, {"actionChannel": valueObj.channel_mentions[0].id})
                    self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()

                else:
                    try:
                        msg = int(valueObj.content)
                        channel = self.bot.client.fetch_channel(msg)
                        self.bot.client.config.put_config_guild(
                            interaction.guild.id, {"actionChannel": channel.id})
                        self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()
                    except:
                        embed.add_field(
                            name="Error", value="Make sure you are entering either the id of the channel or mention the channel by typing # then the channel name")
                        await message.edit(embed=embed)
                        continue

                break

            msg = interaction.message
            menu = self.bot.Prefix(self.bot)

            if self.bot.client.guilds_[
                    str(interaction.guild_id)]["actionChannel"] != None:
                cur_channel = await self.bot.client.fetch_channel(int(self.bot.client.guilds_[
                    str(interaction.guild_id)]["actionChannel"]))
            else:
                cur_channel = None

            embed = Embeds(
                title="Action Log Channel Menu",
                description=f"""Change the settings of your action log channel.
                
                Action Log Channel: {cur_channel}
                """
            )

            await message.edit(embed=embed, view=self.bot.log(self.bot))

        @button(
            label="Main Menu",
            custom_id="menu",
            style=ButtonStyle.blurple)
        async def receive(self, button: Button, interaction: Interaction):
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

    class welcomeText(View):
        def __init__(self, bot):
            super().__init__()
            self.bot = bot

        @button(
            label="General:",
            style=ButtonStyle.red,
            disabled=True
        )
        async def generalTitle(self, button: Button, interaction: Interaction):
            pass
        
        @button(
            label="Turn On/Off",
            style=ButtonStyle.gray
        )
        async def turn(self, button: Button, interaction: Interaction):
            await interaction.response.defer()
            if self.bot.client.guilds_[str(interaction.guild_id)]["welcomeMessage"]:
                self.bot.client.config.put_config_guild(
                    interaction.guild.id, {"welcomeMessage": False})
                self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()
            else:
                self.bot.client.config.put_config_guild(
                    interaction.guild.id, {"welcomeMessage": True})
                self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()

            await welcomeEmbed(self, button, interaction)
        
        @button(
            label="Channel?",
            style=ButtonStyle.blurple
        )
        async def channel(self, button: Button, interaction: Interaction):
            await interaction.response.defer()
            embed = Embeds(
                title="Change the welcome channel",
                description="Type the channel below that you want the welcome messages in by doing #ChannelName"
            )

            await interaction.message.edit(embed=embed, view=None)

            msg: Message = await self.bot.client.wait_for("message", check=lambda i: i.author.id == interaction.user.id)
            await msg.delete()
            
            channel = msg.channel_mentions[0].id

            self.bot.client.config.put_config_guild(
                interaction.guild.id, {"welcomeChannel": channel})
            self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()
            await welcomeEmbed(self, button, interaction)

        @button(
            label="Toggle Type",
            style=ButtonStyle.blurple
        )
        async def toggle(self, button: Button, interaction: Interaction):
            await interaction.response.defer()
            if self.bot.client.guilds_[str(interaction.guild_id)]["welcomeType"]:
                self.bot.client.config.put_config_guild(
                    interaction.guild.id, {"welcomeType": False})
                self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()
            else:
                self.bot.client.config.put_config_guild(
                    interaction.guild.id, {"welcomeType": True})
                self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()

            await welcomeEmbed(self, button, interaction)
        
        @button(
            label="Test message",
            style=ButtonStyle.grey
        )
        async def test(self, button: Button, interaction: Interaction):
            cur_text : str= self.bot.client.guilds_[
                str(interaction.guild_id)]["welcomeText"]
            
            user = interaction.user.name
            server = interaction.guild.name
            
            cur_text = cur_text.format(user=user, server=server)
            
            await interaction.channel.send(f"{cur_text}", delete_after=10)
            
        @button(
            label="Text-Based:",
            style=ButtonStyle.red,
            row=1,
            disabled=True
        )
        async def textTitle(self, button: Button, interaction: Interaction):
            pass

        @button(
            label="Change Text",
            style=ButtonStyle.green,
            row=1
        )
        async def text(self, button: Button, interaction: Interaction):
            await interaction.response.defer()

            embed = Embeds(
                title="Change the welcome text",
                description="Type below what you would like your welcome message to say.\n\nSpecial Arugments:\n Server Name: {server}\nUsername: {user}"
            )

            await interaction.message.edit(embed=embed, view=None)

            msg = await self.bot.client.wait_for("message", check=lambda i: i.author.id == interaction.user.id)
            await msg.delete()
            
            self.bot.client.config.put_config_guild(
                interaction.guild.id, {"welcomeText": msg.content})
            self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()
            await welcomeEmbed(self, button, interaction)
            
        @button(
            label="Banner-Based:",
            style=ButtonStyle.red,
            row=2,
            disabled=True
        )
        async def bannerTitle(self, button: Button, interaction: Interaction):
            pass

        @button(
            label="Background Color",
            style=ButtonStyle.green,
            disabled=True,
            row=2
        )
        async def background(self, button: Button, interaction: Interaction):
            pass

        @button(
            label="Banner",
            style=ButtonStyle.green,
            disabled=True,
            row=2
        )
        async def banner(self, button: Button, interaction: Interaction):
            pass

        @button(
            label="Icon",
            style=ButtonStyle.green,
            disabled=True,
            row=2
        )
        async def icon(self, button: Button, interaction: Interaction):
            pass

        @button(
            label="Color Menu",
            style=ButtonStyle.green,
            disabled=True,
            row=2)
        async def colour(self, button: Button, interaction: Interaction):
            pass

    class welcomeBanner(View):
        def __init__(self, bot):
            super().__init__(timeout=0)
            self.bot = bot
            
        @button(
            label="General:",
            style=ButtonStyle.red,
            disabled=True
        )
        async def generalTitle(self, button: Button, interaction: Interaction):
            pass

        @button(
            label="Turn On/Off",
            style=ButtonStyle.gray
        )
        async def turn(self, button: Button, interaction: Interaction):
            await interaction.response.defer()
            if self.bot.client.guilds_[str(interaction.guild_id)]["welcomeMessage"]:
                self.bot.client.config.put_config_guild(
                    interaction.guild.id, {"welcomeMessage": False})
                self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()
            else:
                self.bot.client.config.put_config_guild(
                    interaction.guild.id, {"welcomeMessage": True})
                self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()

            await welcomeEmbed(self, button, interaction)

        @button(
            label="Channel?",
            style=ButtonStyle.blurple
        )
        async def channel(self, button: Button, interaction: Interaction):
            await interaction.response.defer()
            embed = Embeds(
                title="Change the welcome channel",
                description="Type the channel below that you want the welcome messages in by doing #ChannelName"
            )

            await interaction.message.edit(embed=embed, view=None)

            msg: Message = await self.bot.client.wait_for("message", check=lambda i: i.author.id == interaction.user.id)
            await msg.delete()
            channel = msg.channel_mentions[0].id

            self.bot.client.config.put_config_guild(
                interaction.guild.id, {"welcomeChannel": channel})
            self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()
            await welcomeEmbed(self, button, interaction)
        
        @button(
            label="Toggle Type",
            style=ButtonStyle.blurple
        )
        async def toggle(self, button: Button, interaction: Interaction):
            await interaction.response.defer()
            if self.bot.client.guilds_[str(interaction.guild_id)]["welcomeType"]:
                self.bot.client.config.put_config_guild(
                    interaction.guild.id, {"welcomeType": False})
                self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()
            else:
                self.bot.client.config.put_config_guild(
                    interaction.guild.id, {"welcomeType": True})
                self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()

            await welcomeEmbed(self, button, interaction)
        
        @button(
            label="Test message",
            style=ButtonStyle.grey
        )
        async def test(self, button: Button, interaction: Interaction):
            cur_bg = self.bot.client.guilds_[
                str(interaction.guild_id)]["welcomeBack"]
            cur_banner = self.bot.client.guilds_[
                str(interaction.guild_id)]["welcomeBanner"]
            cur_icon = self.bot.client.guilds_[
                str(interaction.guild_id)]["welcomeIcon"]
            cur_colour_txt = self.bot.client.guilds_[
                str(interaction.guild_id)]["welcomeTxtColor"]
            cur_colour_user = self.bot.client.guilds_[
                str(interaction.guild_id)]["welcomeUserColor"]
            cur_colour_members = self.bot.client.guilds_[
                str(interaction.guild_id)]["welcomeMembersColor"]
            
            api_ini = "sancus/data/api.ini"
            
            api_data = ConfigParser()
            with open(api_ini) as f:
                api_data.read_file(f)
            
            headers = {
                "Authorization" : api_data["FluxPoint"]["api_token"]
            }
            
            data = {
                "username": f"{interaction.user.name}#{interaction.user.discriminator}",
                "avatar": interaction.user.avatar.url,
                "background": f"#{cur_bg}",
                "members": "member #1",
                "icon": cur_icon,
                "banner": cur_banner,
                "color_welcome": f"#{cur_colour_txt}",
                "color_username": f"#{cur_colour_user}",
                "color_members": f"#{cur_colour_members}",
            }
            
            request = requests.get("https://api.fluxpoint.dev/gen/welcome", headers=headers, json=data)
            
            if request.ok:
                image = io.BytesIO(request.content)
                file = discord.File(image, filename="image.png")
                
                embed = Embeds()
                embed.set_image(url="attachment://image.png")
                            
                await interaction.channel.send(file=file, embed=embed, delete_after=10)
            else:
                await interaction.channel.send(json.loads(request.content)["message"])
            
        
        @button(
            label="Text-Based:",
            style=ButtonStyle.red,
            row=1,
            disabled=True
        )
        async def textTitle(self, button: Button, interaction: Interaction):
            pass

        @button(
            label="Change Text",
            style=ButtonStyle.green,
            row=1, 
            disabled=True
        )
        async def text(self, button: Button, interaction: Interaction):
            pass
        
        @button(
            label="Banner-Based:",
            style=ButtonStyle.red,
            row=2,
            disabled=True
        )
        async def bannerTitle(self, button: Button, interaction: Interaction):
            pass

        @button(
            label="Background Color",
            style=ButtonStyle.green,
            row=2
        )
        async def background(self, button: Button, interaction: Interaction):
            await interaction.response.defer()
            embed = Embeds(
                title="Change the background colour",
                description="Type the hex code that you want to use for the background of the banner.\n Find the hex codes here: \n**https://htmlcolorcodes.com/**"
            )

            await interaction.message.edit(embed=embed, view=None)

            msg: Message = await self.bot.client.wait_for("message", check=lambda i: i.author.id == interaction.user.id)
            await msg.delete()

            self.bot.client.config.put_config_guild(
                interaction.guild.id, {"welcomeBack": msg.content})
            self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()
            await welcomeEmbed(self, button, interaction)

        @button(
            label="Banner",
            style=ButtonStyle.green,
            row=2
        )
        async def banner(self, button: Button, interaction: Interaction):
            premades = [
                "love",
                "mountain",
                "purplewave",
                "rainbow",
                "space",
                "sunset",
                "swamp",
                "waifubot",
                "wave"
            ]
            await interaction.response.defer()
            
            embed = Embeds(
                title="Change the banner image",
                description=f"Enter either one of the following banner types or enter a custom image link.\n Link **must** end in .jpg or .png\n{premades}"
            )

            await interaction.message.edit(embed=embed, view=None)

            msg: Message = await self.bot.client.wait_for("message", check=lambda i: i.author.id == interaction.user.id)
            await msg.delete()

            self.bot.client.config.put_config_guild(
                interaction.guild.id, {"welcomeBanner": msg.content})
            self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()
            await welcomeEmbed(self, button, interaction)

        @button(
            label="Icon",
            style=ButtonStyle.green,
            row=2
        )
        async def icon(self, button: Button, interaction: Interaction):
            premades = [
                "cat",
                "chika",
                "dog",
                "dragon",
                "neko",
                "nyancat",
                "pepe",
                "pikachu",
                "senko",
                "shrek"
            ]
            await interaction.response.defer()

            embed = Embeds(
                title="Change the icon image",
                description=f"Enter either one of the following icon types or enter a custom image link.\n Link **must** end in .jpg or .png\n{premades}"
            )

            await interaction.message.edit(embed=embed, view=None)

            msg: Message = await self.bot.client.wait_for("message", check=lambda i: i.author.id == interaction.user.id)
            await msg.delete()

            self.bot.client.config.put_config_guild(
                interaction.guild.id, {"welcomeIcon": msg.content})
            self.bot.client.guilds_ = self.bot.client.config.get_config_guilds()
            await welcomeEmbed(self, button, interaction)

        """@button(
            label="Color Menu",
            style=ButtonStyle.green,
            row=2, disabled=True)
        async def colour(self, button: Button, interaction: Interaction):
            pass"""
