

from discord import interactions
from discord.enums import ButtonStyle
from discord.message import Message
from lib.bot import Bot
from functions.objects import Embeds
from functions.objects import guildObject
from discord.ui import button, Button
from discord.interactions import Interaction
from discord.ui.view import View

import discord
from discord import Embed
from asyncio import sleep

import validators

from discord.ext.commands import context, has_permissions, command, Cog, group

from lib.bot import bot

from .views import *


def channels(client, channel):
    pass


def guild_(client):
    guild__ = client.id()
    return guild__


class Settings(main,Cog):

    def __init__(self, client: Bot):
        self.client = client

    @command(name="setup")
    @has_permissions(manage_messages=True)
    async def _setup(self, ctx: context.Context):
        embed = Embeds(
            title=f"{ctx.guild.name}'s Settings",
            colour=0x000e8a302
        )

        await ctx.message.delete()

        fields = [
            ("Changing Comand Prefix",
             f"Change how users on your server use commands on {self.client.user.name}"),
            ("Filter setting",
             f"Change how the filter reacts, if its on and the custom filter"),
            ("LogChannel",
             f"Change the log channel that your server uses."),
            ("Action Channel",
             f"Change the action channel for {ctx.guild.name}."),
            ("Welcome User Message",
             f"Open the welcome message editor"),
        ]

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        await ctx.send(embed=embed, view=self.menu(self))


