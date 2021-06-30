from lib.cogs.help.help import DEFAULTS
import discord
from discord.embeds import Embed
from discord.ext.commands import command, Cog, has_permissions
from dpymenus import PaginatedMenu

import asyncio
from datetime import datetime

import validators
from time import sleep

from lib.bot import bot

from .settings import Settings
from .roles import Roles
from .react import React

def get_action_channel(self, guildID):
    config = bot.config

    for guild in config.guilds:
        if guild["guildID"] == guildID:
            try:
                channel = self.client.get_channel(int(guild["actionChannel"]))
                return channel
            except:
                return None

def getEmbed(guildid : int, embedname : str):
    config = bot.oldConfig
    return config.embed(str(guildid), embedname)

class Mod(
    Settings,
    Roles,
    React,
    Cog):

    def __init__(self, client):
        self.client = client

    @command()
    @has_permissions(manage_guild=True)
    async def botspam(self, ctx):
        await ctx.message.delete()
        await ctx.send("""*Anime*
```
!waifus - random waifu image
!husbandos - random husbando image
!image anime - random anime image
!image wallpaper - random anime wallpaper image
!image azurlane - random azurlane image
!image nekopara - random nekopara image
!slap @user - slap a user
!hug @user - hug a user
!pat @user - pat a user
```
*Economy*
```
!beg - get some money from generous people
!payday - that daily dose of money
!balance - see your balance in your wallet and bank account
!leaderboard {amount to display} - who is winning the competition
```
 *Games*
```
!rps {r/p/s} - play a game of rock, paper, scissors
!dice {amount} - role the amount of dices you want, max 5 
!8ball {question} - ask the 8 ball a question
!cf {h/t} - which side will the coin land on, head (h) or tails (t)
```
        """)

    @command()
    @has_permissions(manage_permissions=True)
    async def clear(self, ctx, amount = 5):
        """
            Clears a set of messages.
        """
        amount += 1
        cleared = amount + 1
        i = 1
        while i != cleared:
            await ctx.channel.purge(limit=1)
            sleep(1)
            amount == amount -1
            i += 1
        await ctx.send("Clearing is done!!")
        sleep(1)
        await ctx.channel.purge(limit=1)

    @command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        """
            Kicks a user
        """

        mtoprole = member.top_role.position
        ctxtoprole = ctx.author.top_role.position

        guildowner = ctx.guild.owner.id

        if member.id != ctx.author.id and mtoprole < ctxtoprole and member.id != guildowner:

            userurl = member.avatar_url
            
            kicked = Embed(
                title = f'{member.name}#{member.discriminator} ({member.id}) has been kicked',
                description = (f'Reason: {reason}'),
                colour = getEmbed(ctx.guild.id, "mod_kick"),
                timestamp = datetime.utcnow()
            )

            kicked.set_thumbnail(url=userurl)

            await member.send(f'You have been kick from {ctx.guild.name}.\nReason: {reason}')

            await member.kick(reason = reason)
            
            try:
                channel = get_action_channel(self, ctx.guild.id)
                await channel.send(embed=kicked)
                await ctx.send("Done!")

            except:
                print(f"No action channel has been set for {ctx.guild.id}")
                await ctx.send(f"{member.name} has been kicked.")
        
    @command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        """
            Bans a user using either a ID or a full username
        """

        mtoprole = member.top_role.position
        ctxtoprole = ctx.author.top_role.position

        guildowner = ctx.guild.owner.id

        if member.id != ctx.author.id and mtoprole < ctxtoprole and member.id != guildowner:

            await member.send(f'You have been banned from {ctx.guild.name}.\nReason: {reason}')   

            banned = discord.Embed(
                title = f'<@{member.id}> has been banned',
                description = f'Reason: {reason}',
                colour = getEmbed(ctx.guild.id, "mod_ban"),
                timestamp = datetime.utcnow()
            )
            try:
                channel = get_action_channel(self, ctx.guild.id)
                await channel.send(embed=banned)

            except:
                print(f"No action channel has been set for {ctx.guild.id}")
                await ctx.send(f"<@{member.id}>, has been banned")

            await member.ban(reason = reason)

    @command()
    @has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        """Unbans the user.
            
            Uses the full username and discriminator, like 'Sol_Tester#7014'
        """

        banned_users = await ctx.guild.bans()

        try:
            member_name, member_discriminator = member.split('#')
        except:pass

        for ban_entry in banned_users:
            user = ban_entry.user
            try:
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)

                    print(f'{user.id}, @{user.name}#{user.discriminator} has been unbanned')
                    
                    unbanned = discord.Embed(
                        title = f'{user.mention} has been unbanned',
                        description = 'WIP',
                        colour = getEmbed(ctx.guild.id, "mod_unban"),
                        timestamp = datetime.utcnow()
                        )
                    try:
                        channel = get_action_channel(self, ctx.guild.id)
                        await channel.send(embed=unbanned)

                    except:
                        print(f"No action channel has been set for {ctx.guild.id}")
                        await ctx.send(f"<@{user.id}>, has been unbanned")
            
            except:
                if user.id == member:
                    await ctx.guild.unban(user)

                    print(f'{user.id}, @{user.name}#{user.discriminator} has been unbanned')
                    
                    unbanned = discord.Embed(
                        title = f'{user.mention} has been unbanned',
                        colour = getEmbed(ctx.guild.id, "mod_unban"),
                        timestamp = datetime.utcnow()
                        )
                    try:
                        channel = get_action_channel(self, ctx.guild.id)
                        await channel.send(embed=unbanned)

                    except:
                        print(f"No action channel has been set for {ctx.guild.id}")
                        await ctx.send(f"<@{user.id}>, has been unbanned")

    @command()
    @has_permissions(manage_messages=True)
    async def avatar(self, ctx, member : discord.Member):
        """
            Sends a bigger picture of the users avatar.
        """

        avatarURL = member.avatar_url

        embed = Embed(
            title = f"{member.name}#{member.discriminator}'s avatar",
            colour = getEmbed(ctx.guild.id, "mod_avatar"),
            timestamp = datetime.utcnow()
        )

        embed.set_image(url=avatarURL)

        await ctx.send(embed=embed)

    @command(name="warning")
    @has_permissions(manage_messages=True)
    async def _warning(self, ctx, user : discord.Member, *, reason = None):
        """Warn a user

        Augs:
        user : @<userID> or user id to send them a dm warning.
        reason : the reason for the warning.
        """
        embed = Embed(
            title = f"Warning from {ctx.guild.name}",
            description = f"Reason:\n{reason}",
            timestamp = datetime.utcnow()
        )

        await user.send(embed=embed)
        await ctx.send(f"{user.mention} has been warned")
    

    @command()
    @has_permissions(manage_guild=True)
    async def embed(self, ctx):
        """
            Sends an embeded message to a channel.
        """
        await ctx.send("Please enter your title now:")

        try:
            while True:
                msg = await self.client.wait_for('message', timeout=90)
                if msg.guild.id == ctx.guild.id and msg.channel.id == ctx.channel.id and msg.author.id == ctx.author.id:
                    title = msg.content
                    break
        except asyncio.TimeoutError:
            await ctx.send("Timed out. Try again doing the command again.")
            return

        await ctx.send("Please enter your description below:")

        try:
            while True:
                msg = await self.client.wait_for('message', timeout=90)
                if msg.guild.id == ctx.guild.id and msg.channel.id == ctx.channel.id and msg.author.id == ctx.author.id:
                    description = msg.content
                    break
        except asyncio.TimeoutError:
            await ctx.send("Timed out. Try again doing the command again.")
            return

        await ctx.send("Please enter the channel you would like below: #example-channel or you can use the channel ID")

        try:
            while True:
                msg = await self.client.wait_for('message', timeout=90)
                if msg.guild.id == ctx.guild.id and msg.channel.id == ctx.channel.id and msg.author.id == ctx.author.id:
                    channel = msg.content

                    for char in channel:
                        if char in "<#>":
                            channel = channel.replace(char,'')
                    try:
                        channel = self.client.get_channel(int(channel))
                        break
                    except:
                        await ctx.send("Invalid Channel, try again.")

        except asyncio.TimeoutError:
            await ctx.send("Timed out. Try again doing the command again.")
            return

        await ctx.send("Please enter the colour of your message below: \n(Use https://www.google.com/search?q=color+picker and then copy the hex code into here. So purple would be #4c00ff)")

        try:
            while True:
                msg = await self.client.wait_for('message', timeout=90)
                if msg.guild.id == ctx.guild.id and msg.channel.id == ctx.channel.id and msg.author.id == ctx.author.id:
                    colour = msg.content

                    for char in colour:
                        if char in "#":
                            colour = colour.replace(char,'')

                    colour = int(colour, 16)
                    break

        except asyncio.TimeoutError:
            await ctx.send("Timed out. Try again doing the command again.")
            return

        await ctx.send("If you would like a picture then put a link to the image below, use imgur if the image is on your computer. If you don't want one put 'no'.\n Images can be png or jpg.")

        try:
            while True:
                msg = await self.client.wait_for('message', timeout=90)
                if msg.guild.id == ctx.guild.id and msg.channel.id == ctx.channel.id and msg.author.id == ctx.author.id:
                    imageurl = msg.content

                    VALID_IMAGE_EXTENTSIONS = [
                        ".jpg",
                        ".jpeg",
                        ".png",
                        ".gif"
                    ]
                    def extention(imageurl):
                        for extentions in VALID_IMAGE_EXTENTSIONS:
                            if imageurl.endswith(extentions):
                                return True
                        return False

                    if imageurl.lower() == 'no':
                        break

                    if validators.url(imageurl) and extention(imageurl):
                        break

                    else:
                        await ctx.send("Invalid image url")

        except asyncio.TimeoutError:
            await ctx.send("Timed out. Try again doing the command again.")
            return

        await ctx.send("If you would like a thumbnail then put a link to the image below, use imgur if the image is on your computer. If you don't want one put 'no'.\n Images can be png or jpg.")

        try:
            while True:
                msg = await self.client.wait_for('message', timeout=90)
                if msg.guild.id == ctx.guild.id and msg.channel.id == ctx.channel.id and msg.author.id == ctx.author.id:
                    thumbnailurl = msg.content

                    VALID_IMAGE_EXTENTSIONS = [
                        ".jpg",
                        ".jpeg",
                        ".png",
                        ".gif"
                    ]
                    def extention(thumbnailurl):
                        for extentions in VALID_IMAGE_EXTENTSIONS:
                            if thumbnailurl.endswith(extentions):
                                return True
                        return False

                    if thumbnailurl.lower() == 'no':
                        break

                    if validators.url(thumbnailurl) and extention(thumbnailurl):
                        break

                    else:
                        await ctx.send("Invalid image url")

        except asyncio.TimeoutError:
            await ctx.send("Timed out. Try again doing the command again.")
            return

        embed = discord.Embed(
            title = title,
            description = description,
            colour = colour

        )

        if imageurl != 'no':
            embed.set_image(url=imageurl)

        if thumbnailurl != 'no':
            embed.set_thumbnail(url= thumbnailurl)

        await channel.send(embed=embed)
   
    @command()
    @has_permissions(manage_guild=True)
    async def announce(self, ctx):
        """ 
            Creates a message with a phantom @everyone before hand.
        """

        await ctx.send("Enter the title for your announcement below:")

        try:
            while True:
                msgM = await self.client.wait_for('message', timeout=90)
                if msgM.guild.id == ctx.guild.id and msgM.channel.id == ctx.channel.id and msgM.author.id == ctx.author.id:
                    msg = msgM.content
                    break

        except asyncio.TimeoutError:
            await ctx.send("Timed out. Try again")
            return

        await ctx.send("Enter the channel for your announcement")

        try:
            while True:
                msgM = await self.client.wait_for('message', timeout=90)
                if msgM.guild.id == ctx.guild.id and msgM.channel.id == ctx.channel.id and msgM.author.id == ctx.author.id:
                    channel = msgM.content

                    for char in channel:
                        if char in "<#>":
                            channel = channel.replace(char,'')
                    try:
                        Channel = self.client.get_channel(int(channel))
                        break
                    except:
                        await ctx.send("Invalid Channel, try again.")

        except asyncio.TimeoutError:
            await ctx.send("Timed out. Try again")
            return

        await Channel.send(f"@everyone \n{msg}")

    @command()
    @has_permissions(manage_guild=True)
    async def msgsend(self, ctx):
        """
            Sending a basic message using Sancus
        """

        await ctx.send("Enter your message below:")

        try:
            while True:
                msgM = await self.client.wait_for('message', timeout=90)
                if msgM.guild.id == ctx.guild.id and msgM.channel.id == ctx.channel.id and msgM.author.id == ctx.author.id:
                    msg = msgM.content
                    break

        except asyncio.TimeoutError:
            await ctx.send("Timed out. Try again")
            return

        await ctx.send("Enter the channel ID/name below:")

        try:
            while True:
                msgM = await self.client.wait_for('message', timeout=90)
                if msgM.guild.id == ctx.guild.id and msgM.channel.id == ctx.channel.id and msgM.author.id == ctx.author.id:
                    channel = msgM.content
                    try:
                        Channel = self.client.get_channel(int(channel))
                        break
                    except:
                        await ctx.send("Invalid Channel, try again.")

        except asyncio.TimeoutError:
            await ctx.send("Timed out. Try again")
            return

        await Channel.send(f"{msg}")


