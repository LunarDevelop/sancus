import discord
from discord import Embed, Emoji, colour
from discord import interactions
from discord.ext.commands import Cog, command

from datetime import datetime, timedelta

import asyncio

class helpButtons(Cog):
    """Version 6 Help Command
    This version is using the new interaction buttons to navigate a menu."""

    def __init__(self, client) -> None:
        self.client = client

    @command(name="help")
    async def buttons(self, ctx):
        await ctx.message.delete()

    # Emojis used within bot interations
        ModEmoji = self.client.get_emoji(872992608354443314)
        EconEmoji = self.client.get_emoji(872998673422897253)
        GamesEmoji = self.client.get_emoji(873008493530067014)
        MiscEmoji = self.client.get_emoji(873017754255523903)

        CloseEmoji = self.client.get_emoji(872992645302075392)
        OpenEmoji = self.client.get_emoji(872992768073551893)
    #
        if len(self.client.helpInstance) != 0:
            for name, instance, message in self.client.helpInstance:
                if name == ctx.author.id:

                    channel = self.client.get_channel(instance)

                    try:
                        pre_message = await channel.fetch_message(int(message))
                        await pre_message.delete()

                        self.client.helpInstance.remove(
                            (name, instance, message))
                        break
                    except:
                        self.client.helpInstance.remove(
                            (name, instance, message))

        embed = Embed(
            title="Welcome to the new and improved help command",
            description="All you need to do is click a button below. \n\n**Please close this instance or wait for a time out before doing another help command for yourself**"
        )

        class menu(discord.ui.View):
            def __init__(self):
                super().__init__()
                # Row 1
                self.add_item(discord.ui.Button(label='Mod Help', emoji=ModEmoji,
                                                custom_id="mod", style=discord.ButtonStyle.blurple, row=0))
                self.add_item(discord.ui.Button(label='Econ Help', emoji=EconEmoji,
                                                custom_id="econ", style=discord.ButtonStyle.green, row=0))
                self.add_item(discord.ui.Button(label='Games Help', emoji=GamesEmoji,
                                                custom_id="games", style=discord.ButtonStyle.green, row=0))
                self.add_item(discord.ui.Button(label='Misc Help', emoji=MiscEmoji,
                                                custom_id="misc", style=discord.ButtonStyle.green, row=0))
                # Row 2
                self.add_item(discord.ui.Button(label='Close', emoji=CloseEmoji,
                                                custom_id="close", style=discord.ButtonStyle.danger, row=1))
                self.add_item(discord.ui.Button(label='Leave Open', emoji=OpenEmoji,
                                                custom_id="open", style=discord.ButtonStyle.danger, row=1))

        msg = await ctx.send(
            embed=embed,
            view=menu()
        )

        self.client.helpInstance.append(
            (ctx.author.id, ctx.channel.id, msg.id))

        while True:
            try:
                interactionObject = await self.client.wait_for("interaction", timeout=120, check=lambda i: i.user.id == ctx.author.id)
                interactionObject.response.defer

                interaction = interactionObject.data["custom_id"]

                if interaction == "mod":
                    await msg.edit(content="", embed=self.Mod())

                elif interaction == "econ":
                    await msg.edit(content="", embed=self.Econ())

                elif interaction == "games":
                    await msg.edit(content="", embed=self.Games())

                elif interaction == "misc":
                    await msg.edit(content="", embed=self.Misc())

                elif interaction == "close":
                    await msg.delete()
                    self.client.helpInstance.remove(
                        (ctx.author.id, ctx.channel.id, msg.id))
                    return

                elif interaction == "open":
                    await msg.edit(content="", view=None)
                    self.client.helpInstance.remove(
                        (ctx.author.id, ctx.channel.id, msg.id))
                    return

            except asyncio.TimeoutError:
                embed = Embed(
                    description="You have been timed out, be quicker :smile:"
                )

                await msg.edit(content="", components=[], embed=embed, delete_after=15)
                self.client.helpInstance.remove(
                    (ctx.author.id, ctx.channel.id, msg.id))
                return

    def Econ(self):
        embed = Embed(
            title="Economy",
            description="Get those delicious dollar bills",
            colour=0x00094e31e
        )

        fields = [
            ("payday", "Get that pay day money"),
            ("beg", "You might get lucky"),
            ("balance", "See you wallet and bank account"),
            ("leaderboard [amount]", "Are you in the top 5?")
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text="{} = Required, [] = Optional\n" +
                         self.client.embedAuthorName, icon_url=self.client.embedAuthorUrl)

        return embed

    def Mod(self):
        embed = Embed(
            title='Moderation',
            description="For my admins out there",
            colour=0x000e31e4f
        )

        fields = [
            ("kick {userid} [reason]",
             "Kick those players that you don't mind coming back"),
            ("ban {userid} [reason]",
             "Ban those players you don't want to see again"),
            ("unban {userid} [reason]",
             "Unban players who were banned by mistake"),
            ("ping", "Get the ping of the bot"),
            ("avatar {userid}",
             "Get a full size image of the user's avatar"),
            ("userinfo / ui {userid}", "Get information about a user"),
            ("serverinfo / si", "Get information about your server"),
            ("embed", "Send and embed message to a channel on your server/guild"),
            #("announce", "Sends an announcement to a channel for you."),
            ("msgsend", "Sends a message to a channel for you"),
            ("setup menu", "Loads up an embed message with all the settings for the bot")
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text="{} = Required, [] = Optional\n" +
                         self.client.embedAuthorName, icon_url=self.client.embedAuthorUrl)

        return embed

    def Games(self):
        embed = Embed(
            title='Games',
            description="Who doesn't love a spot of gaming",
            colour=0x0008e1ee3
        )

        fields = [
            ("Dice {roll amount | max 5}", "Roll the dice"),
            ("rps {rock, paper or scissors}",
             "Test you luck in a game of Rock Paper Scissors"),
            ("cf {t or h}", "Guess which side the coin will land on, head (h) or tails (t)"),
            ("8ball {question}", "Ask it a yes, no question")
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text="{} = Required, [] = Optional\n" +
                         self.client.embedAuthorName, icon_url=self.client.embedAuthorUrl)

        return embed

    def Misc(self):
        embed = Embed(
            title='Misc Help',
            description="Who doesn't have random stuff",
            colour=0x000e3bc1e
        )

        fields = [
            ("hug {@user}", "Hug a friend, they may need it"),
            ("bothug {@user}", "Tell me who you want me to hug"),
            ("bothugself", "Let me hug myself"),
            ("hugself", "Give your self a hug"),
            ("slap {@user}", "Give a user a cheeky slap"),
            ("pat {@user}", "Pat a fellow user"),
            ("create_poll", "Create a poll for user to vote on"),
            ("gif {search word}", "Get a random gif"),
            ("invite", "Invite Sancus to your own server"),
            ("botserver", "Join my server and see all of my updates early"),
            ("suggest", "Give Solar more ideas for Sancus, 50 Characters minimum"),
            ("covid [country code, 'gb' for the UK]",
             "Get the global status of the current Covid19 pandemic")
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text="{} = Required, [] = Optional\n" +
                         self.client.embedAuthorName, icon_url=self.client.embedAuthorUrl)

        return embed
