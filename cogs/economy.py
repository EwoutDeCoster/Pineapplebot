import inspect
import discord
from discord import colour
from discord import embeds
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
import time

webs = str("Pineapplebot.ga")


class Economy(commands.Cog, name='Economy'):

    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['work'])
    @commands.guild_only()
    async def mine(self, ctx):
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        amount = random.randint(3, 10)

        cursor.execute(
            f"SELECT guild, user FROM economy WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}")
        result = cursor.fetchone()

        if result is None:
            sql = ("INSERT INTO economy(guild, user, silver) VALUES(?,?,?)")
            val = (ctx.guild.id, ctx.author.id, amount)
            cursor.execute(sql, val)
            db.commit()
            embed = discord.Embed(
                title=":pick: Mine", description=f"You just gained <:silver:856609576459304961> **{amount}** by mining", color=0x005ec2)
            embed.set_thumbnail(url=ctx.author.avatar_url_as(size=256))
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

        else:
            sql = (
                "UPDATE economy SET silver = silver + ? where guild = ? and user = ?")
            val = (amount, ctx.guild.id, ctx.author.id)
            cursor.execute(sql, val)
            db.commit()
            embed = discord.Embed(
                title=":pick: Mine", description=f"You just gained <:silver:856609576459304961> **{amount}** by mining", color=0x005ec2)
            embed.set_thumbnail(url=ctx.author.avatar_url_as(size=256))
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
        cursor.close()
        db.close()

    @commands.command(aliases=['bal'])
    @commands.guild_only()
    async def balance(self, ctx):

        def kform(num, round_to=2):
            if abs(num) < 1000:
                return num
            else:
                magnitude = 0
                while abs(num) >= 1000:
                    magnitude += 1
                    num = round(num / 1000.0, round_to)
                return '{:.{}f}{}'.format(round(num, round_to), round_to, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()

        cursor.execute(
            f"SELECT guild, user, silver FROM economy WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}")
        result = cursor.fetchone()

        if result is None:
            embed = discord.Embed(
                title="Balance", description=f"<:silver:856609576459304961> **0**", color=0x005ec2)
            embed.set_thumbnail(url=ctx.author.avatar_url_as(size=256))
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Balance", description=f"<:silver:856609576459304961> **{kform(int(result[2]))}**", color=0x005ec2)
            embed.set_thumbnail(url=ctx.author.avatar_url_as(size=256))
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
        cursor.close()
        db.close()

    @commands.command()
    @commands.guild_only()
    async def donate(self, ctx, person: discord.User = None, amount = None):
        if person is None or amount is None:
            await ctx.send("⚠️ **| Correct usage: `-donate [member] [amount]`**")
            return
        def kform(num, round_to=2):
            if abs(num) < 1000:
                return num
            else:
                magnitude = 0
                while abs(num) >= 1000:
                    magnitude += 1
                    num = round(num / 1000.0, round_to)
                return '{:.{}f}{}'.format(round(num, round_to), round_to, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
        if ctx.author.id == person.id:
            await ctx.send("<a:no:898507018527211540> **| You can't donate to yourself!**")
        else:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()

            cursor.execute(
                f"SELECT guild, user, silver FROM economy WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}")
            result = cursor.fetchone()
            if int(amount) <= result[2]:
                sql = (
                    "UPDATE economy SET silver = silver + ? where guild = ? and user = ?")
                val = (amount, ctx.guild.id, person.id)
                cursor.execute(sql, val)
                db.commit()

                sql1 = (
                    "UPDATE economy SET silver = silver - ? where guild = ? and user = ?")
                val1 = (amount, ctx.guild.id, ctx.author.id)
                cursor.execute(sql1, val1)
                db.commit()
                embed = discord.Embed(
                    title="💖 Donation", description=f"{ctx.author.mention} gave <:silver:856609576459304961> **{kform(int(amount))}** to {person.mention}", color=0x005ec2)
                embed.set_thumbnail(url=ctx.author.avatar_url_as(size=256))
                embed.set_footer(text=f"{webs} | {ctx.author}")
                await ctx.send(embed=embed)

            else:
                await ctx.message.reply("<a:no:898507018527211540> **| You don't have enough silver!**")
            cursor.close()
            db.close()

    @commands.command(aliases=['cf'])
    @commands.guild_only()
    async def coinflip(self, ctx, choice, amount):
        def kform(num, round_to=2):
            if abs(num) < 1000:
                return num
            else:
                magnitude = 0
                while abs(num) >= 1000:
                    magnitude += 1
                    num = round(num / 1000.0, round_to)
                return '{:.{}f}{}'.format(round(num, round_to), round_to, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
        try:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()

            cursor.execute(
                f"SELECT guild, user, silver FROM economy WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}")
            result = cursor.fetchone()
            if amount.lower() == "all":
                amount = result[2]
            if result is None:
                await ctx.message.reply("<a:no:898507018527211540> **| You don't have any silver!**")
            elif int(amount) <= result[2]:

                flip = random.choice(["Heads", "Tails"])
                if flip == "Tails":
                    if choice.lower() == "tails":
                        sql = (
                            "UPDATE economy SET silver = silver + ? where guild = ? and user = ?")
                        val = (amount, ctx.guild.id, ctx.author.id)
                        cursor.execute(sql, val)
                        db.commit()
                        embed = discord.Embed(title="🎉 You won!",
                                              description=f"**It's tails!**\nYou've earned {kform(int(amount))} silver!", color=0x00FF00)
                        embed.set_thumbnail(
                            url="https://www.nicepng.com/png/full/84-848244_1-euro-euro-coin-png.png")
                        embed.set_footer(text=f"{webs}")
                        await ctx.send(embed=embed)
                    elif choice.lower() == "heads":
                        embed = discord.Embed(title="😓 You lost!",
                                              description=f"**It's tails!**\nYou've lost {kform(int(amount))} silver!", color=0xFF4B24)
                        embed.set_thumbnail(
                            url="https://www.nicepng.com/png/full/84-848244_1-euro-euro-coin-png.png")
                        embed.set_footer(text=f"{webs}")
                        await ctx.send(embed=embed)
                        sql = (
                            "UPDATE economy SET silver = silver - ? where guild = ? and user = ?")
                        val = (amount, ctx.guild.id, ctx.author.id)
                        cursor.execute(sql, val)
                        db.commit()
                    else:
                        await ctx.send("<a:no:898507018527211540> **| Choose between 'tails' and 'heads'**")

                else:
                    if choice.lower() == "heads":
                        embed = discord.Embed(title="🎉 You won!",
                                              description=f"**It's heads!**\nYou've earned {kform(int(amount))} silver!", color=0x00FF00)
                        embed.set_thumbnail(
                            url="https://i.imgur.com/J7gkZc6.png")
                        embed.set_footer(text=f"{webs}")
                        await ctx.send(embed=embed)
                        sql = (
                            "UPDATE economy SET silver = silver + ? where guild = ? and user = ?")
                        val = (amount, ctx.guild.id, ctx.author.id)
                        cursor.execute(sql, val)
                        db.commit()
                    elif choice.lower() == "tails":
                        embed = discord.Embed(title="😓 You lost!",
                                              description=f"**It's heads!**\nYou've lost {kform(int(amount))} silver!", color=0xFF4B24)
                        embed.set_thumbnail(
                            url="https://i.imgur.com/J7gkZc6.png")
                        embed.set_footer(text=f"{webs}")
                        await ctx.send(embed=embed)
                        sql = (
                            "UPDATE economy SET silver = silver - ? where guild = ? and user = ?")
                        val = (amount, ctx.guild.id, ctx.author.id)
                        cursor.execute(sql, val)
                        db.commit()

                    else:
                        await ctx.send("<a:no:898507018527211540> **| Choose between 'tails' and 'heads'**")

            else:
                await ctx.message.reply("<a:no:898507018527211540> **| You don't have enough silver!**")
        except:
            pass
        cursor.close()
        db.close()

    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def daily(self, ctx):
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT guild, user, silver FROM economy WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}")
        result = cursor.fetchone()
        reward = random.randint(300, 800)
        if result is None:
            sql = (
                "INSERT INTO economy(guild, user, silver, username, discriminator, avatar) VALUES(?,?,?,?,?,?)")
            val = (ctx.guild.id, ctx.author.id, reward, ctx.author.name,
                   ctx.author.discriminator, str(ctx.author.avatar_url))
            cursor.execute(sql, val)
            db.commit()
        else:
            sql = (
                "UPDATE economy SET silver = silver + ?, username = ?, discriminator = ?, avatar = ? where guild = ? and user = ?")
            val = (reward, ctx.author.name, ctx.author.discriminator,
                   str(ctx.author.avatar_url), ctx.guild.id, ctx.author.id)
            cursor.execute(sql, val)
            sql1 = (
                        "UPDATE main SET serverlogo = ?, guild_name = ? WHERE guild_id = ?")
            val1 = (str(ctx.guild.icon_url), ctx.guild.name, ctx.guild.id)
            cursor.execute(sql1, val1)
            db.commit()
        embed = discord.Embed(
            title="📆 Daily reward", description=f"You've claimed your daily reward!\n<:silver:856609576459304961> **{reward}**", color=0x005ec2)
        embed.set_thumbnail(url=ctx.author.avatar_url_as(size=256))
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def hourly(self, ctx):
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT guild, user, silver FROM economy WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}")
        result = cursor.fetchone()
        reward = random.randint(100, 300)
        if result is None:
            sql = ("INSERT INTO economy(guild, user, silver) VALUES(?,?,?)")
            val = (ctx.guild.id, ctx.author.id, reward)
            cursor.execute(sql, val)
            db.commit()
        else:
            sql = (
                "UPDATE economy SET silver = silver + ? where guild = ? and user = ?")
            val = (reward, ctx.guild.id, ctx.author.id)
            cursor.execute(sql, val)
            db.commit()
        embed = discord.Embed(
            title="🕒 Hourly reward", description=f"You've claimed your hourly reward!\n<:silver:856609576459304961> **{reward}**", color=0x005ec2)
        embed.set_thumbnail(url=ctx.author.avatar_url_as(size=256))
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @commands.cooldown(1, 120, commands.BucketType.user)
    @commands.command(aliases=['rob'])
    @commands.guild_only()
    async def fight(self, ctx, user: discord.Member = None):
        if ctx.author == user:
            await ctx.send("⚠️ **| You can't fight yourself**")
        chances = [0, 1]
        if user is None:
            await ctx.send("⚠️ **| Missing argument: `member`**")
            return
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()

        cursor.execute(
            f"SELECT guild, user, silver, metalsword FROM economy WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}")
        result = cursor.fetchone()
        if result is None:
            await ctx.message.reply("<a:no:898507018527211540> **| You don't have any silver!**")
            cursor.close()
            db.close()
            return

        cursor.execute(
            f"SELECT guild, user, silver, metalsword FROM economy WHERE guild = {ctx.guild.id} AND user = {user.id}")
        result1 = cursor.fetchone()
        if result1 is None:
            await ctx.message.reply(f"<a:no:898507018527211540> **| {user} doesn't have any silver!**")
            cursor.close()
            db.close()
            return
        zin = " "
        zin1 = "."
        if result[3] == 1:
            chances.append(1)
            chances.append(1)
            zin = " using your sword "
        if result1[3] == 1:
            chances.append(0)
            chances.append(0)
            zin1 = " because they had a sword!"
        if result1[2] < 40:
            embed = discord.Embed(
                title="💥 Fight", description=f"{user.mention} escaped because they were too weak!", color=0x005ec2)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
            cursor.close()
            db.close()
            return

        if result[2] < 40:
            embed = discord.Embed(
                title="💥 Fight", description=f"You had to escape because you were too weak to defend yourself!", color=0x005ec2)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
            cursor.close()
            db.close()
            return

        if result[2] >= 40 and result1[2] >= 40:
            winner = random.choice(chances)
            stolen = random.randint(30, 40)

            if winner == 0:

                sql = (
                    "UPDATE economy SET silver = silver - ? where guild = ? and user = ?")
                val = (stolen, ctx.guild.id, ctx.author.id)
                cursor.execute(sql, val)
                db.commit()

                sql1 = (
                    "UPDATE economy SET silver = silver + ? where guild = ? and user = ?")
                val1 = (stolen, ctx.guild.id, user.id)
                cursor.execute(sql1, val1)
                db.commit()

                embed = discord.Embed(
                    title="💥 Fight", description=f"You've **lost** the fight with {user.mention}{zin1} They took <:silver:856609576459304961> **{stolen}**", color=0x005ec2)
                embed.set_thumbnail(
                    url="https://thairesidents.com/wp-content/uploads/2020/09/165-1656043_nfs-9-19e-cartoon-fighting-cloud-clipart.png")
                embed.set_footer(text=f"{webs} | {ctx.author}")
                await ctx.send(embed=embed)

            else:

                sql = (
                    "UPDATE economy SET silver = silver + ? where guild = ? and user = ?")
                val = (stolen, ctx.guild.id, ctx.author.id)
                cursor.execute(sql, val)
                db.commit()

                sql1 = (
                    "UPDATE economy SET silver = silver - ? where guild = ? and user = ?")
                val1 = (stolen, ctx.guild.id, user.id)
                cursor.execute(sql1, val1)
                db.commit()

                embed = discord.Embed(
                    title="💥 Fight", description=f"You **won** the fight with {user.mention}{zin}and you stole <:silver:856609576459304961> **{stolen}**", color=0x005ec2)
                embed.set_thumbnail(
                    url="https://thairesidents.com/wp-content/uploads/2020/09/165-1656043_nfs-9-19e-cartoon-fighting-cloud-clipart.png")
                embed.set_footer(text=f"{webs} | {ctx.author}")
                await ctx.send(embed=embed)

        elif result[2] >= 40:
            embed = discord.Embed(
                title="💥 Fight", description=f"{user.mention} escaped because they were too weak!", color=0x005ec2)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

        elif result1[2] >= 40:
            embed = discord.Embed(
                title="💥 Fight", description=f"You had to escape because you were too weak to defend yourself!", color=0x005ec2)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
        cursor.close()
        db.close()

    @commands.command(aliases=['top'])
    @commands.guild_only()
    async def wealth(self, ctx):
        def kform(num, round_to=2):
            if abs(num) < 1000:
                return num
            else:
                magnitude = 0
                while abs(num) >= 1000:
                    magnitude += 1
                    num = round(num / 1000.0, round_to)
                return '{:.{}f}{}'.format(round(num, round_to), round_to, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT guild, user, silver FROM economy WHERE guild = {ctx.guild.id} ORDER BY silver DESC LIMIT 5")
        result = cursor.fetchmany(5)
        sql1 = (
                        "UPDATE main SET serverlogo = ?, guild_name = ? WHERE guild_id = ?")
        val1 = (str(ctx.guild.icon_url), ctx.guild.name, ctx.guild.id)
        cursor.execute(sql1, val1)
        db.commit()
        i = 0
        embed = discord.Embed(title="Silver leaderboard",
                              description=f"Visit the economy leaderboard [here](https://pineapplebot.ga/economy?guild={ctx.guild.id}).", color=0x0068d6)
        #while i < len(result):
        #    username = self.client.get_user(int(result[i][1]))
        #    embed.add_field(name=f"** **",
        #                    value=f"**{i+1})** {username.mention}\n   <:silver:856609576459304961> **{kform(int(result[i][2]))}**", inline=False)
        #    i += 1
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/856609576459304961.png?v=1")
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)
        cursor.close()
        db.close()

    @commands.command(pass_context=True)
    @commands.guild_only()
    async def slots(self, ctx, amount=None):
        def kform(num, round_to=2):
            if abs(num) < 1000:
                return num
            else:
                magnitude = 0
                while abs(num) >= 1000:
                    magnitude += 1
                    num = round(num / 1000.0, round_to)
                return '{:.{}f}{}'.format(round(num, round_to), round_to, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
        try:
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()

            cursor.execute(
                f"SELECT guild, user, silver FROM economy WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}")
            result = cursor.fetchone()

            if amount == None:
                await ctx.send("<a:no:898507018527211540> **| Please enter an amount.**")
                return

            if amount.lower() == "all":
                amount = result[2]

            if int(amount) < 10:
                await ctx.send("<a:no:898507018527211540> **| Your bet must be at least 10 silver.**")
                return

            if result is None:
                await ctx.send("<a:no:898507018527211540> **| You don't have enough silver!**")
                cursor.close()
                db.close()
                return

            bal = int(result[2])

            amount = int(amount)
            if amount > bal:
                await ctx.send("<a:no:898507018527211540> **| You don't have enough silver!**")
                cursor.close()
                db.close()
                return
            if amount < 0:
                await ctx.send("<a:no:898507018527211540> **| Amount should always be positive**")
                cursor.close()
                db.close()
                return

            slots = ['<:gold:856609522965151785>',
                     ':tada:', ':money_with_wings:', ':moneybag:', ':gift:', ":gem:"]
            slot1 = slots[random.randint(0, 5)]
            slot2 = slots[random.randint(0, 5)]
            slot3 = slots[random.randint(0, 5)]

            slotOutput = '| {} | {} | {} |\n'.format(slot1, slot2, slot3)

            spinningall = discord.Embed(title="🎰 Spinning...", color=0x0068d6)
            spinningall.add_field(
                name="| <a:slots:859388574972510238> | <a:slots:859388574972510238> | <a:slots:859388574972510238> |\n \nSpinning", value="You...")

            spinning2 = discord.Embed(title="🎰 Spinning...", color=0x0068d6)
            spinning2.add_field(
                name=f"| {slot1} | <a:slots:859388574972510238> | <a:slots:859388574972510238> |\n \nSpinning", value="You...")

            spinning1 = discord.Embed(title="🎰 Spinning...", color=0x0068d6)
            spinning1.add_field(
                name=f"| {slot1} | {slot2} | <a:slots:859388574972510238> |\n \nSpinning", value="You...")

            spinning0 = discord.Embed(title="🎰 Spinning...", color=0x0068d6)
            spinning0.add_field(
                name=f"| {slot1} | {slot2} | {slot3} |\n \nSpinning", value="You...")

            spin = await ctx.send(embed=spinningall)
            await spin.edit(embed=spinningall)
            await asyncio.sleep(0.6)
            await spin.edit(embed=spinning2)
            await asyncio.sleep(0.6)
            await spin.edit(embed=spinning1)
            await asyncio.sleep(0.6)
            await spin.edit(embed=spinning0)
            await asyncio.sleep(0.6)

            ok = discord.Embed(title="🎰 Slots Machine",
                               color=discord.Color(0x00FF00))
            ok.add_field(name="{}\nWon".format(slotOutput),
                         value=f'You won {kform(1*amount)} silver')

            won = discord.Embed(title="🎰 Slots Machine",
                                color=discord.Color(0xFFF300))
            won.add_field(name="{}\nJackpot!".format(slotOutput),
                          value=f'You won {kform(3*amount)} silver')

            lost = discord.Embed(title="🎰 Slots Machine",
                                 color=discord.Color(0xFF4B24))
            lost.add_field(name="{}\nLost".format(slotOutput),
                           value=f'You lost {kform(1*amount)} silver')

            if slot1 == slot2 == slot3:
                sql = (
                    "UPDATE economy SET silver = silver + ? where guild = ? and user = ?")
                val = (amount*3, ctx.guild.id, ctx.author.id)
                cursor.execute(sql, val)
                db.commit()
                await spin.edit(embed=won)
                cursor.close()
                db.close()
                return

            if slot1 == slot2 or slot1 == slot3 or slot2 == slot3:
                sql = (
                    "UPDATE economy SET silver = silver + ? where guild = ? and user = ?")
                val = (amount, ctx.guild.id, ctx.author.id)
                cursor.execute(sql, val)
                db.commit()

                await spin.edit(embed=ok)
                cursor.close()
                db.close()
                return

            else:
                sql = (
                    "UPDATE economy SET silver = silver - ? where guild = ? and user = ?")
                val = (amount, ctx.guild.id, ctx.author.id)
                cursor.execute(sql, val)
                db.commit()

                await spin.edit(embed=lost)
                cursor.close()
                db.close()
                return
        except:
            await ctx.send("<a:no:898507018527211540> **| Please enter a valid amount.**")

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command()
    @commands.guild_only()
    async def imposter(self, ctx):
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()

        cursor.execute(
            f"SELECT guild, user, silver FROM economy WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}")
        result = cursor.fetchone()

        if result is None:
            await ctx.send("<a:no:898507018527211540> **| You don't have enough silver!**")
            cursor.close()
            db.close()
            return

        if int(result[2]) < 50:
            await ctx.send("<a:no:898507018527211540> **| You should have at least 50 silver to play.**")
            cursor.close()
            db.close()
            return

        crewmates = ["<:redcrewmate:859517185306787890>", "<:orangecrewmate:859517226335993877>",
                     "<:bluecrewmate:859517308358754324>", "<:greencrewmate:859517285093605488>"]
        imposternr = random.randint(0, 3)
        random.shuffle(crewmates)
        startmsg = discord.Embed(title="Who is the imposter?",
                                 description="**One of these crewmates is the imposter. It's your task to unmask him.**\nUnmasking him results in a reward of 250 silver", color=0xFFF300)
        startmsg.set_footer(text=f"{webs} | {ctx.author}")
        msg = await ctx.send(embed=startmsg)
        await msg.add_reaction(f"{crewmates[0]}")
        await msg.add_reaction(f"{crewmates[1]}")
        await msg.add_reaction(f"{crewmates[2]}")
        await msg.add_reaction(f"{crewmates[3]}")
        startmsg.add_field(
            name="** **\nCrewmates:", value=f"** **\n{crewmates[0]} {crewmates[1]} {crewmates[2]} {crewmates[3]}")
        await msg.edit(embed=startmsg)
        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=30.0)
                if user == ctx.author and str(reaction) in crewmates:
                    if str(reaction.emoji) == crewmates[imposternr]:
                        await msg.delete()
                        sql = (
                            "UPDATE economy SET silver = silver + ? where guild = ? and user = ?")
                        val = (200, ctx.guild.id, ctx.author.id)
                        cursor.execute(sql, val)
                        db.commit()
                        win = discord.Embed(title="You have found the imposter!",
                                            description=f"{crewmates[imposternr]} **was the imposter!**\n \nYou won 250 silver!", color=0x00FF00)
                        win.set_footer(text=f"{webs} | {ctx.author}")
                        await ctx.send(embed=win)
                        cursor.close()
                        db.close()
                        return
                    else:
                        await msg.delete()
                        sql = (
                            "UPDATE economy SET silver = silver - ? where guild = ? and user = ?")
                        val = (50, ctx.guild.id, ctx.author.id)
                        cursor.execute(sql, val)
                        db.commit()
                        los = discord.Embed(title="That was not the imposter!",
                                            description=f"{crewmates[imposternr]} **was the imposter!**\n \nYou've lost 50 silver.", color=0xFF4B24)
                        los.set_footer(text=f"{webs} | {ctx.author}")
                        await ctx.send(embed=los)
                        cursor.close()
                        db.close()
                        return
                else:
                    continue
            except:
                await msg.delete()
                await ctx.message.delete()
                error = await ctx.send("<a:no:898507018527211540> **| Time exceeded**")
                await asyncio.sleep(3)
                await error.delete()

    @commands.command(enabled=True)
    @commands.guild_only()
    async def spin(self, ctx):
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT guild, user, silver FROM economy WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}")
        result = cursor.fetchone()

        if result is None:
            await ctx.send("<a:no:898507018527211540> **| You don't have enough silver!**")
            cursor.close()
            db.close()
            return

        if int(result[2]) < 200:
            await ctx.send("<a:no:898507018527211540> **| You should have at least 200 silver to play.**")
            cursor.close()
            db.close()
            return

        choices = [-200, -150, -100, -50, 50, 100, 150, 200]
        images = {
            -100: "https://i.imgur.com/1X6vK7O.png",
            -150: "https://i.imgur.com/zaFHzJl.png",
            -200: "https://i.imgur.com/oVKJtT1.png",
            -50: "https://i.imgur.com/Ch1Il8H.png",
            100: "https://i.imgur.com/vLwbnxY.png",
            200: "https://i.imgur.com/RfzOGnz.png",
            50: "https://i.imgur.com/PtwWd4G.png",
            150: "https://i.imgur.com/fyWSsEG.png",
        }
        result = random.choice(choices)
        if result > 0:
            word = "won"
            colorr = 0x00FF00
            sql = (
                "UPDATE economy SET silver = silver + ? where guild = ? and user = ?")
            val = (result, ctx.guild.id, ctx.author.id)
            cursor.execute(sql, val)
            db.commit()

        else:
            word = "lost"
            colorr = 0xFF4B24
            sql = (
                "UPDATE economy SET silver = silver - ? where guild = ? and user = ?")
            val = (abs(result), ctx.guild.id, ctx.author.id)
            cursor.execute(sql, val)
            db.commit()

        embed = discord.Embed(
            title="Roulette", description=f"**🔀 Spinning...**", color=0x005ec2)
        embed.set_image(
            url="https://i.imgur.com/wETaSUA.gif")
        embed.set_footer(text=f"{webs} | {ctx.author}")
        emb = await ctx.send(embed=embed)

        rembed = discord.Embed(
            title="Roulette", description=f"**You have {word} {abs(result)} silver**", color=colorr)
        rembed.set_image(
            url=f"{images[result]}")
        rembed.set_footer(text=f"{webs} | {ctx.author}")
        await asyncio.sleep(3)
        await emb.edit(embed=rembed)
        cursor.close()
        db.close()

    @commands.command(enabled=True)
    @commands.guild_only()
    async def roulette(self, ctx):
        await ctx.send("❗ **| Use `-spin` instead.**")

    @commands.command()
    @commands.guild_only()
    async def shop(self, ctx):
        embed = discord.Embed(
            title="Silver shop", description="-buy [item]", color=0x0068d6)
        embed.add_field(
            name="** **", value="**<:pinebulldozer:873214898656665652> Mining machine**\nCollects silver for you.\n**<:silver:856609576459304961> `10K`**")
        embed.add_field(
            name="** **", value="**<:sword:907246919212994560> Metal sword**\nUsed to defend yourself.\n**<:silver:856609576459304961> `30K`**")
        embed.set_thumbnail(url="https://i.imgur.com/IBsL97C.png")
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def buy(self, ctx, *, item = None):
        if item is None:
            await ctx.send("⚠️ **| Missing argument: `item`**")
            return
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT silver, minerig, metalsword FROM economy WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}")
        result = cursor.fetchone()

        if item.lower() == "mining machine" or item.lower() == "miningmachine" or item.lower() == "machine":
            price = 10000
            if result[1] == 0:
                if result[0] >= price:
                    sql = (
                        "UPDATE economy SET silver = silver - ?, minerig = 1 where guild = ? and user = ?")
                    val = (price, ctx.guild.id, ctx.author.id)
                    cursor.execute(sql, val)
                    db.commit()
                    embed = discord.Embed(title="You have bought the mining machine!",
                                          description=f"Use `-machine` for more information", color=0x00FF00)
                    embed.set_thumbnail(url="https://i.imgur.com/2w2lkHO.png")
                    embed.set_footer(text=f"{webs} | {ctx.author}")
                    await ctx.send(embed=embed)
                    cursor.close()
                    db.close()
                else:
                    await ctx.send("<a:no:898507018527211540> **| You don't have enough silver!**")
            else:
                await ctx.send("<a:no:898507018527211540> **| You already have a mining rig!**")
        if item.lower() == "metal sword" or item.lower() == "metalsword":
            price = 30000
            if result[2] == 0:
                if result[0] >= price:
                    sql = (
                        "UPDATE economy SET silver = silver - ?, metalsword = 1 where guild = ? and user = ?")
                    val = (price, ctx.guild.id, ctx.author.id)
                    cursor.execute(sql, val)
                    db.commit()
                    embed = discord.Embed(title="You have bought the metal sword!",
                                          description=f"The sword gives you a bigger chance to win `-fight` and will help you win boss fights.", color=0x00FF00)
                    embed.set_thumbnail(url="https://i.imgur.com/JMug1Ni.png")
                    embed.set_footer(text=f"{webs} | {ctx.author}")
                    await ctx.send(embed=embed)
                    cursor.close()
                    db.close()
                else:
                    await ctx.send("<a:no:898507018527211540> **| You don't have enough silver!**")
            else:
                await ctx.send("<a:no:898507018527211540> **| You already have a metal sword!**")
        else:
            await ctx.send("<a:no:898507018527211540> **| Please enter a valid item!**")

    @commands.command(aliases=['inv'])
    @commands.guild_only()
    async def inventory(self, ctx):
        def kform(num, round_to=2):
            if abs(num) < 1000:
                return num
            else:
                magnitude = 0
                while abs(num) >= 1000:
                    magnitude += 1
                    num = round(num / 1000.0, round_to)
                return '{:.{}f}{}'.format(round(num, round_to), round_to, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT silver, minerig, mineriglvl, metalsword FROM economy WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}")
        result = cursor.fetchone()
        embed = discord.Embed(
            title="Inventory", description=f"**Balance:** <:silver:856609576459304961> {kform(result[0])}", color=0x0068d6)
        if result[1] == 1:
            embed.add_field(
                name=f"<:pinebulldozer:873214898656665652> Mining machine `Level {result[2]}`", value="Collects silver for you (collectable every 8h)\n`-machine`")
        if result[3] == 1:
            embed.add_field(
                name=f"<:sword:907246919212994560> Metal Sword", value="The sword gives you a bigger chance to win `-fight` and will help you win boss fights.")
        embed.set_thumbnail(url="https://i.imgur.com/PEsgp8j.png")
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)
        cursor.close()
        db.close()

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def machine(self, ctx):
        def kform(num, round_to=2):
            if abs(num) < 1000:
                return num
            else:
                magnitude = 0
                while abs(num) >= 1000:
                    magnitude += 1
                    num = round(num / 1000.0, round_to)
                return '{:.{}f}{}'.format(round(num, round_to), round_to, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT silver, minerig, mineriglvl FROM economy WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}")
        result = cursor.fetchone()
        needed = 2500 + 750 * int(result[2]) + \
            100 * int(result[2]) * int(result[2])
        cursor.close()
        db.close()
        if int(result[1]) == 1:
            embed = discord.Embed(title="Mining machine",
                                  description=f"`Level {result[2]}`\n**Upgrade price:** <:silver:856609576459304961>`{kform(needed)}`", color=0x0068d6)
            embed.add_field(
                name="** **", value="`-machine collect` to claim your reward.\n`-machine upgrade` to upgrade your machine.")
            embed.set_thumbnail(url="https://i.imgur.com/2w2lkHO.png")
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<a:no:898507018527211540> **| You don't have a mining rig!**")

    @machine.command()
    @commands.cooldown(1, 9000, commands.BucketType.user)
    @commands.guild_only()
    async def collect(self, ctx):
        def kform(num, round_to=2):
            if abs(num) < 1000:
                return num
            else:
                magnitude = 0
                while abs(num) >= 1000:
                    magnitude += 1
                    num = round(num / 1000.0, round_to)
                return '{:.{}f}{}'.format(round(num, round_to), round_to, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT silver, minerig, mineriglvl FROM economy WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}")
        result = cursor.fetchone()
        reward = round(33 * (int(result[2]) ** 2) + 10*int(result[2]) + 225 + random.randint(1, 15*int(result[2])))
        if result[1] == 1:
            sql = (
                "UPDATE economy SET silver = silver + ? where guild = ? and user = ?")
            val = (reward, ctx.guild.id, ctx.author.id)
            cursor.execute(sql, val)
            db.commit()
            embed = discord.Embed(title="Mining machine reward",
                                  description=f"You have collected **<:silver:856609576459304961> {kform(reward)}**.", color=0x00FF00)
            embed.set_thumbnail(url="https://i.imgur.com/2w2lkHO.png")
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<a:no:898507018527211540> **| You don't have a mining rig!**")

    @machine.command()
    @commands.guild_only()
    async def upgrade(self, ctx):
        db = sqlite3.connect('cogs/main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            f"SELECT silver, minerig, mineriglvl FROM economy WHERE guild = {ctx.guild.id} AND user = {ctx.author.id}")
        result = cursor.fetchone()
        needed = int(2500 + 750 * int(result[2]) +
                           100 * int(result[2]) * int(result[2]))
        if needed < int(result[0]):
            sql = (
                "UPDATE economy SET silver = silver - ?, mineriglvl = mineriglvl + 1 where guild = ? and user = ?")
            val = (needed, ctx.guild.id, ctx.author.id)
            cursor.execute(sql, val)
            db.commit()
            embed = discord.Embed(title="You have upgraded your mining machine!",
                                  description=f"Your mining machine is now `Level {int(result[2])+1}`", color=0x00FF00)
            embed.set_thumbnail(url="https://i.imgur.com/2w2lkHO.png")
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
            return
        elif int(result[1]) == 0:
            await ctx.send("<a:no:898507018527211540> **| You don't have a mining rig!**")
            return
        else:
            await ctx.send("<a:no:898507018527211540> **| You don't have a enough silver!**")
            return

    @commands.command(enabled=False)
    @commands.guild_only()
    async def ct(self, ctx):
        await ctx.send(f"{time.time()}")


def setup(client):
    client.add_cog(Economy(client))
    print('Economy loaded succesfully')
