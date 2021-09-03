from datetime import datetime

from discord.embeds import Embed
from discord.ext import commands


class Mail(commands.Cog):

    # NO UPDATES TO THIS BUT AFTER VERSION 5 THIS WILL BE REWORKED TO ALLOW FOR SERVER SUGGESTION AND BOT SUGGESTIONS

    def __init__(self, client):
        self.client = client
        self.redcircle = "\U0001F534"
        self.greencircle = "\U0001F7E2"

    @commands.command()
    async def suggest(self, ctx, *, suggestion):
        """Sends your suggestion straight to the bots main discord Server

        Suggestion : At least 50 charcters explaining your suggestion"""
        if not ctx.author.bot:
            if len(suggestion) < 50:
                await ctx.channel.send("Your message should be at least 50 characters long")
            else:
                oembed = Embed(
                    title="Suggestion",
                    colour=ctx.author.colour,
                    timestamp=datetime.utcnow()
                )

                oembed.set_thumbnail(url=ctx.author.avatar_url)

                field = [
                    ("Member", ctx.author.display_name, False),
                    ("Message", suggestion, False)
                ]

                for name, value, inline in field:
                    oembed.add_field(name=name, value=value, inline=inline)

                guild = self.client.get_guild(789941733998854176)
                channel = guild.get_channel(789971425246314497)

                msg = await channel.send(embed=oembed)

                await msg.add_reaction("\U0001F7E2")
                await msg.add_reaction("\U0001F534")

                react, user = await self.client.wait_for("reaction_add")

                if react.emoji == "\U0001F7E2":
                    schannel = guild.get_channel(792202614111600650)

                    nembed = Embed(
                        title="Suggestion",
                        colour=ctx.author.colour,
                        timestamp=datetime.utcnow()
                    )

                    nembed.set_thumbnail(url=ctx.author.avatar_url)

                    field = [
                        ("Member", ctx.author.display_name, False),
                        ("Suggestion", suggestion, False)
                    ]

                    for name, value, inline in field:
                        nembed.add_field(name=name, value=value, inline=inline)

                    newembed = await schannel.send(embed=nembed)

                    await newembed.add_reaction("\U0001F7E2")
                    await newembed.add_reaction("\U0001F534")


"""
TODO

=ADD staff checker
=ADD vote system

"""
