import discord
from discord.colour import Colour
from discord.ext import commands

from functions.objects import Embeds

from .econ import bank

import random


class robBank(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="rob", brief="Rob the bank if you dare.")
    async def rob(self, ctx):
        user = ctx.author.id

        chances = random.randrange(1, 3)
        b = bank(self.client,ctx.guild.id,ctx.author.id)
        if chances == 1:
            """ROBBED BANK"""

            amount = random.randrange(1500, 3000)
            b.add_bank_money(ctx.guild.id,amount)

            bank_account, wallet = b.get_balance(ctx.guild.id)

            embed = Embeds(
                title=":moneybag: You have successfully rob Sancus Bank :moneybag:",
                description=f"--You have earned **{amount}** for you troubles.--\n--That brings your total to **{bank_account}** in your bank.--",
                colour=ctx.author.colour
            )


            await ctx.send(embed=embed)

        else:
            """FAILED"""
            amount = random.randrange(650, 1000)
            b.remove_bank_money(ctx.guild.id, amount)

            bank_account, wallet = b.get_balance(ctx.guild.id)

            embed = Embeds(
                title=":oncoming_police_car: You have failed to rob Sancus Bank :oncoming_police_car: ",
                description=f"--You have been fined **{amount}** from the police.--\n--That bring you total to **{bank_account}** in your bank.--",
                colour=ctx.author.colour
            )

            await ctx.send(embed=embed)
