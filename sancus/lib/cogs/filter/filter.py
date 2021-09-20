import discord
from discord import Embed
from discord.ext import commands
import requests
import asyncio

from lib.bot import bot


class Filter(commands.Cog):

    def __init__(self, client : bot):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            check = requests.get(
                f"https://www.purgomalum.com/service/containsprofanity?text=${message.content}")
            check = check.text
                    
            if str(message.guild.id) in self.client.guilds_:
                guild = self.client.guilds_[str(message.guild.id)]
                filter = guild["filter"]
                words = guild["filterWords"]
                delete = guild["filterDelete"]
            
            else:
                return

            if filter:
                if check == 'true':
                    if delete == True:
                        await message.delete()
                        
                    elif delete == False:
                        response = requests.get(
                            "https://insult.mattbas.org/api/insult")

                        embed = Embed(
                            colour=0x000ff0000,
                            description=response.text
                        )
                        await message.channel.send(embed=embed)
                        
                elif message.content in words:
                    if delete == True:
                        await message.delete()

                    elif delete == False:
                        response = requests.get(
                            "https://insult.mattbas.org/api/insult")

                        embed = Embed(
                            colour=0x000ff0000,
                            description=response.text
                        )
                        await message.channel.send(embed=embed)
