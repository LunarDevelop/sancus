import discord
from discord.colour import Colour
from discord.ext import commands

from .econ import bank

import random

class robBank(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="rob", brief="Rob the bank if you dare.")
    async def rob(self, ctx):
            user = ctx.author.id

            chances = random.randrange(1,3)

            if chances == 1:
                """ROBBED BANK"""

                amount = random.randrange(1500,3000)
                bank.add_bank_money(user, amount)

                
                wallet, bank_account = bank.get_balance(user)
                
                embed = discord.Embed(
                    title = ":moneybag: You have successfully rob Sancus Bank :moneybag:",
                    description = f"--You have earned {amount} for you troubles.--\n--That bring you total to {bank_account} in your bank.--",
                    colour = ctx.author.colour
                    )

                await ctx.send(embed=embed)


            else:
                """FAILED"""
                amount = random.randrange(650,1000)
                bank.remove_bank_money(user, amount)

                wallet, bank_account = bank.get_balance(user)

                embed = discord.Embed(
                    title = ":oncoming_police_car: You have failed to rob Sancus Bank :oncoming_police_car: ",
                    description = f"--You have been fined {amount} from the police.--\n--That bring you total to {bank_account} in your bank.--",
                    colour = ctx.author.colour
                    )
                await ctx.send(embed=embed)



    