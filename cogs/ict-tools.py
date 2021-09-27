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


webs = str("Pineapplebot.ga")


class Ict(commands.Cog, name='ICT tools'):

    def __init__(self, client):
        self.client = client

    @commands.command(name='shorturl')
    @commands.guild_only()
    async def shorturl(self, ctx, arg1, arg2):
        try:
            key = "9999edf2914f0da88e0224b9b10ba035db4eb"
            url = urllib.parse.quote('{}'.format(arg1))
            name = '{}'.format(arg2)
            r = requests.get(
                'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(key, url, name))
            print("{}".format(r))
            d = r.json()
            short = d["url"]["shortLink"]
            embed = discord.Embed(title="🔗 Short URL", color=0x006ec2)
            embed.add_field(name="URL:", value=f"{short}", inline=True)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
            print(f"{ctx.author} used shorturl for {arg1} and called it {arg2}")
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(
                name="Usage:", value="`-shorturl [url] [name]`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(name='iplookup')
    @commands.guild_only()
    async def iplookup(self, ctx, ip):
        try:
            key = "470a28351104ed5b6aa6259fe76baf9a"
            r = requests.get(
                f'http://api.ipstack.com/{ip}?access_key={key}&format=1')

            d = r.json()
            ip = d["ip"]
            soort = d["type"]
            land = d["country_name"]
            stad = d["city"]
            zipp = d["zip"]
            lat = d["latitude"]
            long = d["longitude"]
            embed = discord.Embed(
                title="🕵️ IP lookup", description="Find the location of an IP adress (not always accurate)", color=0x002aff)
            embed.set_thumbnail(
                url="https://pngimg.com/uploads/hacker/hacker_PNG33.png")
            embed.add_field(name=f"{soort}", value=f"{ip}", inline=False)
            embed.add_field(name="City", value=f"{stad}", inline=True)
            embed.add_field(name="Zip", value=f"{zipp}", inline=True)
            embed.add_field(name="Latitude", value=f"{lat}", inline=False)
            embed.add_field(name="Longitude", value=f"{long}", inline=True)
            embed.add_field(name="Country", value=f"{land}", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
            print(f"{ctx.author} looked up {ip}")
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(
                name="Usage:", value="`-iplookup [ip]`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(name='qr')
    @commands.guild_only()
    async def qr(self, ctx, url):
        try:
            embed = discord.Embed(
                title="🔗 QR code", description=f"QR code for {url}", color=0x006ec2)
            embed.set_image(
                url=f"https://www.qrtag.net/api/qr_9.png?url={url}")
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
            print(f"{ctx.author} made a qr code for {url}")
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(name="Usage:", value="`-qr [url]`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(name='screenshot')
    @commands.guild_only()
    async def screenshot(self, ctx, url):
        try:
            loading = discord.Embed(
                title="📸 Screenshot", description="<a:loading:841639840785498173> Screenshot is processing...", color=0x006ec2)
            loading.set_footer(text="This might take a while.")
            msg = await ctx.send(embed=loading)
            r = requests.get(
                f'https://shot.screenshotapi.net/screenshot?&url={url}&full_page=true&output=json&file_type=png&block_ads=true&no_cookie_banners=true&wait_for_event=load')
            d = r.json()
            screen = d["screenshot"]
            embed = discord.Embed(
                title="📸 Screenshot", description=f"Screenshot of {url}", color=0x006ec2)
            embed.set_image(
                url=f"{screen}")
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await msg.edit(embed=embed)
            print(f"{ctx.author} made a screenshot from {url}")
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(
                name="Usage:", value="`-screenshot [url]`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Ict(client))
    print('ICT-tools loaded succesfully')
