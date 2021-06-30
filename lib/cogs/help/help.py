from discord import Embed
from discord.ext.commands import Cog, command
from dpymenus import PaginatedMenu

from datetime import datetime

from functions.embedsDefaults import EmbedDefaults

DEFAULTS = EmbedDefaults()

class Help(Cog):

    def __init__(self, client):
        self.client = client

    def page_one(self):
        embed = Embed(
            title = "Economy Commands {Currently Disabled Due to Updates}",
            description = "Use the arrows which the bot has reacted with to change the pages"
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
                ("announce", "Sends an announcement to a channel for you."),
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
            ("suggest", "Give Solar more ideas for Sancus, 50 Characters minimum")
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
            menu.set_timeout(90)

            page1 = self.page_one()
            page2 = self.page_two()
            page3 = self.page_three()
            page4 = self.page_four()
            page5 = self.page_five()
            page6 = self.page_six()

            if ctx.author.guild_permissions.manage_messages:
                menu.add_pages([page1, page2, page3, page4, page5, page6])

            else:
                menu.add_pages([page1, page2, page3, page4, page5])

            await menu.open()
