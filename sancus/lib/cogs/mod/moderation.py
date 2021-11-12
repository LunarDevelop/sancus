import discord
from discord.ext.commands import Cog
from discord.message import Message

class antispam(Cog):
    
    def __init__(self, client) -> None:
        super().__init__()
        
        self.client = client
        
        
    @Cog.listener()
    async def on_message(self, msg:Message):
        if not msg.author.bot:
            mentionList = msg.mentions + msg.role_mentions
            
            if len(mentionList) > 5:
                await msg.delete()
    