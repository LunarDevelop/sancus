from configparser import ConfigParser
import discord
import io
import requests
from discord.ext.commands import Cog
from discord import Embed, File
from datetime import datetime

from lib.bot import bot
from functions.exceptions import NoLogChannel


class Members(Cog):

    def __init__(self, client):
        self.client = client

    # When Player joins message
    @Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild

        total_users = guild.member_count

        userurl = member.display_avatar.url

        embed = Embed(
            title=f'{member.name}#{member.discriminator} ({member.id}) has joined the guild, {guild.name}',
            description=member.mention,
            colour=0x0000203F9
        )

        embed.set_thumbnail(url=userurl)
        embed.timestamp = datetime.utcnow()
        embed.add_field(name="Total Users:", value=total_users, inline=True)

        embed.set_footer(text=self.client.embedAuthorName,
                         icon_url=self.client.embedAuthorUrl)

        try:
            await (await self.client.getLogChannel(guild.id)).send(embed=embed)

        except:
            pass

    # When Player leaves message
    @Cog.listener()
    async def on_member_remove(self, member):

        guild = member.guild

        channel = await self.client.getLogChannel(guild.id)

        userurl = member.display_avatar.url

        userleft = Embed(
            title=f'{member.name}#{member.discriminator} ({member.id}) has left the guild, {guild.name}',
            description=f'{member.mention}',
            colour=0x000e00101
        )

        userleft.set_thumbnail(url=userurl)

        userleft.set_footer(text=self.client.embedAuthorName,
                            icon_url=self.client.embedAuthorUrl)

        await channel.send(embed=userleft)

    # If nickname changes
    @Cog.listener()
    async def on_member_update(self, before, after):
        channel = await self.client.getLogChannel(before.guild.id)

        if before.nick != after.nick:

            embed = Embed(
                title=f'{before.name} changed their nickname',
                description=f"\n**BEFORE:** {before.nick}\n\n**AFTER:** {after.nick}",
                colour=0x00002ee00
            )

            embed.set_thumbnail(url=before.display_avatar.url)

            embed.set_footer(text=self.client.embedAuthorName,
                             icon_url=self.client.embedAuthorUrl)

            await channel.send(embed=embed)
