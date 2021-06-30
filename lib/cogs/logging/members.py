from configparser import ConfigParser
import discord, io, requests
from discord.ext.commands import Cog
from discord import Embed, File
from datetime import datetime

from lib.bot import bot
from functions.exceptions import NoLogChannel

def getLogChannel(self, guildid : int):
    for guild in bot.config.guilds:
        if guild["guildID"] == str(guildid):
            try:
                LogChannel = self.client.get_channel(int(guild["logChannel"]))
        
                return LogChannel
            except:pass

def getEmbed(guildid : int, embedname : str):
    return bot.oldConfig.embed(guildid, embedname)

#make join messages

class Members(Cog):

    def __init__(self, client):
        self.client = client

    #When Player joins message
    @Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild

        total_users = guild.member_count

        userurl = member.avatar_url

        embed = Embed(
            title = f'{member.name}#{member.discriminator} ({member.id}) has joined the guild, {guild.name}',
            description = member.mention,
            colour = getEmbed(member.guild.id, "member_join")
        )

        embed.set_thumbnail(url=userurl)
        embed.timestamp = datetime.utcnow()
        embed.add_field(name="Total Users:", value=total_users,inline=True)

        try:
            channel = getLogChannel(self, guild.id)
            await channel.send(embed=embed)

        except:
            pass
        
        for guild in bot.config.guilds:
            if guild["guildID"] == str(guild.id):
                break

        style = guild["welcomeStyle"]

        if style.lower() == 'default':
            try:
                welcome_channel = self.client.get_channel(int(bot.config.general(member.guild.id, "welcome_channel")))
                await welcome_channel.send(f"Everyone say hello to {member.mention}. \n Pleasure to meet you.")
            
            except:
                pass

        elif style.lower() == 'banner':
            config = ConfigParser()
            with open("./data/config.ini", "r") as f:
                config.read(f)

            headers = {
            "Content-Type" : "application/json",
            "Authorization" : config.get("DEFAULT", "flux_token")
            }

            data = {
                "username" : f"{member.author.name}#{member.author.discriminator}",
                "avatar" : str(member.author.avatar_url),
                "background" : str(bot.config.general(member.guild.id, "welcome_background")),
                "members" : f"Members: {member.guild.member_count}",
                "icon" : str(bot.config.general(member.guild.id, "welcome_icon")),
                "banner" : str(bot.config.general(member.guild.id, "welcome_banner")),
                "color_welcome" : str(bot.config.general(member.guild.id, "welcome_text_color")),
                "color_username" : str(bot.config.general(member.guild.id, "welcome_username_color")),
                "color_members" : str(bot.config.general(member.guild.id, "welcome_members_color")),
            }

            r = requests.get(url="https://api.fluxpoint.dev/gen/welcome", headers=headers, json=data)
            image = io.BytesIO(r.content)

            welcome_channel = self.client.get_channel(int(bot.config.general(member.guild.id, "welcome_channel")))
            await welcome_channel.send(file=File(image, "welcomeImage.png"))

    #When Player leaves message
    @Cog.listener()
    async def on_member_remove(self, member):
        
        guild = member.guild

        channel =  getLogChannel(self, guild.id)
        
        userurl = member.avatar_url

        userleft = Embed(
            title = f'{member.name}#{member.discriminator} ({member.id}) has left the guild, {guild.name}',
            description = f'{member.mention}',
            colour = getEmbed(member.guild.id, "member_leave")
        )

        userleft.set_thumbnail(url=userurl)

        await channel.send(embed=userleft)

    @Cog.listener()
    async def on_member_update(self, before, after):
        channel = getLogChannel(self, before.guild.id)

        if before.nick != after.nick:

            embed = Embed(
                title = f'{before.name} changed their nickname',
                description = f"\n**BEFORE:** {before.nick}\n\n**AFTER:** {after.nick}",
                colour = getEmbed(before.guild.id, "member_update")
            )

            embed.set_thumbnail(url = before.avatar_url)

            await channel.send(embed=embed)