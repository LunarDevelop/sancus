from discord.ext.commands.core import has_permissions
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
    @has_permissions(manage_roles=True)
    async def give(self, ctx : Context, user : Member, *, roles : str):
        """This command will give server admins access to give roles to users
        by simply tagging the user and then the roles that you want them to have.

        You can tag a user who's not in the channel by doing the follow:
        `<@userID>` and replacing userID with their id number

        And you can tag a role using `<@&roleID>` if you are unable to tag the role normally
        Don't worry if a user already has one of the roles they will be skipped by the system
        """
        roles = roles.split(" ")
        roleList = ""

        for role in roles:
            role = role.replace("<@&", " ").replace(">", " ")

            role = ctx.guild.get_role(int(role))
            await user.add_roles(role)
            roleList += role.name +", "
        return await ctx.send(f"{user.mention} has been given the following roles: {roleList}")