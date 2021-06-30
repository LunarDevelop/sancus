from discord.ext.commands import Cog

import statcord
import json

from .discordservices import discordServices

from datetime import datetime, timedelta

class services(
    discordServices,
    Cog):

    def __init__(self, client):
        self.client = client
        self.key = "statcord.com-1po1xPOflYwkobUIerDB"
        self.api = statcord.Client(self.client,self.key)
        self.api.start_loop()


    @Cog.listener()
    async def on_command(self,ctx):
        self.api.command_run(ctx)

        with open('./data/botData.json', 'r') as f:
            data = json.load(f)

        today = datetime.utcnow()
        weekago = timedelta(days=7)
        dayOfWeek = (today - weekago).strftime("%d/%m/%Y")
        
        try:
            data['commands'][ctx.command.name]['usage'] += 1
            data['commands'][ctx.command.name]['last_used'] = datetime.timestamp(datetime.utcnow())

        except KeyError:
            data['commands'][ctx.command.name] = {
                "usage" : 1,
                "last_used" : datetime.timestamp(datetime.utcnow())
            }

        try:
            data['perDay'][today.strftime("%d/%m/%Y")]['commandsUsed'] += 1

            if ctx.author.id not in data['perDay'][today.strftime("%d/%m/%Y")]['engageUsers']:
                data['perDay'][today.strftime("%d/%m/%Y")]['engageUsers'].append(ctx.author.id)

            data['perDay'][today.strftime("%d/%m/%Y")]['totalUsers'] = len(self.client.users)

        except:
            data['perDay'][today.strftime("%d/%m/%Y")] ={
                'commandsUsed' : 1,
                'engageUsers' : [ctx.author.id],
                'totalUsers' : len(self.client.users)
            }

            if dayOfWeek in data['perDay']:
                data['perDay'].pop(dayOfWeek)

        with open('./data/botData.json', 'w') as f:
            json.dump(data, f, indent=4)