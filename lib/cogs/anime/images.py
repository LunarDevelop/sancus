from discord.ext.commands import command, Cog, group
from discord import Embed

from configparser import ConfigParser
import requests, json, datetime

config = ConfigParser()

with open("./data/config.ini", "r") as f:
    config.read_file(f)

class Images(Cog):
###All commands have temporary been disabled to due an api error after release of Version 5 This will be investigated

    @group(name="images")
    async def _image(self, ctx):
        """A group to display different images"""

    @_image.command(name="anime")
    async def _anime_(self,ctx):

        url = "https://gallery.fluxpoint.dev/api/sfw/anime"

        headers = {
            "Authorization" : config.get("DEFAULT", "flux_token")
        }

        r = requests.get(url=url, headers=headers)

        embed = Embed(
            name="Anime",
            colour = self.config.embed(ctx.guild.id, "anime_image_anime")
        )

        embed.set_image(url=json.loads(r.content.decode("UTF-8"))['file'])

        embed.set_footer(text = f"Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.\nCheck them out at https://fluxpoint.dev\n{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

        await ctx.send(embed=embed)

    @_image.command(name="wallpaper")
    async def _wallpaper_(self,ctx):

        url = "https://gallery.fluxpoint.dev/api/sfw/wallpaper"

        headers = {
            "Authorization" : config.get("DEFAULT", "flux_token")
        }

        r = requests.get(url=url, headers=headers)

        embed = Embed(
            name="Wallpaper",
            colour = self.oldConfig.embed(ctx.guild.id, "anime_image_wallpaper")
        )

        embed.set_image(url=json.loads(r.content.decode("UTF-8"))['file'])

        embed.set_footer(text = f"Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.\nCheck them out at https://fluxpoint.dev\n{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

        await ctx.send(embed=embed)

    @_image.command(name="azurlane")
    async def _azurlane_(self,ctx):

        url = "https://gallery.fluxpoint.dev/api/sfw/azurlane"

        headers = {
            "Authorization" : config.get("DEFAULT", "flux_token")
        }

        r = requests.get(url=url, headers=headers)

        embed = Embed(
            name="Azurlane",
            colour = self.config.embed(ctx.guild.id, "anime_image_azurlane")
        )

        embed.set_image(url=json.loads(r.content.decode("UTF-8"))['file'])

        embed.set_footer(text = f"Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.\nCheck them out at https://fluxpoint.dev\n{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

        await ctx.send(embed=embed)

    @_image.command(name="nekopara")
    async def _nekopara_(self,ctx):
        url = "https://gallery.fluxpoint.dev/api/sfw/nekopara"

        headers = {
            "Authorization" : config.get("DEFAULT", "flux_token")
        }

        r = requests.get(url=url, headers=headers)

        embed = Embed(
            name="Nekopara",
            colour = self.config.embed(ctx.guild.id, "anime_image_nekopara")
        )

        embed.set_image(url=json.loads(r.content.decode("UTF-8"))['file'])

        embed.set_footer(text = f"Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.\nCheck them out at https://fluxpoint.dev\n{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

        await ctx.send(embed=embed)

    @_image.command(name="slap")
    async def _slap(self,ctx):
        url = "https://nekos.life/api/v2/img/slap"

        r = requests.get(url=url)

        embed = Embed(
            name="NSFW Nekopara",
            colour = self.config.embed(ctx.guild.id, "anime_image_nekopara")
        )

        embed.set_image(url=json.loads(r.content.decode("UTF-8"))['url'])

        embed.set_footer(text = f"{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

        await ctx.send(embed=embed)

    @_image.command(name="meow")
    async def _meow(self,ctx):
        url = "https://nekos.life/api/v2/img/meow"

        r = requests.get(url=url)

        embed = Embed(
            name="NSFW Nekopara",
            colour = self.config.embed(ctx.guild.id, "anime_image_nekopara")
        )

        embed.set_image(url=json.loads(r.content.decode("UTF-8"))['url'])

        embed.set_footer(text = f"{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

        await ctx.send(embed=embed)

    @_image.command(name="pat")
    async def _pat(self,ctx):
        url = "https://nekos.life/api/v2/img/pat"

        r = requests.get(url=url)

        embed = Embed(
            name="NSFW Nekopara",
            colour = self.config.embed(ctx.guild.id, "anime_image_nekopara")
        )

        embed.set_image(url=json.loads(r.content.decode("UTF-8"))['url'])

        embed.set_footer(text = f"{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

        await ctx.send(embed=embed)

    @_image.command(name="memes")
    async def _memes_(self,ctx):
        url = "https://gallery.fluxpoint.dev/api/album/3"

        headers = {
            "Authorization" : config.get("DEFAULT", "flux_token")
        }

        r = requests.get(url=url, headers=headers)

        embed = Embed(
            name="Meme",
            colour = self.config.embed(ctx.guild.id, "anime_image_nekopara")
        )

        embed.set_image(url=json.loads(r.content.decode("UTF-8"))['file'])

        embed.set_footer(text = f"Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.\nCheck them out at https://fluxpoint.dev\n{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

        await ctx.send(embed=embed)

    @_image.command(name="doki")
    async def _doki_(self,ctx):
        url = "https://gallery.fluxpoint.dev/api/album/1"

        headers = {
            "Authorization" : config.get("DEFAULT", "flux_token")
        }

        r = requests.get(url=url, headers=headers)

        embed = Embed(
            name="Doki Doki",
            colour = self.config.embed(ctx.guild.id, "anime_image_nekopara")
        )
        
        embed.set_image(url=json.loads(r.content.decode("UTF-8"))['file'])

        embed.set_footer(text = f"Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.\nCheck them out at https://fluxpoint.dev\n{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

        await ctx.send(embed=embed)

    @_image.command(name="chibi")
    async def _chibi_(self,ctx):
        url = "https://gallery.fluxpoint.dev/api/album/18"

        headers = {
            "Authorization" : config.get("DEFAULT", "flux_token")
        }

        r = requests.get(url=url, headers=headers)

        embed = Embed(
            name="Chibi",
            colour = self.config.embed(ctx.guild.id, "anime_image_nekopara")
        )

        embed.set_image(url=json.loads(r.content.decode("UTF-8"))['file'])

        embed.set_footer(text = f"Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.\nCheck them out at https://fluxpoint.dev\n{datetime.utcnow().strftime('%B %d %Y - %H:%M UTC')}")

        await ctx.send(embed=embed)
