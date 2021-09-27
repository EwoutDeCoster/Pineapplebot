import discord
from discord.ext import commands
import asyncio
import time
import urllib
import requests
import sys
import os
from datetime import datetime, timedelta
import time
import math
from discord import FFmpegPCMAudio
from discord.utils import get
from pathlib import Path
from youtube_dl import YoutubeDL

webs = str("Pineapplebot.ga")


class Radio(commands.Cog, name='Radio'):

    def __init__(self, client):
        self.client = client
        self.is_playing = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.vc = ""
        self.voteskip = []
        self.nowplaying = ""
        self.nowplayingimg = ""
        self.duration = 0
        self.starttime = 0

    @commands.command()
    @commands.guild_only()
    async def airhorn(self, ctx):
        await ctx.message.delete()
        global player
        url = 'airhorn.mp3'
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await asyncio.sleep(1)

        try:
            player = await channel.connect()
        except:
            await ctx.send("⚠ **| An unknown error occured.**")
        player.play(FFmpegPCMAudio(url))

     # searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" %
                                        item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title'], 'thumb': info["thumbnail"], 'duration': info['duration']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # get the first url
            m_url = self.music_queue[0][0]['source']
            self.nowplaying = self.music_queue[0][0]['title']
            self.nowplayingimg = self.music_queue[0][0]['thumb']
            self.duration = self.music_queue[0][0]['duration']

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(
                m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            self.starttime = math.floor(time.time())
            self.voteskip = []
        else:
            self.is_playing = False
            self.voteskip = []

    # infinite loop checking
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            self.nowplaying = self.music_queue[0][0]['title']
            self.nowplayingimg = self.music_queue[0][0]['thumb']
            self.duration = self.music_queue[0][0]['duration']

            # try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])

            # print(self.music_queue)
            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(
                m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            self.starttime = math.floor(time.time())
        else:
            self.is_playing = False
            self.nowplaying = ""
            self.nowplayingimg = ""
            self.duration = 0

    async def stopmusic(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected() and self.is_playing:
            self.vc.stop()
            self.is_playing = False
            self.music_queue = []
            self.vc = ""
            self.voteskip = []
            self.nowplaying = ""
            self.nowplayingimg = ""
        else:
            pass

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(name="play", aliases=['p'])
    @commands.guild_only()
    async def p(self, ctx, *args):
        try:
            query = " ".join(args)

            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                # you need to be connected so that the bot knows where to go
                await ctx.send("⚠ **| Connect to a voice channel!**")
            else:
                song = self.search_yt(query)
                if type(song) == type(True):
                    await ctx.send("⚠ **| Could not download song. Make sure it's not a livestream.**")
                else:
                    embed = discord.Embed(
                        title="Added to queue", description="**{}**\n`{:0>8}`".format(song['title'], str(timedelta(seconds=song['duration']))), color=0xFF9F26)
                    embed.set_thumbnail(
                        url=f"{song['thumb']}")
                    await ctx.send(embed=embed)
                    print(song['duration'])
                    print("{:0>8}".format(
                        str(timedelta(seconds=song['duration']))))

                    self.music_queue.append(
                        [song, voice_channel, ctx.author.id])

                    if self.is_playing == False:
                        await self.play_music()
        except UnexpectedQuoteError as e:
            await ctx.send(f"Something went wrong: {e}")

    @commands.command(name="showtime")
    @commands.guild_only()
    async def showtime(self, ctx):
        await ctx.send(f"{math.floor(time.time())}")

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.group(name="queue", aliases=['q', 'songlist'], invoke_without_command=True)
    @commands.guild_only()
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += f"`{i+1}` " + self.music_queue[i][0]['title'] + " **|** `{:0>8}`".format(
                str(timedelta(seconds=self.music_queue[i][0]['duration']))) + "\n"

        # print(retval)
        if retval != "":
            embed = discord.Embed(
                title="Queue", color=0xFF9F26)
            embed.set_thumbnail(
                url="https://i.imgur.com/oijI9GJ.png")
            embed.add_field(name="Songs:", value=retval, inline=False)
            embed.set_footer(
                text="Use \"-queue remove [number]\" to remove a song.")
            await ctx.send(embed=embed)
        else:
            await ctx.send("⚠ **| No music in queue**")

    @q.command()
    async def remove(self, ctx, index: int):
        if self.music_queue[index - 1][2] == ctx.author.id:
            name = self.music_queue[index - 1][0]['title']
            self.music_queue.pop(index - 1)
            await ctx.send(f"<:check_pine:834872371281264661> **| Removed** `{name}` **from the queue.**")
        else:
            await ctx.send("⚠ **| Someone else added this song.**")

    @commands.cooldown(1, 2, commands.BucketType.guild)
    @commands.has_permissions(manage_messages=True)
    @commands.command(name="forceskip", aliases=['fs'])
    @commands.guild_only()
    async def forceskip(self, ctx):
        try:
            if self.vc != "" and self.vc:
                if self.nowplaying == "":
                    await ctx.send("⚠ **| Nothing is being played**")
                else:
                    self.vc.stop()
                    # try to play next in the queue if it exists
                    await self.play_music()
                    await ctx.send("<:skip:844309432682807377> **| Skipped**")
        except:
            pass

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()
    @commands.command(name="np", aliases=['nowplaying', 'currentsong'])
    async def np(self, ctx):
        if self.nowplaying == "":
            await ctx.send("⚠ **| Nothing is being played**")
        else:
            embed = discord.Embed(
                title="Now Playing:", color=0xFF9F26)
            embed.set_thumbnail(
                url=f"{self.nowplayingimg}")
            embed.add_field(
                name="** **", value=f"<a:playing:844309432699060266> **{self.nowplaying}**\n`{str(timedelta(seconds=(math.floor(time.time()) - self.starttime)))} - {str(timedelta(seconds=self.duration))}`", inline=False)
            await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name="skip", aliases=['s'])
    async def skip(self, ctx):
        try:

            if self.vc != "" and self.vc:
                if ctx.author.id in self.voteskip:
                    await ctx.send("⚠ **| You already voted to skip**")
                else:
                    if self.nowplaying == "":
                        await ctx.send("⚠ **| Nothing is being played**")
                    else:
                        self.voteskip.append(ctx.author.id)
                        if len(self.voteskip) >= math.floor(len(ctx.author.voice.channel.members) / 1.5):
                            self.vc.stop()
                            # try to play next in the queue if it exists
                            await self.play_music()
                            await ctx.send("<:skip:844309432682807377> **| Skipped**")
                        else:
                            await ctx.send(f"<:skip:844309432682807377> **| {len(self.voteskip)} / {math.floor(len(ctx.author.voice.channel.members) / 1.5)}**")
        except:
            pass

    @commands.command()
    @commands.guild_only()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        try:
            await channel.connect()
            await ctx.message.reply(f"🔊 **| Connected to {channel.mention}.**")
            self.nowplaying = ""
            self.nowplayingimg = ""
        except:
            await ctx.message.reply("⚠ **| Already connected to voice.**")

    @commands.command()
    @commands.guild_only()
    async def songs(self, ctx):
        songs = os.listdir("music/")
        output = " \n"
        outp = (output.join(s[:-4] for s in songs))
        await ctx.send(outp)

    @commands.command(name="disconnect", aliases=['disc'])
    @commands.guild_only()
    async def disconnect(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.message.reply("🛑 **| Disconnected from voice.**")
            self.is_playing = False
            self.music_queue = []
            self.vc = ""
            self.voteskip = []
            self.nowplaying = ""
            self.nowplayingimg = ""
        else:
            await ctx.message.reply("⚠ **| Already disconnected from voice.**")

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel and after.channel == None and member.id == 463388759866474506:
            self.music_queue = []
            self.vc = ""
            self.voteskip = []
            self.nowplaying = ""
            self.nowplayingimg = ""

    @commands.command()
    @commands.guild_only()
    async def resume(self, ctx):
        global player
        try:
            player.resume()
            await ctx.send("<:play:844309432887803975> **| Resumed the music**")
        except:
            pass
        try:
            self.vc.resume()
            await ctx.send("<:play:844309432887803975> **| Resumed the music**")
        except:
            pass

    @commands.command()
    @commands.guild_only()
    async def pause(self, ctx):
        global player
        try:
            player.pause()
            await ctx.send("<:pause:844309432669306931> **| Paused the music**")
        except:
            pass
        try:
            self.vc.pause()
            await ctx.send("<:pause:844309432669306931> **| Paused the music**")
        except:
            pass

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def radio(self, ctx):
        embed = discord.Embed(
            title="Radio", description="Available radio channels:", color=0xFF9F26)
        embed.set_thumbnail(
            url="https://media.istockphoto.com/vectors/radio-flat-icon-vector-id905456552?b=1&k=6&m=905456552&s=612x612&w=0&h=AdeAoOa8OsCNS3AIQ_RWee5dS724XDrGhFtXF8QOSWM=")
        embed.add_field(name="MNM", value="-radio mnm", inline=False)
        embed.add_field(name="Q-Music", value="-radio qmusic", inline=False)
        embed.add_field(name="Studio Brussel",
                        value="-radio stubru", inline=False)
        embed.add_field(name="NRJ", value="-radio nrj", inline=False)
        embed.add_field(name="Top Radio",
                        value="-radio topradio", inline=False)
        embed.add_field(name="Radio 1",
                        value="-radio radio1", inline=False)
        embed.add_field(name="VRT Nieuws",
                        value="-radio nieuws", inline=False)
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @radio.command()
    @commands.guild_only()
    async def mnm(self, ctx):
        if self.is_playing:
            return
        url = 'http://icecast.vrtcdn.be/mnm-high.mp3'
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        global player
        if voice and voice.is_connected():
            player.stop()
        else:
            try:
                player = await channel.connect()
            except:
                await ctx.send("⚠ | Could not connect to your channel.")
        try:
            embed = discord.Embed(title="Radio", color=0x01afe5)
            embed.set_thumbnail(url="https://images.squarespace-cdn.com/content/v1/520141b3e4b067924ab14494/1580640807953-MGQWUKXBB905L3Y8HJVK/ke17ZwdGBToddI8pDm48kHqYAt3UgyjNg-0dlUc4K5hZw-zPPgdn4jUwVcJE1ZvWhcwhEtWJXoshNdA9f1qD7UnCxNA8dHvmd7460Z7fbKEmJ2gL2qv94i4UWS2y7YfwkXCxk_sn2atIO3dASbw33Q/mnm-logo.png?format=300w")
            embed.add_field(
                name="MNM", value="Now connected!", inline=False)
            await ctx.send(embed=embed)
            self.nowplaying = "MNM"
        except:
            await ctx.send("⚠ | An unknown error occured.")
        player.play(FFmpegPCMAudio(url))

    @radio.command()
    @commands.guild_only()
    async def stubru(self, ctx):
        url = 'http://icecast.vrtcdn.be/stubru-high.mp3'
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        global player
        if voice and voice.is_connected():
            player.stop()
        else:
            try:
                player = await channel.connect()
            except:
                await ctx.send("⚠ | Could not connect to your channel.")
        try:
            embed = discord.Embed(title="Radio", color=0xE3E879)
            embed.set_thumbnail(
                url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/VRT_StuBru_logo.svg/200px-VRT_StuBru_logo.svg.png")
            embed.add_field(name="Studio Brussel",
                            value="Now connected!", inline=False)
            await ctx.send(embed=embed)
            self.nowplaying = "Studio Brussel"
        except:
            await ctx.send("⚠ | An unknown error occured.")
        player.play(FFmpegPCMAudio(url))

    @radio.command()
    @commands.guild_only()
    async def qmusic(self, ctx):
        url = 'http://22663.live.streamtheworld.com/QMUSIC.mp3'
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        global player
        if voice and voice.is_connected():
            player.stop()
        else:
            try:
                player = await channel.connect()
            except:
                await ctx.send("⚠ | Could not connect to your channel.")
        try:
            embed = discord.Embed(title="Radio", color=0xE6E6E6)
            embed.set_thumbnail(
                url="https://imgix.mychannels.video/imgix/c516b493-f3cd-4a41-8711-d9e326947cdc/Qlogo_redwhite_on_carbongrey.png?")
            embed.add_field(
                name="Q-Music", value="Now connected!", inline=False)
            await ctx.send(embed=embed)
            self.nowplaying = "Q-Music"
        except:
            await ctx.send("⚠ | An unknown error occured.")
        player.play(FFmpegPCMAudio(url))

    @radio.command()
    @commands.guild_only()
    async def nrj(self, ctx):
        url = 'https://22723.live.streamtheworld.com/NRJBELGIE.mp3'
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        global player
        if voice and voice.is_connected():
            player.stop()
        else:
            try:
                player = await channel.connect()
            except:
                await ctx.send("⚠ | Could not connect to your channel.")
        try:
            embed = discord.Embed(title="Radio", color=0xe20f22)
            embed.set_thumbnail(
                url="https://img.nrj.fr/AJypbDUw_qkZ8lw7Y4T1ELMKqRM=/https://www.nrj.fr/uploads/assets/nrj/logo-nrj.png")
            embed.add_field(
                name="NRJ", value="Now connected!", inline=False)
            await ctx.send(embed=embed)
            self.nowplaying = "NRJ"
        except:
            await ctx.send("⚠ | An unknown error occured.")
        player.play(FFmpegPCMAudio(url))

    @radio.command()
    @commands.guild_only()
    async def topradio(self, ctx):
        global player
        url = 'https://str.topradio.be/topradio.mp3'
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            player.stop()
        else:
            try:
                player = await channel.connect()
            except:
                await ctx.send("⚠ | Could not connect to your channel.")
        try:
            embed = discord.Embed(title="Radio", color=0x85CDDC)
            embed.set_thumbnail(
                url="https://www.topradio.be/assets/page/img/TOpradio.jpg")
            embed.add_field(name="Top Radio",
                            value="Now connected!", inline=False)
            await ctx.send(embed=embed)
            self.nowplaying = "Top Radio"
        except:
            await ctx.send("⚠ | An unknown error occured.")
        player.play(FFmpegPCMAudio(url))

    @radio.command()
    @commands.guild_only()
    async def parkies(self, ctx):
        url = 'https://manager2.creativradio.com:1965/stream'
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        global player
        if voice and voice.is_connected():
            player.stop()
        else:
            try:
                player = await channel.connect()
            except:
                await ctx.send("⚠ | Could not connect to your channel.")
        try:
            embed = discord.Embed(title="Radio", color=0x6EAF47)
            embed.set_thumbnail(
                url="https://www.radioparkies.com/uploads/1/5/0/6/15065266/43578267842-4f80ccf73a-c_orig.jpg")
            embed.add_field(name="Radio Parkies",
                            value="Now connected!", inline=False)
            await ctx.send(embed=embed)
            self.nowplaying = "Radio Parkies"
        except:
            await ctx.send("⚠ | An unknown error occured.")
        player.play(FFmpegPCMAudio(url))

    @radio.command()
    @commands.guild_only()
    async def radio1(self, ctx):
        url = 'http://icecast-servers.vrtcdn.be/radio1-high.mp3'
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        global player
        if voice and voice.is_connected():
            player.stop()
        else:
            try:
                player = await channel.connect()
            except:
                await ctx.send("⚠ | Could not connect to your channel.")
        try:
            embed = discord.Embed(title="Radio", color=0x0072BB)
            embed.set_thumbnail(
                url="https://i.imgur.com/FIFDNY4.png")
            embed.add_field(name="Radio 1",
                            value="Now connected!", inline=False)
            await ctx.send(embed=embed)
            self.nowplaying = "Radio 1"
        except:
            await ctx.send("⚠ | An unknown error occured.")
        player.play(FFmpegPCMAudio(url))

    @radio.command()
    @commands.guild_only()
    async def nieuws(self, ctx):
        url = 'http://progressive-audio.lwc.vrtcdn.be/content/fixed/11_11niws-snip_hi.mp3'
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        global player
        if voice and voice.is_connected():
            player.stop()
        else:
            try:
                player = await channel.connect()
            except:
                await ctx.send("⚠ | Could not connect to your channel.")
        try:
            embed = discord.Embed(title="Radio", color=0x5EFA70)
            embed.set_thumbnail(
                url="https://yt3.ggpht.com/ytc/AAUvwniLzc8lcIbuEK4QYzX279fmc1FCCRDi9LO5QOe9YQ=s900-c-k-c0x00ffffff-no-rj")
            embed.add_field(name="VRT Nieuws",
                            value="Now connected!", inline=False)
            await ctx.send(embed=embed)
            self.nowplaying = "VRT Nieuws"
        except:
            await ctx.send("⚠ | An unknown error occured.")
        player.play(FFmpegPCMAudio(url))


def setup(client):
    client.add_cog(Radio(client))
    print('Radio loaded succesfully')
