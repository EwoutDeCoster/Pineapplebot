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
from datetime import datetime, timedelta, date
from decimal import Decimal
import sqlite3

webs = str("Pineapplebot.ga")


class Starboard(commands.Cog, name='Starboard'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == "⭐":
            db = sqlite3.connect('cogs/main.sqlite')
            cursor = db.cursor()
            cursor.execute(
            f"SELECT guild, stars, channel FROM starboard WHERE guild = {payload.guild_id}")
            result = cursor.fetchone()

            chnl = self.client.get_channel(802982004990672948)
            msg = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
            i = 0
            stars = 0
            while i < len(msg.reactions):
                if msg.reactions[i].emoji == "⭐":
                    stars = msg.reactions[i].count
                i += 1
            if stars >= int(result[1]):
                await chnl.send(f"{msg.content}")

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_remove(self, payload):
        if payload.emoji.name == "⭐":
            msg = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
            i = 0
            stars = 0
            while i < len(msg.reactions):
                if msg.reactions[i].emoji == "⭐":
                    stars = msg.reactions[i].count
                i += 1
            print(stars)



def setup(client):
    client.add_cog(Starboard(client))
    print('Starboard loaded succesfully')
