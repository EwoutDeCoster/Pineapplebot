import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import time
import random
import os
import urllib
import requests
import sys
import sqlite3


webs = str("Pineapplebot.ga")


class Log(commands.Cog, name='Log'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message_delete(self, message):
        try:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT modlog_id FROM main WHERE guild_id = {message.guild.id}")
            result = cursor.fetchone()
            channel = self.client.get_channel(int(result[0]))

            embed = discord.Embed(color=0xff0000, timestamp=datetime.utcnow())
            embed.add_field(
                name=f"** **", value=f"**Message sent by** {message.author.mention} **deleted in** {message.channel.mention}\n{message.content}", inline=False)
            embed.set_author(name=f"{message.author}",
                             icon_url=f"{message.author.avatar_url}")
            try:
                embed.set_image(url=message.attachments[0].url)
            except IndexError:
                pass
            embed.set_footer(
                text=f"Author: {message.author.id} | Message ID: {message.id}")
            try:
                sql = ("DELETE FROM reactionroles where message = ? AND guild = ?")
                val = (message.id, message.guild.id)
                cursor.execute(sql, val)
                db.commit()
            except:
                print("No field deleted")

            await channel.send(embed=embed)
            cursor.close()
            db.close()
        except:
            pass

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message_edit(self, before, after):
        try:
            if before.author.bot:
                return
            elif before.content != after.content:
                db = sqlite3.connect('cogs/main.sqlite')
                cursor = db.cursor()
                cursor.execute(
                    f"SELECT modlog_id FROM main WHERE guild_id = {before.guild.id}")
                result = cursor.fetchone()
                channel = self.client.get_channel(int(result[0]))

                embed = discord.Embed(
                    color=0x00e1ff, timestamp=datetime.utcnow())
                embed.add_field(
                    name=f"** **", value=f"{before.author.mention} **edited a message in** {before.channel.mention}  [Show!]({before.jump_url})", inline=False)
                embed.set_author(name=f"{before.author}",
                                 icon_url=f"{before.author.avatar_url}")
                embed.add_field(
                    name="Before", value=f"{before.content}", inline=False)
                embed.add_field(
                    name="After", value=f"{after.content}", inline=False)
                embed.set_footer(
                    text=f"Author: {before.author.id} | Message ID: {before.id}")
                await channel.send(embed=embed)
                cursor.close()
                db.close()
        except:
            pass

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_voice_state_update(self, member, before, after):
        try:
            if before.channel != after.channel:
                db = sqlite3.connect('cogs/main.sqlite')
                cursor = db.cursor()
                cursor.execute(
                    f"SELECT modlog_id FROM main WHERE guild_id = {member.guild.id}")
                result = cursor.fetchone()
                channel = self.client.get_channel(int(result[0]))

                if after.channel != None:
                    embed = discord.Embed(
                        color=0x00ff00, timestamp=datetime.utcnow())
                    embed.add_field(
                        name=f"** **", value=f"{member.mention} **joined voice channel** {after.channel.mention}", inline=False)
                    embed.set_author(name=f"{member}",
                                     icon_url=f"{member.avatar_url}")
                    embed.set_footer(
                        text=f"ID: {member.id}")
                    await channel.send(embed=embed)
                if after.channel == None:
                    embed = discord.Embed(
                        color=0xff0000, timestamp=datetime.utcnow())
                    embed.add_field(
                        name=f"** **", value=f"{member.mention} **left voice channel** {before.channel.mention}", inline=False)
                    embed.set_author(name=f"{member}",
                                     icon_url=f"{member.avatar_url}")
                    embed.set_footer(
                        text=f"ID: {member.id}")
                    await channel.send(embed=embed)

                cursor.close()
                db.close()
        except:
            pass


def setup(client):
    client.add_cog(Log(client))
    print('Log loaded succesfully')
