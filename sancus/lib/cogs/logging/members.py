from configparser import ConfigParser
import json
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
    async def on_member_join(self, member : discord.Member):
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
        
        #Welcome message
        if self.client.guilds_[str(guild.id)]["welcomeMessage"]:
            try:
                cur_channel :discord.TextChannel = await self.client.fetch_channel(self.client.guilds_[
                    str(guild.id)]["welcomeChannel"])
            except:
                return
            
            cur_bg = self.client.guilds_[
                str(guild.id)]["welcomeBack"]
            cur_banner = self.client.guilds_[
                str(guild.id)]["welcomeBanner"]
            cur_icon = self.client.guilds_[
                str(guild.id)]["welcomeIcon"]
            cur_colour_txt = self.client.guilds_[
                str(guild.id)]["welcomeTxtColor"]
            cur_colour_user = self.client.guilds_[
                str(guild.id)]["welcomeUserColor"]
            cur_colour_members = self.client.guilds_[
                str(guild.id)]["welcomeMembersColor"]
            
            cur_text: str = self.client.guilds_[
                str(guild.id)]["welcomeText"]
            
            if self.client.guilds_[
                str(guild.id)]["welcomeType"]:
                
                api_ini = "sancus/data/api.ini"

                api_data = ConfigParser()
                with open(api_ini) as f:
                    api_data.read_file(f)

                headers = {
                    "Authorization": api_data["FluxPoint"]["api_token"]
                }

                data = {
                    "username": f"{member.name}#{member.discriminator}",
                    "avatar": member.avatar.url,
                    "background": f"#{cur_bg}",
                    "members": f"member #{total_users}",
                    "icon": cur_icon,
                    "banner": cur_banner,
                    "color_welcome": f"#{cur_colour_txt}",
                    "color_username": f"#{cur_colour_user}",
                    "color_members": f"#{cur_colour_members}",
                }
                print(json.dumps(data))

                request = requests.get(
                    "https://api.fluxpoint.dev/gen/welcome", headers=headers, json=data)

                image = io.BytesIO(request.content)
                file = discord.File(image, filename="image.png")

                await cur_channel.send(file=file)
                
            else:
                user = member.name
                server = guild.name

                cur_text = cur_text.format(user=user, server=server)

                await cur_channel.send(cur_text)
        
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

        try:
            await channel.send(embed=userleft)
        except:
            return

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

            try:
                await channel.send(embed=embed)
            except:
                return
