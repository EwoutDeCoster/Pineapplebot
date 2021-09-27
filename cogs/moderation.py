import discord
from discord.ext import commands
import asyncio
import datetime
import time
import sqlite3

webs = str("Pineapplebot.ga")


class Moderation(commands.Cog, name='Moderation'):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):

        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT modlog_id FROM main WHERE guild_id = {ctx.author.guild.id}")
        result = cursor.fetchone()

        try:
            channel = self.client.get_channel(int(result[0]))

            message = ctx.message
            await message.delete()
            embed = discord.Embed(title=f"{member} got banned from the server",
                                  description=f"Reason: {reason}", color=0xff0000)
            embed.set_author(
                name="Pineapple", icon_url=f"{message.author.avatar_url}")
            embed.set_thumbnail(url="https://i.imgur.com/WPPqs5S.png")
            embed.set_footer(text=f"{webs} | Moderator: {ctx.author}")
            await ctx.send(embed=embed)
            await channel.send(embed=embed)
        except:
            msg = await ctx.send("Set a mod-log channel by using -moderation setlog [channel]")
            await asyncio.sleep(8)
            await msg.delete()
        try:
            await member.ban(reason=reason)
            print(f'{member} got banned for {reason} in {ctx.guild.name}')
            directmsg = discord.Embed(
                title=f"You got banned from {member.guild.name}", description=f"Reason: {reason}", color=0xff0000)
            directmsg.set_author(
                name="Pineapple", icon_url=f"https://i.imgur.com/WPPqs5S.png")
            directmsg.set_footer(text=f"{webs} | Moderator: {ctx.author}")
            await member.send(embed=directmsg)
        except:
            await ctx.send(f"⚠ | Member {member} could not be banned")

        cursor.close()
        db.close()

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT modlog_id FROM main WHERE guild_id = {ctx.author.guild.id}")
            result = cursor.fetchone()
            channel = self.client.get_channel(int(result[0]))
            message = ctx.message
            await message.delete()
            embed = discord.Embed(title=f"{member} got kicked from the server",
                                  description=f"Reason: {reason}", color=0xff0000)
            embed.set_author(
                name="Pineapple", icon_url=f"{message.author.avatar_url}")
            embed.set_thumbnail(url="https://i.imgur.com/Xxr6OqW.png")
            embed.set_footer(text=f"{webs} | Moderator: {ctx.author}")
            await ctx.send(embed=embed)
            await channel.send(embed=embed)
            cursor.close()
            db.close()
        except:
            return

        try:
            directmsg = discord.Embed(
                title=f"You got kicked from {member.guild.name}", description=f"Reason: {reason}", color=0xff0000)
            directmsg.set_author(
                name="Pineapple", icon_url=f"https://i.imgur.com/Xxr6OqW.png")
            directmsg.set_footer(text=f"{webs} | Moderator: {ctx.author}")
            await member.send(embed=directmsg)
        except:
            print(f"Couldn't send a dm to {member}")
        try:
            await member.kick(reason=reason)
            print(f'{member} got kicked for {reason}')
        except:
            await ctx.send("⚠ | Failed to kick that member.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        message = ctx.message
        await message.delete()

        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT modlog_id FROM main WHERE guild_id = {ctx.author.guild.id}")
        result = cursor.fetchone()
        channel = self.client.get_channel(int(result[0]))
        sql = (
            "INSERT INTO warnings(guild, user, warning) VALUES(?,?,?)")
        val = (message.guild.id, member.id, reason)
        cursor.execute(sql, val)
        db.commit()

        embed = discord.Embed(
            title=f"You got a warning in {member.guild.name}", description=f"Warning: {reason}", color=0xff0000)
        embed.set_author(
            name="Pineapple", icon_url=f"https://i.imgur.com/rjxnHHM.png")
        embed.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Warning.svg/832px-Warning.svg.png")
        embed.set_footer(text=f"{webs} | {member.guild.name}")
        await member.send(embed=embed)

        moderation = discord.Embed(
            title=f"{member} got warned", description=f"Warning: {reason}", color=0xff0000)
        moderation.set_author(
            name="Pineapple", icon_url=f"https://i.imgur.com/rjxnHHM.png")
        moderation.set_footer(text=f"{webs} | Moderator: {ctx.author}")
        await channel.send(embed=moderation)
        print(f'{member} got warned for {reason}')
        confirmsg = await ctx.send(f"**<:check_pine:834872371281264661> *{member} got warned!***")
        await asyncio.sleep(3)
        await confirmsg.delete()
        cursor.close()
        db.close()

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def warnings(self, ctx, member: discord.Member):
        try:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT user, warning FROM warnings WHERE guild = {ctx.author.guild.id} and user = {member.id}")
            result = cursor.fetchall()
            amount = len(result)
            i = 0
            embed = discord.Embed(
                title=f"Warnings for {self.client.get_user(int(result[0][0]))}", color=0xff0000)

            while i < amount:
                embed.add_field(
                    name=f"Warning {i + 1}", value=f"{result[i][1]}", inline=False)
                i += 1
            await ctx.send(embed=embed)
        except:
            await ctx.send(f"**❗ | Could not find any warnings for {member}.**")

    @commands.command()
    @commands.guild_only()
    async def report(self, ctx, member: discord.Member, *, reason=None):
        try:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT modlog_id FROM main WHERE guild_id = {ctx.author.guild.id}")
            result = cursor.fetchone()
            mod = self.client.get_channel(int(result[0]))
            message = ctx.message

            embed = discord.Embed(title="Report", color=0xff0000)
            embed.set_author(
                name="Pineapple", icon_url=f"https://i.imgur.com/rjxnHHM.png")
            embed.add_field(name=f"{ctx.author} has reported {member}",
                            value=f"Reason: {reason}", inline=True)
            embed.set_footer(text=f"{webs}")
            await mod.send(embed=embed)
            await message.delete()
            print(f'{member} got reported by {ctx.author} for {reason}')
            cursor.close()
            db.close()
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(
                name="Usage:", value="`-report [member] [reason]`", inline=False)
            embed.set_footer(text=f"{webs}")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def modmail(self, ctx, *, msg):
        try:
            message = ctx.message
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT modlog_id FROM main WHERE guild_id = {ctx.author.guild.id}")
            result = cursor.fetchone()
            log = self.client.get_channel(int(result[0]))
            await message.delete()

            lg = discord.Embed(
                title="Modmail", description=f"{ctx.author.mention} used modmail!", color=0xFF5A00)
            lg.set_author(name="Pineapple",
                          icon_url=f"https://i.imgur.com/rjxnHHM.png")
            lg.add_field(name=f"{ctx.author} used modmail!",
                         value=f"Message: {msg}", inline=True)
            lg.set_footer(text=f"{webs}")
            await log.send(embed=lg)
            print(f'{ctx.author} used modmail: {msg}')
            cursor.close()
            db.close()
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(
                name="Usage:", value="`-modmail [message]`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(enabled=False)
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def dm(self, ctx, member: discord.Member, *, msg):
        try:
            message = ctx.message
            await member.send(f"{msg}")
            await message.delete()
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(
                name="Usage:", value="`-dm [person] [message]`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
            print(f"{ctx.author} has sent a dm to {member}: {msg}")
        try:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT modlog_id FROM main WHERE guild_id = {ctx.author.guild.id}")
            result = cursor.fetchone()
            log = self.client.get_channel(int(result[0]))

            embed = discord.Embed(
                title="DM", description=f"{ctx.author.mention} used DM to message {member.mention}!\n\n **Message:** {msg}",
                color=0xFF5A00)
            embed.set_author(
                name="Pineapple", icon_url=f"https://i.imgur.com/rjxnHHM.png")
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await log.send(embed=embed)

        except:
            return

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        try:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT modlog_id FROM main WHERE guild_id = {ctx.author.guild.id}")
            result = cursor.fetchone()
            log = self.client.get_channel(int(result[0]))

            ch = ctx.channel.mention
            await ctx.channel.purge(limit=amount + 1)
            msg = await ctx.send(f'❗ | **{amount}** messages were deleted!')
            embed = discord.Embed(
                title="Clear", description=f"{ctx.author.mention} removed **{amount}** messages in {ch}", color=0xFF5A00)
            embed.set_author(
                name="Pineapple", icon_url=f"https://i.imgur.com/rjxnHHM.png")
            embed.set_footer(text=f"{webs}")
            await log.send(embed=embed)
            time.sleep(2)
            await msg.delete()
            print(f"{ctx.author} removed {amount} messages in {ch}")
            cursor.close()
            db.close()
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(
                name="Usage:", value="`-clear [number]`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(enabled=False)
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def spam(self, ctx, *, person):
        try:
            message = ctx.message
            await message.delete()
            print(f"{ctx.author} used spam: {person}")
            await ctx.send(f"{person}")
            await asyncio.sleep(0.4)
            await ctx.send(f"{person}")
            await asyncio.sleep(0.4)
            await ctx.send(f"{person}")
            await asyncio.sleep(0.4)
            await ctx.send(f"{person}")
            await asyncio.sleep(0.4)
            await ctx.send(f"{person}")
            await asyncio.sleep(0.4)
            await ctx.send(f"{person}")
            await asyncio.sleep(0.4)
            await ctx.send(f"{person}")
            await asyncio.sleep(0.4)
            await ctx.send(f"{person}")
            await asyncio.sleep(0.4)
            await ctx.send(f"{person}")
            await asyncio.sleep(0.4)
            await ctx.send(f"{person}")
            await asyncio.sleep(0.4)
            await ctx.send(f"{person}")
            await asyncio.sleep(0.4)
            await ctx.send(f"{person}")
            await asyncio.sleep(0.4)
            await ctx.send(f"{person}")
            await asyncio.sleep(0.4)
            await ctx.send(f"{person}")
            await asyncio.sleep(0.4)
            await ctx.send(f"{person}")
            await asyncio.sleep(0.4)
            await ctx.send(f"{person}")
            time.sleep(2)

            def check(m):
                return m.author == self.client.user

            await ctx.channel.purge(limit=16, check=check)
        except:
            await ctx.author.send("**Don't trick me xoxo**")

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    @commands.guild_only()
    async def giverole(self, ctx, role: discord.Role, user: discord.Member):
        await user.add_roles(role)
        await ctx.message.delete()
        conf = await ctx.message.reply(f"<:check_pine:834872371281264661> **| {role.name} has been given to {user.mention}.**")

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    @commands.guild_only()
    async def removerole(self, ctx, role: discord.Role, user: discord.Member):
        await user.remove_roles(role)
        await ctx.message.delete()
        conf = await ctx.send(f"<:check_pine:834872371281264661> **| {role.name} has been removed from {user.mention}.**")

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    @commands.guild_only()
    async def slowmode(self, ctx, seconds):
        try:
            if seconds == "disable":
                await ctx.channel.edit(slowmode_delay=0)
                await ctx.message.delete()
                await ctx.send("⏱ **| Slowmode has been disabled!**")
            elif int(seconds) < 0:
                await ctx.send("⚠ **| Enter a positive value!**")
                return
            elif int(seconds) == 0:
                await ctx.channel.edit(slowmode_delay=0)
                await ctx.message.delete()
                await ctx.send("⏱ **| Slowmode has been disabled!**")
                return
            else:
                await ctx.channel.edit(slowmode_delay=seconds)
                await ctx.message.delete()
                await ctx.send(f"⏱ **| This channel is now in slowmode! You can now send messages every `{seconds}` seconds**.")
        except:
            await ctx.send("⚠ **| The argument should be a number!**")


def setup(client):
    client.add_cog(Moderation(client))
    print('Moderation loaded succesfully')
