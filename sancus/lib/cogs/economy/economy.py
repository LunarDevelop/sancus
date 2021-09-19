from discord import Embed
from discord.ext.commands import command, CommandOnCooldown
from discord.ext.commands import Cog

import random
import datetime
import time
import calendar

from .econ import bank as b

from .robBank import robBank

from lib.bot import bot
from functions.objects import Embeds


class Econ(
        robBank,
        Cog):

    def __init__(self, client : bot):
        self.client = client
        self.exceptions = bot.exceptions

    @command()
    async def balance(self, ctx):
        if ctx.author.name[-1].lower() == 's':
            name = f"{ctx.author.name}'"
        else:
            name = f"{ctx.author.name}'s"

        embed = Embeds(
            title=f"{name} balance",
        )
        bank = b(self.client, ctx.guild.id, ctx.author.id)
        account, wallet = bank.get_balance(ctx.guild.id)

        embed.add_field(name="Wallet:", value=str(wallet), inline=True)
        embed.add_field(name="Bank Account:", value=str(account), inline=True)

        await ctx.send(embed=embed)

    @command()
    async def payday(self, ctx):
        bank = b(self.client, ctx.guild.id, ctx.author.id)
        """timeout = self.oldConfig.timeout(ctx.guild.id, "payday")
        cur_time = ctx.message.created_at.utctimetuple()

        try:
            timedata = self.oldConfig.user(str(ctx.author.id))['payday']
            outputTime = int(timedata) + int(timeout)
            UNIXTime = calendar.timegm(cur_time)
            if UNIXTime >= outputTime:

                bank.add_bank_money(750)
                await ctx.send(embed=Embeds(description=f"{ctx.author.mention}, 750 Kudos has been added to you bank account."))
                self.oldConfig.set_user(
                    str(ctx.author.id), "payday", calendar.timegm(cur_time))

            else:
                remainingUNIX = outputTime - UNIXTime

                error = self.exceptions.CommandOnCooldown(remainingUNIX)
                raise error

        except self.exceptions.CommandOnCooldown as error:
            timing = time.gmtime(error.remaining)
            h = timing.tm_hour
            m = timing.tm_min
            s = timing.tm_sec

            embed = Embeds(
                title="Command on cooldown",
                colour=ctx.author.color
            )

            fields = [
                ("Hours remaining", h), ("Minutes remaining",
                                         m), ("Seconds remaining", s)
            ]

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/819496847990063114/829872480545013790/Timer-595b40b65ba036ed117d45fc.png")

            await ctx.send(embed=embed)"""

        
        bank.add_bank_money(ctx.guild.id, 750)
        await ctx.send(embed=Embeds(description=f"{ctx.author.mention}, 750 Kudos has been added to you bank account."))

    @command()
    async def beg(self, ctx):
        guildid = ctx.guild.id
        userid = ctx.author.id
        bank = b(self.client, guildid, userid)

        """timeout = self.oldConfig.timeout(ctx.guild.id, "beg")
        cur_time = ctx.message.created_at.utctimetuple()
        try:
            timedata = self.oldConfig.user(str(ctx.author.id))['beg']

            outputTime = int(timedata) + int(timeout)
            UNIXTime = calendar.timegm(cur_time)
            if UNIXTime >= outputTime:
                rand = 1
                if rand == 1:
                    amount = random.randint(1, 360)
                    bank.add_wallet_money(amount)

                    await ctx.send(embed=Embeds(description=f"{ctx.author.mention}, you got very lucky this time and have been given {amount} in Kudos"))

                elif rand == 2:
                    amount = random.randint(1, 360)
                    bank.remove_wallet_money(amount)

                    await ctx.send(embed=Embeds(description=f"{ctx.author.mention}, unlucky! Some guy just stole {amount} Kudos from you."))

                else:
                    await ctx.send(embed=Embeds(description="No one seems to be interested, try again later."))

                self.oldConfig.set_user(
                    str(ctx.author.id), "beg", calendar.timegm(cur_time))

            else:
                remainingUNIX = outputTime - UNIXTime

                error = self.exceptions.CommandOnCooldown(remainingUNIX)
                raise error

        except self.exceptions.CommandOnCooldown as error:
            timing = time.gmtime(error.remaining)
            h = timing.tm_hour
            m = timing.tm_min
            s = timing.tm_sec

            embed = Embeds(
                title="Command on cooldown",
                colour=ctx.author.color
            )

            fields = [
                ("Hours remaining", h), ("Minutes remaining",
                                         m), ("Seconds remaining", s)
            ]

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=True)

            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/819496847990063114/829872480545013790/Timer-595b40b65ba036ed117d45fc.png")

            await ctx.send(embed=embed)

        except:"""
        rand = random.randint(0, 2)
        if rand == 1:
            amount = random.randint(1, 360)
            bank.add_wallet_money(ctx.guild.id, amount)

            await ctx.send(embed=Embeds(description=f"{ctx.author.mention}, you got very lucky this time and have been given {amount} in Kudos"))

        elif rand == 2:
            amount = random.randint(1, 360)
            try:
                bank.remove_wallet_money(ctx.guild.id, amount)

                await ctx.send(embed=Embeds(description=f"{ctx.author.mention}, unlucky! Some guy just stole {amount} Kudos from you."))

            except:
                await ctx.send(embed=Embeds(description=f"{ctx.author.mention}, unlucky! Some guy just tried to rob from you. But you don't have any money"))

        else:
            await ctx.send(embed=Embeds(description="No one seems to be interested, try again later."))
            """
            self.oldConfig.set_user(
                str(ctx.author.id), "beg", calendar.timegm(cur_time))
"""
    @command()
    async def gamble(self, ctx):
        pass

    #@command()
    async def leaderboard(self, ctx, x=5):
        users = {}

        for user in self.client.users_:
            users[str(user)] = int(self.oldConfig.USERS.get(str(user))[
                "bank"]) + int(self.oldConfig.USERS.get(str(user))["wallet"])

        users = {k: v for k, v in sorted(
            users.items(), key=lambda item: item[1], reverse=True)}

        embed = Embed(
            title="***Leaderboard***",
            description="Both bank and wallets have been added together",
            colour=ctx.author.color
        )

        fields = []
        for user in users:
            fields.append(
                (f"{self.client.get_user(int(user))}:", users.get(user)))

        if x == 1:
            field = [fields[0]]

        else:
            field = fields[0:x-1]

        for name, value in field:
            embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text=self.client.embedAuthorName,
                         icon_url=self.client.embedAuthorUrl)

        await ctx.send(embed=embed)
        
