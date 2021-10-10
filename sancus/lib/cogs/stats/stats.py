import discord
from discord.ext import commands
import json
import requests


class Stats(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def covid(self, ctx, *, country="global"):
        embed = discord.Embed(
            title="CoronaVirus COVID-19 Updates",
            colour=discord.Colour.gold()
        )

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/780587146163650580/780834378406035476/Virus-PNG-Pic.png")

        if country == "global":
            confirmed, deaths, recovered = get_gobal_covid()
            embed.add_field(
                name=f'Location: {country}', value=f"Confirmed cases: {confirmed}\nRecovered cases: {recovered}\nDeaths: {deaths}")

        else:
            name, slug = get_slug(country)

            confirmed, deaths, recovered, active = get_country_stats(slug)

            embed.add_field(
                name=f'Location: {name}', value=f"Confirmed cases: {confirmed}\nActive cases: {active}\nRecovered cases: {recovered}\nDeaths: {deaths}")

        await ctx.send(embed=embed)


def get_gobal_covid():
    url = "https://api.covid19api.com/world/total"

    response = requests.request("GET", url)

    data = response.json()

    confirmed = data['TotalConfirmed']
    deaths = data['TotalDeaths']
    recovered = data['TotalRecovered']

    return confirmed, deaths, recovered


def get_slug(country):
    url = "https://api.covid19api.com/countries"
    response = requests.request("GET", url)
    data = response.json()

    for countries in data:
        if countries['Country'].lower() == country or countries['ISO2'].lower() == country.lower():
            return countries['Country'], countries['Slug']


def get_country_stats(slug):
    url = f"https://api.covid19api.com/live/country/{slug}"
    response = requests.request("GET", url)
    data = response.json()

    confirmed = 0
    deaths = 0
    recovered = 0
    active = 0

    for days in data:
        confirmed += days['Confirmed']
        deaths += days['Deaths']
        recovered += days['Recovered']
        active += days['Active']

    return confirmed, deaths, recovered, active
