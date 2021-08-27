import discord
from discord.embeds import Embed
from discord.ext import commands
import requests, json, random, io

class GIFS(commands.Cog):

    APIKEY = "QYT7O4HIG3UU"
    RANDOMURL = "https://g.tenor.com/v1/random?"
    URL = "https://g.tenor.com/v1/gifs?"
    LMT = 8

    @commands.command()
    async def gif(self, ctx, search_term):
        f"""Search for a gif and {self.client.user.name} will return a random gif from the list
        
        Args:
        
        - Search term: what kind of gif do you want
        """

        #replace any spaces with nothing to remove them
        for char in search_term:
            if char in " ":
                search_term = search_term.replace(char,'')

        #set the url link with all of the required args
        url = self.RANDOMURL + "key=%s&q=%s&media_filter=%s&limit=%s&contentfilter=%s" % (self.APIKEY, search_term, "minimal", 10, "medium")

        r = requests.get(url)

        #check if requested info was code 200
        if r.ok:
            try:
                gif = json.loads(r.content)
                giflist = gif['results']
                ran = random.randint(0, (len(giflist)-1))
                image = giflist[ran]['url']
                                
                await ctx.send(image)

            except: await ctx.send("I can't find any gif matching that word")

        elif r.status_code == 429:
            await ctx.send("Rate limit exceeded")

        else:
            await ctx.send("GIF loading has failed contact Bot Owner ( Solar#0404 )")
