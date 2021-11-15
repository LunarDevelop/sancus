import discord
from sancus.functions.objects import Embeds


class reporting():

    async def caseReport(self, ctx, type, message, user=None):
        """This will detect if there is a case already reported and get the number for the next report
        
        self -> the bot itself
        ctx -> context of the report, so can send a message to the guild if need.
        type -> the type of report you are sending
        message -> the message for the case report
        user -> if want to include the user in the case embed (might not be used just exploring options)
        
        returns ->
                    case number -> so can send to the user and reply to the user who made the case
                    message link -> so can automatically be direct to the channel"""

        guild = self.guilds_[str(ctx.guild.id)]
        caseChannel = guild["caseChannel"]
        try:
            caseChannel = await ctx.guild.fetch_channel(int(caseChannel))
        except TypeError:
            return None

        id = caseChannel.last_message_id

        if id == None:

            embed = Embeds(
                title=f"Case #1 | {type.upper()}",
                description=message,
                colour=0x0002C2F33
            )

            return await caseChannel.send(embed=embed)
        
        msg =  await caseChannel.fetch_message(id)

        msg_embed : discord.Embed = msg.embeds[0]
        msg_num = int(msg_embed.title.split(" | ")[0].replace("Case #", ""))
        case_num = msg_num + 1

        embed = Embeds(
            title=f"Case #{case_num} | {type.upper()}",
            description=message,
            color=0x0002C2F33
        )

        return await caseChannel.send(embed=embed)