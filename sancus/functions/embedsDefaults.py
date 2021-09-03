from discord import Embed
from .config import config

from datetime import datetime
import time

config = config()


class EmbedDefaults():

    def timeout(self, ctx, guildid):
        embed = Embed(
            title="Timed out",
            description="This embeded menu has timed out. Rerun the command to get the menu back.",
            colour=config.embed(guildid, "main_timeout"),
            timestamp=datetime.utcnow()
        )

        # Add thumbnail / add custom thumbnail system
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/819496847990063114/819497096692498452/clock.png")

        return embed

    def cancel(self, ctx, guildid):
        embed = Embed(
            title="Canceled",
            description="This embeded menu has been canceled. Rerun the command to get the menu back.",
            colour=config.embed(guildid, "main_cancel"),
            timestamp=datetime.utcnow()
        )

        # Add thumbnail / add custom thumbnail system
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/819496847990063114/819497119953584148/x-png-18.png")

        return embed
