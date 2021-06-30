import discord
from discord.ext import commands
import asyncio

from datetime import datetime

from lib.bot import bot

from .members import Members

def getLogChannel(self, guildid):
    for guild in bot.config.guilds:
        if guild["guildID"] == str(guildid):
            try:
                LogChannel = self.client.get_channel(int(guild["logChannel"]))
        
                return LogChannel
            except:pass

class Logging(
    Members,
    commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """
        Logs edited message to log channel of the guild
        """
        c = bot.oldConfig

        if not after.author.bot:
            if before.content != after.content:
                
                Log_Channel = getLogChannel(self, before.guild.id)

                embed= discord.Embed(
                    title = f"Message edited by {before.author.name}#{before.author.discriminator}",
                    description = f"ID: {before.author.id}\nNick: {before.author.nick}",
                    colour = c.getembed(before.guild.id, "log_edited"),
                    timestamp = datetime.utcnow()
                    )

                embed.set_thumbnail(url= before.author.avatar_url)
                fields = [
                    ("Before", before.content, False),
                    ("After", after.content, False),
                    ("Channel", before.channel.name, True)
                    ]

                for name, value, inline, in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await Log_Channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        """
        Logs deleted message to log channel of the guild
        """
        c = bot.oldConfig

        message = payload.cached_message

        if not message.author.bot:
            
            try:
                Log_Channel = getLogChannel(self, payload.guild_id)

                embed = discord.Embed(
                    title = f"Message deleted by {message.author.name}#{message.author.discriminator}",
                    description = f"ID: {message.author.id}",
                    colour = c.getembed(payload.guild_id, "log_deleted"),
                    timestamp = datetime.utcnow()
                    )
                
                embed.set_thumbnail(url= message.author.avatar_url)

                fields = [
                    ("Content:", message.content, False)
                    ]

                for name, value, inline, in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                
                await Log_Channel.send(embed=embed)
            except:pass