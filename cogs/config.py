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
import sqlite3

webs = str("Pineapplebot.ga")


class Config(commands.Cog, name='Config'):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def welcome(self, ctx):
        embed = discord.Embed(
            title="⚙️ Welcome commands", description="Configure welcome events. \n(vars for welcome messages: [members], [server], [user], [mention], [membercount])", color=0x006ce0)
        embed.add_field(
            name="-welcome channel [channel]", value="Set the welcome channel", inline=False)
        embed.add_field(
            name="-welcome message [message]", value="Set the welcome message", inline=False)
        embed.add_field(
            name="-welcome dm [message]", value="Set a dm welcome message", inline=False)
        embed.add_field(
            name="-welcome role [role]", value="Set a welcome role", inline=False)
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @welcome.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT welcomech_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, welcomech_id) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"⚙ **| Channel has been set to** {channel.mention}")

            else:
                sql = ("UPDATE main SET welcomech_id = ? where guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"⚙ **| Channel has been updated to** {channel.mention}")

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else:
            await ctx.send("**⚠ | You don't have the perms to do that!**")

    @welcome.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def message(self, ctx, *, message):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT welcomemsg FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, welcomemsg) VALUES(?,?)")
                val = (ctx.guild.id, message)
                await ctx.send(f"⚙ **| Welcome message has been set to:** {message}")
            else:
                sql = ("UPDATE main SET welcomemsg = ? where guild_id = ?")
                val = (message, ctx.guild.id)
                await ctx.send(f"⚙ **| Welcome message has been updated to:** {message}")

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else:
            await ctx.send("**⚠ | You don't have the perms to do that!**")

    @welcome.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def dm(self, ctx, *, msg):
        try:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            sql = ("UPDATE main SET welcomedm = ? where guild_id = ?")
            val = (msg, ctx.guild.id)
            await ctx.send(f"⚙ **| Welcome dm message has been updated to:**\n {msg}")

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        except:
            await ctx.send("**⚠ | Failed to update DM join message.**")

    @welcome.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def role(self, ctx, role: discord.Role):
        try:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            sql = ("UPDATE main SET role = ? where guild_id = ?")
            val = (role.id, ctx.guild.id)
            await ctx.send(f"⚙ **| Join role has been updated to:\n** {role}")

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        except:
            await ctx.send("**⚠ | Failed to update join role.**")

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def membercount(self, ctx):
        embed = discord.Embed(
            title="⚙️ Member Count", description="Set the voice channel for the member count.", color=0x006ce0)
        embed.add_field(name="-membercount id [voice channel id]",
                        value="Set the voice channel for the member count", inline=False)
        embed.add_field(name="-membercount refresh",
                        value="Manualy refresh the membercounter", inline=False)
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @membercount.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def id(self, ctx, channel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT membercnt_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, membercnt_id) VALUES(?,?)")
                val = (ctx.guild.id, channel)
                await ctx.send(f"⚙ **| Member count channel id has been set to: {channel}**")
            else:
                sql = ("UPDATE main SET membercnt_id = ? where guild_id = ?")
                val = (channel, ctx.guild.id)
                await ctx.send(f"⚙ **| Member count channel id has been updated to: {channel}**")

            cursor.execute(sql, val)
            db.commit()
            try:
                cursor.execute(
                    f"SELECT membercnt_id FROM main WHERE guild_id = {ctx.guild.id}")
                getchannel = cursor.fetchone()
                channell = ctx.guild.get_channel(int(getchannel[0]))
                await channell.edit(name=f'Members: {ctx.guild.member_count}')
            except:
                ctx.send("**⚠ | Could not update membercount**")
            cursor.close()
            db.close()
        else:
            await ctx.send("**⚠ | You don't have the perms to do that!**")

    @membercount.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def refresh(self, ctx):
        await ctx.message.delete()
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT membercnt_id FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result == None:
            print("No channel set")
        else:
            try:
                channell = ctx.guild.get_channel(int(result[0]))
                await channell.edit(name=f'Members: {ctx.guild.member_count}')
                msg = await ctx.send("**⚙ |  Membercount refreshed**")
                await asyncio.sleep(2)
                await msg.delete()
            except:
                errormsg = await ctx.send("**⚠ | No membercount set**")
                await asyncio.sleep(2)
                await errormsg.delete()
        cursor.close()
        db.close()

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def moderation(self, ctx):
        embed = discord.Embed(
            title="⚙️ Moderation", description="Configure moderation commands", color=0x006ce0)
        embed.add_field(
            name="-moderation setlog [channel]", value="Set the log channel for moderators", inline=False)
        embed.add_field(
            name="-moderation urlfilter [enable | disable]", value="Enable or disable the url filter", inline=False)
        embed.add_field(
            name="-moderation invitefilter [enable | disable]", value="Enable or disable the invite filter", inline=False)
        embed.set_footer(
            text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @moderation.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def setlog(self, ctx, channel: discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT modlog_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, modlog_id) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"⚙ **| Moderation log has been set to {channel.mention}**")

            else:
                sql = ("UPDATE main SET modlog_id = ? where guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"⚙ **| Moderation log has been updated to {channel.mention}**")

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else:
            await ctx.send("**⚠ | You don't have the perms to do that!**")

    @moderation.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def urlfilter(self, ctx, arg):
        if arg.lower() == "enable":
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            sql = (
                "UPDATE main SET urlfilter = ? where guild_id = ?")
            val = ("1", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            await ctx.send(f"⚙** | Url filter has been enabled!**")
        elif arg.lower() == "disable":
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            sql = (
                "UPDATE main SET urlfilter = ? where guild_id = ?")
            val = ("0", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            await ctx.send(f"⚙** | Url filter has been disabled!**")
        else:
            await ctx.send("**⚠ | Valid arguments: `enable`, `disable`!**")

    @moderation.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def invitefilter(self, ctx, arg):
        if arg.lower() == "enable":
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            sql = (
                "UPDATE main SET invitefilter = ? where guild_id = ?")
            val = ("1", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            await ctx.send(f"⚙** | Invite filter has been enabled!**")
        elif arg.lower() == "disable":
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            sql = (
                "UPDATE main SET invitefilter = ? where guild_id = ?")
            val = ("0", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            await ctx.send(f"⚙** | Invite filter has been disabled!**")
        else:
            await ctx.send("**⚠ | Valid arguments: `enable`, `disable`!**")

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def suggestions(self, ctx):
        embed = discord.Embed(
            title="⚙️ Suggestions", description="Set the channels for server suggestions!", color=0x006ce0)
        embed.add_field(name="-suggestions setchannel [channel]",
                        value="Set the channel where new suggestions will be send to and people will be able to vote.", inline=False)
        embed.add_field(name="-suggestions sethandledchannel [channel]",
                        value="Set the channel where the rejected and accepted suggesions will be displayed.", inline=False)
        embed.set_image(url="https://i.imgur.com/rtWtBch.png")
        embed.set_footer(
            text=f"This is an example of how you could name your channels.")
        await ctx.send(embed=embed)

    @suggestions.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def setchannel(self, ctx, channel: discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT sugs FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, sugs) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"⚙ | Suggestions channel has been set to {channel.mention}")

            else:
                sql = ("UPDATE main SET sugs = ? where guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"⚙ | Suggestions channel has been updated to {channel.mention}")

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else:
            await ctx.send("**⚠ | You don't have the perms to do that!**")

    @suggestions.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def sethandledchannel(self, ctx, channel: discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT handsugs FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, handsugs) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"⚙ | Handled suggestions channel has been set to {channel.mention}")

            else:
                sql = ("UPDATE main SET handsugs = ? where guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"⚙ | Handled suggestions channel has been updated to {channel.mention}")

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else:
            await ctx.send("**⚠ | You don't have the perms to do that!**")


def setup(client):
    client.add_cog(Config(client))
    print('Config loaded succesfully')
