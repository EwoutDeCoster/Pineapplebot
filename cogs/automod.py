import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
import sqlite3

vers = str("v2.0")
webs = str("Pineapplebot.ga")


class Automod(commands.Cog, name='Automod'):

    def __init__(self, client):
        self.client = client

    @commands.guild_only()
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT invitefilter, urlfilter FROM main WHERE guild_id = {message.author.guild.id}")
            result = cursor.fetchone()
            try:
                if "https://giant.gfycat.com/DamagedFakeKinglet.mp4" in message.content:
                    await message.delete()
                    await message.author.send("**⚠ | Don't try this again...**")
                if result[0] == "1" and ("discord.gg/" in message.content or "discordapp.com/invite" in message.content):
                    await message.delete()
                    await message.author.send(f"You can't send invite links in **{message.guild.name}**!")
                    cursor.execute(
                        f"SELECT modlog_id FROM main WHERE guild_id = {message.guild.id}")
                    resultt = cursor.fetchone()
                    channel = self.client.get_channel(int(resultt[0]))
                    embed = discord.Embed(
                        color=0xff0000, timestamp=datetime.utcnow())
                    embed.add_field(
                        name=f"** **", value=f"{message.author.mention} **used an invite url in** {message.channel.mention}", inline=False)
                    embed.add_field(
                        name=f"Invite", value=f"{message.content}", inline=False)
                    embed.set_author(name=f"{message.author}",
                                     icon_url=f"{message.author.avatar_url}")
                    embed.set_footer(
                        text=f"ID: {message.author.id}")
                    await channel.send(embed=embed)
                if result[1] == "1" and ("http://" in message.content or "https://" in message.content):
                    await message.delete()
                    await message.author.send(f"You can't send links in **{message.guild.name}**!")
                    cursor.execute(
                        f"SELECT modlog_id FROM main WHERE guild_id = {message.guild.id}")
                    resultt = cursor.fetchone()
                    channel = self.client.get_channel(int(resultt[0]))
                    embed = discord.Embed(
                        color=0xff0000, timestamp=datetime.utcnow())
                    embed.add_field(
                        name=f"** **", value=f"{message.author.mention} **send a link in** {message.channel.mention}", inline=False)
                    embed.add_field(
                        name=f"Message:", value=f"{message.content}", inline=False)
                    embed.set_author(name=f"{message.author}",
                                     icon_url=f"{message.author.avatar_url}")
                    embed.set_footer(
                        text=f"ID: {message.author.id}")
                    await channel.send(embed=embed)

                cursor.close()
                db.close()

            except:
                pass
        else:
            return

    @commands.guild_only()
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not before.bot and before.nick != after.nick:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT checknicks, modlog_id FROM main WHERE guild_id = {before.guild.id}")
            result = cursor.fetchone()
            if result[0] == "1" and after.nick is not None:
                if after.nick.startswith("!") or after.nick.startswith(" ") or after.name.startswith("?") or after.nick.startswith("\"") or after.nick.startswith("#") or after.nick.startswith("$") or after.nick.startswith("%") or after.nick.startswith("&") or after.nick.startswith("\'") or after.nick.lower().startswith("aaa") or "卐" in after.nick:
                    try:
                        hoist = after.nick
                        await after.edit(nick="no hoisting")
                    except:
                        pass
                    try:
                        channel = self.client.get_channel(int(result[1]))
                        embed = discord.Embed(
                            color=0xff0000, timestamp=datetime.utcnow())
                        embed.add_field(
                            name=f"** **", value=f"{before.mention} **tried to change his nickname to** `{hoist}`", inline=False)
                        embed.set_author(name=f"{before}",
                                         icon_url=f"{before.avatar_url}")
                        embed.set_footer(
                            text=f"ID: {before.id}")
                        await channel.send(embed=embed)
                    except:
                        pass
            elif result[0] == "1" and after.nick is None:
                if after.id == 310068607549964289:
                    return
                elif after.name.startswith("!") or after.name.startswith(" ") or after.name.startswith("?") or after.name.startswith("\"") or after.name.startswith("#") or after.name.startswith("$") or after.name.startswith("%") or after.name.startswith("&") or after.name.startswith("\'") or after.name.lower().startswith("aaa") or "卐" in after.name:
                    try:
                        hoist = after.name
                        await after.edit(nick="no hoisting")
                    except:
                        pass
                    try:
                        channel = self.client.get_channel(int(result[1]))
                        embed = discord.Embed(
                            color=0xff0000, timestamp=datetime.utcnow())
                        embed.add_field(
                            name=f"** **", value=f"{before.mention} **tried to change his actual name to** `{hoist}`", inline=False)
                        embed.set_author(name=f"{before}",
                                         icon_url=f"{before.avatar_url}")
                        embed.set_footer(
                            text=f"ID: {before.id}")
                        await channel.send(embed=embed)
                    except:
                        pass


def setup(client):
    client.add_cog(Automod(client))
    print('Automod loaded succesfully')
