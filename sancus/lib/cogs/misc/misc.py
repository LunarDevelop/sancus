from discord import Embed, Member
from discord.ext.commands import command, Cog

from lib.bot import bot

from datetime import datetime
import json
import requests

from .voting import Polls
from .gifs import GIFS
Test_Servers = [780211278614364160]


class Misc(
        Polls,
        GIFS,
        Cog):

    def __init__(self, client):
        self.client = client
        self.config = bot.config

    @command()
    async def github(self, ctx):
        "GitHub repository link"

        embed = Embed(
            title="Bot Repository",
            description=f"Want to see all the behind the scenes code for {self.client.user.mention}",
            colour=0x0009900ff
        )

        embed.set_thumbnail(
            url="https://avatars.githubusercontent.com/u/18133?s=200&v=4")
        embed.url = "https://github.com/Solar-Productions/sancus"

        embed.set_footer(text=self.client.embedAuthorName,
                         icon_url=self.client.embedAuthorUrl)

        await ctx.send(embed=embed)

    @command()
    async def invite(self, ctx):
        embed = Embed(
            title=f"Invite {self.client.user.name} to your server",
            description=f"Get access to the bot on your own server and use all the features",
            url="https://bit.ly/sancus404",
            colour=0x0009900ff
        )

        embed.set_thumbnail(url=self.client.user.display_avatar.url)

        embed.set_footer(text=self.client.embedAuthorName,
                         icon_url=self.client.embedAuthorUrl)

        await ctx.send(embed=embed)

    @command()
    async def support(self, ctx):
        embed = Embed(
            title="Support??",
            description="Do you want to check out the offical support server or get some new software for yourself?",
            url="https://discord.gg/XZB8mnY6f8",
            colour=0x0009900ff
        )

        embed.set_thumbnail(url=self.client.user.display_avatar.url)

        embed.set_footer(text=self.client.embedAuthorName,
                         icon_url=self.client.embedAuthorUrl)

        await ctx.send(embed=embed)

###

    @command()
    async def hug(self, ctx, member: Member):
        """Hug a user by simply tagging them in the command

        **Args:**

        Member: Tag the user you want to hug"""

        url = "https://nekos.life/api/v2/img/hug"

        r = requests.get(url=url).json()

        embed = Embed(
            description=f"{member.mention} you have received a hug by {ctx.author.mention}",
            colour=bot.oldConfig.embed(ctx.guild.id, "anime_image_nekopara")
        )

        embed.set_image(url=r["url"])

        embed.set_footer(text=self.client.embedAuthorName,
                         icon_url=self.client.embedAuthorUrl)

        await ctx.send(embed=embed)

    @command(name="pat")
    async def _pat(self, ctx, member: Member):
        """Pat some on the back or head

        **Args:**

        Member: Tag the user you want to pat"""

        url = "https://nekos.life/api/v2/img/pat"

        r = requests.get(url=url)

        embed = Embed(
            description=f"{member.mention} you have received a pat by {ctx.author.mention}",
            colour=bot.oldConfig.embed(ctx.guild.id, "anime_image_nekopara")
        )

        embed.set_image(url=json.loads(r.content.decode("UTF-8"))['url'])

        embed.set_footer(text=self.client.embedAuthorName,
                         icon_url=self.client.embedAuthorUrl)

        await ctx.send(embed=embed)

    @command()
    async def slap(self, ctx, *, member: Member):
        """Slap someone's face

        **Args:**

        Member: Tag the user you want to slap"""

        url = "https://nekos.life/api/v2/img/slap"

        r = requests.get(url=url)

        embed = Embed(
            description=f"{member.mention} you have received a slap by {ctx.author.mention}",
            colour=bot.oldConfig.embed(ctx.guild.id, "anime_image_nekopara")
        )

        embed.set_image(url=json.loads(r.content.decode("UTF-8"))['url'])

        embed.set_footer(text=self.client.embedAuthorName,
                         icon_url=self.client.embedAuthorUrl)

        await ctx.send(embed=embed)

    # Ping command
    @command()
    async def ping(self, ctx):
        "Gets the ping of the bot"

        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')
        print(f'Pong! {round(self.client.latency * 1000)}ms')

    @command()
    async def patreon(self, ctx):
        embed = Embed(
            title="Patreon Perks",
            description=f"Help support Sancus and the others in their continued adventure to climb the ladder.",
            url=" https://www.patreon.com/solarbam",
            colour=0x0009900ff
        )

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/789247201678327838/880746027999690772/Digital-Patreon-Logo_FieryCoral.png")

        embed.set_footer(text=self.client.embedAuthorName,
                         icon_url=self.client.embedAuthorUrl)

        await ctx.send(embed=embed)

    @command()
    async def info(self, ctx):
        embed = Embed(
            title="About me | The creator, Solar",
            description="""I started programming stuff in Secondary School here in the UK. Sancus was my first big project and the first libray that I understood. He is also made the ground work for me to go out and learn serval other things. For example learn HTML, CSS and JS to make the website (still working on it :P ) and C# to make the API link to my database. Along side many other things. 
            \n I inspire to continue coding and make some sort of living of it. Current trying to find a starting place for all of that but I love coding and love being a part of the amazing community
            \n\n The idea behind Sancus was orginally just to have a bit of fun and make a cool bot for my mate. I then decided to expand upon that and make a full functional bot with tons of features and make it public, which I believe I am getting very close to fully functional personally. There are still sections which need to fined tuned but so far it is all okay."""
        )

        embed.set_footer(text=self.client.embedAuthorName,
                         icon_url=self.client.embedAuthorUrl)

        await ctx.send(embed=embed)
