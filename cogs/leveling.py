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
import math
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

webs = str("Pineapplebot.ga")
options = [1, 1, 2, 2, 3, 3, 4]


class Leveling(commands.Cog, name='Leveling'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.guild.id == 850430800150659104 or message.guild.id == 110373943822540800 or message.guild.id == 439866052684283905 or message.guild.id == 796048327024050176 or message.guild.id == 110373943822540800:
                return
        except:
            pass
        try:
            if message.author.bot:
                return
            elif message.content.startswith("-"):
                db = sqlite3.connect('cogs/main.sqlite')
                cursor = db.cursor()
                sql = (
                    "UPDATE leveling SET avatar = ?, username = ?, discriminator = ? WHERE guild_id = ? and user = ?")
                val = (str(message.author.avatar_url), message.author.name, message.author.discriminator,
                       str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()
                return
            else:
                db = sqlite3.connect('cogs/main.sqlite')
                cursor = db.cursor()
                cursor.execute(
                    f"SELECT user FROM leveling WHERE guild_id = '{message.guild.id}' and user = '{message.author.id}'")
                result = cursor.fetchone()
                if result is None:
                    sql = (
                        "INSERT INTO leveling(guild_id, user, exp, lvl, avatar, username, discriminator) VALUES(?,?,?,?,?,?,?)")
                    val = (message.guild.id, message.author.id,
                           random.choice(options), 0, str(message.author.avatar_url), message.author.name, message.author.discriminator)
                    cursor.execute(sql, val)
                    db.commit()

                else:
                    cursor.execute(
                        f"SELECT user, exp, lvl FROM leveling WHERE guild_id = '{message.guild.id}' and user = '{message.author.id}'")
                    result1 = cursor.fetchone()
                    exp = int(result1[1])
                    sql = (
                        "UPDATE leveling SET exp = exp + ?, avatar = ?, username = ?, discriminator = ? WHERE guild_id = ? and user = ?")
                    val = (random.choice(options), str(message.author.avatar_url), message.author.name, message.author.discriminator,
                           str(message.guild.id), str(message.author.id))
                    cursor.execute(sql, val)
                    db.commit()

                    cursor.execute(
                        f"SELECT user, exp, lvl FROM leveling WHERE guild_id = '{message.guild.id}' and user = '{message.author.id}'")
                    result2 = cursor.fetchone()
                    xp_start = int(result2[1])
                    lvl_start = int(result2[2])
                    xp_end = math.floor(
                        5 * (lvl_start ^ 2) + 50 * lvl_start + 100)
                    if xp_end < xp_start:
                        await message.channel.send(f"{message.author.mention} has leveled up to level {lvl_start + 1}!")
                        sql = (
                            "UPDATE leveling SET lvl = ? WHERE guild_id = ? and user = ?")
                        val = (int(lvl_start + 1), str(message.guild.id),
                               str(message.author.id))
                        cursor.execute(sql, val)
                        db.commit()
                        sql1 = (
                            "UPDATE leveling SET exp = ? WHERE guild_id = ? and user = ?")
                        val1 = (0, str(message.guild.id),
                                str(message.author.id))
                        cursor.execute(sql1, val1)
                        db.commit()
                cursor.close()
                db.close()
        except:
            pass

    @commands.command()
    @commands.guild_only()
    async def rank(self, ctx, user: discord.User = None):
        def kform(num, round_to=1):
            if abs(num) < 1000:
                return num
            else:
                magnitude = 0
                while abs(num) >= 1000:
                    magnitude += 1
                    num = round(num / 1000.0, round_to)
                return '{:.{}f}{}'.format(round(num, round_to), round_to, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

        if user is not None:
            if user.bot:
                await ctx.send("**Bot's can't be ranked.**")
            else:
                db = sqlite3.connect('cogs/main.sqlite')
                cursor = db.cursor()
                cursor.execute(
                    f"SELECT user, exp, lvl FROM leveling WHERE guild_id = '{ctx.guild.id}' and user = '{user.id}'")
                result = cursor.fetchone()
                sql = (
                    "UPDATE main SET serverlogo = ? WHERE guild_id = ?")
                val = (str(ctx.guild.icon_url), ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                if result is None:
                    await ctx.send("**That user is not ranked.**")
                else:
                    lvl_start = int(result[2])
                    #embed = discord.Embed(title=f"{user.name}", color=0x006ac7)
                    # embed.set_thumbnail(url=f"{user.avatar_url}")
                    # embed.add_field(
                    #    name="Level", value=f"{lvl_start}", inline=True)
                    # embed.add_field(name="Experience",
                    #                value=f"{str(result[1])} / {math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)}", inline=True)
                    #embed.set_footer(text=f"Pineapplebot.ga | {ctx.author}")
                    # await ctx.send(embed=embed)
                    base = Image.open("cardb.png").convert("RGBA")
                    txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

                    asset = user.avatar_url_as(size=256)
                    data = BytesIO(await asset.read())
                    pfp = Image.open(data)

                    pfp = pfp.resize((180, 180))
                    base.paste(pfp, (50, 50))

                    # get a font
                    fnt = ImageFont.truetype("arial.ttf", 35)
                    nm = ImageFont.truetype("arial.ttf", 50)
                    xpp = ImageFont.truetype("arial.ttf", 25)
                    # get a drawing context
                    d = ImageDraw.Draw(txt)

                    d.text((260, 45), f"{user}", font=nm,
                           fill=(7, 99, 190, 255))
                    d.text((260, 110), f"Level: {lvl_start}", font=fnt, fill=(
                        255, 255, 255, 255))
                    d.text(
                        (260, 155), f"Exp: {kform(result[1])} / {kform(math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100))}", font=xpp, fill=(255, 255, 255, 255))

                    assett = Image.open(
                        f"levelbars/{math.floor(100*(result[1]/math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)))}.png")
                    base.paste(assett, (260, 195))

                    out = Image.alpha_composite(base, txt)
                    out.save('levelcard.png')
                    await ctx.send(file=discord.File('levelcard.png'))
                cursor.close()
                db.close()
        elif user is None:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f"SELECT user, exp, lvl FROM leveling WHERE guild_id = '{ctx.guild.id}' and user = '{ctx.author.id}'")
            result = cursor.fetchone()
            sql = (
                "UPDATE main SET serverlogo = ? WHERE guild_id = ?")
            val = (str(ctx.guild.icon_url), ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            if result is None:
                msg = await ctx.send("**📊 | That user is not ranked.**")
                await asyncio.sleep(3)
                await msg.delete()
            else:
                lvl_start = int(result[2])
                # embed = discord.Embed(
                #    title=f"{ctx.author.name}", color=0x006ac7)
                # embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
                # embed.add_field(
                #    name="Level", value=f"{str(result[2])}", inline=True)
                # embed.add_field(name="Experience",
                #                value=f"{str(result[1])} / {math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)}", inline=True)
                #embed.set_footer(text=f"Pineapplebot.ga | {ctx.author}")
                # await ctx.send(embed=embed)
                base = Image.open("cardb.png").convert("RGBA")
                txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

                asset = ctx.author.avatar_url_as(size=256)
                data = BytesIO(await asset.read())
                pfp = Image.open(data)

                pfp = pfp.resize((180, 180))
                base.paste(pfp, (50, 50))

                # get a font
                fnt = ImageFont.truetype("arial.ttf", 35)
                nm = ImageFont.truetype("arial.ttf", 50)
                xpp = ImageFont.truetype("arial.ttf", 25)
                # get a drawing context
                d = ImageDraw.Draw(txt)

                d.text((260, 45), f"{ctx.author}", font=nm,
                       fill=(7, 99, 190, 255))
                d.text((260, 110), f"Level: {lvl_start}", font=fnt, fill=(
                    255, 255, 255, 255))
                d.text(
                    (260, 155), f"Exp: {kform(result[1])} / {kform(math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100))}", font=xpp, fill=(255, 255, 255, 255))

                assett = Image.open(
                    f"levelbars/{math.floor(100*(result[1]/math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)))}.png")
                base.paste(assett, (260, 195))

                out = Image.alpha_composite(base, txt)
                out.save('levelcard.png')
                await ctx.send(file=discord.File('levelcard.png'))
            cursor.close()
            db.close()

    @commands.command()
    @commands.guild_only()
    async def leaderboard(self, ctx):
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT lvl, exp, user FROM leveling WHERE guild_id = {ctx.guild.id} ORDER BY lvl DESC, exp DESC LIMIT 5")
        result = cursor.fetchmany(5)
        sql = (
                "UPDATE main SET serverlogo = ?, guild_name = ? WHERE guild_id = ?")
        val = (str(ctx.guild.icon_url), ctx.guild.name, ctx.guild.id)
        cursor.execute(sql, val)
        db.commit()
        if result is not None:
            embed = discord.Embed(title="Levels leaderboard",
                                  description=f"{ctx.guild.name}", color=0x0068d6)
            embed.add_field(name="** **", value=f"Visit the leveling leaderboard [here](https://pineapplebot.ga/leveling.html?&guild={ctx.guild.id})")
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

        #if len(result) == 1:
        #    lvl1 = int(result[0][0])
        #    xp1 = int(result[0][1])
        #    usr1 = self.client.get_user(int(result[0][2]))
#
        #    embed = discord.Embed(title="Levels leaderboard",
        #                          description=f"{ctx.guild.name}", color=0x0068d6)
        #    embed.set_thumbnail(
        #        url="https://www.freeiconspng.com/uploads/leaderboard-icon-3.png")
        #    embed.add_field(
        #        name=f"1) {usr1}", value=f"**level:** {lvl1} \n**Experience:** {xp1}\n\n\n", inline=False)
        #    embed.set_footer(text=f"{webs} | {ctx.author}")
        #    await ctx.send(embed=embed)
#
        #if len(result) == 2:
        #    lvl1 = int(result[0][0])
        #    xp1 = int(result[0][1])
        #    usr1 = self.client.get_user(int(result[0][2]))
#
        #    lvl2 = int(result[1][0])
        #    xp2 = int(result[1][1])
        #    usr2 = self.client.get_user(int(result[1][2]))
#
        #    embed = discord.Embed(title="Levels leaderboard",
        #                          description=f"{ctx.guild.name}", color=0x0068d6)
        #    embed.set_thumbnail(
        #        url="https://www.freeiconspng.com/uploads/leaderboard-icon-3.png")
        #    embed.add_field(
        #        name=f"1) {usr1}", value=f"**level:** {lvl1} \n**Experience:** {xp1}\n\n\n", inline=False)
        #    embed.add_field(
        #        name=f"2) {usr2}", value=f"**level:** {lvl2} \n**Experience:** {xp2}\n\n\n", inline=False)
        #    embed.set_footer(text=f"{webs} | {ctx.author}")
        #    await ctx.send(embed=embed)
#
        #if len(result) == 3:
        #    lvl1 = int(result[0][0])
        #    xp1 = int(result[0][1])
        #    usr1 = self.client.get_user(int(result[0][2]))
#
        #    lvl2 = int(result[1][0])
        #    xp2 = int(result[1][1])
        #    usr2 = self.client.get_user(int(result[1][2]))
#
        #    lvl3 = int(result[2][0])
        #    xp3 = int(result[2][1])
        #    usr3 = self.client.get_user(int(result[2][2]))
#
        #    embed = discord.Embed(title="Levels leaderboard",
        #                          description=f"{ctx.guild.name}", color=0x0068d6)
        #    embed.set_thumbnail(
        #        url="https://www.freeiconspng.com/uploads/leaderboard-icon-3.png")
        #    embed.add_field(
        #        name=f"1) {usr1}", value=f"**level:** {lvl1} \n**Experience:** {xp1}\n\n\n", inline=False)
        #    embed.add_field(
        #        name=f"2) {usr2}", value=f"**level:** {lvl2} \n**Experience:** {xp2}\n\n\n", inline=False)
        #    embed.add_field(
        #        name=f"3) {usr3}", value=f"**level:** {lvl3} \n**Experience:** {xp3}\n\n\n", inline=False)
        #    embed.set_footer(text=f"Pineapplebot.ga | {ctx.author}")
        #    await ctx.send(embed=embed)
#
        #if len(result) == 4:
        #    lvl1 = int(result[0][0])
        #    xp1 = int(result[0][1])
        #    usr1 = self.client.get_user(int(result[0][2]))
#
        #    lvl2 = int(result[1][0])
        #    xp2 = int(result[1][1])
        #    usr2 = self.client.get_user(int(result[1][2]))
#
        #    lvl3 = int(result[2][0])
        #    xp3 = int(result[2][1])
        #    usr3 = self.client.get_user(int(result[2][2]))
#
        #    lvl4 = int(result[3][0])
        #    xp4 = int(result[3][1])
        #    usr4 = self.client.get_user(int(result[3][2]))
#
        #    embed = discord.Embed(title="Levels leaderboard",
        #                          description=f"{ctx.guild.name}", color=0x0068d6)
        #    embed.set_thumbnail(
        #        url="https://www.freeiconspng.com/uploads/leaderboard-icon-3.png")
        #    embed.add_field(
        #        name=f"1) {usr1}", value=f"**level:** {lvl1} \n**Experience:** {xp1}\n\n\n", inline=False)
        #    embed.add_field(
        #        name=f"2) {usr2}", value=f"**level:** {lvl2} \n**Experience:** {xp2}\n\n\n", inline=False)
        #    embed.add_field(
        #        name=f"3) {usr3}", value=f"**level:** {lvl3} \n**Experience:** {xp3}\n\n\n", inline=False)
        #    embed.add_field(
        #        name=f"4) {usr4}", value=f"**level:** {lvl4} \n**Experience:** {xp4}\n\n\n", inline=False)
        #    embed.set_footer(text=f"Pineapplebot.ga | {ctx.author}")
        #    await ctx.send(embed=embed)
#
        #if len(result) > 4:
        #    lvl1 = int(result[0][0])
        #    xp1 = int(result[0][1])
        #    usr1 = self.client.get_user(int(result[0][2]))
#
        #    lvl2 = int(result[1][0])
        #    xp2 = int(result[1][1])
        #    usr2 = self.client.get_user(int(result[1][2]))
#
        #    lvl3 = int(result[2][0])
        #    xp3 = int(result[2][1])
        #    usr3 = self.client.get_user(int(result[2][2]))
#
        #    lvl4 = int(result[3][0])
        #    xp4 = int(result[3][1])
        #    usr4 = self.client.get_user(int(result[3][2]))
#
        #    lvl5 = int(result[4][0])
        #    xp5 = int(result[4][1])
        #    usr5 = self.client.get_user(int(result[4][2]))
#
        #    embed = discord.Embed(title="Levels leaderboard",
        #                          description=f"{ctx.guild.name}", color=0x0068d6)
        #    embed.set_thumbnail(
        #        url="https://www.freeiconspng.com/uploads/leaderboard-icon-3.png")
        #    embed.add_field(
        #        name=f"1) {usr1}", value=f"**level:** {lvl1} \n**Experience:** {xp1}\n\n\n", inline=False)
        #    embed.add_field(
        #        name=f"2) {usr2}", value=f"**level:** {lvl2} \n**Experience:** {xp2}\n\n\n", inline=False)
        #    embed.add_field(
        #        name=f"3) {usr3}", value=f"**level:** {lvl3} \n**Experience:** {xp3}\n\n\n", inline=False)
        #    embed.add_field(
        #        name=f"4) {usr4}", value=f"**level:** {lvl4} \n**Experience:** {xp4}\n\n\n", inline=False)
        #    embed.add_field(
        #        name=f"5) {usr5}", value=f"**level:** {lvl5} \n**Experience:** {xp5}\n\n\n", inline=False)
        #    embed.set_footer(text=f"Pineapplebot.ga | {ctx.author}")
        #    await ctx.send(embed=embed)

        cursor.close()
        db.close()

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def levels(self, ctx):
        embed = discord.Embed(title="Levels commands", color=0x0068d6)
        embed.set_thumbnail(
            url="https://www.freeiconspng.com/uploads/leaderboard-icon-3.png")
        embed.add_field(
            name=f"-rank (optional: [user])", value=f"Show the leveling card of a user", inline=True)
        embed.add_field(
            name=f"-leaderboard", value=f"Show de leveling leaderboard of the server", inline=True)
        embed.add_field(
            name=f"-levels set [user] (optional: [lvl] [exp])", value=f"Reset or set the level of a user.", inline=True)
        embed.set_footer(text=f"Pineapplebot.ga | {ctx.author}")
        await ctx.send(embed=embed)

    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    @levels.command(name="set")
    async def _set(self, ctx, user: discord.User, level=0, exp=0):
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        sql = (
            f"UPDATE leveling SET lvl = ?, exp = ? WHERE guild_id = {ctx.guild.id} and user = {user.id}")
        val = (level, exp)
        cursor.execute(sql, val)
        db.commit()
        if level == 0 and exp == 0:
            await ctx.send(f"📊 | Levels have been reset for {user.mention}!")
        else:
            await ctx.send(f"📊 | {user.mention} has been given **{level}** levels and **{exp}** exp!")
        await ctx.message.delete()
        cursor.close()
        db.close()


def setup(client):
    client.add_cog(Leveling(client))
    print('Leveling loaded succesfully')
