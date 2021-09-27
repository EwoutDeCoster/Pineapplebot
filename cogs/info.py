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
import datetime
from datetime import timedelta
from decimal import Decimal
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd

webs = str("Pineapplebot.ga")


class Info(commands.Cog, name='Info'):

    def __init__(self, client):
        self.client = client

    @commands.command(name='website')
    async def website(self, ctx):
        embed = discord.Embed(title="Website", url="https://www.pineapplebot.ga/",
                              description="You can visit our website for more information about the bot by clicking on the title.",
                              color=0x0a4d8b)
        embed.set_author(
            name="Pineapple", icon_url=f"{ctx.author.avatar_url}")
        embed.set_thumbnail(
            url="https://pineappleserver.ga/assets/images/pineapple-transp.png")
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)
        print(f'{ctx.author} used Website cmd')

    @commands.command(name='invite')
    async def invite(self, ctx):
        await ctx.send('The invite link has been sent to you in a dm!')
        await ctx.author.send(':link:  **- Pineapple invite url-** \n \nhttps://discord.com/oauth2/authorize?client_id=463388759866474506&scope=bot&permissions=261992480759')
        message = ctx.message
        await message.add_reaction("<:check_pine:834872371281264661>")
        print(f'{ctx.author} used Invite cmd')

    @commands.command(name="chamilo")
    @commands.guild_only()
    async def chamilo(self, ctx):
        embed = discord.Embed(title="HoGent", url="https://login.hogent.be/",
                              description="Hogent login", color=0xffffff)
        embed.set_author(
            name="Pineapple", icon_url=f"{ctx.author.avatar_url}")
        embed.set_thumbnail(
            url="https://fedserv.ads.hogent.be/adfs/portal/logo/logo.png?id=ED23A82D0E5C16C313E81FBCAE1AB77DF511C0650DEC60879D1607737A4213A6")
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)
        print(f'{ctx.author} used Chamilo cmd')

    @commands.command(name='ufora')
    @commands.guild_only()
    async def ufora(self, ctx):
        embed = discord.Embed(title="UGent", url="https://login.ugent.be/login?",
                              description="UGent login", color=0xffffff)
        embed.set_author(
            name="Pineapple", icon_url=f"{ctx.author.avatar_url}")
        embed.set_thumbnail(url="https://www.ugent.be/logo.png")
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)
        print(f'{ctx.author} used Ufora cmd')

    @commands.command(name="artist")
    @commands.guild_only()
    async def artist(self, ctx, *, artist):
        try:
            r = requests.get(
                f"https://api.deezer.com/artist/{artist}")
            d = r.json()
            name = d["name"]
            link = d["link"]
            picture = d["picture_big"]
            followers = d["nb_fan"]
            albums = d["nb_album"]

            embed = discord.Embed(
                title=f"{name}", url=f"{link}", color=0x00ccff)
            embed.set_author(
                name="Deezer", icon_url=f"https://e-cdns-files.dzcdn.net/img/common/opengraph-logo.png")
            embed.add_field(name="👨‍👩‍👧‍👦 Followers",
                            value=f"{followers}", inline=True)
            embed.add_field(name="💽 Albums", value=f"{albums}", inline=True)
            embed.set_image(
                url=f"{picture}")
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(
                name="Usage:", value="`-artist [name]`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(name="fruit")
    @commands.guild_only()
    async def fruit(self, ctx, fruit):
        vrucht = fruit
        try:

            r = requests.get(f"https://www.fruityvice.com/api/fruit/{vrucht}")
            d = r.json()
            name = d["name"]
            carbo = d["nutritions"]["carbohydrates"]
            pro = d["nutritions"]["protein"]
            fat = d["nutritions"]["fat"]
            calo = d["nutritions"]["calories"]
            sug = d["nutritions"]["sugar"]

            embed = discord.Embed(
                title=f"{name}", description="nutritional values (/100g):", color=0xffc800)
            embed.add_field(name="Calories", value=f"{calo}", inline=True)
            embed.add_field(name="Carbohydrates",
                            value=f"{carbo}g", inline=True)
            embed.add_field(name="Protein", value=f"{pro}g", inline=True)
            embed.add_field(name="Fat", value=f"{fat}g", inline=True)
            embed.add_field(name="Sugar", value=f"{sug}g", inline=True)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(
                name="Usage:", value="`-fruit [name]`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(name="movie")
    @commands.guild_only()
    async def movie(self, ctx, *, name):
        try:
            movie = name
            key = "5e765da300e3f42f23ba5924af46b6c5"
            r = requests.get(
                f'https://api.themoviedb.org/3/search/movie?api_key={key}&query={movie}')
            d = r.json()
            title = d["results"][0]["original_title"]
            description = d["results"][0]["overview"]
            rating = d["results"][0]["vote_average"]
            date = d["results"][0]["release_date"]
            movieimg = d["results"][0]["poster_path"]
            lang = d["results"][0]["original_language"]

            embed = discord.Embed(
                title=f"{title}", description=f"{description}", color=0xffc800)
            embed.add_field(name="⭐Rating", value=f"{rating}/10", inline=True)
            embed.add_field(name="⌛ Release date",
                            value=f"{date}", inline=True)
            embed.add_field(name="💬 Language", value=f"{lang}", inline=True)
            embed.set_image(
                url=f"https://www.themoviedb.org/t/p/w600_and_h900_bestv2{movieimg}")
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(
                name="Usage:", value="`-movie [name]`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(name="steam")
    @commands.guild_only()
    async def steam(self, ctx, name):
        try:
            success = 0
            key = "602D5C46267114B070AB9A92AEA978F3"
            r = requests.get(
                f'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={key}&vanityurl={name}')
            d = r.json()
            sid = d["response"]["steamid"]
            success = d["response"]["success"]
        except:
            await ctx.send(f"**Player {name} doesn't exist or the profile is private!**\nMake sure your have your **vanity url** set!\n https://www.maketecheasier.com/assets/uploads/2017/11/how-to-find-steam-id-custom-url.jpg.webp")
        if success == 1:
            try:
                q = requests.get(
                    f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={sid}")
                s = q.json()
                steamid = s["response"]["players"][0]["steamid"]
                username = s["response"]["players"][0]["personaname"]
                profileurl = s["response"]["players"][0]["profileurl"]
                icon = s["response"]["players"][0]["avatarfull"]
                lastlogoff = s["response"]["players"][0]["lastlogoff"]
                realname = s["response"]["players"][0]["realname"]
                statuss = s["response"]["players"][0]["personastate"]

                rr = requests.get(
                    f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={key}&steamid={sid}&format=json")
                g = rr.json()

                games = g["response"]["game_count"]

                lp = requests.get(
                    f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={key}&steamid={sid}&format=json")
                gm = lp.json()

                lastplayed = gm["response"]["games"][0]["name"]
                lastplayedtime = gm["response"]["games"][0]["playtime_2weeks"]

                lastonline = time.ctime(lastlogoff)

                if statuss == 0:
                    status = "⚪ Offline"
                if statuss == 1:
                    status = "🟢 Online"
                if statuss == 2:
                    status = "🔴 Busy"
                if statuss == 3:
                    status = "🟠 Away"
                if statuss == 4:
                    status = "⏰ Snooze"
                if statuss == 5:
                    status = "👀 Looking for trade"
                if statuss == 6:
                    status = "🎲 Looking to play"

                embed = discord.Embed(
                    title=f"{username}", url=f"{profileurl}", color=0x0168b7)
                embed.set_thumbnail(url=f"{icon}")
                embed.add_field(name="Real name",
                                value=f"{realname}", inline=True)
                embed.add_field(name="Status", value=f"{status}", inline=True)
                embed.add_field(name="Games", value=f"{games}", inline=True)
                embed.add_field(
                    name="Recently played", value=f"{lastplayed} ({lastplayedtime} min / 2weeks)", inline=True)
                embed.set_footer(
                    text=f"Last online: {lastonline} | id: {steamid}")
                await ctx.send(embed=embed)

            except:
                await ctx.send(f"**⚠ | Player {name} doesn't exist or the profile is private!**\n   Make sure your have your **vanity url** set!\n https://www.maketecheasier.com/assets/uploads/2017/11/how-to-find-steam-id-custom-url.jpg.webp")

    @commands.command()
    @commands.guild_only()
    async def coc(self, ctx, cocid):
        try:

            headers = {
                'Accept': 'application/json',
                'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjVmMWI3ZTRiLWI3M2EtNGZmZi1hZWY1LTAwMDI5MTEwNGRkZCIsImlhdCI6MTYxNjg5MDM0MCwic3ViIjoiZGV2ZWxvcGVyL2MwZTRhNjAxLTc2YTMtYzFkYS1kZDU4LTIwMDhiN2JjMDY3NSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjYyLjE3MS4xNzUuMjIzIl0sInR5cGUiOiJjbGllbnQifV19.XaAzzXqvEB8Dg8q0syVUqmzJo_i9qbA6v7v5teq6cE7IpVyxcT1UvFAXTLcLIC9jF-Zw16s73evm2hEnGVKeBQ',
            }

            r = requests.get(
                f'https://api.clashofclans.com/v1/players/%23{cocid}', headers=headers)
            d = r.json()
            name = d["name"]
            thlevel = d["townHallLevel"]
            explvl = d["expLevel"]
            trophies = d["trophies"]

            builderHlevel = d["builderHallLevel"]
            builderbattlewins = d["versusBattleWins"]
            clanname = d["clan"]["name"]
            clanlvl = d["clan"]["clanLevel"]
            clanbadge = d["clan"]["badgeUrls"]["large"]

            embed = discord.Embed(title="Clash of Clans stats", color=0xffbb00)
            embed.set_thumbnail(
                url="https://images-na.ssl-images-amazon.com/images/I/81MYd8u7plL.png")
            embed.add_field(name="Name", value=f"{name}", inline=True)
            embed.add_field(name="Townhall",
                            value=f"Level {thlevel}", inline=True)
            embed.add_field(name="XP level", value=f"{explvl}", inline=True)
            embed.add_field(name="Trophies", value=f"{trophies}", inline=True)
            embed.add_field(name="Builderhall",
                            value=f"Level {builderHlevel}", inline=True)
            embed.add_field(name="Builder victories",
                            value=f"{builderbattlewins}", inline=True)

            c = discord.Embed(color=0xffbb00)
            c.set_thumbnail(url=f"{clanbadge}")
            c.add_field(name="Clan", value=f"{clanname}", inline=True)
            c.add_field(name="Clan level", value=f"{clanlvl}", inline=True)
            c.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
            await ctx.send(embed=c)
        except:
            await ctx.send("**⚠ | Use a valid clash of clans playertag.**")

    @commands.command()
    @commands.guild_only()
    async def guilds(self, ctx):
        await ctx.message.reply(f"🍍 **| Pineapple is currently in `{len(self.client.guilds)}` servers!**")

    @commands.command(name="guildinfo")
    @commands.guild_only()
    async def guild_info(self, ctx):
        header = f"Server information - {ctx.guild.name}\n\n"
        rows = {
            "Name": ctx.guild.name,
            "ID": ctx.guild.id,
            "Region": str(ctx.guild.region).title(),
            "Owner": ctx.guild.owner.display_name,
            "Shard ID": ctx.guild.shard_id,
            "Created on": ctx.guild.created_at.strftime("%d/%m/%y %H:%M:%S"),
            "Most recent member": [Member for Member in ctx.guild.members if Member.joined_at is max([Member.joined_at for Member in ctx.guild.members])][0].display_name,
            "...joined": max([Member.joined_at for Member in ctx.guild.members]).strftime("%d/%m/%y %H:%M:%S"),
            "Nº of members": len(ctx.guild.members),
            "...of which human": len([Member for Member in ctx.guild.members if not Member.bot]),
            "...of which bots": len([Member for Member in ctx.guild.members if Member.bot]),
            "Nº of banned members": len(await ctx.guild.bans()),
            "Nº of categories": len(ctx.guild.categories),
            "Nº of text channels": len(ctx.guild.text_channels),
            "Nº of voice channels": len(ctx.guild.voice_channels),
            "Nº of roles": len(ctx.guild.roles),
            "Nº of invites": len(await ctx.guild.invites()),
        }
        table = header + \
            "\n".join(
                [f"{key}{' '*(max([len(key) for key in rows.keys()])+2-len(key))}{value}" for key, value in rows.items()])
        await ctx.message.reply(f"```{table}```{ctx.guild.icon_url}")

    async def get_badges(self, user):
        flags = user.public_flags
        badges = {
            "partner": "<:partner:834863803216691282>",
            "hypesquad": "<:HypeSquad:834863616816709736>",
            "hypesquad_bravery": "<:bravery:834863577457754193>",
            "hypesquad_brilliance": "<:brilliance:834863518058414090>",
            "hypesquad_balance": "<:balance:834863316630896670>",
            "verified_bot_developer": "<:bot_developer:834863380434911292>"
        }
        text = ""
        if flags.hypesquad_balance:
            text += f'{badges["hypesquad_balance"]} '
        if flags.hypesquad_bravery:
            text += f'{badges["hypesquad_bravery"]} '
        if flags.hypesquad_brilliance:
            text += f'{badges["hypesquad_brilliance"]} '
        if flags.verified_bot_developer:
            text += f'{badges["verified_bot_developer"]} '
        if flags.hypesquad:
            text += f'{badges["hypesquad"]} '
        if flags.partner:
            text += f'{badges["partner"]} '
        if not user.premium_since is None:
            text += '<:booster:834863416773574686>'
        if not text == "":
            return text
        else:
            return "None"

    @commands.command(name="userinfo")
    @commands.guild_only()
    async def _userinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

        status_types = {
            "online": "<:online:834874755793944606>",
            "offline": "<:offline:834874855274184704>",
            "idle": "<:idle:834874781160570941>",
            "dnd": "<:dnd:834874823922548746>"
        }

        roles = f"{ctx.guild.default_role}, "
        for role in user.roles:
            if not role.id == ctx.guild.id:
                roles += f"<@&{role.id}>, "
            else:
                continue
        roles = roles[:-2]

        joined_at = f"{user.joined_at.strftime('%d/%m/%Y at %H:%M')} "
        created_at = f"{user.created_at.strftime('%d/%m/%Y at %H:%M')} "

        embed = discord.Embed(color=user.color)
        embed.set_author(name=user,
                         icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)

        embed.add_field(name="ID",
                        value=user.id)
        embed.add_field(name="Status",
                        value=f"{status_types[user.raw_status]}")
        embed.add_field(name="Badges",
                        value=await self.get_badges(user))
        embed.add_field(name="Dates",
                        value=f"**Created At:** {created_at}\n**Joined At:** {joined_at}",
                        inline=False)
        embed.add_field(name="Roles",
                        value=roles,
                        inline=False)
        await ctx.message.reply(embed=embed)

    @commands.command()
    async def testja(self, ctx):
        created_at = f"{ctx.author.created_at.strftime('%d/%m/%Y')}"
        await ctx.send(f"")

    @commands.command()
    @commands.guild_only()
    async def profile(self, ctx):
        created_at = f"{ctx.author.created_at.strftime('%d/%m/%Y')}"
        embed = discord.Embed(
            title="Profile", url=f"https://www.pineapplebot.ga/profile?&username={ctx.author.name}&createdon={created_at}&id={ctx.author.id}&discriminator={ctx.author.discriminator}&image={str(ctx.author.avatar_url)}", description=f"Go to your profile by clicking [here](https://www.pineapplebot.ga/profile?&username={ctx.author.name}&createdon={created_at}&id={ctx.author.id}&discriminator={ctx.author.discriminator}&image={str(ctx.author.avatar_url)}).", color=0x0a4d8b)
        embed.set_thumbnail(url=ctx.author.avatar_url_as(size=256))
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.message.reply(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def crypto(self, ctx, *, cc=None):
        try:
            if cc is None:
                ccbed = discord.Embed(
                    title='Command Usage:', description=f'-crypto [crypto currency]', color=0x0a4d8b, timestamp=datetime.utcnow())
                await ctx.send(embed=ccbed)

            else:
                loading = discord.Embed(color=0x0a4d8b,
                                        description=f"<a:loading:841639840785498173> Getting {cc} stats.")
                loadmes = await ctx.send(embed=loading)

                url = f"https://api.coingecko.com/api/v3/coins/{cc}?market_data=true&community_data=true&developer_data=true&sparkline=true"
                stats = requests.get(url)
                d = stats.json()
                sym = d["symbol"]
                try:
                    if d["market_data"]["price_change_24h"] >= 0:
                        pc = "<:arrow_up:835293504518357062>"
                    else:
                        pc = "<:arrow_down:835293537780236347>"

                    if d["market_data"]["price_change_percentage_24h"] >= 0:
                        day = "<:arrow_up:835293504518357062>"
                    else:
                        day = "<:arrow_down:835293537780236347>"

                    if d["market_data"]["price_change_percentage_7d"] >= 0:
                        week = "<:arrow_up:835293504518357062>"
                    else:
                        week = "<:arrow_down:835293537780236347>"

                    if d["market_data"]["price_change_percentage_30d"] >= 0:
                        month = "<:arrow_up:835293504518357062>"
                    else:
                        month = "<:arrow_down:835293537780236347>"

                    if d["market_data"]["price_change_percentage_1y"] >= 0:
                        year = "<:arrow_up:835293504518357062>"
                    else:
                        year = "<:arrow_down:835293537780236347>"

                    embed = discord.Embed(title=f'{d["name"]} ({sym.upper()})',
                                          description=f'These are the current stats of {d["name"]}.', color=0x0a4d8b)

                    embed.add_field(
                        name="Current price", value=f'€ {round(Decimal(d["market_data"]["current_price"]["eur"]), 8)}', inline=True)

                    embed.add_field(name="Price change 24h",
                                    value=f'{pc}  € {round(Decimal(d["market_data"]["price_change_24h"]), 8)}', inline=True)

                    embed.set_thumbnail(url=f'{d["image"]["large"]}')

                    perc = discord.Embed(color=0x0a4d8b)

                    perc.add_field(
                        name="Last 24h", value=f'{day} {d["market_data"]["price_change_percentage_24h"]}%', inline=True)

                    perc.add_field(
                        name="Last 7d", value=f'{week} {d["market_data"]["price_change_percentage_7d"]}%', inline=True)

                    perc.add_field(
                        name="Last month", value=f'{month} {d["market_data"]["price_change_percentage_30d"]}%', inline=True)

                    perc.add_field(
                        name="Last year", value=f'{year} {d["market_data"]["price_change_percentage_1y"]}%', inline=True)

                    await loadmes.edit(embed=embed)
                    await ctx.send(embed=perc)
                except:
                    ccbed3 = discord.Embed(
                        title="Invalid crypto currency.", color=0x0a4d8b, timestamp=datetime.utcnow())
                    ccbed3.set_author(name="Error!")
                    await loadmes.edit(embed=ccbed3)

        except:
            ccbed3 = discord.Embed(
                title="Invalid crypto currency.", color=0x0a4d8b, timestamp=datetime.utcnow())
            ccbed3.set_author(name="Error!")
            await loadmes.edit(embed=ccbed3)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def covid(self, ctx):
        embed = discord.Embed(title="Covid commands", color=0x00eeff)
        embed.set_thumbnail(
            url="https://www.keckmedicine.org/wp-content/uploads/2020/12/covid-vaccine.png")
        embed.add_field(name="-covid vaccines",
                        value=f"Get an overview of all first and second doses.", inline=True)
        embed.add_field(name="-covid delivered",
                        value=f"Get a list of all the vaccines types and the amount delivered.", inline=True)
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @covid.group(invoke_without_command=True)
    @commands.guild_only()
    async def vaccines(self, ctx):
        url = f"https://covid-vaccinatie.be/api/v1/administered.json"
        stats = requests.get(url)
        d = stats.json()
        arr = d["result"]["administered"]
        up = requests.get(
            "https://covid-vaccinatie.be/api/v1/last-updated.json")
        l = up.json()
        lastupdate = l["result"]["last_updated"]["updated"]
        i = 0
        first = 0
        sec = 0
        while i < len(arr):
            first += d["result"]["administered"][i]["first_dose"]
            sec += d["result"]["administered"][i]["second_dose"]
            i += 1
        embed = discord.Embed(title="Vaccinations in Belgium", color=0x00eeff)
        embed.set_thumbnail(
            url="https://www.keckmedicine.org/wp-content/uploads/2020/12/covid-vaccine.png")
        embed.add_field(name="First dose", value=f"{first:,}", inline=True)
        embed.add_field(name="Second dose", value=f"{sec:,}", inline=True)
        embed.set_footer(text=f"Last updated: {lastupdate}")
        await ctx.send(embed=embed)

    @covid.command()
    @commands.guild_only()
    async def delivered(self, ctx):
        url = f"https://covid-vaccinatie.be/api/v1/delivered.json"
        stats = requests.get(url)
        up = requests.get(
            "https://covid-vaccinatie.be/api/v1/last-updated.json")
        l = up.json()
        d = stats.json()
        arr = d["result"]["delivered"]
        lastupdate = l["result"]["last_updated"]["updated"]
        astra = 0
        pfizer = 0
        johnson = 0
        moderna = 0
        i = 0
        while i < len(arr):
            if d["result"]["delivered"][i]["manufacturer"] == "Pfizer/BioNTech":
                pfizer += d["result"]["delivered"][i]["amount"]
            if d["result"]["delivered"][i]["manufacturer"] == "AstraZeneca/Oxford":
                astra += d["result"]["delivered"][i]["amount"]
            if d["result"]["delivered"][i]["manufacturer"] == "Johnson&Johnson":
                johnson += d["result"]["delivered"][i]["amount"]
            if d["result"]["delivered"][i]["manufacturer"] == "Moderna":
                moderna += d["result"]["delivered"][i]["amount"]
            i += 1
        embed = discord.Embed(
            title="Vaccines delivered to Belgium", color=0x00eeff)
        embed.set_thumbnail(
            url="https://www.keckmedicine.org/wp-content/uploads/2020/12/covid-vaccine.png")
        embed.add_field(name="Pfizer / BioNTech",
                        value=f"{pfizer:,}", inline=False)
        embed.add_field(name="AstraZeneca / Oxford",
                        value=f"{astra:,}", inline=False)
        embed.add_field(name="Johnson & Johnson",
                        value=f"{johnson:,}", inline=False)
        embed.add_field(name="Moderna", value=f"{moderna:,}", inline=False)
        embed.set_footer(text=f"Last updated: {lastupdate}")
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def trading(self, ctx):
        await ctx.send("het werkt")

    @trading.command()
    @commands.guild_only()
    async def day(self, ctx, arg, dayone, daytwo):
        try:
            msft = yf.Ticker(f'{arg}').history(
                start=f'{dayone}', end=f'{daytwo}', interval='5m')
            mpf.plot(msft, type='candle', volume=True,
                     title=f"{arg.upper()} {dayone}",
                     figratio=(14, 6),
                     mav=(5, 10, 30), tight_layout=True,
                     style='mike', savefig='msft.png')
            print(msft)
            await ctx.send(file=discord.File('msft.png'))
        except:
            await ctx.send("**⚠ | Make sure all information is correct.**")


def setup(client):
    client.add_cog(Info(client))
    print('Info loaded succesfully')
