import discord
from discord.ext import commands
import asyncio
import datetime
import time
from datetime import datetime, timedelta
import random
import os
import urllib
import requests
import sys
from uuid import uuid4
import sqlite3


webs = str("Pineapplebot.ga")

numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
           "6⃣", "7⃣", "8⃣", "9⃣", "🔟")


class Poll(commands.Cog, name='Poll'):

    def __init__(self, client):
        self.client = client
        self.polls = []

    @commands.command(name="createpoll", aliases=["mkpoll"])
    @commands.guild_only()
    async def create_poll(self, ctx, question: str, *options):
        if len(options) > 10:
            await ctx.message.delete()
            msg = await ctx.send("⚠ You can only add a maximum of 10 options!")
            await asyncio.sleep(3)
            await msg.delete()

        else:
            embed = discord.Embed(title="🗳️ Poll",
                                  description=question,
                                  colour=0xff9500,
                                  timestamp=datetime.utcnow())

            fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False),
                      ("Instructions", "React to vote!", False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
                embed.set_footer(text=f"{ctx.author}")

            message = await ctx.send(embed=embed)

            for emoji in numbers[:len(options)]:
                await message.add_reaction(emoji)

            self.polls.append((message.channel.id, message.id))

    @commands.command(name='poll')
    @commands.guild_only()
    async def poll(self, ctx, *, text):
        try:
            if "@everyone" in text or "@here" in text or "@someone" in text and not ctx.author.guild_permissions.manage_messages:
                await ctx.message.delete()
                await ctx.author.send(f"⚠ | You can't mention @everyone in **{ctx.guild.name}**!")
            else:
                message = ctx.message
                await message.delete()

                msg = await ctx.send(f"**{ctx.author.mention}:** \n{text}")

                await msg.add_reaction("<:check_pine:834872371281264661>")
                await msg.add_reaction("<:cross_pine:834872413027303484>")
                print(f'{ctx.author} made a poll: {text}')
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(
                name="Usage:", value="`-poll [message]`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(name='suggest')
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def suggest(self, ctx, *, sug):
        try:
            x = uuid4()
            sugid = str(x)[:8]
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT sugs FROM main WHERE guild_id = {ctx.author.guild.id}")
            result = cursor.fetchone()
            channel = self.client.get_channel(int(result[0]))

            embed = discord.Embed(color=0x005ec2)
            embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
            embed.add_field(name="Submitter",
                            value=f"{ctx.author}", inline=False)
            embed.add_field(name="Suggestion", value=f"{sug}", inline=True)
            embed.set_footer(text=f"User: {ctx.author.id} | sID: {sugid}")
            msg = await channel.send(embed=embed)
            await msg.add_reaction("<:check_pine:834872371281264661>")
            await msg.add_reaction("<:cross_pine:834872413027303484>")

            sql = (
                "INSERT INTO suggestions(id, guild, user, message, msgid) VALUES(?,?,?,?,?)")
            val = (sugid, ctx.guild.id, ctx.author.id, sug, msg.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            dmem = discord.Embed(title=f"{ctx.guild.name}", description=f"Hey {ctx.author.mention}, Your suggestion has been send to the {channel.mention} channel. \n\n Please wait for people to vote for it and for it to be approved or rejected by the staff. \n\nYour suggestion ID: **{sugid}**", color=0x005ec2)
            dmem.set_thumbnail(url=f"{ctx.guild.icon_url}")
            dmem.set_footer(text=f"User: {ctx.author.id} | sID: {sugid}")
            await ctx.author.send(embed=dmem)

            conf = await ctx.send("📝 **| Suggestion has been send!**")
            await ctx.message.delete()
            await asyncio.sleep(3)
            await conf.delete()
        except:
            await ctx.send("**⚠ | Make sure you enter a suggestion!**")

    @commands.command(name='approve')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def approve(self, ctx, sid, *, review=None):
        try:
            await ctx.message.delete()
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT handsugs FROM main WHERE guild_id = {ctx.author.guild.id}")
            result = cursor.fetchone()
            channel = self.client.get_channel(int(result[0]))
            cursor.execute(
                f"SELECT id, guild, user, message, msgid FROM suggestions WHERE guild = {ctx.author.guild.id} AND id = \"{sid}\"")
            result1 = cursor.fetchone()
            if result1 is None:
                err = await ctx.send("⚠ **| No message with this sID.**")
                await asyncio.sleep(3)
                await err.delete()
                return

            sid = str(result1[0])
            userid = int(result1[2])
            sug = str(result1[3])
            msgid = int(result1[4])
            user = self.client.get_user(int(userid))
            print(channel)

            message = await ctx.fetch_message(int(msgid))

            yes = message.reactions[0].count - 1
            no = message.reactions[1].count - 1

            await message.delete()

            embed = discord.Embed(color=0x00ff00)
            embed.set_author(name=f"{ctx.guild.name}",
                             icon_url=f"{ctx.guild.icon_url}")
            embed.add_field(
                name="Results", value=f"<:check_pine:834872371281264661>: {yes}\n<:cross_pine:834872413027303484>: {no}", inline=False)
            embed.add_field(name="Suggestion", value=f"{sug}", inline=False)
            embed.add_field(name="Submitter",
                            value=f"{user.mention}", inline=False)
            embed.add_field(name="Approved By",
                            value=f"{ctx.author.mention}", inline=False)
            if review is not None:
                embed.add_field(name="Response:",
                                value=f"{review}", inline=False)
            embed.set_footer(text=f"sID: {sid}")
            await channel.send(embed=embed)

            dmem = discord.Embed(
                title=f"{ctx.guild.name}", description=f"Hey {user.mention}, Your suggestion has been approved by {ctx.author.mention} ! \n\n **Your suggestion was:**\n*{sug}*", color=0x00ff00)
            dmem.set_thumbnail(url=f"{ctx.guild.icon_url}")
            dmem.set_footer(text=f"User: {user.id} | sID: {sid}")
            await user.send(embed=dmem)

            sql = ("DELETE FROM suggestions where id = ? AND guild = ?")
            val = (sid, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()

            cursor.close()
            db.close()
        except:
            await ctx.send("⚠ **| Make sure your sID is correct.**")

    @commands.command(name='reject')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def reject(self, ctx, sid, *, review=None):
        try:
            await ctx.message.delete()
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT handsugs FROM main WHERE guild_id = {ctx.author.guild.id}")
            result = cursor.fetchone()
            channel = self.client.get_channel(int(result[0]))
            cursor.execute(
                f"SELECT id, guild, user, message, msgid FROM suggestions WHERE guild = {ctx.author.guild.id} AND id = \"{sid}\"")
            result1 = cursor.fetchone()
            if result1 is None:
                err = await ctx.send("⚠ **| No message with this sID.**")
                await asyncio.sleep(3)
                await err.delete()
                return

            sid = str(result1[0])
            userid = int(result1[2])
            sug = str(result1[3])
            msgid = int(result1[4])
            user = self.client.get_user(int(userid))
            print(channel)

            message = await ctx.fetch_message(int(msgid))

            yes = message.reactions[0].count - 1
            no = message.reactions[1].count - 1

            await message.delete()

            embed = discord.Embed(color=0xff0000)
            embed.set_author(name=f"{ctx.guild.name}",
                             icon_url=f"{ctx.guild.icon_url}")
            embed.add_field(
                name="Results", value=f"<:check_pine:834872371281264661>: {yes}\n<:cross_pine:834872413027303484>: {no}", inline=False)
            embed.add_field(name="Suggestion", value=f"{sug}", inline=False)
            embed.add_field(name="Submitter",
                            value=f"{user.mention}", inline=False)
            embed.add_field(name="Rejected By",
                            value=f"{ctx.author.mention}", inline=False)
            if review is not None:
                embed.add_field(name="Response:",
                                value=f"{review}", inline=False)
            embed.set_footer(text=f"sID: {sid}")
            await channel.send(embed=embed)
            if review is not None:
                dmem = discord.Embed(
                    title=f"{ctx.guild.name}", description=f"Hey {user.mention}, Your suggestion has been rejected by {ctx.author.mention}!\n\n**Staff response:** {review}\n\n **Your suggestion was:** *{sug}*", color=0xff0000)
            if review is None:
                dmem = discord.Embed(
                    title=f"{ctx.guild.name}", description=f"Hey {user.mention}, Your suggestion has been rejected by {ctx.author.mention}!\n\n **Your suggestion was:** *{sug}*", color=0xff0000)
            dmem.set_thumbnail(url=f"{ctx.guild.icon_url}")
            dmem.set_footer(text=f"User: {user.id} | sID: {sid}")
            await user.send(embed=dmem)

            sql = ("DELETE FROM suggestions where id = ? AND guild = ?")
            val = (sid, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()

            cursor.close()
            db.close()
        except:
            await ctx.send("⚠ **| Make sure your sID is correct.**")

    @commands.command(name='ignore')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def ignore(self, ctx, sid, *, review=None):
        await ctx.message.delete()
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT handsugs FROM main WHERE guild_id = {ctx.author.guild.id}")
        result = cursor.fetchone()
        channel = self.client.get_channel(int(result[0]))
        cursor.execute(
            f"SELECT id, guild, user, message, msgid FROM suggestions WHERE guild = {ctx.author.guild.id} AND id = \"{sid}\"")
        result1 = cursor.fetchone()
        if result1 is None:
            err = await ctx.send("⚠ **| No message with this sID.**")
            await asyncio.sleep(3)
            await err.delete()
            return

        sid = str(result1[0])
        userid = int(result1[2])
        sug = str(result1[3])
        msgid = int(result1[4])
        user = self.client.get_user(int(userid))
        print(channel)
        sql = ("DELETE FROM suggestions where id = ? AND guild = ?")
        val = (sid, ctx.guild.id)
        cursor.execute(sql, val)
        db.commit()

        try:
            message = await ctx.fetch_message(int(msgid))

            await message.delete()
        except:
            pass
        if review is not None:
            dmem = discord.Embed(
                title=f"{ctx.guild.name}", description=f"Hey {user.mention}, Your suggestion has been ignored by {ctx.author.mention}!\n\n **Reason:** {review}", color=0xff0000)
            dmem.set_thumbnail(url=f"{ctx.guild.icon_url}")
            dmem.set_footer(text=f"User: {user.id} | sID: {sid}")
            await user.send(embed=dmem)

    @commands.group()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def sendsuggestion(self, ctx, sidd):
        try:
            await ctx.message.delete()
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT id, guild, user, message, msgid FROM suggestions WHERE guild = {ctx.author.guild.id} AND id = \"{sidd}\"")
            result = cursor.fetchone()
            sid = str(result[0])
            userid = int(result[2])
            sug = str(result[3])
            user = self.client.get_user(int(userid))

            embed = discord.Embed(color=0x005ec2)
            embed.set_author(name=f"{ctx.author}",
                             icon_url=f"{ctx.author.avatar_url}")
            embed.set_thumbnail(url=f"{user.avatar_url}")
            embed.add_field(name="Submitter",
                            value=f"{user.mention}", inline=False)
            embed.add_field(name="Suggestion", value=f"{sug}", inline=True)
            embed.set_footer(text=f"User: {userid} | sID: {sid}")
            await ctx.send(embed=embed)
            cursor.close()
            db.close()
        except:
            await ctx.send("⚠ **| Make sure your sID is correct.**")

    @commands.command(name="testfetch")
    @commands.guild_only()
    async def testfetch(self, ctx, msg):
        message = await ctx.fetch_message(msg)
        await ctx.message.reply(f"{message.reactions}")
        await message.add_reaction('<:booster:834863416773574686>')


def setup(client):
    client.add_cog(Poll(client))
    print('Poll loaded succesfully')
