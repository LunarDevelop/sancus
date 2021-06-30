import discord
from discord.ext import commands
from typing import Optional

import json

class Info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="userinfo",aliases= ['ui'],brief="Displays a speific user's info")
    async def user_info(self,ctx, *, User : Optional[discord.Member]):
        user = User or ctx.author

        embed = discord.Embed(
            title = "User Info",
            colour = user.colour
            )
        
        embed.set_thumbnail(url=user.avatar_url)

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
            #CURRENTLY BROKEN ("Status: ", user.status, True),
            ("Roles: ", rolesUser, False),
            ("Account Created: ", user.created_at, True),
            ("Joined This Server: ", user.joined_at, True),
            ]
        
        for name, value, inline in fields:
            embed.add_field(name=name,value=value,inline=inline)
        

        await ctx.send(embed=embed)


    @commands.command(name= "serverinfo", aliases=['si'])
    async def server_info(self,ctx):
        server = ctx.guild
        embed = discord.Embed(
            title = "Server Info",
            colour = 0x6666FF
            )
        

        fields = [
            ("Server Name: ", server.name, True),
            ("Server ID: ", server.id, True),
            ("Total Members: ", server.member_count, True)
            ]
        
        for name, value, inline in fields:
            embed.add_field(name=name,value=value,inline=inline)

        embed.set_image(url=server.icon_url)
        

        await ctx.send(embed=embed)

    @commands.command()
    async def botinfo(self, ctx):
        client = self.client

        embed = discord.Embed(
            title = "Bot Info",
            colour = 0x0003503fc
        )

        total_guilds = 0
        total_users = 0
        total_commands_ran = 0
        
        with open("./data/botData.json", "r") as f:
            command_data = json.load(f)
            
        for command in command_data['commands']:
            data = command_data['commands'].get(command)
            total_commands_ran += data['usage']

        for guilds in client.guilds:
            total_guilds += 1

        for users in client.users:
            total_users += 1

        appinfo = await client.application_info()

        fields = [
            ("Bot Name: ", appinfo.name, True),
            ("Bot ID: ", appinfo.id, True),
            ("Bot Owner: ", appinfo.owner.mention, True),
            ("Total Guilds: ", total_guilds, True),
            ("Total Users: ", total_users, True),
            ("Total Commands Ran", total_commands_ran, True)
            ]

        
        for name, value, inline in fields:
            embed.add_field(name=name,value=value,inline=inline)
            
        embed.set_thumbnail(url=client.user.avatar_url)

        await ctx.send(embed=embed)