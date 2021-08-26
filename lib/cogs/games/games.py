from discord import Embed
import discord
from discord.ext.commands import command, Cog
import random

from asyncio import sleep

from discord.ui import button


class Games(Cog):

    def __init__(self, client):
        self.client = client

    @command(name="8", aliases=['8ball'])
    async def _8ball(self, ctx, *, question):

        responses = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes – definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            "Don't count on it.",
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.']

        await ctx.send(f'Question: {question} \nAnswer: {random.choice(responses)}')

    @command(aliases=['ftc', 'cf', 'coinflip'])
    async def flipthecoin(self, ctx, *, hot):
        if hot.lower() in ["t", "h"]:
            ran = random.randint(0, 1)
            if hot.lower() == 't':
                if ran == 1:
                    await ctx.send("TAILS! You won!")
                else:
                    await ctx.send("HEADS! You lose.")

            elif hot.lower() == 'h':
                if ran == 0:
                    await ctx.send("HEADS! You won!")
                else:
                    await ctx.send("TAILS! You lose.")
        else:
            await ctx.send("Please choose between `h` for heads and `t` for tails")

    @command()
    async def rps(self, ctx):
        """Version 6
        Now get to put your choice instead of typing it"""

        player_input = None

        RockEmoji = self.client.get_emoji(873215841360035861)
        PaperEmoji = self.client.get_emoji(873215881147215912)
        ScissorsEmoji = self.client.get_emoji("scissors")

        embed = Embed(
            description="What do you want to draw?",
            colour=0x000d16532
        )

        class View(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(discord.ui.Button(label="Rock",
                              custom_id="rock", emoji=RockEmoji))
                self.add_item(discord.ui.Button(label="Paper",
                              custom_id="paper", emoji=PaperEmoji))
                self.add_item(discord.ui.Button(label="Scissors",
                              custom_id="scissors", emoji="✂️"))

        msg = await ctx.send(
            embed=embed,
            view=View()
        )

        interactionObject = await self.client.wait_for("interaction", timeout=120, check=lambda i: i.user.id == ctx.author.id)
        interactionObject.response.defer

        player_input = interactionObject.data["custom_id"]

        if player_input.lower() in ["rock", "paper", "scissors"]:
            ran = random.randint(0, 2)
            if ran == 0:
                ai_input = 'Rock'
                if player_input.lower() == 'paper':
                    await msg.edit(embed=Embed(
                        title="You Won!",
                        description=f"***Sancus played***: {ai_input}\nYour input: {player_input.capitalize()}",
                        colour=0x000d16532
                    ), view=None)

                elif player_input.lower() == 'rock':
                    await msg.edit(embed=Embed(
                        title="You Tied!",
                        description=f"***Sancus played***: {ai_input}\nYour input: {player_input.capitalize()}",
                        colour=0x000d16532
                    ), view=None)

                elif player_input.lower() == 'scissors':
                    await msg.edit(embed=Embed(
                        title="You Lost!",
                        description=f"***Sancus played***: {ai_input}\nYour input: {player_input.capitalize()}",
                        colour=0x000d16532
                    ), view=None)

            elif ran == 1:
                ai_input = 'Paper'
                if player_input.lower() == 'scissors':
                    await msg.edit(embed=Embed(
                        title="You Won!",
                        description=f"***Sancus played***: {ai_input}\nYour input: {player_input.capitalize()}",
                        colour=0x000d16532
                    ), view=None)

                elif player_input.lower() == 'paper':
                    await msg.edit(embed=Embed(
                        title="You Tied!",
                        description=f"***Sancus played***: {ai_input}\nYour input: {player_input.capitalize()}",
                        colour=0x000d16532
                    ), view=None)

                elif player_input.lower() == 'rock':
                    await msg.edit(embed=Embed(
                        title="You Lost!",
                        description=f"****Sancus played****: {ai_input}\nYour input: {player_input.capitalize()}",
                        colour=0x000d16532
                    ), view=None)

            elif ran == 2:
                ai_input = 'Scissors'
                if player_input.lower() == 'rock':
                    await msg.edit(embed=Embed(
                        title="You Won!",
                        description=f"***Sancus played***: {ai_input}\nYour input: {player_input.capitalize()}.",
                        colour=0x000d16532
                    ), view=None)
                elif player_input.lower() == 'scissors':
                    await msg.edit(embed=Embed(
                        title="You Tied!",
                        description=f"***Sancus played***: {ai_input}\nYour input: {player_input.capitalize()}",
                        colour=0x000d16532
                    ), view=None)

                elif player_input.lower() == 'paper':
                    await msg.edit(embed=Embed(
                        title="You Lost!",
                        description=f"***Sancus played***: {ai_input}\nYour input: {player_input.capitalize()}",
                        colour=0x000d16532
                    ), view=None)

        else:
            await ctx.send("Invaild Option\nYou can choose betwwen:\n`rock`, `paper` or `scissors`")

    @command()
    # @cooldown(1, 30, commands.BucketType.user)
    async def dice(self, ctx, *, number=1):
        if number > 5:
            await ctx.send("Please only roll 5 dice at a time!")
        else:
            for i in range(number):
                j = i + 1
                diceroll = random.randint(1, 6)
                await ctx.send(f"Dice {j}: {diceroll}")
                await sleep(0.75)
