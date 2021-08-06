from discord import Embed, Emoji, colour
from discord.ext.commands import Cog, command
from dpymenus import PaginatedMenu

from discord_components import Button, Select, SelectOption, component

from datetime import datetime, timedelta

import asyncio

from functions.embedsDefaults import EmbedDefaults

DEFAULTS = EmbedDefaults()

class Help(Cog):
    """Version 3 of the help command using the dpyemnus.
    This section is deprecated and will be removed in version 7, to insure that everything is working properly"""

    def __init__(self, client):
        self.client = client

    def page_one(self):
        embed = Embed(
            title = "Economy",
            description = "Get those delicious dollar bills",
            colour = 0x00094e31e
        )

        fields = [
            ("payday", "Get that pay day money"),
            ("beg", "You might get lucky"),
            ("balance", "See you wallet and bank account")
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    def page_two(self):
        embed = Embed(
            title ='Games Help', 
            description = "Use the arrows which the bot has reacted with to change the pages"
            )

        fields = [
            ("Dice {roll amount, max 5}", "Roll the dice"),
            ("rps {rock, paper, scissors}", "Test you luck in a game of Rock Paper Scissors"),
            ("cf {t, h}", "Guess which side the coin will land on, head (h) or tails (t)"),
            ("8ball {question}", "Ask it a yes, no question")
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    def page_three(self):
        embed = Embed(
            title='Stats Help', 
            description = "Use the arrows which the bot has reacted with to change the pages"
            )

        fields = [
            ("covid19", "Get the global status of the current Covid19 pandemic")
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
        
        return embed
    
    def page_four(self):
        embed = Embed(
            title='Anime Help', 
            description = "Use the arrows which the bot has reacted with to change the pages"
            )

        fields = [
            ("waifus", "Have a look at some waifus"),
            ("husbandos", "Have a look at some husbandos"),
            ("image anime" , "Random anime image"),
            ("image wallpaper" , "Random wallpaper image"),
            ("image nekopara" , "Random nekopara image"),
            ("image azurlane" , "Random azurlane image"),
            ("image slap" , "Random slap image"),
            ("image memes" , "Random meme image"),
            ("image doki" , "Random doki image"),
            ("image chibi" , "Random chibi image"),
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    def page_five(self):
        embed = Embed(
            title='Mod Commands', 
            description = "Use the arrows which the bot has reacted with to change the pages"
        )

        fields = [
                ("kick {userid} [reason]", "Kick those players that you don't mind coming back"),
                ("ban {userid} [reason]", "Ban those players you don't want to see again"),
                ("unban {userid} [reason]", "Unban players who were banned by mistake"),
                ("ping", "Get the ping of the bot"),
                ("avatar {userid}", "Get a full size image of the user's avatar"),
                ("userinfo / ui {userid}", "Get information about a user"),
                ("serverinfo / si", "Get information about your server"),
                ("embed", "Send and embed message to a channel on your server/guild"),
                #("announce", "Sends an announcement to a channel for you."),
                ("msgsend", "Sends a message to a channel for you"),
                ("setup menu", "Loads up an embed message with all the settings for the bot")
            ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
        
        return embed

    def page_six(self):
        embed = Embed(
            title='Misc Help', 
            description = "Use the arrows which the bot has reacted with to change the pages"
            )

        fields = [
            ("hug {@user}", "Hug a friend, they may need it"),
            ("bothug {@user}", "Tell me who you want me to hug"),
            ("bothugself", "Let me hug myself"),
            ("hugself", "Give your self a hug"),
            ("slap {@user}", "Give a user a cheeky slap"),
            ("pat {@user}", "Pat a fellow user"),
            ("create_poll", "Create a poll for user to vote on"),
            ("gif {search word}", "Get a random gif"),
            ("invite", "Invite Sancus to your own server"),
            ("botserver", "Join my server and see all of my updates early"),
            ("suggest", "Give Solar more ideas for Sancus, 50 Characters minimum"),
            ("covid19", "Get the global status of the current Covid19 pandemic")
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
        
        return embed

    
    @command(name= 'help', aliases = ['commands'])
    async def help(self, ctx, commandname = None):
        """Help command for helpful things. 
        
        Args:
        
        {CommandName}: A command name to give you helpful info about that command"""
        if commandname != None:
            command = self.client.get_command(commandname)

            embed = Embed(
                title = command.name,
                description = command.callback.__doc__
            )

            await ctx.send(embed=embed)

        else:

            menu = PaginatedMenu(ctx)
            menu.set_timeout(30)

            page1 = self.page_one()
            page2 = self.page_two()
            page4 = self.page_four()
            page5 = self.page_five()
            page6 = self.page_six()

            if ctx.author.guild_permissions.manage_messages:
                menu.add_pages([page1, page2, page4, page5, page6])

            else:
                menu.add_pages([page1, page2, page4, page5])

            await menu.open()

class helpButtons(Cog):
    """Version 6 Help Command
    This version is using the new interaction buttons to navigate a menu."""
    
    def __init__(self, client) -> None:
        self.client = client
        
    @command(name="help")
    async def buttons(self, ctx):
        await ctx.message.delete()
        
        ModEmoji = self.client.get_emoji(872992608354443314)
        EconEmoji = self.client.get_emoji(872998673422897253)
        GamesEmoji = self.client.get_emoji(873008493530067014)
        MiscEmoji = self.client.get_emoji(873017754255523903)
        
        CloseEmoji = self.client.get_emoji(872992645302075392)
        OpenEmoji = self.client.get_emoji(872992768073551893)
        
        if len(self.client.help_instance) != 0:
            for name, instance, message in self.client.help_instance:
                if name == ctx.author.id:
                    time = datetime.strptime(instance, ("%H,%M"))
                    
                    if time - timedelta(minutes=2):
                        waitmsg = await ctx.send(embed=Embed(
                            description="Please wait till the last help is cancel or click the button below to end it and run the command again."
                        ),
                            components=[Button(label="Cancel Previous Help Command", emoji = CloseEmoji, style=4)])
                        
                        try:
                            interaction = await self.client.wait_for("button_click", timeout=15)
                            await interaction.respond(type=6)
                            
                            for guild in self.client.guilds:
                                for channel in guild.channels:
                                    try:
                                        pre_message = await channel.fetch_message(int(message))
                                        await pre_message.delete()
                                        await waitmsg.edit(embed=Embed(
                                            description="Try the command again, after this message has been deleted in 4 seconds."
                                                ),
                                            components=[],
                                            delete_after = 3.5
                                            )
                                        
                                        self.client.help_instance.remove((name,instance,message))
                                        return
                                                                                   
                                    except:
                                        pass
                            
                        except asyncio.TimeoutError:
                            await waitmsg.delete()
                            return
        
        embed =Embed(
                title = "Welcome to the new and improved help command",
                description = "All you need to do is click a button below. \n\n**Please close this instance or wait for a time out before doing another help command for yourself**"
            )
        
        msg = await ctx.send(
                embed=embed,
                components = [
                    [
                        Button(label = "Mod Help", id = "mod", emoji = ModEmoji, style=1), 
                        Button(label = "Econ Help", id = "econ", emoji = EconEmoji, style=3),
                        Button(label = "Games Help", id = "games", emoji = GamesEmoji, style=3),
                        Button(label = "Misc Help", id = "misc", emoji = MiscEmoji, style=3),                       
                        ],
                    [
                        Button(label = "Close", id = "close", emoji = CloseEmoji, style=4),
                        Button(label = "Leave Open", id = "open", emoji = OpenEmoji, style=4)
                    ]
                    ]
            )
        
        time=datetime.utcnow().strftime("%H,%M")
        
        self.client.help_instance.append((ctx.author.id, time, msg.id))
        print(self.client.help_instance)
        
        while True:
            try:
                interaction = await self.client.wait_for("button_click", timeout=120, check = lambda i: i.user.id == ctx.author.id)
                
                if interaction.custom_id == "mod":
                    await msg.edit(content="",embed=self.Mod())
                    
                elif interaction.custom_id == "econ":
                    await msg.edit(content="",embed=self.Econ())
                    
                elif interaction.custom_id == "games":
                    await msg.edit(content="",embed=self.Games())
                
                elif interaction.custom_id == "misc":
                    await msg.edit(content="", embed=self.Misc())
                    
                elif interaction.custom_id == "close":
                    await msg.delete()
                    self.client.help_instance.remove((ctx.author.id, time, msg.id))
                    print(self.client.help_instance)
                    return
                    
                elif interaction.custom_id == "open":
                    await msg.edit(content="", components=[])
                    return
                    
                else:
                    await msg.edit(content="FAILED")
                    
                await interaction.respond(type=6)
                
            except asyncio.TimeoutError:
                embed = Embed(
                    description = "You have been timed out, be quicker :smile:"
                )
                
                await msg.edit(content="", components=[], embed=embed)
                return
            
    def Econ(self):
        embed = Embed(
            title = "Economy",
            description = "Get those delicious dollar bills",
            colour = 0x00094e31e
        )

        fields = [
            ("payday", "Get that pay day money"),
            ("beg", "You might get lucky"),
            ("balance", "See you wallet and bank account"),
            ("leaderboard [amount]", "Are you in the top 5?")
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
            
        embed.set_footer(text="{} = Required, [] = Optional\n"+self.client.embedAuthorName, icon_url=self.client.embedAuthorUrl)

        return embed
    
    def Mod(self):
        embed = Embed(
            title='Moderation', 
            description = "For my admins out there",
            colour = 0x000e31e4f
        )

        fields = [
                ("kick {userid} [reason]", "Kick those players that you don't mind coming back"),
                ("ban {userid} [reason]", "Ban those players you don't want to see again"),
                ("unban {userid} [reason]", "Unban players who were banned by mistake"),
                ("ping", "Get the ping of the bot"),
                ("avatar {userid}", "Get a full size image of the user's avatar"),
                ("userinfo / ui {userid}", "Get information about a user"),
                ("serverinfo / si", "Get information about your server"),
                ("embed", "Send and embed message to a channel on your server/guild"),
                #("announce", "Sends an announcement to a channel for you."),
                ("msgsend", "Sends a message to a channel for you"),
                ("setup menu", "Loads up an embed message with all the settings for the bot")
            ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
            
        embed.set_footer(text="{} = Required, [] = Optional\n"+self.client.embedAuthorName, icon_url=self.client.embedAuthorUrl)
        
        return embed
    
    def Games(self):
        embed = Embed(
            title ='Games', 
            description = "Who doesn't love a spot of gaming",
            colour = 0x0008e1ee3
            )

        fields = [
            ("Dice {roll amount | max 5}", "Roll the dice"),
            ("rps {rock, paper or scissors}", "Test you luck in a game of Rock Paper Scissors"),
            ("cf {t or h}", "Guess which side the coin will land on, head (h) or tails (t)"),
            ("8ball {question}", "Ask it a yes, no question")
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
            
        embed.set_footer(text="{} = Required, [] = Optional\n"+self.client.embedAuthorName, icon_url=self.client.embedAuthorUrl)

        return embed
    
    def Misc(self):
        embed = Embed(
            title='Misc Help', 
            description = "Who doesn't have random stuff",
            colour = 0x000e3bc1e
            )

        fields = [
            ("hug {@user}", "Hug a friend, they may need it"),
            ("bothug {@user}", "Tell me who you want me to hug"),
            ("bothugself", "Let me hug myself"),
            ("hugself", "Give your self a hug"),
            ("slap {@user}", "Give a user a cheeky slap"),
            ("pat {@user}", "Pat a fellow user"),
            ("create_poll", "Create a poll for user to vote on"),
            ("gif {search word}", "Get a random gif"),
            ("invite", "Invite Sancus to your own server"),
            ("botserver", "Join my server and see all of my updates early"),
            ("suggest", "Give Solar more ideas for Sancus, 50 Characters minimum"),
            ("covid [country code, 'gb' for the UK]", "Get the global status of the current Covid19 pandemic")
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
            
        embed.set_footer(text="{} = Required, [] = Optional\n"+self.client.embedAuthorName, icon_url=self.client.embedAuthorUrl)
        
        return embed