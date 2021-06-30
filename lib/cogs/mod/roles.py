import discord
import asyncio
from discord.embeds import Embed
from discord.ext.commands import has_permissions, command, Cog
import random


class Roles(Cog):

    PERMISSION_LIST = [
            "add_reactions",
            "administrator",
            "attach_files",
            "ban_members",
            "change_nickname",
            "connect",
            "create_instant_invite",
            "deafen_members",
            "embed_links",
            "external_emojis",
            "kick_members",
            "manage_channels",
            "manage_emojis",
            "manage_guild",
            "manage_messages",
            "manage_nicknames",
            "manage_permissions",
            "manage_roles",
            "manage_webhooks",
            "mention_everyone",
            "move_members",
            "mute_members",
            "priority_speaker",
            "read_message_history",
            "read_messages",
            "send_messages",
            "send_tts_messages",
            "speak",
            "stream",
            "use_external_emojis",
            "use_voice_activation",
            "value",
            "view_audit_log",
            "view_channel",
            "view_guild_insights",
            "Methods"
        ]

    async def __init__(self, client):
        self.client = client
        print("ROLES")

    @command()
    @has_permissions(manage_roles=True) 
    async def roles(self, ctx):
        await ctx.send("WIP feature. Coming soon.")

        
    @command()
    @has_permissions(manage_roles=True) 
    async def editroles(self, ctx):
        await ctx.send("WIP feature. Coming soon.")

        embed = discord.Embed(
            title = 'Create roles',
            description = "This is a series of menus that will help you create roles.",
            colour = 0xedbae5 
        )

        await ctx.send(embed=embed)

        ROLES = await ctx.guild.fetch_roles()
    
        async def _name(ctx):
            await ctx.send("Please input the name of the role you want to add")

            try:
                while True:
                    msg = await self.client.wait_for('message')
                    if msg.guild.id == ctx.guild.id and msg.channel.id == ctx.channel.id and msg.author.id == ctx.author.id:
                        name = msg.content
                        return name
            
            except: pass

        async def _perms(ctx):
            embed = discord.Embed(
                title = "Permissions",
                colour = 0x000fcba03
            )

            embed.add_field(name="List", value= self.PERMISSION_LIST, inline=False)

            await ctx.send(embed=embed)

            await ctx.send("Please list the permission that you would like the role to have. Separate them by putting ` , ` in between.")

            try:
                while True:
                    msg = await self.client.wait_for('message')
                    if msg.guild.id == ctx.guild.id and msg.channel.id == ctx.channel.id and msg.author.id == ctx.author.id:
                        perms = msg.content
                        perms = perms.split(" , ")

                        return perms
            
            except: pass


        async def _colour(ctx):
            await ctx.send("Please input a colour for you role. \n Use https://www.google.com/search?q=color+picker to choose your colour then copy the hex code into this channel.")

            try:
                while True:
                    msg = await self.client.wait_for('message')
                    if msg.guild.id == ctx.guild.id and msg.channel.id == ctx.channel.id and msg.author.id == ctx.author.id:
                        colour = msg.content

                        for char in colour:
                            if char in "#":
                                colour = colour.replace(char,'')

                        color = int(colour, 16)
                        return color
            
            except: pass

        async def _mentionable(ctx):
            await ctx.send("Do you want to allow this role to be mentionable. `yes` or `no`")

            try:
                while True:
                    msg = await self.client.wait_for('message')
                    if msg.guild.id == ctx.guild.id and msg.channel.id == ctx.channel.id and msg.author.id == ctx.author.id:
                        mentionable = msg.content

                        if mentionable.lower() == 'yes':
                            mentionable = True
                            return mentionable

                        else: 
                            mentionable = False  
                            return mentionable 
            
            except: pass

        async def _hoist(ctx):
            await ctx.send("Do you want to allow this role to be displayed seperately on the members list. `yes` or `no`")

            try:
                while True:
                    msg = await self.client.wait_for('message')
                    if msg.guild.id == ctx.guild.id and msg.channel.id == ctx.channel.id and msg.author.id == ctx.author.id:
                        mentionable = msg.content

                        if mentionable.lower() == 'yes':
                            mentionable = True
                            return mentionable

                        else: 
                            mentionable = False  
                            return mentionable 
            
            except: pass
        
        async def _position(ctx):
            await ctx.send("What place do you want to have this role appear in the heirachy for your roles?\nFrom the list below chose the position that you would like this role to be.")

            rolenames = ''
            print(ROLES, "\n")
            count = 2

            for roles in ROLES:
                print(roles, "\n")
                print(rolenames, "\n")
                if roles.name != "@everyone":
                    if rolenames == '':
                        rolenames = f"1) {roles.name}\n"
                    
                    else:
                        rolenames +=  f"{count}) {roles.name}\n"
                        count += 1

            await ctx.send(rolenames)

            try:
                while True:
                    msg = await self.client.wait_for('message')
                    if msg.guild.id == ctx.guild.id and msg.channel.id == ctx.channel.id and msg.author.id == ctx.author.id:
                        position = msg.content
                        return position
            
            except: pass

        async def _reason(ctx):
            await ctx.send("Please input the reason you want to add this role, this is to display on the audit log. If you do not want a reason then type `None`.")

            try:
                while True:
                    msg = await self.client.wait_for('message')
                    if msg.guild.id == ctx.guild.id and msg.channel.id == ctx.channel.id and msg.author.id == ctx.author.id:
                        reason = msg.content

                        if reason.lower() == "none":
                            return None
                        else: return reason
            
            except: pass

        name = await _name(ctx)
        #perms = await _perms(ctx)
        colour = await _colour(ctx)
        mentionable = await _mentionable(ctx)
        hoist = await _hoist(ctx)
        position = await _position(ctx)
        reason = await _reason(ctx)

        await ctx.guild.create_role(name=name, colour=colour, mentionable=mentionable, hoist=hoist, reason=reason)

        positions = {
            name : position
        }

        await ctx.guild.edit_role_positions(position=positions)
