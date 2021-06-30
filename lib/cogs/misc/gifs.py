import discord
from discord.ext import commands
import requests, json, random, io

class GIFS(commands.Cog):

    APIKEY = "QYT7O4HIG3UU"
    RANDOMURL = "https://g.tenor.com/v1/random?"
    URL = "https://g.tenor.com/v1/gifs?"
    LMT = 8

    @commands.command()
    async def gif(self, ctx, *, search_term):
        if search_term is None:
            await ctx.send("Please try again and enter word or phrase for the gif you want. So its something like this `s!gif good morning`")

        for char in search_term:
            if char in " ":
                search_term = search_term.replace(char,'')

        url = self.RANDOMURL + "key=%s&q=%s&media_filter=%s&limit=%s&contentfilter=%s" % (self.APIKEY, search_term, "minimal", 10, "medium")

        r = requests.get(url)

        if r.status_code == 200 or r.status_code == 202:
            try:
                gif = json.loads(r.content)
                giflist = gif['results']
                ran = random.randint(0, len(giflist))
                image = giflist[ran]['media']

                await ctx.send(giflist[ran]['url'])

            except: await ctx.send("I can't find any gif matching that word")

        elif r.status_code == 429:
            await ctx.send("Rate limit exceeded")

        else:
            await ctx.send("GIF loading has failed contact Bot Owner")