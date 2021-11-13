
import discord
from discord.embeds import Embed
from discord.ext.commands import command, Cog, Context, has_permissions

from datetime import datetime

from lib.bot import bot

from .settings import Settings
from .moderation import antispam

from functions.objects import Embeds, warningObject


class Mod(
    Settings,
    antispam,
        Cog):

    def __init__(self, client):
        self.client :bot = client

    # Clear command
    @command()
    @has_permissions(manage_permissions=True)
    async def clear(self, ctx, amount=5):
        """Clears a set of using the amount to say how many will be removed

        Args:

        Amount: The amount of messages to remove"""

        await ctx.channel.purge(limit=amount, bulk=True)
        await ctx.send("Clearing is done!!", delete_after=1)

    # Kick User
    @command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a user from your server, this means they can rejoin your server if they wish.

        Args:

        Member: Tag or use the id number of the person you want to kick
        Reason: (Optional) Why are you kicking them.
        """

        # Gets the members top role and the person who executed the commands top role
        mTopRole = member.top_role.position
        ctxTopRole = ctx.author.top_role.position

        guildowner = ctx.guild.owner.id

        # checks if the user can ban the member
        if member.id != ctx.author.id and mTopRole < ctxTopRole and member.id != guildowner:

            userurl = member.display_avatar.url

            kicked = Embed(
                title=f'{member.name}#{member.discriminator} ({member.id}) has been kicked',
                description=(f'Reason: {reason}'),
                timestamp=datetime.utcnow()
            )

            kicked.set_thumbnail(url=userurl)

            kicked.set_footer(text=self.client.embedAuthorName,
                              icon_url=self.client.embedAuthorUrl)

            # Tries to message the member to tell them why they have been kicked but if it fails then ignore
            try:
                await member.send(f'You have been kick from {ctx.guild.name}.\nReason: {reason}')
            except:
                pass

            await member.kick(reason=reason)

            # Logging the kick
            try:
                channel = self.client.get_action_channel(ctx.guild.id)
                await channel.send(embed=kicked)
                await ctx.send("Done!")

            except:
                print(f"No action channel has been set for {ctx.guild.id}")
                await ctx.send(f"{member.name} has been kicked.")

        # Tells user if they can't kick the person
        else:
            await ctx.send("You cannot kick that person, you are below them on the role chain.")

    # Ban User
    @command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason was provided"):
        """Bans a user using either a ID or a full username

        Args:

        Member: Tag or use the id number of the person you want to ban
        Reason: (Optional) Why are you banning them.
        """
        try:
            member = await ctx.guild.fetch_member(int(member))
        except:
            pass

        botUser = await ctx.guild.fetch_member(self.client.user.id)
        mTopRole = member.top_role.position
        ctxTopRole = ctx.author.top_role.position
        bTopRole = botUser.top_role.position

        guildowner = ctx.guild.owner.id

        memberchannel = None

        if member.id != ctx.author.id and mTopRole < ctxTopRole and member.id != guildowner and mTopRole < bTopRole:

            banned = discord.Embed(
                title=f'{member.name} has been banned',
                description=f'Reason: {reason}',
                timestamp=datetime.utcnow()
            )

            banned.set_footer(text=self.client.embedAuthorName,
                              icon_url=self.client.embedAuthorUrl)

            try:
                try:
                    memberchannel = await member.create_dm()
                except:
                    pass

                await member.ban(reason=reason)
                if memberchannel != None:
                    await memberchannel.send(f'You have been banned from {ctx.guild.name}.\nReason: {reason}')
                await ctx.send(f"<@{member.id}>, has been banned")

            except:
                await ctx.send("There has been and error with the command!\nEnsure that the person you are trying to ban does not have a role above the bot, and try again.")
                return False

            try:
                channel = await self.client.getActionChannel(ctx.guild.id)
                await channel.send(embed=banned)

            except:
                pass
            return True

        else:
            await ctx.send("You cannot ban this user!")
            return False

    # Unban User
    @command()
    @has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        """Unbans the user.

        Uses the full username and discriminator, like 'Sol_Tester#7014'
        **You cannot tag the user as they are not in your server, you will need to find username and discriminator out**

        Args:

        Member: id number of the person you want to unban
        """
        check = False
        member_name = "None"
        member_discriminator = "None"
        member_id = "None"

        banned_users = await ctx.guild.bans()

        try:
            member_name, member_discriminator = member.split('#')
        except:
            pass

        try:
            member_id = int(member)
        except:
            pass

        for ban_entry in banned_users:
            user = ban_entry.user

            unbanned = discord.Embed(
                title=f'{user.name} has been unbanned',
                timestamp=datetime.utcnow()
            )

            unbanned.set_footer(text=self.client.embedAuthorName,
                                icon_url=self.client.embedAuthorUrl)

            try:
                if ((user.name, user.discriminator) == (member_name, member_discriminator)) or (user.id == member_id) or (user == member):
                    check == True

                    try:
                        await ctx.guild.unban(user)

                    except:
                        await ctx.send("An error has occured while trying to unban the user.\n*Try again or contact Solar#0404")

                    channel = await self.client.getActionChannel(ctx.guild.id)

                    if channel != None:
                        try:
                            await channel.send(embed=unbanned)
                            await ctx.send(f"{user.mention}, has been unbanned")
                        except:
                            await ctx.send(f"{user.mention}, has been unbanned")

                    else:
                        await ctx.send(f"<@{user.id}>, has been unbanned")

                    return

            except:
                if user.id == member:
                    check == True

                    try:
                        await ctx.guild.unban(user)

                    except:
                        await ctx.send("An error has occured while trying to unban the user.\n*Try again or contact Solar#0404")

                    channel = self.client.get_action_channel(
                        self, ctx.guild.id)

                    if channel != None:
                        await channel.send(embed=unbanned)

                    else:
                        await ctx.send(f"<@{user.id}>, has been unbanned")

                    return

            if check != True:
                await ctx.send("Cannot unban user.\nThey might not be banned or you spelled their name incorrectly.\n*Try again if you want*")

    @command()
    @has_permissions(manage_messages=True)
    async def warn(self, ctx:Context, user: discord.Member, *, reason=None):
        """Warn a user

        Args:

        Member : Tag the member or member id to send them a dm warning.
        Reason : the reason for the warning.
        """
        #Direct Warning
        embed = Embed(
            title=f"Warning from {ctx.guild.name}",
            description=f"Reason:\n{reason}",
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text=self.client.embedAuthorName,
                         icon_url=self.client.embedAuthorUrl)

        await user.send(embed=embed)
        await ctx.send(f"{user.mention} has been warned")

        #Case message
        embed = discord.Embed(
            title=f'{user.name} has been warned',
            description=f'Reason: {reason}',
            timestamp=ctx.message.created_at
        )

        embed.set_footer(text=self.client.embedAuthorName,
                         icon_url=self.client.embedAuthorUrl)

        try:
            channel = await self.client.getCaseChannel(ctx.guild.id)
            await channel.send(embed=embed)

        except:
            pass
        
        #Updating warnings on DB
        warning = warningObject(
            username=user.name,
            id=user.id,
            reason=reason,
            date=ctx.message.created_at.strftime("%d/%m/%y %I:%M:%S%p %Z")
        )
        warnings = self.client.guilds_[str(ctx.guild.id)]["warnings"]
        warnings.append(warning.__dict__)

        self.client.config.put_config_guild(ctx.guild.id, {"warnings":warnings})
    
    @command()
    @has_permissions(manage_messages=True)
    async def warnings(self, ctx :Context):
        """Display all warning messages, 
        TODO this will eventually be able to show warnings between a certain date
        """
        embed = Embeds(
            title="List of warnings issued",
            description="All of the warnings that have been issued on this server"
        )

        for warning in self.client.guilds_[str(ctx.guild.id)]["warnings"]:
            embed.add_field(
                name=f"{warning['username']} Report's",
                value=f"Reason: {warning['reason']}\nDate and time: {warning['date']}"
            )

        await ctx.send(embed=embed)

    # Show Avatar of a Player
    @command()
    @has_permissions(manage_messages=True)
    async def avatar(self, ctx, member: discord.Member):
        """Sends a bigger picture of the users avatar.

        Args:

        Member : The member you would like to see the avartar of
        """

        avatarURL = member.display_avatar.url

        embed = Embed(
            title=f"{member.name}#{member.discriminator}'s avatar",
            colour=member.colour,
            timestamp=datetime.utcnow()
        )

        embed.set_image(url=avatarURL)

        embed.set_footer(text=self.client.embedAuthorName,
                         icon_url=self.client.embedAuthorUrl)

        await ctx.send(embed=embed)
