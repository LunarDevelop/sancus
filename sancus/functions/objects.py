from typing import Optional, Union
import json
from discord import Embed
import datetime
from typing import Optional, TypeVar, Union, Any
from discord import Embed, colour

from discord.embeds import EmptyEmbed, _EmptyEmbed
from discord.colour import Colour


T = TypeVar('T')
MaybeEmpty = Union[T, _EmptyEmbed]


class Embeds(Embed):

    def __init__(self, *,
                 colour: Union[int, Colour, _EmptyEmbed] = EmptyEmbed,
                 color: Union[int, Colour, _EmptyEmbed] = EmptyEmbed,
                 title: MaybeEmpty[Any] = EmptyEmbed,
                 type = EmptyEmbed,
                 url: MaybeEmpty[Any] = EmptyEmbed,
                 description: MaybeEmpty[Any] = EmptyEmbed
                 ):
        super().__init__(colour=colour, color=color, title=title, type=type,
                         url=url, description=description, timestamp=datetime.datetime.utcnow())

        self._footer = {}
        self._footer['text'] = "Lunar Development"
        self._footer['icon_url'] = "https://cdn.discordapp.com/attachments/789247201678327838/879862055404965938/stage_1629845776.jpeg"

class warning():
    username : str
    reason : Optional[str]
    date : datetime.datetime

class guildObject():

    def __init__(self,
                 id: int,
                 prefix: str = "s!",
                 filter: bool = False,
                 filterDelete: bool = True,
                 filterWords: Optional[list] = None,
                 logChannel: Optional[int] = None,
                 caseChannel: Optional[int] = None,
                 modCmdChannel: Optional[int] = None,
                 nicknameChannel: Optional[int] = None,
                 autoModChannel: Optional[int] = None,
                 warnings : Optional[list] = None,               
                 welcomeMessage: bool = False,
                 welcomeType: bool = False,  # False means text based # True means banner style
                 welcomeChannel: Optional[int] = None,
                 welcomeText: Optional[str] = "Welcome {user} to {server} server",
                 welcomeBack: Optional[str] = "#00ff00",
                 welcomeBanner: Optional[str] = None,
                 welcomeIcon: Optional[str] = None,
                 welcomeTxtColor: str = "#000000",
                 welcomeUserColor: str = "#000000",
                 welcomeMembersColor: str = "#000000",
                 ) -> None:

        self.id = id
        self.prefix = prefix
        self.filter = filter
        self.filterDelete = filterDelete
        self.filterWords = filterWords
        self.logChannel = logChannel
        self.caseChannel = caseChannel
        self.modCmdChannel = modCmdChannel
        self.nicknameChannel = nicknameChannel
        self.autoModChannel = autoModChannel
        self.warnings = warnings
        self.welcomeMessage = welcomeMessage
        self.welcomeType = welcomeType
        self.welcomeChannel = welcomeChannel
        self.welcomeText = welcomeText
        self.welcomeBack = welcomeBack
        self.welcomeBanner = welcomeBanner
        self.welcomeIcon = welcomeIcon
        self.welcomeTxtColor = welcomeTxtColor
        self.welcomeUserColor = welcomeUserColor
        self.welcomeMembersColor = welcomeMembersColor


class userObject():
    
    def __init__(self,
                 id : int,
                 banks : list[dict] = []) -> None:
        self.id = id
        self.banks = banks
        

class reactObject():

    def __init__(self,
                 id: int,
                 name: str,
                 roles: list,
                 emojis: Optional[list] = None,
                 buttons: Optional[list] = None,
                 selects: Optional[list] = None,
                 ) -> None:
        self.id = id
        self.name = name
        self.roles = roles
        self.emojis = emojis
        self.buttons = buttons
        self.selects = selects
