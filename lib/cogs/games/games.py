import discord
from discord.ext.commands import command, Cog
import random

from asyncio import sleep

class Games(Cog):

    def __init__(self, client):
        self.client = client
        
    @command(name= "8", aliases=['8ball'])
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
        
        ran = random.randint(0,1)
        if hot == 't':
            if ran == 1:
                await ctx.send("TAILS! You won!")
            else:
                await ctx.send("HEADS! You lose.")
        
        elif hot == 'h':
            if ran == 0:
                await ctx.send("HEADS! You won!")
            else:
                await ctx.send("TAILS! You lose.")

    @command()
    async def rps(self, ctx, *, player_input):
        ran = random.randint(0,2)
        if ran == 0:
            ai_input = 'Rock'
            await ctx.send(f"Sancus played: {ai_input}")
            if player_input.lower() == 'paper':
                await ctx.send("You won!")
            
            elif player_input.lower() == 'rock':
                await ctx.send("You tied!")

            elif player_input.lower() == 'scissors':
                await ctx.send("You lost!")

        elif ran == 1:
            ai_input = 'Paper'
            await ctx.send(f"Sancus played: {ai_input}")
            if player_input.lower() == 'scissors':
                await ctx.send("You won!")

            elif player_input.lower() == 'paper':
                await ctx.send("You tied!")
            
            elif player_input.lower() == 'rock':
                await ctx.send("You lost!")

        elif ran == 2:
            ai_input = 'Scissors'
            await ctx.send(f"Sancus played: {ai_input}")
            if player_input.lower() == 'rock':
                await ctx.send("You won!")

            elif player_input.lower() == 'scissors':
                await ctx.send("You tied!")
            
            elif player_input.lower() == 'paper':
                await ctx.send("You lost!")
    
    @command()
    #@cooldown(1, 30, commands.BucketType.user)
    async def dice(self, ctx, *, number=1):
        if number > 5:
            await ctx.send("Please only roll 5 dice at a time!")
        else:
            for i in range(number):
                j = i + 1
                diceroll = random.randint(1,6)
                await ctx.send(f"Dice {j}: {diceroll}")
                await sleep(0.75)



