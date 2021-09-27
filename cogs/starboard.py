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

webs = str("Pineapplebot.ga")


class Starboard(commands.Cog, name='Starboard'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_add(self, payload):
        message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if payload.emoji.name == "⭐":
            print("jep")

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_raw_reaction_remove(self, payload):
        message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if payload.emoji.name == "⭐":
            print("loes")
            print(message)



def setup(client):
    client.add_cog(Starboard(client))
    print('Starboard loaded succesfully')
