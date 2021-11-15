from discord.member import Member
from discord.ext.commands import Cog, command
from discord.role import Role
from sancus.lib.bot import Bot
from discord.ext.commands.context import Context


class userCmds(Cog):

    def __init__(self, client) -> None:
        super().__init__()
        self.client : Bot = client

    @command()
    async def give(self, ctx : Context, user : Member, *, role : Role=""):
        """This command will give server admins access to give users roles
        by simply tagging the user and then the role.

        You can tag a user who's not in the channel by doing the follow:
        `<@userID>` and replacing userID with their id number

        And you can tag a role using `<@&roleID>` if you are unable to tag the role normally
        """

        if role in user.roles:
            return await ctx.send("User already has that role.")

        await user.add_roles(role)
        return await ctx.send(f"{user.mention} has been given the {role.mention} role")