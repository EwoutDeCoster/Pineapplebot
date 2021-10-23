import discord
from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
import os
from dotenv import load_dotenv
import asyncio
import urllib
import requests
import time
import random
from datetime import datetime, timedelta
import sys
import sqlite3
from discord import Intents
from PIL import Image, ImageDraw, ImageFont
import logging
from io import BytesIO
import math
import json

# Pre made: dev, prob
statuss = "-help | Pineapplebot.ga"
webs = "Pineapplebot.ga"

load_dotenv()
TOKEN = os.getenv('BOTTOKEN')

client = commands.Bot(command_prefix='-',
                      intents=Intents.all(), case_insensitive=True)


dislog = logging.getLogger('discord')
dislog.setLevel(logging.WARNING)
dishdlr = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
dishdlr.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
dislog.addHandler(dishdlr)
client.dislog = dislog

client.remove_command('help')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            client.load_extension(f'cogs.{filename[:-3]}')
        except Exception as e:
            print(f'Failed to load {filename}')
            print(e)


@client.event
async def on_ready():
    print('Bot is online!')
    if statuss == "dev":
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(f'Maintenance pending...'))
    elif statuss == "prob":
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game(f'Currently unavailable'))
    else:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f'{statuss}'))
    db = sqlite3.connect('cogs/main.sqlite')
    cursor = db.cursor()
    sql = (
        "UPDATE botstats SET users = ?, servers = ?, avatar = ?")
    val = (len(client.users), len(client.guilds), str(client.user.avatar_url))
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


@tasks.loop(seconds=3600)  # repeat after every 10 seconds
async def statsloop():
    db = sqlite3.connect('cogs/main.sqlite')
    cursor = db.cursor()
    sql = (
        "UPDATE botstats SET users = ?, servers = ?")
    val = (len(client.users), len(client.guilds))
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


@client.event
async def on_guild_join(guild):
    success = False
    index = 0
    while not success:
        try:
            embed = discord.Embed(
                title="Pineapple", description="Thanks for inviting pineapple to the server!", color=0x0a4d8b)
            embed.add_field(
                name="** **", value="See all commands [here](https://www.pineapplebot.ga/commands).")
            embed.set_thumbnail(url="https://i.imgur.com/rjxnHHM.png")
            embed.set_footer(text=f"{webs}")
            await guild.channels[index].send(embed=embed)
        except discord.Forbidden:
            index += 1
        except AttributeError:
            index += 1
        except IndexError:
            pass
        else:
            success = True
    else:
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT guild_name FROM main WHERE guild_id = {guild.id}")
        result = cursor.fetchone()
        if result is None:
            sql = (
                "INSERT INTO main(guild_id, guild_name, owner, serverlogo) VALUES(?,?,?,?)")
            val = (guild.id, guild.name, guild.owner.id, str(guild.icon_url))
            print(f"{guild.name} has been added to the database")
        else:
            sql = ("INSERT main SET owner = ?, serverlogo = ? where guild_id = ?")
            val = (guild.owner.id, str(guild.icon_url), guild.id)

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

# Delete data wanneer bot gekickt wordt.


@client.event
async def on_guild_remove(guild):
    print(f"Got Kicked: {guild.name} | {guild.id}")
    db = sqlite3.connect('cogs/main.sqlite')
    cursor = db.cursor()
    sql = ("DELETE FROM main WHERE guild_id = ?")
    val = (guild.id)
    cursor.execute(sql, val)

    sql1 = ("DELETE FROM economy WHERE guild = ?")
    val1 = (guild.id)
    cursor.execute(sql1, val1)

    sql2 = ("DELETE FROM leveling WHERE guild_id = ?")
    val2 = (guild.id)
    cursor.execute(sql2, val2)

    sql3 = ("DELETE FROM reactionroles WHERE guild = ?")
    val3 = (guild.id)
    cursor.execute(sql3, val3)

    sql4 = ("DELETE FROM starboard WHERE guild = ?")
    val4 = (guild.id)
    cursor.execute(sql4, val4)

    sql5 = ("DELETE FROM suggestions WHERE guild = ?")
    val5 = (guild.id)
    cursor.execute(sql5, val5)

    sql6 = ("DELETE FROM warnings WHERE guild = ?")
    val6 = (guild.id)
    cursor.execute(sql6, val6)

    db.commit()
    cursor.close()
    db.close()


