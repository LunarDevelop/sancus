import discord
from discord.ext import commands
import asyncio

from datetime import datetime

from lib.bot import bot

from .members import Members


class Logging(
        Members,
        commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        """Logs edited message to log channel of the guild
        """
        try:
            before = payload.cached_message
            after = await (await (await self.client.fetch_guild(payload.guild_id)).fetch_channel(payload.channel_id)).fetch_message(payload.message_id)

            if not after.author.bot:
                if before.content != after.content:

                    Log_Channel = await self.client.getLogChannel(before.guild.id)

                    embed = discord.Embed(
                        title=f"Message edited by {before.author.name}#{before.author.discriminator}",
                        description=f"ID: {before.author.id}\nNick: {before.author.nick}",
                        colour=0x000f8f500,
                        timestamp=datetime.utcnow()
                    )

                    embed.set_thumbnail(url=before.author.display_avatar.url)
                    fields = [
                        ("Before", before.content, False),
                        ("After", after.content, False),
                        ("Channel", before.channel.name, True)
                    ]

                    for name, value, inline, in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    embed.set_footer(text=self.client.embedAuthorName,
                                     icon_url=self.client.embedAuthorUrl)

                    try:
                        await Log_Channel.send(embed=embed)
                    except:
                        pass
        except:
            pass

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        """
        Logs deleted message to log channel of the guild
        """
        message = payload.cached_message

        if not message.author.bot:

            if message.content in self.client.all_commands:
                return

            try:
                Log_Channel = await self.client.getLogChannel(payload.guild_id)

                embed = discord.Embed(
                    title=f"Message deleted by {message.author.name}#{message.author.discriminator}",
                    description=f"ID: {message.author.id}",
                    colour=0x000fe0100,
                    timestamp=datetime.utcnow()
                )

                embed.set_thumbnail(url=message.author.display_avatar.url)

                fields = [
                    ("Content:", message.content, False)
                ]

                for name, value, inline, in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                embed.set_footer(text=self.client.embedAuthorName,
                                 icon_url=self.client.embedAuthorUrl)

                await Log_Channel.send(embed=embed)
            except:
                pass

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        try:
            logChannel = self.getLogChannel(payload.guild_id)

            if logChannel != None:
                if payload.cached_messages[0]:
                    embed = discord.Embed(
                        title=f"Bulk Message Delete",
                        description=f"Author name: {payload.cached_messages[0].author.id}",
                        colour=0x000fe0100,
                        timestamp=datetime.utcnow()
                    )

                    embed.set_thumbnail(
                        url=payload.cached_messages[0].author.avatar_url)

                    fields = [
                        ("Content:", payload.cached_messages[0].content, False)
                    ]

                    for name, value, inline, in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    embed.set_footer(text=self.client.embedAuthorName,
                                     icon_url=self.client.embedAuthorUrl)

                    await logChannel.send(embed=embed)
        except:
            pass