'''
    # Setting Actionchannel
    @_setup.command()
    async def actionchannel(self, ctx, new: int):
        """Changing the action channel where all moderations action preformed by the bot are carried out

        Channel ID : You need to enter the channel id number so it can assigned to the action log channel"""

        newObject = guildObject(ctx.guild.id)
        newObject.actionChannel = str(new)

        ApiConnection.guild.put(newObject)

        bot.config = APIconfig()

        await ctx.send(f'Action Channel set to {new}.')

    # Setting WelcomeChannel
    @_setup.group(name="welcome")
    async def _welcome(self, ctx):
        """A group of commands to manage welcoming users to your guild

        Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.
        Check them out at https://fluxpoint.dev """

    @_welcome.command(name="help")
    async def _help(self, ctx):
        """Commands:
        ```
- set : set the channel that your welcome messages to come from
- type : either a banner or default welcome message

Only availbe if your server is using the banner welcome message:

- background : set the background color for the banner
- banner : set the banner image from a predefined list
- icon : set the banner icon from a predefined list
- color welcome : set the hex color for the welcome message on the banner
- color username : set the hex color for the username on the banner
- color count : set the hex color for the member count on the banner
- custom banner : set the banner image from a custom .png or .jpg link
- custom banner : set the banner icon from a custom .png or .jpg link```
         """

        embed = Embed(
            title=f"{str(ctx.command.name).capitalize()} | Help",
            description=f"{self._help.callback.__doc__}",
            color=ctx.author.colour
        )

        await ctx.send(embed=embed)

    @_welcome.command(name="set")
    async def _set(self, ctx, new: int):
        """Welcome channel for all of your new members

        If you want to turn this feature off just type 0 in to this command otherwise you'll need:
        Channel ID : You need to enter the channel id number so it can assigned to the welcome channel"""
        newObject = guildObject(ctx.guild.id)
        newObject.welcomeChannel = str(new)

        ApiConnection.guild.put(newObject)

        bot.config = APIconfig()
        await ctx.send(f'Welcome Channel set to {new}.')

    @_welcome.command(name="type")
    async def _type(self, ctx, style: str):
        """Change the style of the welcome message

        ```Banner : Will start to create a banner message for you guild's new users
Default : Just a generic message which says hello to your new users```

Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.
        Check them out at https://fluxpoint.dev"""

        newObject = guildObject(ctx.guild.id)
        newObject.logChannel = str(style)

        ApiConnection.guild.put(newObject)

        bot.config = APIconfig()

        if style.lower() == "default":

            await ctx.send(f'Welcome Style set to {style}.')
        elif style.lower() == "banner":

            embed = Embed(
                title="Banner welcome message",
                description="Style has been set to `Banner`\nCommands avaliable for this are as follows",
                colour=0x000000
            )

            fields = [
                ("background", "If you are not using a banner you can use a colour background"),
                ("banner", "Change the background banner for the welcome message"),
                ("icon", "Change the icon which is used in the welcome message"),
                #("count", "Turn member count on or offw"),
                ("color welcome", "Change the welcome text color"),
                ("color username", "Change the username text color"),
                ("color count", "Change the members count text color"),
                ("custom banner", "Set a custom banner for the welcome message"),
                ("custom icon", "Set a custom icon for the welcome message"),
            ]

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

            await ctx.send(embed=embed)

        else:
            await ctx.send("The options for this are currently: \n```\nbanner : which is a custom image banner and will run through the setup for that\ndefault : Which is a standard hello message for new users.```")

    @_welcome.command(name="background")
    async def _background(self, ctx, colour):
        """Change the background colour for the welcome message. Use a colour from the list below or use a hex colour.
```
red
blue
green
purple
yellow
pink
orange```
Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.
        Check them out at https://fluxpoint.dev.
"""
        if self.is_hex(colour):
            newObject = guildObject(ctx.guild.id)
            newObject.logChannel = str(colour)

            ApiConnection.guild.put(newObject)

            bot.config = APIconfig()
            await ctx.send(f'Background set to {colour}.')

        else:
            await ctx.send(f'Make sure you are using a valid hex colour')

    @_welcome.command(name="banner")
    async def _banner(self, ctx, banner):
        """Decide on the banner image that your welcome message will use, options are:
```
love
mountain
purplewave
rainbow
space
sunset
swamp
waifubot
wave```

Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.
        Check them out at https://fluxpoint.dev"""

        if banner in ["love", "mountain", "purplewave", "rainbow", "space", "sunset", "swamp", "waifubot", "wave"]:
            newObject = guildObject(ctx.guild.id)
            newObject.logChannel = str(banner)

            ApiConnection.guild.put(newObject)

            bot.config = APIconfig()

            await ctx.send(f'Banner set to {banner}.')

        else:
            await ctx.send("Your options are:\n```\nlove\nmountain\npurplewave\nrainbow\nspace\nsunset\nswamp\nwaifubot\nwave```\n ***Run the command again and use one of the options above***")

    @_welcome.command(name="icon")
    async def _icon(self, ctx, icon):
        """Decide on the icon that your welcome message will use, options are:
```
cat
chika
dog
neko
nyancat
pepe
pikachu
senko
shrek```

Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.
        Check them out at https://fluxpoint.dev"""

        if icon in ["cat", "chika", "dog", "neko", "nyancat", "pepe", "pikachu", "senko", "shrek"]:
            newObject = guildObject(ctx.guild.id)
            newObject.logChannel = str(icon)

            ApiConnection.guild.put(newObject)

            bot.config = APIconfig()
            await ctx.send(f'Icon set to {icon}.')

        else:
            await ctx.send("Your options are:\n```\ncat\nchika\ndog\nneko\nnyancat\npepe\npikachu\nsenko\nshrek```\n ***Run the command again and use one of the options above***")

    # @_welcome.command(name="count")
    async def _count(self, ctx, text: str):
        """Change the member count text.
        Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.
        Check them out at https://fluxpoint.dev"""

        bot.config.set_general(
            str(ctx.guild.id), "welcome_counttext", str(text))

    @_welcome.group(name="colors")
    async def _colors(self, ctx):
        """A group for the color commands

        Commands:
        ```welcome : Change the welcome text color
        username : Change the username text color
        count : Change the members count text color```

        Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.
        Check them out at https://fluxpoint.dev"""
        pass

    @_colors.command(name="welcome")
    async def _welcome_(self, ctx, color):
        """Change the color of the welcome message

        Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.
        Check them out at https://fluxpoint.dev"""

        await ctx.send("Feature disabled for now\nWill return at a later date")

        """
        if self.is_hex(color):
            pass

        else:
            await ctx.send(f'Make sure you are using a valid hex colour')
        """

    @_colors.command(name="username")
    async def _username_(self, ctx, color):
        """Change the color of the username text

        Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.
        Check them out at https://fluxpoint.dev"""

        await ctx.send("Feature disabled for now\nWill return at a later date")

        """if self.is_hex(color):
            bot.config.set_general(str(ctx.guild.id), "welcome_username_colour", str(color))
            await ctx.send(f'Welcome username colour set to {color}.')
        else:
            await ctx.send(f'Make sure you are using a valid hex colour')"""

    @_colors.command(name="count")
    async def _count_(self, ctx, color):
        """Change the color of the count text

        Credit goes to Builderb#0001 on Discord and the Fluxpoint team for all of the banner messages and custom images.
        Check them out at https://fluxpoint.dev"""

        await ctx.send("Feature disabled for now\nWill return at a later date")

        """if self.is_hex(color):
            bot.config.set_general(str(ctx.guild.id), "welcome_count_colour", str(color))
            await ctx.send(f'Member count colour set to {color}.')
        else:
            await ctx.send(f'Make sure you are using a valid hex colour')"""

    @_welcome.group(name="custom")
    async def _custom(self, ctx):
        """A group of commands for adding custom banners and icons to the welcome messages

        Commands:
        ```banner : Adding a custom banner to the welcome message
        icon : Adding a custom icons to the welcome message```

        s!"""
        pass

    @_custom.command(name="banner")
    async def _banner_(self, ctx, httpsLink):
        """Add a custom http imag link banner to your welcome message"""

        VALID_IMAGE_EXTENTSIONS = [
            ".jpg",
            ".jpeg",
            ".png"
        ]

        def extention(imageurl):
            for extentions in VALID_IMAGE_EXTENTSIONS:
                if imageurl.endswith(extentions):
                    return True
            return False

        if validators.url(httpsLink) and extention(httpsLink):
            newObject = guildObject(ctx.guild.id)
            newObject.logChannel = str(httpsLink)

            ApiConnection.guild.put(newObject)

            bot.config = APIconfig()
            await ctx.send(f'Banner set to {httpsLink}.')

        else:
            await ctx.send("Invalid image url")

    @_custom.command(name="icon")
    async def _icon_(self, ctx, httpsLink):
        """Add a custom http imag link icon to your welcome message"""

        VALID_IMAGE_EXTENTSIONS = [
            ".jpg",
            ".jpeg",
            ".png"
        ]

        def extention(imageurl):
            for extentions in VALID_IMAGE_EXTENTSIONS:
                if imageurl.endswith(extentions):
                    return True
            return False

        if validators.url(httpsLink) and extention(httpsLink):
            newObject = guildObject(ctx.guild.id)
            newObject.logChannel = str(httpsLink)

            ApiConnection.guild.put(newObject)

            bot.config = APIconfig()
            await ctx.send(f'Icon set to {httpsLink}.')
        else:
            await ctx.send("Invalid image url")
'''
