from logging import exception
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
from datetime import datetime, timedelta, date
from decimal import Decimal
import sqlite3

webs = str("Pineapplebot.ga")


class Vote(commands.Cog, name='Vote'):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        try:
            if message.channel.id == 902203209014190132 and message.guild.id == 828628284806922251:
                usrid = int(message.content)
                usr = self.client.get_user(usrid)
                db = sqlite3.connect('cogs/main.sqlite')
                cursor = db.cursor()
                cursor.execute(
                f"SELECT user FROM votes WHERE user = '{message.content}'")
                result = cursor.fetchone()
                if result is not None:
                    return
                sql = (
                    f"INSERT INTO votes(user) VALUES('{message.content}')")
                cursor.execute(sql)
                db.commit()
                cursor.close()
                db.close()
                embed = discord.Embed(
                    title="📩 Vote", description="**Thank you for voting!**\n\nUse `-vote claim` in a server to claim your reward!", color=0x0068d6)
                embed.set_thumbnail(
                    url=f"{str(self.client.user.avatar_url)}")
                embed.set_footer(text=f"You can vote every 12 hours.")
                await usr.send(embed=embed)
                
        except Exception as e :
            print(f"{e.__class__.__name__}: {e}")

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def vote(self, ctx):
        embed = discord.Embed(
            title="📩 Vote", description="**You can vote for the bot on [Top.gg](https://top.gg/bot/463388759866474506).**", color=0x0068d6)
        embed.set_thumbnail(
            url=f"{str(self.client.user.avatar_url)}")
        embed.set_footer(text=f"You can vote every 12 hours.")
        await ctx.send(embed=embed)

    @vote.command()
    @commands.guild_only()
    async def claim(self, ctx):
        def kform(num, round_to=2):
            if abs(num) < 1000:
                return num
            else:
                magnitude = 0
                while abs(num) >= 1000:
                    magnitude += 1
                    num = round(num / 1000.0, round_to)
                return '{:.{}f}{}'.format(round(num, round_to), round_to, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
        price = random.randint(1000, 10000)
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
        f"SELECT user FROM votes WHERE user = '{str(ctx.author.id)}'")
        result = cursor.fetchone()
        if result is None:
            await ctx.send("<a:no:898507018527211540> **| You haven't voted yet! Use `-vote` to vote.**")
        else:
            sql = (
                f"DELETE FROM votes WHERE user = '{str(ctx.author.id)}'")
            cursor.execute(sql)
            db.commit()
            cursor.execute(
                f"SELECT user FROM economy WHERE user = {ctx.author.id}")
            eco = cursor.fetchone()
            if eco is not None:
                sql = (
                "UPDATE economy SET silver = silver + ? where guild = ? and user = ?")
                val = (price, ctx.guild.id, ctx.author.id)
                cursor.execute(sql, val)
                db.commit()
            else:
                sql = ("INSERT INTO economy(guild, user, silver) VALUES(?,?,?)")
                val = (ctx.guild.id, ctx.author.id, price)
                cursor.execute(sql, val)
                db.commit()
            embed = discord.Embed(
                title="🎁 Vote Reward", description=f"You just received <:silver:856609576459304961> **{kform(price)}** for voting", color=0x005ec2)
            embed.set_thumbnail(url=ctx.author.avatar_url_as(size=256))
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
            cursor.close()
            db.close()




def setup(client):
    client.add_cog(Vote(client))
    print('Vote loaded succesfully')