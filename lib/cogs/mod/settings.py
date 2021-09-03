

from functions.objects import guildObject
from functions.apiConnection import ApiConnection, APIconfig

import discord
from discord import Embed
from asyncio import sleep

import validators

from discord.ext.commands import has_permissions, command, Cog, group

from lib.bot import bot
from functions.embedsDefaults import EmbedDefaults

DEFAULTS = EmbedDefaults()


def channels(client, channel):
    pass


def guild_(client):
    guild__ = client.id()
    return guild__


class Settings(Cog):

    def __init__(self, client):
        self.client = client

    @group(name="setup")
    async def _setup(self, ctx):
        pass

    @_setup.command()
    async def menu_(self, ctx):
        """Setup command for all the stuff you need"""

        embed = discord.Embed(
            title="Set Up Command",
            colour=0x000e8a302
        )

        msg = await ctx.send(embed=embed)

        async with ctx.channel.typing():

            fields = [
                ("Changing Comand Prefix", f"You can change your prefix within your server, by typing the command `setup prefix <new prefix>`. So for example it would `setup prefix !!`. That would change the prefix to !! instead of your current prefix"),
                ("Filter setting", f"You can change the setting for the filter on your server by typing `setup filter`"),
                ("Filter Type", f"Change the filter type. `setup filtertype`"),
                ("LogChannel", "Change the log channel that your server uses. `setup logchannel`"),
                ("Action Channel",
                 "Change the action channel for your server. `setup actionchannel`")
                ("Welcome message menu",
                 f"Edit your welcome messages. 'setup welcome help'"),
                #("Enable/Disable commands", f"You can disable or enable commands for your server by doing the following \n setup disableCommand <command> or `setup enableCommand <command>`"),
                #("Embed (beta)", f"Settings for embed messages. `setup embeds help`"),
                #("Channel settings (beta)", f"Add or remove channels from your guild. `setup channel help`")
            ]

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

                await sleep(1)
                await msg.edit(embed=embed)

    # setting prefix statements

    @_setup.command()
    async def prefix(self, ctx, new: str):
        """Change your server's prefix to use the bot. 

        Prefix cannot be more then 5 charcters in length
        """

        if len(new) > 5:
            await ctx.send("The prefix can not be more then 5 characters in length")

        else:

            newObject = guildObject(ctx.guild.id)
            newObject.prefix = str(new)

            ApiConnection.guild.put(newObject)

            bot.config = APIconfig()

            await ctx.send(f'Prefix set to {new}.')

    # Filter Setting
    @_setup.command(name="filter")
    async def _filter(self, ctx, new: int):
        """Change the filter settings for your server

        0 = Filter Off
        1 = Filter On"""

        msg = await ctx.send("Updating Config...Please wait.")

        newObject = guildObject(ctx.guild.id)
        newObject.filter = str(new)

        ApiConnection.guild.put(newObject)

        bot.config = APIconfig()

        await msg.edit(content=f'Filter set to {new}.')

    # Filter Type Setting
    @_setup.command()
    async def filtertype(self, ctx, new: int):
        """Change the filter type for your server

        0 - Delete Messages
        1- Return an Insult"""

        newObject = guildObject(ctx.guild.id)
        newObject.filterType = str(new)

        ApiConnection.guild.put(newObject)

        bot.config = APIconfig()

        await ctx.send(f'Filter Type set to {new}.')

    @_setup.command()
    async def cfilter(self, ctx):
        """Opens the custom filter menu"""

        await ctx.send("This feature is currently in development.")

    # Setting Logchannel
    @_setup.command()
    async def logchannel(self, ctx, new: int):
        """Changing the the log channel where everything that happens on the server is logged for you to view

        Channel ID : You need to enter the channel id number so it can assigned to the log channel"""

        newObject = guildObject(ctx.guild.id)
        newObject.logChannel = str(new)

        ApiConnection.guild.put(newObject)

        bot.config = APIconfig()

        await ctx.send(f'Log Channel has been set to {new}.')

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

    @_setup.group(name='embeds')
    async def _embeds(self, ctx):
        """Group for the embed commands

        Commands:
            set: Changes the colour of the embed that you have selected
            list: Lists all the embeds that are on your guild and their colours"""
        pass

    @_embeds.command()
    async def menu(self, ctx):
        """Setup command for all the stuff you need"""

        embed = discord.Embed(
            title="Embed Command",
            colour=0x000e8a302
        )

        msg = await ctx.send(embed=embed)

        async with ctx.channel.typing():

            fields = [
                ("set", f"Set the embeds message colour"),
                ("list", "List all the embed message that have custom colours")
            ]

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

                await sleep(1)
                await msg.edit(embed=embed)

    @_embeds.command(name="set")
    async def set_(self, ctx, embedname, colour):
        """Change the embed colour

        Args:
            embed name: The name of the embed which you can find by doing the command `embeds list`
            colour: The hex colour for the embed."""

        bot.oldConfig.set_embed(str(ctx.guild.id), embedname, colour)

    @_embeds.command(name="list")
    async def list_(self, ctx):
        """List all the embeds for your guild"""

        doptionlist = []
        coptionlist = []
        colour = bot.oldConfig.embed(str(ctx.guild.id), "setting_menus")
        doptionlist = bot.config.EMBEDS['DEFAULT']

        defaults = Embed(
            title="Default list of embed colours",
            colour=colour
        )
        for option in doptionlist:
            defaults.add_field(
                name=option, value=doptionlist.get(option), inline=False)

        try:
            coptions = bot.oldConfig.EMBEDS[str(ctx.guild.id)]

        except:
            await ctx.send(embed=defaults)
            return

        customembeds = Embed(
            title="Custom embeds for your server",
            colour=colour
        )

        for option, value in coptionlist:
            customembeds.add_field(name=option, value=value, inline=False)

        menu = PaginatedMenu(ctx)
        menu.set_timeout(90)
        menu.set_timeout_page(DEFAULTS.timeout(ctx.guild.id))
        menu.set_cancel_page(DEFAULTS.cancel(ctx.guild.id))

        menu.add_pages([customembeds, defaults])

        await menu.open()

    @_setup.group(name='timeout')
    async def _timeout(self, ctx):
        """Group for the embed commands

        Commands:
            set: Changes the colour of the embed that you have selected
            list: Lists all the embeds that are on your guild and their colours"""
        pass

    @_timeout.command()
    async def menu(self, ctx):
        """Setup command for all the stuff you need"""

        embed = discord.Embed(
            title="Embed Command",
            colour=0x000e8a302
        )

        msg = await ctx.send(embed=embed)

        async with ctx.channel.typing():

            fields = [
                ("set [embedName] [hexColour]",
                 f"Set the timeout for a command"),
                ("list", "List all the commands which have a timeout")
            ]

            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)

                await sleep(1)
                await msg.edit(embed=embed)

    @_timeout.command(name="set")
    async def set_(self, ctx, timeoutname, seconds):
        """Change the embed colour

        Args:
            timeout name: The name of the timeout which you can find by doing the command `timeout list`
            seconds: The amount of seconds you want the command to be on cooldown for."""

        bot.oldConfig.set_timeout(str(ctx.guild.id), timeoutname, seconds)
        await ctx.send(f"{timeoutname}, changed to {seconds}")

    @_timeout.command(name="list")
    async def list_(self, ctx):
        """List all the timouts for your guild"""

        doptionlist = []
        coptionlist = []
        colour = bot.oldConfig.embed(str(ctx.guild.id), "setting_menus")
        doptionlist = bot.oldConfig.TIMEOUTS['DEFAULT']

        defaults = Embed(
            title="Default list of timeout settings",
            colour=colour
        )
        for option in doptionlist:
            defaults.add_field(
                name=option, value=doptionlist.get(option), inline=False)

        try:
            coptionlist = bot.oldConfig.TIMEOUTS[str(ctx.guild.id)]

        except:
            await ctx.send(embed=defaults)
            return

        customtimeouts = Embed(
            title="Custom timeout for your server",
            colour=colour
        )

        for option, value in coptionlist:
            customtimeouts.add_field(name=option, value=value, inline=False)

        menu = PaginatedMenu(ctx)
        menu.set_timeout(90)
        menu.set_timeout_page(DEFAULTS.timeout(ctx.guild.id))
        menu.set_cancel_page(DEFAULTS.cancel(ctx.guild.id))

        menu.add_pages([customtimeouts, defaults])

        await menu.open()

    @group(name="channel")
    async def _channels(self, ctx):
        """Group for editing channel, and settings on your guild

        Commands:
            remove: Deletes a channel from your guild
            create: Create a new text channel"""
        pass

    @_channels.command()
    async def remove(self, ctx, channelID):
        """Remove a channel from your server with this command, works with voice or text channels

        Args:
            channelID : The id of the channel you wish to remove.
        """
        channel = ctx.guild.get_channel(int(channelID))

        await channel.delete()
        await ctx.send(f"Channel named, **{channel}** has been deleted")

    @_channels.command()
    async def create(self, ctx, channelID):
        """Remove a channel from your server with this command, works with voice or text channels

        Args:
            channelID : The id of the channel you wish to remove.
        """

        await ctx.guild.create_text_channel(name=channelID)

    @_channels.group(name='voice')
    async def _voice(self, ctx):
        """A sub group within channels for editing voice channels

        Commands:
            create: Creates a new voice channel"""
        pass

    @_voice.command()
    async def create(self, ctx, *, name):
        """Create a new voice channel on your server, for text channels use `channels create` command
        Early development, more features to come.

        Args:
            name : The name of which you want your channel called
        """

        await ctx.guild.create_voice_channel(name=name)

    def is_hex(s):
        try:
            int(s, 16)
            return True
        except ValueError:
            return False

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
