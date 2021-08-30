from discord import Embed
import datetime
from typing import TypeVar, Union, Any
from discord import Embed, colour
from discord.types.embed import EmbedType
from discord.embeds import EmptyEmbed, _EmptyEmbed
from discord.colour import Colour


T = TypeVar('T')
MaybeEmpty = Union[T, _EmptyEmbed]


class Embeds(Embed):

    def __init__(self, *,
                 colour: Union[int, Colour, _EmptyEmbed] = EmptyEmbed,
                 color: Union[int, Colour, _EmptyEmbed] = EmptyEmbed,
                 title: MaybeEmpty[Any] = EmptyEmbed,
                 type: EmbedType = EmptyEmbed,
                 url: MaybeEmpty[Any] = EmptyEmbed,
                 description: MaybeEmpty[Any] = EmptyEmbed
                 ):
        super().__init__(colour=colour, color=color, title=title, type=type,
                         url=url, description=description, timestamp=datetime.datetime.utcnow())

        self._footer = {}
        self._footer['text'] = "Lunar Development"
        self._footer['icon_url'] = "https://cdn.discordapp.com/attachments/789247201678327838/879862055404965938/stage_1629845776.jpeg"


class guildObject():

    def __init__(self, guildID):
        self.guildID = guildID
        self.prefix = None
        self.logChannel = None
        self.actionChannel = None
        self.logChannel = None
        self.welcomeChannel = None
        self.welcomeStyle = None
        self.welcomeBanner = None
        self.welcomeIcon = None
