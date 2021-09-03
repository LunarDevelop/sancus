from asyncio.tasks import sleep
import sys
from discord import Embed
from discord.ext import commands

from lib.bot import bot


class Errors(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            embed = Embed(
                title=f"{str(ctx.command.name).capitalize()} | Help",
                description=f"__**Please pass all required arguments**__\n{ctx.command.callback.__doc__}",
                color=ctx.author.colour
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandNotFound):
            pass

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send('This command has been disabled. Contact server adminastator if you believe this to be an error.')

        elif isinstance(error, commands.TooManyArguments):
            embed = Embed(
                title=f"{str(ctx.command.name).capitalize()} | Help",
                description=f"__**You have given too many arguments for this command**__\n{ctx.command.callback.__doc__}",
                color=ctx.author.colour
            )
            await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandOnCooldown):

            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)

            s = int(s)
            m = int(m)
            h = int(h)

            if h != 0:
                await ctx.send(f'This command has a cooldown, please wait another `{h}` hour/s, `{m}` minute/s and `{s}` second/s before trying again.')

            elif m > 0:
                await ctx.send(f'This command has a cooldown, please wait another `{m}` minutes and `{s}` second/s before trying again.')

            elif m == 0:
                await ctx.send(f'This command has a cooldown, please wait another `{s}` seconds before trying again.')

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('You do not have the permissions to use this command')

        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.send("This command requires an NSFW channel to be able to run")
