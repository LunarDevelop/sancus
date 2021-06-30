import discord
from discord.ext import commands

import random 
import json

class Trivia(commands.Cog):
    
    MINECRAFT = [ 
    ("How many End Portal Frame are there?","12"),
    ("What is the minimum obsideden do you need to build the nether portal?","10"),
    ("How big is a chunk?","16x16"),
    ("What y level do you need to be on to found diamond?","16"),
    ("Is gold armor better then iron armor?","false"),
    ("How many items of the same kind do you need to mmake a full set of armor?","26"),
    ("how many items do you need to make a stack? (for most item)","64"),
    ("What is the max enchant level?","30"),
    ("How do you breed cows?","wheat"),
    ("how do you breed sheeps?","wheat"),
    ("How do you breed pigs?","carrots"),
    ("How do you breed chicken?","seeds"),
    ("What is the max farm only using 1 water block?","9x9"),
    ("where do you found bedrock?","0"),
    ("when did minecraft come out","2011"),
    ]

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mctrivia (self, ctx):
        _random = random.randint(0, len(self.MINECRAFT))

        question = self.MINECRAFT[_random][0]
        answear = self.MINECRAFT[_random][1]

        await ctx.send(question)