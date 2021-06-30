from discord import Embed
from discord.ext.commands import command, Cog, group

import random, json, requests, calendar, time
from datetime import datetime

from lib.bot import bot

from .images import Images


class Anime(
            #Images,
            Cog
            ):

    def __init__(self, client):
        self.client = client
        self.config = bot.config
        self.oldConfig = bot.oldConfig
        self.exceptions = bot.exceptions

###Display an waifu
    @command()
    async def waifus(self,ctx, Id : int = None):
        """Displays a random (unless specified) waifu from the file

        Args:
            Id (int, optional): The ID number of the waifu image that is requested
        """

        #Timeouts have been removed while I rework them with the API
           
        with open("data/images/anime/waifus.json", 'r') as f:
            waifus = json.load(f)

        if Id is None:
            randomint = random.randint(0, (len(waifus)-1))

            embed = Embed(
                title= waifus[randomint]['name'],
                colour = self.oldConfig.embed(ctx.guild.id, "anime_waifus")
            )

            embed.set_image(url=waifus[randomint]['link'])
            embed.set_footer(text = f"ID: {waifus[randomint]['id']}\nIf the name is wrong please contact SolarBAM404#1179 so he can correct the name\n{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

            await ctx.send(embed=embed)

        else:
            for e in range(0, len(waifus)):
                if waifus[e]['id'] == int(Id):
                    break

            embed = Embed(
                title=waifus[e]['name'],
                colour = self.config.embed(ctx.guild.id, "anime_waifus")
            )

            embed.set_image(url=waifus[e]['link'])
            embed.set_footer(text = f"ID: {waifus[e]['id']}\nIf the name is wrong please contact SolarBAM404#1179 so he can correct the name\n{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

            await ctx.send(embed=embed)

###Display an husbando
    @command()
    async def husbandos(self,ctx, Id = None):
        """Displays a random (unless specified) husbando from the file

        Args:
            Id (int, optional): The ID number of the husbando image that is requested
        """
        

        with open("data/images/anime/husbandos.json", 'r') as f:
            husbandos = json.load(f)

        if Id is None:
            randomint = random.randint(0, (len(husbandos)))

            embed = Embed(
                title=husbandos[randomint]['name'],
                colour = self.oldConfig.embed(ctx.guild.id, "anime_husbandos")
            )

            embed.set_image(url=husbandos[randomint]['link'])
            embed.set_footer(text = f"ID: {husbandos[randomint]['id']}\nIf the name is wrong please contact SolarBAM404#1179 so he can correct the name\n{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

            await ctx.send(embed=embed)

        else:
            for e in range(0, len(husbandos)):
                if husbandos[e]['id'] == int(Id):
                    break

            embed = Embed(
                title= f"{husbandos[e]['name']}",
                colour = self.oldConfig.embed(ctx.guild.id, "anime_husbandos")
            )

            embed.set_image(url=husbandos[e]['link'])
            embed.set_footer(text = f"ID: {husbandos[e]['id']}\nIf the name is wrong please contact SolarBAM404#1179 so he can correct the name\n{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

            await ctx.send(embed=embed)
    
###Display the number of Anime Images that are on the bot
    @command()
    async def totalAimages(self,ctx):
        """
        Display the total images in both waifus and husbandos
        """
        with open("data/images/anime/husbandos.json", 'r') as f:

            husbandos = json.load(f)

        with open("data/images/anime/waifus.json", 'r') as f:

            waifus = json.load(f)

        total = len(husbandos) + len(waifus)

        embed = Embed (
            title = "Total images within Anime commands",
            colour = self.config.embed(ctx.guild.id, "anime_totalimages") 
        )

        fields = [
            ("Waifus:", len(waifus)),
            ("Husbandos:", len(husbandos)),
            ("Total:", total)
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value,inline=True)

        await ctx.send(embed=embed)

###Just lists all of images on the bot
    ###Needs to be written in version 5 after release to allow more images to be shown
    @command()
    async def listAnime(self, ctx, TYPE):
        """Display a list of anime id and names in the type

        Args:
            TYPE (string): `waifus` or `husbandos`
        """
        with open(f"data/images/anime/{TYPE}.json", 'r') as f:
            data = json.load(f)

        embed = Embed(
            title = f"List of {TYPE}",
            colour = 0xe3b7d2 
        )

        for instance in data:
            embed.add_field(name=f"ID: {instance['id']}",value=f"Name: {instance['name']}")

        await ctx.send(embed=embed)