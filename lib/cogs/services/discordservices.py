from discord.ext.commands import Cog, command

import requests

class discordServices(Cog):

    def __init__(self, client) -> None:
        self.client = client

    @command()
    async def add_server(self, ctx):
        url = "https://api.discordservices.net/bot/341999214043332619/stats"

        data = {
            "servers" : int(len(self.client.guilds))
        }

        headers = {
            "Authorization" : "REDACTED"
        }
        
        response = requests.post(url=url, json=data, headers=headers)

    @Cog.listener()
    async def on_guild_join(self, guild):

        #Discord Bot List 
        url = "https://discordbotlist.com/api/v1/bots/341999214043332619/stats"

        data = {
            "guilds" : len(self.client.guilds),
            "users" : len(self.client.users)
        }

        headers = {
            "Authorization" : "REDACTED"
        }
        
        requests.post(url=url, data=data, headers=headers)

        #DiscordServices.net
        url = "https://api.discordservices.net/bot/341999214043332619/stats"

        data = {
            "servers" : int(len(self.client.guilds))
        }

        headers = {
            "Authorization" : "REDACTED"
        }
        
        requests.post(url=url, json=data, headers=headers)

