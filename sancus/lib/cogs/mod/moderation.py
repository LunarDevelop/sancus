import discord
from discord.abc import Message
from discord.ext.commands import Cog

class antispam(Cog):
    
    def __init__(self, client) -> None:
        super().__init__()
        
        self.client = client
        
        
    @Cog.listener(name="Anti Mention Spam")
    async def on_message(self, msg:Message):
        mentionList = msg.mentions
        
        if len(mentionList) > 5:
            await msg.delete()
    