@client.event
async def on_member_join(member):

    db = sqlite3.connect('cogs/main.sqlite')
    cursor = db.cursor()
    cursor.execute(
        f"SELECT welcomech_id, membercnt_id, welcomedm FROM main WHERE guild_id = {member.guild.id}")
    result = cursor.fetchone()
    if result[0] is None:
        return
    else:
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT welcomemsg FROM main WHERE guild_id = {member.guild.id}")
        result1 = cursor.fetchone()

        guild = member.guild
        channel = client.get_channel(int(result[0]))

        base = Image.open("welcome.png").convert("RGBA")
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

        # get a font
        fnt = ImageFont.truetype(
            "/usr/share/fonts/googlefonts/JetBrainsMono-VariableFont_wght.ttf", 40)
        # get a drawing context
        d = ImageDraw.Draw(txt)

        d.text((260, 70), "Welcome", font=fnt, fill=(255, 255, 255, 128))
        d.text((260, 120), f"{member.display_name}!",
               font=fnt, fill=(255, 255, 255, 255))

        out = Image.alpha_composite(base, txt)
        out.save('nice.png')

        mention = member.mention
        user = member.name
        members = guild.member_count
        server = member.guild.name
        membercount = guild.member_count
        if result[2] is None:
            return
        else:
            await member.send(str(result[2]).format(members=members, server=server, user=user, mention=mention, membercount=membercount))
        try:
            await channel.send(content=str(result1[0]).format(members=members, server=server, user=user, mention=mention), file=discord.File('nice.png'))
        except:
            await channel.send(str(result1[0]).format(members=members, server=server, user=user, mention=mention))
    try:
        channell = guild.get_channel(int(result[1]))
        await channell.edit(name=f'Members: {guild.member_count}')
        print(f'{member} Joined')
    except:
        pass
    try:
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT role FROM main WHERE guild_id = {member.guild.id}")
        wrole = cursor.fetchone()
        rll = discord.utils.get(member.guild.roles, id=int(wrole[0]))
        await member.add_roles(rll)
    except:
        print('error join role')


@client.event
async def on_member_remove(member):
    db = sqlite3.connect('cogs/main.sqlite')
    cursor = db.cursor()
    cursor.execute(
        f"SELECT membercnt_id FROM main WHERE guild_id = {member.guild.id}")
    result = cursor.fetchone()
    try:
        guild = member.guild
        channell = guild.get_channel(int(result[0]))
        await channell.edit(name=f'Members: {guild.member_count}')
    except:
        pass
    cursor.close()
    db.close()


@client.command(name="setbotstatus")
async def setbotstatus(ctx, *, st):
    if ctx.author.id == 302075047244333056:
        await client.change_presence(activity=discord.Game(f'{st}'))
        msg = await ctx.send(f"🤖 | The bot status has changed to \"**{st}**\"")

    else:
        msg = await ctx.send(f"**<a:no:898507018527211540> | {ctx.author.mention} You don't have the perms to do that**")
        await asyncio.sleep(3)
        await msg.delete()


@client.event
async def on_command_error(ctx, Exc):
    if isinstance(Exc, commands.CommandNotFound):
        return
    elif isinstance(Exc, commands.MissingRequiredArgument):
        await ctx.send("<a:no:898507018527211540> **| Missing required argument.**")
        return
    elif isinstance(Exc, commands.BadArgument):
        await ctx.send("<a:no:898507018527211540> **| Bad argument.**")
        return
    elif isinstance(Exc, commands.DisabledCommand):
        await ctx.send("<a:no:898507018527211540> **| Command is disabled.**")
        return
    elif isinstance(Exc, commands.NoPrivateMessage):
        return
    elif isinstance(Exc, commands.BotMissingRole):
        print(
            f"<a:no:898507018527211540> **| I don't have te perms to do that. Missing the following perms:** `{Exc}`")
        return
    elif isinstance(Exc, discord.errors.Forbidden):
        return
    elif isinstance(Exc, commands.errors.UnexpectedQuoteError):
        await ctx.send("<a:no:898507018527211540> **| Unexpected Quote**")
        return
    elif isinstance(Exc, commands.MissingPermissions):
        try:
            missing = [perm.replace('_', ' ').replace(
                'guild', 'server').title() for perm in Exc.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format(
                    "**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = '<a:no:898507018527211540> **| You need the** `{}` **permission(s) to use this command.**'.format(
                fmt)
            await ctx.send(_message)
            return
        except:
            return
    elif isinstance(Exc, commands.CommandOnCooldown):
        try:
            if Exc.retry_after > 86400:
                remaining = math.floor(Exc.retry_after / 86400)
                await ctx.send(f"<a:hourglass:898511862075904061> **| This command is on cooldown, please retry in** `{remaining}d`.**")
            elif Exc.retry_after > 3600:
                remaining = math.floor(Exc.retry_after / 3600)
                await ctx.send(f"<a:hourglass:898511862075904061> **| This command is on cooldown, please retry in `{remaining}h`.**")
            elif Exc.retry_after > 60:
                remaining = math.floor(Exc.retry_after / 60)
                await ctx.send(f"<a:hourglass:898511862075904061> **| This command is on cooldown, please retry in `{remaining}m`.**")
            else:
                await ctx.send(f"<a:hourglass:898511862075904061> **| This command is on cooldown, please retry in `{math.floor(Exc.retry_after)}s`.**")
            return
        except:
            pass
    elif isinstance(Exc, commands.BotMissingPermissions):
        try:
            missing = [perm.replace('_', ' ').replace(
                'guild', 'server').title() for perm in Exc.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format(
                    "**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = '<a:no:898507018527211540> **| I need the `{}` permission(s) to run this command.**'.format(
                fmt)
            await ctx.send(_message)
            return
        except:
            pass
    
    elif isinstance(Exc, MissingPermissions):
        return
    elif isinstance(Exc, discord.errors.Forbidden):
        return

    else:
        try:
            msg = await ctx.send("<a:no:898507018527211540> **| An unknown error occured.**")
        except:
            pass
    raise Exc

statsloop.start()
client.run(TOKEN)
