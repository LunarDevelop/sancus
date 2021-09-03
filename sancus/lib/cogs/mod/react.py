import datetime
from typing import Optional, TypeVar, Union, Any
from discord import embeds
from discord.embeds import EmptyEmbed
from discord import Embed
from discord.emoji import Emoji
from discord.interactions import Interaction
from discord.reaction import Reaction
from discord.role import Role
from discord.types.embed import EmbedType
from discord.embeds import _EmptyEmbed

from discord.ui import Button, Select, View
from discord.components import SelectOption, ButtonStyle
from discord.ext.commands import Cog, command, group, Context
from discord.user import BU

from functions.objects import Embeds

import emoji
import asyncio
import json
import validators

from lib.bot import bot

T = TypeVar('T')
MaybeEmpty = Union[T, _EmptyEmbed]


class ReactionEmbed(Embeds):
    "Embeds for my reaction menu system"

    def __init__(self, *, title: MaybeEmpty[Any] = EmptyEmbed, type: EmbedType = EmptyEmbed, url: MaybeEmpty[Any] = EmptyEmbed, description: MaybeEmpty[Any] = EmptyEmbed):
        super().__init__(colour=0x0006AF32D, title=title, type=type,
                         url=url, description=description)


class reaction(Cog):

    def __init__(self, client) -> None:
        self.client = client
        self.colour = 0x0006AF32D,

    @command(name="react", brief="Add, remove and modify reaction roles")
    async def _react_(self, ctx: Context):
        """Reaction role message

        Add, remove and modify reaction role message for people to get roles in your server"""

        await ctx.message.delete()

        main_menu = ReactionEmbed(
            title="Reaction Role Main Menu",
            description="Do you want to add, remove or modify a reaction role message"
        )

        class MainView(View):
            "Main Menu Button"

            def __init__(self, client):
                super().__init__()
                self.add_item(Button(label="Add",
                              custom_id="add", emoji=client.addEmoji))
                self.add_item(Button(label="Remove",
                              custom_id="remove", emoji=client.deleteEmoji))
                self.add_item(Button(label="Modify",
                              custom_id="modify", emoji=client.adjustEmoji))

        msg = await ctx.send(embed=main_menu, view=MainView(self.client))

        # Wait for interaction
        interactionObject = await self.client.wait_for("interaction", timeout=120, check=lambda i: i.user.id == ctx.author.id)
        interactionObject.response.defer

        # What is the interaction
        choice = interactionObject.data["custom_id"]

        async def add():
            # Type of reaction
            react_types = ["Button", "Select", "Emoji"]
            react_type = None

            # Roles info
            react_roles = None
            react_role_link: Optional[list[Role]] = None

            # Reaction Message info
            react_name = None
            react_message_types = ["PreMade", "Custom"]
            react_message_type = None
            react_message_id = None
            react_message_cOe = None
            react_message_content = None
            react_message_embed = None
            react_embed_title = None
            react_embed_content = None
            react_embed_colour = None
            react_embed = EmptyEmbed
            react_role_list_final = []

            # React
            react_emoji_list = None
            react_emoji_roles = None
            react_button_list: Optional[list[Button]] = None
            react_button_content: Optional[list[str]] = None
            react_button_colour: Optional[list[str]] = None
            react_button_colour_instance: Optional[str] = None
            react_button_ids : Optional[list[int]]= []
            react_select_objects: Optional[list[SelectOption]] = None
            react_select_title: Optional[list[str]] = None
            react_select_ids : Optional[list[int]] = []]

            # Misc
            react_channel = None

            # Embeds
            react_type_embed = ReactionEmbed(
                title="What embed type would you like?",
                description="""**Button** : A simple button like you see below with an emoji if you wish\n 
                **Select** : A dropdown menu where you can select multiple role or just one\n
                **Emojis** : The old fashion way of just using different emojis for different roles"""
            )
            
            react_name_embed = ReactionEmbed(
                title="What would you like it to be called?",
                description="This is solely so you can access it later, to modify or remove it."
            )

            react_message_type_embed = ReactionEmbed(
                title="Premade or custom message?",
                description="""Do you want the reaction message to be from a premade message ( i.e made by you)\n
                Or a message made by the bot? \nThis option means that you are able to make an embed message like this on"""
            )

            react_message_channel_embed = ReactionEmbed(
                title="Which channel is the message in?",
                description="Please select the channel that you either want your message in or the channel the premade message is in."
            )

            react_message_id_embed = ReactionEmbed(
                title="What is the message id of the message",
                description="""Which message would you like to use for your reaction role message, just paste the id number of the message below.\n
                If you need to know how to get an ID of the message look at this article:
                https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-"""
            )

            react_message_cOe_embed = ReactionEmbed(
                title="Type of message",
                description="Would you like to have the message to be an embed message (like this one) or a standard message?"
            )

            react_message_content_embed = ReactionEmbed(
                title="What would you like the message to be?",
                description="What will the message say"
            )

            react_message_embedTitle_embed = ReactionEmbed(
                title="What is the title of the embed?",
                description="In this embed the title is `What is the title of the embed?`"
            )

            react_message_embedContent_embed = ReactionEmbed(
                title="What will the embed message say?",
                description="What do you want the embed message to say in the description (which is this text here)?"
            )

            react_message_embedColour_embed = ReactionEmbed(
                title="What colour do you want the embed to be?",
                description="The colour needs to be a hex colour."
            )

            react_role_embed = ReactionEmbed(
                title="What roles are being used for this reaction role message?",
                description="""Choose one or multiple roles from the list below of the ones you want to be part of this reaction role message\n 
                You can choose up to 10 different roles per reaction message"""
            )

            react_emoji_embed = ReactionEmbed(
                title="Emoji Time",
                description="Please react to this message using all the emojis you want then click the done button"
            )

            react_select_title_embed = ReactionEmbed(
                title="Selection Title",
                description="What do you want the item's title to be?\nUse a common seperatated list such as `example1,example2,example3`"
            )

            react_button_content_embed = ReactionEmbed(
                title="What will the button say?",
                description="Please type enter what you would like each of the buttons to say, using a comma (,) to seperate the list."
            )

            react_button_colour_embed = ReactionEmbed(
                title="Colour of the button?",
                description="You can see the colours on the buttons below"
            )

            react_role_link_embed = ReactionEmbed(
                title="Linking the roles to the reaction",
                description="Choose the role that goes with the emoji or id below.\n The id is just the name of the select object or button from before."
            )

            # Buttons

            class react_type_buttons(View):

                def __init__(self):
                    super().__init__(timeout=None)

                    self.add_item(Button(
                        label="Button",
                        custom_id="button"
                    ))
                    self.add_item(Button(
                        label="Select",
                        custom_id="select"
                    ))
                    self.add_item(Button(
                        label="Emoji",
                        custom_id="emoji"
                    ))

            class react_message_type_buttons(View):

                def __init__(self):
                    super().__init__()

                    self.add_item(
                        Button(
                            label="Premade",
                            custom_id="premade"
                        )
                    )
                    self.add_item(
                        Button(
                            label="Bot Made",
                            custom_id="custom"
                        )
                    )

            class react_message_cOe_buttons(View):

                def __init__(self):
                    super().__init__()
                    self.add_item(Button(
                        label="Standard message",
                        custom_id="content"
                    ))
                    self.add_item(Button(
                        label="Embed",
                        custom_id="embed"
                    ))

            class react_emoji_donebutton(View):

                def __init__(self):
                    super().__init__()

                    self.add_item(
                        Button(
                            label="Done",
                            value="done",
                            emoji=self.client.tickEmoji
                        )
                    )

            class react_button_colour_buttons(View):

                def __init__(self):
                    super().__init__()

                    self.add_item(
                        Button(
                            label="Grey",
                            value=ButtonStyle.secondary,
                            ButtonStyle=ButtonStyle.secondary
                        )
                    )
                    self.add_item(
                        Button(
                            label="Blurple",
                            value=ButtonStyle.secondary,
                            ButtonStyle=ButtonStyle.primary
                        )
                    )
                    self.add_item(
                        Button(
                            label="Green",
                            value=ButtonStyle.secondary,
                            ButtonStyle=ButtonStyle.success
                        )
                    )
                    self.add_item(
                        Button(
                            label="Red",
                            value=ButtonStyle.secondary,
                            ButtonStyle=ButtonStyle.danger
                        )
                    )

            # Selects

            class react_message_channel_select(View):
                """Choosing which channel the message is/should be in

                channelList parameter needs to be 2d array with the following as the object
                [chanelName, channelId]"""

                def __init__(self, channelList):
                    super().__init__()
                    options = []

                    for channel in channelList:
                        selectOption = SelectOption(
                            label=channel[0],
                            value=str(channel[1])
                        )

                        options.append(selectOption)

                    self.add_item(Select(
                        custom_id="message_channel",
                        placeholder="Select the channel from this list",
                        options=options
                    ))

            class react_role_select(View):
                """Role selection menu

                roleList needs to be a 2d array with items like this
                [roleName,roleId]"""

                def __init__(self, roleList):
                    super().__init__()
                    options = []
                    for role in roleList:
                        options.append(SelectOption(
                            label=role[0],
                            value=role[1]
                        ))

                    self.add_item(
                        Select(
                            custom_id="RoleSelect",
                            options=options,
                            max_values=10
                        )
                    )

            class react_role_link_select(View):
                """Select role from drop down menu with embed showing which button, select or emoji you need to link

                I will figure this out in a bit once I get to this stage. Will be last stage of the system
                """

                def __init__(self, roles: list[Role.id]):
                    super().__init__()
                    options: list[SelectOption] = []
                    for role in roles:
                        react_role = ctx.guild.get_role(role)
                        option = SelectOption(
                            label=react_role.name,
                            value=react_role.id
                        )
                        options.append(option)

                    self.add_item(
                        Select(
                            custom_id="selection",
                            options=options
                        )
                    )

        # Start

        # Order of action
        # Name
        # Type
        # Channel
        # Message type (premade or custom)
        # Content or Embed / or message id
        # Message Content or Embed title/description/colour
        # Roles
        # Emoji or Buttons or Selects
        # Roles -> Option

            # Name
            await msg.edit(embed=react_name_embed, view=None)
            
            message = await self.client.wait_for("message", check=lambda i: i.user.id == ctx.author.id)
            
            react_name = message.content()

            # Type Selection
            await msg.edit(embed=react_type_embed, view=react_type_buttons())

            interactionObject = await self.client.wait_for("interaction", check=lambda i: i.user.id == ctx.author.id)
            interactionObject.response.defer

            react_type = interactionObject.data["custom_id"]

            # Channel Selection

            channels = []

            for channel in ctx.guild.channels:
                channels.append([channel.name, channel.id])

            await msg.edit(embed=react_message_channel_embed, view=react_message_channel_select(channels))

            interactionObject = await self.client.wait_for("interaction", check=lambda i: i.user.id == ctx.author.id)
            interactionObject.response.defer

            react_channel = int(interactionObject.data["custom_id"])

            # Message Type

            await msg.edit(embed=react_message_type_embed, view=react_message_type_buttons)

            interactionObject = await self.client.wait_for("interaction", check=lambda i: i.user.id == ctx.author.id)
            interactionObject.response.defer

            react_message_type = interactionObject.data["custom_id"]

            # Content or Embed

            if react_message_type == "custom":
                await msg.edit(embed=react_message_cOe_embed, view=react_message_cOe_buttons)

                interactionObject = await self.client.wait_for("interaction", check=lambda i: i.user.id == ctx.author.id)
                interactionObject.response.defer

                react_message_cOe = interactionObject.data["custom_id"]

            # Message ID
            if react_message_type == "premade":
                await msg.edit(embed=react_message_id_embed, view=None)

                while True:
                    interactionObject = await self.client.wait_for("message", check=lambda i: i.user.id == ctx.author.id)

                    try:
                        interactionObject = int(interactionObject)

                        await ctx.guild.get_channel(react_channel).fetch_message(interactionObject)
                        break

                    except:

                        react_message_id_embed.add_field(
                            name="Invalid message", value="Ensure it is a number and you right click on a message not a user.")

                        msg.edit()

                react_message_id = int(interactionObject)

            # Message Content

            if react_message_cOe == "content":
                await msg.edit(embed=react_message_content_embed, view=None)

                react_message_content = (await self.client.wait_for("message", check=lambda i: i.user.id == ctx.author.id and i.channel.id == ctx.channel.id)).content

            # Embed Title

            if react_message_cOe == "embed":
                await msg.edit(embed=react_message_embedTitle_embed, view=None)

                react_embed_title = (await self.client.wait_for(
                    "message",
                    check=lambda i: i.user.id == ctx.author.id and i.channel.id == ctx.channel.id)).content

            # Embed Description
            if react_message_cOe == "embed" and react_embed_title != None:
                await msg.edit(embed=react_message_embedContent_embed, view=None)

                react_embed_content = (await self.client.wait_for(
                    "message",
                    check=lambda i: i.user.id == ctx.author.id and i.channel.id == ctx.channel.id)).content

            # Embed Colour

            if react_message_cOe == "embed" and react_embed_content != None:
                await msg.edit(embed=react_message_embedColour_embed, view=None)

                while True:
                    react_embed_colour = (await self.client.wait_for(
                        "message",
                        check=lambda i: i.user.id == ctx.author.id and i.channel.id == ctx.channel.id)).content

                    if not self.client.is_hex(react_embed_colour):
                        react_message_embedColour_embed.add_field(
                            name="Invalid Hex Colour",
                            value="""Please make sure you are using a hex colour code,
                            Use the link below for a colour select if you need it:
                            https://htmlcolorcodes.com/color-picker/"""
                        )

                    else:
                        break

            react_embed = Embed(
                title=react_embed_title,
                description=react_embed_content,
                colour=0x000+int(react_embed_colour, 16)
            )

            # Roles

            roleList = []

            for role in await ctx.guild.fetch_roles():
                roleList.append([role.name, role.id])

            await msg.edit(embed=react_role_embed, view=react_role_select(roleList))

            interactionObject = await self.client.wait_for("interaction", check=lambda i: i.user.id == ctx.author.id)
            interactionObject.response.defer

            react_roles = interactionObject.data["values"]

            # Emoji

            if react_type == "emoji":

                await msg.edit(embed=react_emoji_embed, view=react_emoji_donebutton)

                interactionObject = await self.client.wait_for("interaction", check=lambda i: i.user.id == ctx.author.id and i.data["custom_id"] == "done")
                interactionObject.response.defer

                react_emoji_list: list[Reaction] = msg.reactions

                await msg.clear_reactions()

            # Buttons

                # Content
            if react_type == "button":

                await msg.edit(embed=react_button_content_embed, view=None)

                react_button_content: str = (await self.client.wait_for(
                    "message",
                    check=lambda i: i.user.id == ctx.author.id and i.channel.id == ctx.channel.id)).content()

                react_button_content.split(",")

                # Colours
            if react_type == "button" and react_button_content != None:
                react_button_ids = 0
                for button in react_button_content:
                    await msg.edit(embed=react_button_colour_embed, view=react_button_colour_buttons)

                    interactionObject = await self.client.wait_for("interaction", check=lambda i: i.user.id == ctx.author.id)
                    interactionObject.response.defer

                    react_button_colour.append(
                        interactionObject.data["custom_id"])

                    react_button_list:list[Button]
                    react_button_ids += 1
                    
                    react_button_list.append(
                        Button(
                            label=react_button_content,
                            custom_id=len(react_button_list)+1,
                            style=react_button_colour
                        )
                    )

            # Select

                # Title
            if react_type == "select":
                await msg.edit(embed=react_select_title_embed, view=None)

                react_select_title_message = (await self.client.wait_for(
                    "message",
                    check=lambda i: i.user.id == ctx.author.id and i.channel.id == ctx.channel.id)).content

                react_select_title = react_select_title_message.split(
                    ",")

            # Roles -> Option
            
                    # React gets saved to a list in the order of the emoji/interaction list
                    # So just need to match the two list up to find the role needed

                # Emojis

            if react_type == "emoji":
                react_role_list_link: list[Role] = react_roles
                react_role_list_final: list[Role] = []
                for emoji in react_emoji_list:
                    emoji: Reaction
                    react_role_link_embed.add_field(
                        name="emoji:", value=emoji.emoji)

                    await msg.edit(embed=react_role_embed, view=react_role_link_select(react_role_list_link))

                    interactionObject: Interaction = await self.client.wait_for("interaction", check=lambda i: i.user.id == ctx.author.id)
                    interactionObject.response.defer

                    react_role_list_final.append(
                        interactionObject.data["values"])

                    del react_role_list_link[react_role_list_link.index(
                        interactionObject.data["values"])]

                    react_role_link_embed.remove_field(0)

                # Buttons

            if react_type == "button":
                react_role_list_link: list[Role] = react_roles
                react_role_list_final: list[Role] = []
                
                for title in react_button_content:
                    
                    react_role_link_embed.add_field(
                        name="Button Title:", value=title)

                    await msg.edit(embed=react_role_embed, view=react_role_link_select(react_role_list_link))

                    interactionObject: Interaction = await self.client.wait_for("interaction", check=lambda i: i.user.id == ctx.author.id)
                    interactionObject.response.defer

                    react_role_list_final.append(
                        interactionObject.data["values"])

                    del react_role_list_link[react_role_list_link.index(
                        interactionObject.data["values"])]

                    react_role_link_embed.remove_field(0)

                # Selects

            if react_type == "select":
                react_role_list_link: list[Role] = react_roles
                react_role_list_final: list[Role] = []

                for title in react_select_title:

                    react_role_link_embed.add_field(
                        name="Button Title:", value=title)

                    await msg.edit(embed=react_role_embed, view=react_role_link_select(react_role_list_link))

                    interactionObject: Interaction = await self.client.wait_for("interaction", check=lambda i: i.user.id == ctx.author.id)
                    interactionObject.response.defer

                    react_role_list_final.append(
                        interactionObject.data["values"])

                    del react_role_list_link[react_role_list_link.index(
                        interactionObject.data["values"])]

                    react_role_link_embed.remove_field(0)

            # Finishing up

            FinishedData : dict = {
                "name": react_name,
                "data": {
                    "guildId" : ctx.guild.id,
                    "messageId" : react_message_id,
                    "emojis" : react_emoji_list,
                    "buttonsIds" : react_button_ids,
                    "selectIds" : react_select_ids,
                    "roles" : react_role_list_final
                }
            }

            file = open("sancus/data/reaction", "r")
            data : list[dict] = json.load(file)
            data.append(FinishedData)

            json.dump(data,file, indent=4)
            return True

        def remove():
            pass

        def modify():
            pass

        # If statements
        if choice == "add":
            await add()

        elif choice == "remove":
            remove()

        elif choice == "modify":
            modify()
