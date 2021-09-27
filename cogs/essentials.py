import discord
from discord import message
from discord import client
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta
import time
import random
import os
import urllib
import requests
import sys
import sqlite3
import speedtest

vers = str("v2.0")
webs = str("Pineapplebot.ga")
st = speedtest.Speedtest()


class Essentials(commands.Cog, name='Essentials'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        try:

            if "kekw" in message.content.lower() and not message.author.bot:
                await message.add_reaction("<:kekw:829283834750435341>")
            if 'sheesh' in message.content.lower():
                await message.add_reaction("<:sheesh:846726354291785749>")
            if " heh " in message.content.lower() or "heh " in message.content.lower() or message.content.lower() == "heh":
                await message.add_reaction("<a:loading:841639840785498173>")
            if self.client.user.mentioned_in(message) and len(message.content) <= 22 and not "everyone" in message.content.lower() and not "here" in message.content.lower() and not "someone" in message.content.lower():
                embed = discord.Embed(description="Prefix: `-`",
                                      color=0x0a4d8b)
                embed.set_author(
                    name="Pineapple Bot", icon_url="https://cdn.discordapp.com/avatars/463388759866474506/b282e13b4fe1c13a637b31704e5c4b11.webp?size=1024", url=f"https://www.{webs}")
                embed.set_footer(
                    text=f"Ping: {round(self.client.latency * 1000)}ms")
                await message.reply(embed=embed)
        except:
            pass

    @commands.command(name="partnership")
    @commands.guild_only()
    async def botpromote(self, ctx, footertext=None):
        if ctx.author.id == 302075047244333056:
            if footertext == None:
                footertext = ctx.guild.name
            await ctx.message.delete()
            embed = discord.Embed(
                description="Pineapple is the all in one bot for your discord server! It features Moderation, reaction roles, leveling, crypto, ...\n \n[Invite](https://discord.com/oauth2/authorize?client_id=463388759866474506&scope=bot&permissions=8) Pineapple today!", color=0x0a4d8b)
            embed.set_author(name="Pineapple Bot", url="https://www.pineapplebot.ga/",
                             icon_url="https://i.imgur.com/rjxnHHM.png")
            embed.set_image(url="https://i.imgur.com/rjxnHHM.png")
            embed.set_footer(text=f"{webs} | {footertext}")
            await ctx.send(embed=embed)
        else:
            await ctx.message.delete()
            embed = discord.Embed(
                description="If you're interested in a partnership with pineapple, you can learn more by sending ccaved a dm:\n \n[Learn more!](https://discord.com/users/302075047244333056)", color=0x0a4d8b)
            embed.set_author(name="Partnership",
                             icon_url="https://i.imgur.com/rjxnHHM.png")
            embed.set_image(url="https://i.imgur.com/rjxnHHM.png")
            embed.set_footer(text=f"{webs} | Partnerships")
            await ctx.send(embed=embed)

    @commands.command(name="servers")
    @commands.guild_only()
    async def servers(self, ctx):
        if ctx.author.id == 302075047244333056:
            servers = list(self.client.guilds)
            lijstje = ""
            for x in range(len(servers)):
                lijstje = lijstje + f"`{(servers[x-1].name)}`" + ", "
            await ctx.send(f"{lijstje}")
        else:
            pass

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.message.reply(f"👀 **| {round(self.client.latency * 1000)}ms**")
        print(f"Ping: {round(self.client.latency * 1000)}ms")

    @commands.command(name='version')
    @commands.guild_only()
    async def version(self, ctx):
        embed = discord.Embed(
            title="Version", description=vers, color=0x0a4d8b)
        embed.set_thumbnail(
            url="https://i.imgur.com/rjxnHHM.png")
        embed.set_footer(text=f"{webs}")
        await ctx.send(embed=embed)
        print(f'{ctx.author} Version cmd')

    @commands.command(name='say')
    @commands.guild_only()
    @commands.has_permissions(mention_everyone=True)
    async def say(self, ctx, *, text):
        message = ctx.message
        await message.delete()
        try:
            await ctx.send(f"{text}")
        except:
            await ctx.send("⚠ | Say command usage: `-say [message]`")
        print(f"{ctx.author} used say cmd to say: {text}")

    @commands.command(name='members')
    @commands.guild_only()
    async def members(self, ctx):
        member = ctx.author
        guild = member.guild
        await ctx.message.reply(f"📈 **| There currently are `{guild.member_count}` members here!**")
        print(f'{ctx.author} used membercount')

    @commands.command(name="humans")
    @commands.guild_only()
    async def humans(self, ctx):
        await ctx.message.reply(f"📈 **| There are currently `{len([Member for Member in ctx.guild.members if not Member.bot])}` humans here!**")

    @commands.command(name="users")
    @commands.guild_only()
    async def users(self, ctx):
        await ctx.message.reply(f"👀 **| I'm watching `{len(self.client.users):,}` users!**")

    @commands.command(nam="finduser")
    @commands.guild_only()
    async def getuser(self, ctx, usrid):
        user = self.client.get_user(int(usrid))
        embed = discord.Embed(
            title=f"{user}", url=f"https://discord.com/users/{usrid}", description=f"ID: {usrid}", color=0x0a4d8b)
        embed.set_footer(text=f"Pineappleserver.ga | {ctx.author}")
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def announce(self, ctx):
        await ctx.send("command options:\n-announce normal \"[title]\" \"[message]\"")

    @announce.command()
    @commands.guild_only()
    @commands.has_permissions(mention_everyone=True)
    async def normal(self, ctx, title, msg):
        if ctx.message.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            embed = discord.Embed(
                title=f"{title}", description=f"{msg}", color=0x006ec2)
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(embed=embed)
        else:
            messagee = await ctx.send("**⚠ | You don't have the permissions to do that.**")
            await asyncio.sleep(3)
            await messagee.delete()

    @announce.command()
    @commands.guild_only()
    @commands.has_permissions(mention_everyone=True)
    async def tag(self, ctx, title, msg, tag):
        if ctx.message.author.guild_permissions.manage_messages:
            await ctx.message.delete()
            embed = discord.Embed(
                title=f"{title}", description=f"{msg}", color=0x006ec2)
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send(f"{tag}", embed=embed)
        else:
            messagee = await ctx.send("**⚠ | You don't have the permissions to do that.**")
            await asyncio.sleep(3)
            await messagee.delete()

    @commands.group()
    @commands.guild_only()
    async def timer(self, ctx, minutes):
        if int(minutes) == 1:
            await ctx.message.reply(f"⏰ | Timer is set for {minutes} minute")
            await asyncio.sleep(int(minutes) * 60)
            await ctx.send(f"**🔔 | {ctx.author.mention} your timer went off!**")
        else:
            if int(minutes) > 180:

                err = await ctx.send("**⚠ | The max timer is 180 min.**")
                await asyncio.sleep(3)
                await ctx.message.delete()
                await err.delete()
            else:
                await ctx.message.reply(f"⏰ | Timer is set for {minutes} minutes")
                await asyncio.sleep(int(minutes) * 60)
                await ctx.send(f"**🔔 | {ctx.author.mention} your timer went off!**")

    @commands.command()
    @commands.guild_only()
    async def studytimer(self, ctx, minutes):
        if ctx.message.author.guild_permissions.manage_messages:
            if int(minutes) == 1:
                await ctx.message.reply(f"⏰ | Timer is set for {minutes} minute")
            else:
                await ctx.message.reply(f"⏰ | Timer is set for {minutes} minutes")
            await asyncio.sleep(int(minutes) * 60)
            embed = discord.Embed(title="🔔 Timer went off!",
                                  description="<@&836598412597133373> time to take a break!", color=0x006ec2)
            embed.set_thumbnail(
                url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/271/books_1f4da.png")
            embed.set_footer(text=f"{ctx.guild.name}")
            await ctx.send("<@&836598412597133373>", embed=embed)
        else:
            no = discord.Embed(title="⚠ Command error", color=0xff4000)
            no.add_field(
                name="Permission error:", value="You don't have the permissions to do that!", inline=False)
            no.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=no)

    @commands.command(name='confirm')
    @commands.guild_only()
    @commands.has_permissions(mention_everyone=True)
    async def confirm(self, ctx, *, text):
        message = ctx.message
        await message.delete()
        try:
            msg = await ctx.send(f"{text}")
            await msg.add_reaction("<:check_pine:834872371281264661>")
        except:
            await ctx.send("⚠ | Confirm command usage: `-confirm [message]`")
        print(f"{ctx.author} used check cmd to say: {text}")

    # leave server
    @commands.command(name="ts8f6bcd4621d373cade4e832627b4f6")
    @commands.guild_only()
    async def ts8f6bcd4621d373cade4e832627b4f6(self, ctx):
        # await ctx.send("‼️ **Leaving the server in 1 minute!**")
        # await asyncio.sleep(57)
        # await ctx.send("**Leaving...**")
        # await asyncio.sleep(3)
        await ctx.guild.leave()
        print(f"Left {ctx.guild.name} with the Hash command")

    @commands.group(name="rr", invoke_without_command=True)
    async def rr(self, ctx):
        embed = discord.Embed(
            title='Command Usage:', description=f'-rr addrole [emoji] [role] [message id]', color=0x0a4d8b, timestamp=datetime.utcnow())
        await ctx.send(embed=embed)

    @rr.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, emoji=None, rolee: discord.Role = None, msgid=None):
        if emoji == None or rolee == None or msgid == None:
            embed = discord.Embed(
                title='Command Usage:', description=f'-rr addrole [emoji] [role] [message id]', color=0x0a4d8b, timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        else:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            sql = (
                "INSERT INTO reactionroles(guild, user, message, role, emoji) VALUES(?,?,?,?,?)")
            val = (ctx.guild.id, ctx.author.id, msgid, rolee.id, emoji)
            message = await ctx.fetch_message(int(msgid))
            await message.add_reaction(f"{emoji}")
            print(f"{emoji}")
            cursor.execute(sql, val)
            db.commit()
            await ctx.message.delete()
            cursor.close()
            db.close()
    
    @rr.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, emoji=None , msgid=None):
        if emoji == None or msgid == None:
            embed = discord.Embed(
                title='Command Usage:', description=f'-rr removerole [emoji] [message id]', color=0x0a4d8b, timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        else:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            sql = ("DELETE FROM reactionroles where message = ? AND emoji = ? AND guild = ?")
            val = (msgid, emoji, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            await ctx.message.delete()



    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_add(self, payload):
        try:
            if not payload.member.bot:
                db = sqlite3.connect('cogs/main.sqlite')
                cursor = db.cursor()
                cursor.execute(
                    f"SELECT user, role, message, emoji FROM reactionroles WHERE guild = \'{payload.guild_id}\' and (emoji = \'{payload.emoji.name}\' or emoji = \'<:{payload.emoji.name}:{payload.emoji.id}>\' or emoji = \'<a:{payload.emoji.name}:{payload.emoji.id}>\')  and message = \'{payload.message_id}\'")
                result = cursor.fetchone()
                if result == None:
                    cursor.close()
                    db.close()
                    return
                else:
                    role = discord.utils.get(self.client.get_guild(
                        payload.guild_id).roles, id=result[1])
                    await payload.member.add_roles(role)
                    cursor.close()
                    db.close()
        except:
            pass

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_remove(self, payload):
        try:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT user, role, message, emoji FROM reactionroles WHERE guild = \'{payload.guild_id}\' and (emoji = \'{payload.emoji.name}\' or emoji = \'<:{payload.emoji.name}:{payload.emoji.id}>\' or emoji = \'<a:{payload.emoji.name}:{payload.emoji.id}>\')  and message = \'{payload.message_id}\'")
            result = cursor.fetchone()
            if result == None:
                cursor.close()
                db.close()
                return
            else:
                role = discord.utils.get(self.client.get_guild(
                    payload.guild_id).roles, id=result[1])
                await self.client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
                cursor.close()
                db.close()
        except:
            pass

    @commands.command()
    async def speedtest(self, ctx):
        if ctx.author.id == 302075047244333056:
            loading = discord.Embed(color=0x0a4d8b,
                                    description=f"<a:loading:841639840785498173> Performing speedtest.")
            loadmes = await ctx.send(embed=loading)

            downloadsp = st.download() / 1000000
            uploadsp = st.upload() / 1000000
            pingsp = st.results.ping
            embed = discord.Embed(
                title='Speedtest:', description=f'**Download:** {round(downloadsp, 1)} Mbps\n**Upload:** {round(uploadsp, 1)} Mbps\n**Ping: **{round(pingsp)}ms', color=0x0a4d8b, timestamp=datetime.utcnow())
            embed.set_thumbnail(
                url="https://www.ookla.com/s/images/ookla/index/gauge-blue-1x.png")
            await loadmes.edit(embed=embed)
        else:
            return

    @commands.command()
    async def vote(self, ctx):
        embed = discord.Embed(
            title="📩 Vote", description="**You can vote for the bot on the following platforms:**\n** **\n[Botclub](https://botclub.ml/bot/463388759866474506)", color=0x0068d6)
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/463388759866474506/b282e13b4fe1c13a637b31704e5c4b11.webp?size=1024")
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(mention_everyone=True)
    async def check(self, ctx, *, message):
        await ctx.message.delete()
        msg = await ctx.send(f"{message}")
        await msg.add_reaction('<:check_pine:834872371281264661>')


def setup(client):
    client.add_cog(Essentials(client))
    print('Essentials loaded succesfully')
