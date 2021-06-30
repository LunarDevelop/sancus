from discord import Embed, Member
from discord.ext.commands import command, Cog

from lib.bot import bot

from datetime import datetime
import json, requests


from .triva import Trivia
from .voting import Polls
from .gifs import GIFS


class Misc(Trivia,
            Polls,
            GIFS,
            Cog):

    def __init__(self, client):
        self.client = client
        self.config = bot.config

    #Github command
    #@commands.command()
    async def gitlab(self, ctx):
        await ctx.send("Check out my GitLab page, where you can find all of my code: https://tinyurl.com/sancus-gitlab")

    @command(name="invite",brief ="Invite Sancus to your server")
    async def invite(self, ctx):
        await ctx.send(f"{ctx.author.mention}, here is my invite link: https://tinylink.net/oJgq2 :space_invader:")

    @command(name="botserver", brief="Join the offical server for Sancus ")
    async def botserver(self,ctx):
        await ctx.send(f"{ctx.author.mention}, come and joining my official server: https:discord.gg/XZB8mnY6f8 :flag_white: ")

    @command()
    async def hug(self, ctx, member : Member):
        url = "https://nekos.life/api/v2/img/hug"

        r = requests.get(url=url)

        embed = Embed(
            description=f"{member.mention} you have received a hug by {ctx.author.mention}",
            colour = self.config.embed(ctx.guild.id, "anime_image_nekopara")
        )

        embed.set_image(url=json.loads(r.content.decode("UTF-8"))['url'])

        embed.set_footer(text = f"{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

        await ctx.send(embed=embed)

    @command(name="pat")
    async def _pat(self,ctx, member : Member):
        url = "https://nekos.life/api/v2/img/pat"

        r = requests.get(url=url)

        embed = Embed(
            description=f"{member.mention} you have received a pat by {ctx.author.mention}",
            colour = self.config.embed(ctx.guild.id, "anime_image_nekopara")
        )

        embed.set_image(url=json.loads(r.content.decode("UTF-8"))['url'])

        embed.set_footer(text = f"{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

        await ctx.send(embed=embed)

    @command()
    async def bothug(self, ctx, *, member : Member):
        await ctx.send(f'{member.mention}, you have been sent a hug from <@341999214043332619>')
    
    @command()
    async def bothugself(self, ctx):
        await ctx.send(f'<@341999214043332619>, has received a hug from him self.')

    @command()
    async def hugself(self, ctx):
        await ctx.send(f'{ctx.author.mention}, has hugged themself.')

    @command()
    async def slap(self, ctx, *, member : Member):
        url = "https://nekos.life/api/v2/img/slap"

        r = requests.get(url=url)

        embed = Embed(
            description=f"{member.mention} you have received a slap by {ctx.author.mention}",
            colour = self.config.embed(ctx.guild.id, "anime_image_nekopara")
        )

        embed.set_image(url=json.loads(r.content.decode("UTF-8"))['url'])

        embed.set_footer(text = f"{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

        await ctx.send(embed=embed)

    @command()
    async def botlisting(self, ctx):
        embed = Embed(
            title = f"Sancus is avaliable on the following listing sites",
            colour = 0x000000
        )

    #Ping command
    @command()
    async def ping(self, ctx):
        """
            Gets the ping of the bot
        """

        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')
        print(f'Pong! {round(self.client.latency * 1000)}ms')

    @command()
    async def patreon(self, ctx):

        await ctx.send("Here is my patreon page: https://www.patreon.com/solarbam")

    @command()
    async def privicy(self, ctx):
        embed = Embed(
            title = f"Privicy Policy",
            #description = "Sancus only stores the user ID of each user who uses any of the economy commands. By using the commands you agree to have sancus store the information. Sancus also stores guild id numbers in order to provide customise features for each server. By using Sancus on your discord server you agree to have the guild id number stored.\n To remove any information stored by the bot please message SolarBAM404#1179 and he will instantly remove the information.",
            colour = 0x000000
        )

        embed.add_field(
            name="Types of data",
            value="Information that is stores are stored for the use within features that are provided by the bot. \nThis includes: \n1) User ID numbers, \n2) Guild IDs",
            inline= False
        )

        embed.add_field(
            name= "Processing the data",
            description = "The data is kept and stored within a secure area that can only be accessed through the bot it self. The data is automatically taken once the bot has joined a guild (for Guild ID) and once a user has used a command which requires storing the user ID. Types of commands which need user ID are stated below. No data is used by third-party applications",
            inline = False
        )


        embed.set_thumbnail(url=self.client.user.avatar_url)

        await ctx.send(embed=embed)