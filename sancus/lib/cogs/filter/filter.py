import discord
from discord import Embed
from discord.ext import commands
import requests
import asyncio

from lib.bot import bot


class Filter(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        c = bot.config
        if not message.author.bot:
            check = requests.get(
                f"https://www.purgomalum.com/service/containsprofanity?text=${message.content}")
            check_ = check.text

            for guild in bot.config.guilds:
                if guild["guildID"] == str(message.guild.id):
                    filter_ = str(guild["filter"])
                    type_ = int(guild["filterType"])

            if filter_ == '1':
                if check_ == 'true':
                    if type_ == 0:
                        await message.delete()
                    elif type_ == 1:
                        response = requests.get(
                            "https://insult.mattbas.org/api/insult")

                        embed = Embed(
                            colour=0x000ff0000,
                            description=response.text
                        )
                        await message.channel.send(embed=embed)
