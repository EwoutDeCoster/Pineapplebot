import discord
from discord.ext import commands
import datetime
import asyncio
import sqlite3

vers = str("v2.0")
webs = str("Pineapplebot.ga")


class Automod(commands.Cog, name='Automod'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    @commands.guild_only()
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


def setup(client):
    client.add_cog(Automod(client))
    print('Automod loaded succesfully')
