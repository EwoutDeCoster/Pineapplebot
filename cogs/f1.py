import discord
from discord.ext import commands
import asyncio
import datetime
import time
import random
import os
import urllib
import requests
import sys


webs = str("Pineapplebot.ga")


class F1(commands.Cog, name='F1'):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def f1(self, ctx):
        embed = discord.Embed(
            title="F1 commands", description="List of all the available F1 commands.", color=0xff0000)
        embed.set_thumbnail(
            url="https://logodownload.org/wp-content/uploads/2016/11/formula-1-logo-7.png")
        embed.add_field(name="-f1 races (optional: year)",
                        value="Get all the races from a year.", inline=False)
        embed.add_field(name="-f1 lastrace",
                        value="Get the result of last race.", inline=False)
        embed.add_field(name="-f1 standings drivers",
                        value="Get the drivers standings.", inline=False)
        embed.add_field(name="-f1 standings constructors",
                        value="Get the constructors standings.", inline=False)
        embed.add_field(name="-f1 champion (optional: year)",
                        value="Get the champion from a year.", inline=False)
        embed.add_field(name="-f1 lastqualifying",
                        value="Get the the results of last qualifying", inline=False)
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @f1.command()
    @commands.guild_only()
    async def races(self, ctx, yr=2021):
        r = requests.get(f"https://ergast.com/api/f1/{yr}.json")
        d = r.json()
        year = d["MRData"]["RaceTable"]["season"]
        races = d["MRData"]["RaceTable"]["Races"]
        i = 0
        embed = discord.Embed(
            title=f"F1 {year}", description=f"These are the races of the {year} Formula 1 season", color=0xff0000)
        embed.set_thumbnail(
            url="https://logodownload.org/wp-content/uploads/2016/11/formula-1-logo-7.png")
        while i < len(races):
            name = d["MRData"]["RaceTable"]["Races"][i]["raceName"]
            date = d["MRData"]["RaceTable"]["Races"][i]["date"]

            embed.add_field(name=f"{i+1} {name}",
                            value=f"{date}", inline=True)
            i += 1

        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @f1.command()
    @commands.guild_only()
    async def lastrace(self, ctx):
        r = requests.get(f"http://ergast.com/api/f1/current/last/results.json")
        d = r.json()
        race = d["MRData"]["RaceTable"]["Races"][0]["raceName"]
        fullrace = d["MRData"]["RaceTable"]["Races"][0]["Circuit"]["circuitName"]
        date = d["MRData"]["RaceTable"]["Races"][0]["date"]
        drivers = d["MRData"]["RaceTable"]["Races"][0]["Results"]
        i = 0
        embed = discord.Embed(
            title=f"F1 - {race}", description=f"Last race was at {fullrace} on {date}.", color=0xff0000)
        embed.set_thumbnail(
            url="https://logodownload.org/wp-content/uploads/2016/11/formula-1-logo-7.png")
        while i < len(drivers):
            pos = d["MRData"]["RaceTable"]["Races"][0]["Results"][i]["position"]
            dnfornot = d["MRData"]["RaceTable"]["Races"][0]["Results"][i]["positionText"]
            drivervn = d["MRData"]["RaceTable"]["Races"][0]["Results"][i]["Driver"]["givenName"]
            driveran = d["MRData"]["RaceTable"]["Races"][0]["Results"][i]["Driver"]["familyName"]
            if "R" in dnfornot:
                dnf = "DNF - "
            else:
                dnf = ""
            embed.add_field(name=f"{drivervn} {driveran}",
                            value=f"{dnf}Place: {pos}", inline=True)
            i += 1

        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @f1.command()
    @commands.guild_only()
    async def lastqualifying(self, ctx):
        r = requests.get(
            f"http://ergast.com/api/f1/current/last/qualifying.json")
        d = r.json()
        race = d["MRData"]["RaceTable"]["Races"][0]["raceName"]
        fullrace = d["MRData"]["RaceTable"]["Races"][0]["Circuit"]["circuitName"]
        date = d["MRData"]["RaceTable"]["Races"][0]["date"]
        drivers = d["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"]
        i = 0
        embed = discord.Embed(
            title=f"F1 Qualifying - {race}", description=f"Last qualifying was at {fullrace} on {date}.", color=0xff0000)
        embed.set_thumbnail(
            url="https://logodownload.org/wp-content/uploads/2016/11/formula-1-logo-7.png")
        while i < len(drivers):
            drivervn = d["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"][i]["Driver"]["givenName"]
            driveran = d["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"][i]["Driver"]["familyName"]
            try:
                Q = d["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"][i]["Q3"]
                best = "Q3"
            except:
                try:
                    Q = d["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"][i]["Q2"]
                    best = "Q2"
                except:
                    Q = d["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"][i]["Q1"]
                    best = "Q1"
                if Q == "":
                    Q = "NO TIME"
            embed.add_field(name=f"{drivervn} {driveran}",
                            value=f"{best}: {Q}", inline=True)
            i += 1
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @f1.group(invoke_without_command=True)
    @commands.guild_only()
    async def standings(self, ctx):
        await ctx.send("constructors / drivers")

    @standings.command()
    @commands.guild_only()
    async def drivers(self, ctx):
        r = requests.get(
            f"http://ergast.com/api/f1/current/driverStandings.json")
        d = r.json()
        year = d["MRData"]["StandingsTable"]["StandingsLists"][0]["season"]
        roundd = d["MRData"]["StandingsTable"]["StandingsLists"][0]["round"]
        drivers = d["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
        i = 0

        embed = discord.Embed(
            title=f"F1 drivers standings - {year}", description=f"These are the current drivers standings after round {roundd}.", color=0xff0000)
        embed.set_thumbnail(
            url="https://logodownload.org/wp-content/uploads/2016/11/formula-1-logo-7.png")
        while i < len(drivers):
            drivervn = d["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"][i]["Driver"]["givenName"]
            driveran = d["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"][i]["Driver"]["familyName"]
            points = d["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"][i]["points"]
            team = d["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"][i]["Constructors"][0]["name"]
            embed.add_field(name=f"{drivervn} {driveran}",
                            value=f"{team}\nPoints: {points}", inline=True)
            i += 1
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @standings.command()
    @commands.guild_only()
    async def constructors(self, ctx):
        r = requests.get(
            f"https://ergast.com/api/f1/current/constructorStandings.json")
        d = r.json()
        year = d["MRData"]["StandingsTable"]["StandingsLists"][0]["season"]
        roundd = d["MRData"]["StandingsTable"]["StandingsLists"][0]["round"]
        teams = d["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]
        i = 0

        embed = discord.Embed(
            title=f"F1 drivers standings - {year}", description=f"These are the current constructors standings after round {roundd}.", color=0xff0000)
        embed.set_thumbnail(
            url="https://logodownload.org/wp-content/uploads/2016/11/formula-1-logo-7.png")
        while i < len(teams):
            points = d["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"][i]["points"]
            name = d["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"][i]["Constructor"]["name"]
            embed.add_field(name=f"{name}",
                            value=f"Points: {points}", inline=True)
            i += 1
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @f1.command()
    @commands.guild_only()
    async def champion(self, ctx, yr=2020):
        r = requests.get(
            f"http://ergast.com/api/f1/{yr}/driverStandings.json")
        d = r.json()
        year = d["MRData"]["StandingsTable"]["StandingsLists"][0]["season"]
        drivervn = d["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"][0]["Driver"]["givenName"]
        driveran = d["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"][0]["Driver"]["familyName"]
        team = d["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"][0]["Constructors"][0]["name"]
        embed = discord.Embed(
            title=f"F1 World Champion - {year}", description=f"", color=0xff0000)
        embed.set_thumbnail(
            url="https://logodownload.org/wp-content/uploads/2016/11/formula-1-logo-7.png")
        embed.add_field(name=f"{drivervn} {driveran}",
                        value=f"{team}", inline=True)
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(F1(client))
    print('F1 loaded succesfully')
