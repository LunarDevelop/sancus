import discord
from discord.ext import commands
from typing import Optional

import json

from functions.objects import Embeds


class Info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="userinfo", aliases=['ui'], brief="Displays a speific user's info")
    async def user_info(self, ctx, *, User: Optional[discord.Member]):
        user : discord.Member = User or ctx.author

        embed = Embeds(
            title="User Info",
            colour=user.colour
        )

        embed.set_thumbnail(url=user.display_avatar.url)

        roleUser = user.roles
        rolesUser = []
        for role in roleUser:
            if role.name == '@everyone':
                pass
            else:
                rolesUser.append(role.name)

        fields = [
            ("Display Name: ", user.display_name, True),
            ("Is Bot: ", user.bot, True),
            ("UserName: ", f"{user.name}#{user.discriminator}", False),
            ("Roles: ", rolesUser, False),
            ("Account Created: ", user.created_at, True),
            ("Joined This Server: ", user.joined_at, True),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command(name="serverinfo", aliases=['si'])
    async def server_info(self, ctx):
        server : discord.Guild = ctx.guild
        embed = Embeds(
            title="Server Info",
            colour=0x6666FF
        )

        fields = [
            ("Server Name: ", server.name, True),
            ("Server ID: ", server.id, True),
            ("Total Members: ", server.member_count, True),
            ("AFK Channel: ", server.afk_channel, True),
            ("AFK Timeout: ", server.afk_timeout, True),
            
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        try:
            embed.set_thumbnail(url=server.icon.url)
        except:
            pass

        await ctx.send(embed=embed)
