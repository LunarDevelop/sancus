from discord.ext.commands import Cog, command, group
from discord import Embed

import emoji, asyncio, json

from lib.bot import bot

class React(Cog):

    def __init__(self, client):
        self.client = client

    @group(name="react")
    async def _react(self, ctx):
        """The group message for all react message settings
        
        Commands:
        menu - all the commands for the react commands"""
        
    @_react.command(name="menu")
    async def _menu(self, ctx):
        embed = Embed(
            title = "Reaction roles settings"
        )

        fields = [
            ("list", "All of your current active reaction messages."),
            ("add", "Sets up a new reaction message"),
            ("remove", "Removes a reaction message")
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        await ctx.send(embed=embed)

    #@_react.command(name="list")
    async def _list(self, ctx):
        try:
            reactList = bot.oldConfig.REACTIONS[str(ctx.guild.id)]

            embed = Embed(
                title="Reaction messages"
            )

            for key in reactList:
                embed.add_field(name=key, value=reactList.get(key), inline=False)

            await ctx.send()

        except KeyError:
            await ctx.send("You do not yet have any reaction messages")

    @_react.command(name="add")
    async def _add(self, ctx):
        """Stage wait for messages
        Name
        message or message id
        reaction id/s
        role id/s
        """

        self.name_check = True
        self.message_check = True
        self.role_check = True

        self.channel = None

        await ctx.message.delete()
        
        #menu section
        
        embed = Embed(
            title="Please wait for reaction to be added....",
            colour = 0x000A1F357
        )

        embedMSG = await ctx.send(embed=embed)

        async def MAIN():
            if self.message_check == False and self.name_check == False and self.role_check == False:
                await END()

            await embedMSG.clear_reactions()

            embed.clear_fields()
            embed.description = None

            await embedMSG.edit(content=None, embed=embed)

            fields =[
                ("❌ | Cancel", "Exit the menu, all progress will be lost", True)            
            ]
            
            if self.name_check:
                await embedMSG.add_reaction(emoji.emojize(":speech_balloon:"))

            if self.message_check:
                await embedMSG.add_reaction("#️⃣")
                await embedMSG.add_reaction("💠")

            if self.role_check:
                await embedMSG.add_reaction("⚡")            

            if self.role_check:
                fields.insert(0, (emoji.emojize(":zap: | Role"), "Choose the role ID and emoji for the reaction.", True))

            if self.message_check:
                fields.insert(0, (emoji.emojize(":diamond_shape_with_a_dot_inside: | Create Message"), "Create a message for your role reaction", True))
                fields.insert(0, (emoji.emojize(":hash: | Message ID"), "Select a previous message or a custom message to become your reaction message", True))  

            if self.name_check:
                fields.insert(0, (emoji.emojize(":speech_balloon: | Name"), "Select the name for your reaction message", True))

            await embedMSG.add_reaction("❌")

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            embed.title = "Add Reaction Message"

            await embedMSG.edit(embed=embed)


            def mainCheck(reaction, user):
                return user == ctx.author and (str(reaction.emoji) in [emoji.emojize(':speech_balloon:'), '#️⃣', '💠', '⚡', '❌']) and reaction.message == embedMSG

            while True:
                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=90, check=mainCheck)
                    await embedMSG.clear_reactions()
                    break
                
                except asyncio.TimeoutError:
                    await embedMSG.clear_reactions()
                    await embedMSG.edit(content=f"{ctx.author.mention} Timed out. Try again doing the command again.", delete_after=10.0, embed=None)
                    return
            

            if str(reaction.emoji) == emoji.emojize(':speech_balloon:'):
                await CREATE()

            elif str(reaction.emoji) == '#️⃣':
                await MESSAGE_ID()

            elif str(reaction.emoji) == '💠':
                await NEW_MESSAGE()

            elif str(reaction.emoji) == '⚡':
                await ROLE_ID()

            elif str(reaction.emoji) == '❌':
                await embedMSG.delete()

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        async def CREATE():
            embed.clear_fields()

            embed.title = "Name Reaction Message"
            embed.description = "What do you want you the reaction message to be called. \n\nThis is purely so you can edit it down the line. \nPeople will not see this name."

            await embedMSG.edit(embed=embed)
            
            while True:
                try:
                    msg = await self.client.wait_for('message', timeout=60, check=check)
                    await embedMSG.clear_reactions()

                    self.name = msg.content
                    await msg.delete()

                    self.name_check = False

                    embed.title = "Please wait for reaction to be added..."

                    await MAIN()
                    break 

                except asyncio.TimeoutError:
                    await embedMSG.clear_reactions()
                    await embedMSG.edit(content=f"{ctx.author.mention} Timed out. Try again doing the command again.", delete_after=10.0, embed=None)
                    return 

        async def MESSAGE_ID():
            embed.clear_fields()

            embed.title = "Message ID"
            embed.description = "What channel id is your premade message in?"

            await embedMSG.edit(embed=embed)
            
            while True:
                try:
                    msg = await self.client.wait_for('message', timeout=60, check=check)
                    await embedMSG.clear_reactions()

                    try:
                        self.channel_id = int(msg.content)
                        await msg.delete()

                        channel = self.client.get_channel(self.channel_id)

                        if channel != None:
                            while True:
                                try:
                                    embed.description = "What is the message ID of the premade reaction message."
                                    await embedMSG.edit(embed=embed)

                                    msg = await self.client.wait_for('message', timeout=60, check=check)

                                    self.message = int(msg.content)
                                    await msg.delete()
                                    break

                                except ValueError:
                                    await msg.delete()

                                    embed.description =  "What is the message ID of the premade reaction message.\n\n **Make sure it is an id number**"
                                    await embedMSG.edit(embed=embed)
                                
                                except asyncio.TimeoutError:
                                    await embedMSG.clear_reactions()
                                    await embedMSG.edit(content=f"{ctx.author.mention} Timed out. Try again doing the command again.", delete_after=10.0, embed=None)
                                    return 

                            self.message_check= False

                            embed.title = "Please wait for reaction to be added..."

                            await MAIN()
                            break 

                        else:
                            embed.description =  "What channel would you like the message in? Use the channel id.\n\n **Make sure it is an valid channel id**"
                            await embedMSG.edit(embed=embed)


                    except ValueError: 
                        await msg.delete()

                        embed.description =  "What channel is your premade message in?? Use the channel id.\n\n **Make sure it is an id number**"
                        await embedMSG.edit(embed=embed)

                except asyncio.TimeoutError:
                    await embedMSG.clear_reactions()
                    await embedMSG.edit(content=f"{ctx.author.mention} Timed out. Try again doing the command again.", delete_after=10.0, embed=None)
                    return 

        async def NEW_MESSAGE():
            embed.clear_fields()

            embed.title = "Message ID"
            embed.description = "What is your message?"

            await embedMSG.edit(embed=embed)
            
            while True:
                try:
                    msg = await self.client.wait_for('message', timeout=120, check=check)
                    await embedMSG.clear_reactions()

                    self.message_content = msg.content
                    await msg.delete()

                    embed.description = "What channel would you like the message in? Use the channel id."

                    await embedMSG.edit(embed=embed)

                    while True:
                        try:
                            msg = await self.client.wait_for('message', timeout=120, check=check)
                            await embedMSG.clear_reactions()

                            self.channel = int(msg.content)

                            channel = self.client.get_channel(self.channel)

                            await msg.delete()

                            if channel != None:

                                break

                            else:
                                embed.description =  "What channel would you like the message in? Use the channel id.\n\n **Make sure it is an valid channel id**"
                                await embedMSG.edit(embed=embed)

                        except ValueError: 
                            await msg.delete()

                            embed.description =  "What channel would you like the message in? Use the channel id.\n\n **Make sure it is an id number**"
                            await embedMSG.edit(embed=embed)
                        
                        except asyncio.TimeoutError:
                            await embedMSG.clear_reactions()
                            await embedMSG.edit(content=f"{ctx.author.mention} Timed out. Try again doing the command again.", delete_after=10.0, embed=None)
                            return 

                    self.message_check = False

                    embed.title = "Please wait for reaction to be added..."

                    await MAIN()
                    break

                except asyncio.TimeoutError:
                    await embedMSG.clear_reactions()
                    await embedMSG.edit(content=f"{ctx.author.mention} Timed out. Try again doing the command again.", delete_after=10.0, embed=None)
                    return 

        async def ROLE_ID():
            "Add ❌ for finishing all of the roles"
            
            embed.clear_fields()
            
            roles = ctx.guild.roles
            roles.reverse()
            self.roleList = {}

            for role in roles:
                if role.name != "@everyone":
                    embed.add_field(name=f"Name = {role.name}", value=f"ID = {role.id}", inline=False)

            embed.title = "The Roles and Reaction"
            embed.description = f"The tricky part. \nFor this section you will need id number for the role and the emoji.\n\n**You will need to wait for '❌' to disappear before continuing.**\n\nPlease post the id number then react to your message with the emoji you would like to represent that role.\n\nWhen you are finished use the ❌ reaction"

            await embedMSG.edit(embed=embed)

            await embedMSG.add_reaction("❌")

            while True:
                def cancel_check(reaction, user):
                    return user == ctx.author and reaction.message == embedMSG
                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=3, check=cancel_check)

                    if str(reaction.emoji) == '❌':
                        embed.title = "Please wait for reaction to be added..."
                        if len(self.roleList) != 0:
                            self.role_check = False
                        await MAIN()
                        break

                except:pass

                await embedMSG.clear_reactions()

                while True:
                    msg = await self.client.wait_for('message', check=check)
                    
                    roleid = msg.content
                    
                    def reaction_check(reaction, user):
                        return user == ctx.author and reaction.message == msg

                    while True:
                        reaction, user = await self.client.wait_for('reaction_add', check=reaction_check)
                        
                        try:
                            reaction = str(reaction.emoji.id)
                        
                        except:
                            reaction = str(reaction.emoji)
                        
                        await msg.delete()

                        break
                    break

                self.roleList[roleid] = reaction
                await embedMSG.add_reaction("❌")

        async def END():
            if self.channel != None:
                self.channel = self.client.get_channel(self.channel)
                msg = await self.channel.send(self.message_content)

                self.message = msg.id
                self.channel_id = self.channel.id

            
            channel = self.client.get_channel(self.channel_id)

            with open('./data/reactions.json', 'r') as f:
                file = json.load(f)

            try:
                file[str(ctx.guild.id)][self.name] = {
                    "message_id" : self.message,
                    "roles" : self.roleList
                }

            except KeyError:
                file[str(ctx.guild.id)] = {}
                file[str(ctx.guild.id)][self.name] = {
                    "message_id" : self.message,
                    "roles" : self.roleList
                }

            with open('./data/reactions.json', 'w') as f:
                json.dump(file, f, indent=4)
            
            msg = channel.get_partial_message(self.message)
            for roles in self.roleList:
                try:
                    await msg.add_reaction(await ctx.guild.fetch_emoji(self.roleList.get(roles)))
                except:
                    await msg.add_reaction(self.roleList.get(roles))

            await embedMSG.delete()
            await ctx.send("Your reaction message has been created!")
            return

        await MAIN()



    @_react.command(name="remove")
    async def _remove(self, ctx):
        array = ""
        with open("./data/reactions.json", "r") as f:
            file = json.load(f)

        embed = Embed()

        embed.title = "Current Reaction Messages"

        for name in file[str(ctx.guild.id)]:
            array += f"{name}\n"

        embed.description = f"{array}\n\Which one would you like to remove?"

        embedMSG = await ctx.send(embed=embed)

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        while True:
            try:

                msg = await self.client.wait_for('message', timeout=90, check=check)

                message = msg.content

                await msg.delete()

                if message in file[str(ctx.guild.id)]:
                    file[str(ctx.guild.id)].pop(message)
                    
                    with open("./data/reactions.json", 'w') as f:
                        json.dump(file, f, indent=4)

                    await embedMSG.edit(content=f"{message} has been removed.", embed=None, delete_after=10)
                    return

            except asyncio.TimeoutError:
                await embedMSG.clear_reactions()
                await embedMSG.edit(content=f"{ctx.author.mention} Timed out. Try again doing the command again.", delete_after=10.0, embed=None)
                return 


    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot != True:
            with open("./data/reactions.json", "r") as f:
                file = json.load(f)
            try:
                for name in file[str(payload.guild_id)]:
                    
                    if file[str(payload.guild_id)][name].get("message_id") == payload.message_id:

                        for role in file[str(payload.guild_id)][name]["roles"]:
                            
                            if (str(file[str(payload.guild_id)][name]["roles"].get(role))) == str(payload.emoji.id) or (str(file[str(payload.guild_id)][name]["roles"].get(role))) == str(payload.emoji):

                                guild = self.client.get_guild(payload.guild_id)
                                Role = guild.get_role(int(role))
                                await payload.member.add_roles(Role, reason="From reaction message")

            except KeyError: pass

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = await self.client.fetch_guild(payload.guild_id)

        member = await guild.fetch_member(payload.user_id)

        if member.bot != True:
            with open("./data/reactions.json", "r") as f:
                file = json.load(f)
            try:
                for name in file[str(payload.guild_id)]:
                    
                    if file[str(payload.guild_id)][name].get("message_id") == payload.message_id:

                        for role in file[str(payload.guild_id)][name]["roles"]:
                            
                            if (str(file[str(payload.guild_id)][name]["roles"].get(role))) == str(payload.emoji.id) or (str(file[str(payload.guild_id)][name]["roles"].get(role))) == str(payload.emoji):

                                guild = self.client.get_guild(payload.guild_id)
                                Role = guild.get_role(int(role))
                                await member.remove_roles(Role, reason="From reaction message")

            except KeyError: pass