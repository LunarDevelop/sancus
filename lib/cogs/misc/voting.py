import discord
from discord.ext import commands

import requests
import json
import asyncio

class Polls(commands.Cog):

    def __init__(self, client):
        self.client = client

    def createPoll(self, data):

        url = "https://strawpoll.com/api/poll"

        apiKey = "UZ29S6O8HFCWA9BJSCKSK7UUD93SC3RF"

        headers = {'API-KEY':apiKey}

        poll = requests.post(url, json=data, headers=headers).json()

        return poll

    def getResults(self, poll):
        answerList = []
        url = f"https://strawpoll.com/api/poll/{poll}"

        request = requests.get(url)
        request = request.json()

        for answersList in request['content']['poll']['poll_answers']:
            answers = (answersList['answer'], answersList['votes'])
            answerList.append(answers)
        return answerList

    @commands.command()
    async def create_poll(self, ctx):
        print("Poll creation requested")
        titleC = False
        answersC = False
        maC = False

        await ctx.send("Please enter the question or topic.")

        while True:
            while titleC != True:
                try:
                    title = await self.client.wait_for("message", timeout= 90.0)
                    if title.author.id == ctx.author.id:
                        titleM = title.content

                        await ctx.send(f"Your question is : {titleM}")
                        titleC = True
                        break

                except asyncio.TimeoutError:
                    await ctx.send("Timed out. Try again")
                    return
            
            await ctx.send("Please enter the question or topic.")
            while answersC != True:
                try:
                    answers = await self.client.wait_for("message", timeout= 90.0)
                    if answers.author.id == ctx.author.id:
                        answers = answers.content

                        answersList = answers.split(',')

                        await ctx.send(f"Your answers are : {answersList}")
                        answersC = True
                        break

                except asyncio.TimeoutError:
                    await ctx.send("Timed out. Try again")
                    return

            await ctx.send("Multiple answers: True or False")

            while maC != True:

                try:
                    ma = await self.client.wait_for("message", timeout= 90.0)
                    if ma.author.id == ctx.author.id:
                        ma = ma.content
                        ma = ma.capitalize() 

                        await ctx.send(f"Your answers are : {ma}")
                        maC = True
                        break


                except asyncio.TimeoutError:
                    await ctx.send("Timed out. Try again")
                    return

            if titleC and answersC and maC:
                break
        
        data={
            "poll": {
                "title": titleM,
                "answers": answersList,
                "ma": ma
            }
            }

        contents = (self.createPoll(data))

        id_ = contents['content_id']

        link = "https://strawpoll.com/"+ id_

        await ctx.send(f"Here is the link to your straw poll: \n{link}")
        



          
