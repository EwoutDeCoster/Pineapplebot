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


class Help(commands.Cog, name='Help'):

    def __init__(self, client):
        self.client = client

    @commands.command(name="help")
    @commands.guild_only()
    async def help(self, ctx):

        embed = discord.Embed(
            title="Help", description="Go to our website for more information about the Pineapple Bot", color=0x0a4d8b)
        embed.add_field(
            name="** **", value="Visit our website by clicking [here](https://www.pineapplebot.ga/).")
        embed.set_thumbnail(url="https://i.imgur.com/rjxnHHM.png")
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

        # await ctx.message.add_reaction('<:check_pine:834872371281264661>')
#
        # menu = discord.Embed(color=0x0a4d8b,
        #                     description="This is the Pineapple Bot help menu. Use the reactions to navigate.\nFor more information, visit https://www.pineapplebot.ga/")
        # menu.set_author(name="Information",
        #                icon_url=ctx.message.author.avatar_url)
#
        # menu.add_field(name="Contents",
        #               value="**1.** Essential Commands\n**2.** Info commands\n**3.** Fun Commands\n**4.** Moderation/setup",
        #               inline=False)
        # menu.add_field(name="Reactions",
        #               value="⏪ Go to the first page\n ◀️ Go backwards a page\n ⏹️ Delete the message\n ▶️ Go forward a page"
        #                     "\n ⏩ Go to the last page\n 🔢 Navigate to a page number\n ℹ️ Information",
        #               inline=False)
        #menu.set_footer(text="React with ▶️ to escape this page")
#
        # admin = discord.Embed(color=0x0a4d8b,
        #                      description="Commands to moderate your server and setup the bot!")
        # admin.set_author(name="Help For Moderation/setup Commands 4/4",
        #                 icon_url=ctx.message.author.avatar_url)
#
        # admin.add_field(name="-report [user] [reason]",
        #                value="Report a user.", inline=True)
        # admin.add_field(name="-modmail [msg]",
        #                value="Contact staff members.", inline=True)
        # admin.add_field(name="-ban [user] [reason]",
        #                value="Ban a user.", inline=True)
        # admin.add_field(name="-kick [user] [reason]",
        #                value="Kick a user.`", inline=True)
        # admin.add_field(name="-warn [user] [message]",
        #                value="Warn a user.", inline=True)
        # admin.add_field(name="-warnings [user]",
        #                value="Get all the warnings of a user.", inline=True)
        # admin.add_field(name="-clear [number]",
        #                value="Delete a number of messages in a channel.", inline=True)
        # admin.add_field(name="-moderation",
        #                value="Get a help menu for all the moderation setup commands.", inline=True)
        # admin.add_field(name="-membercount",
        #                value="Get a help menu for all the moderation setup commands.", inline=True)
        # admin.add_field(name="-welcome",
        #                value="Get a help menu for all the moderation setup commands.", inline=True)
        # admin.add_field(name="-suggestions",
        #                value="Get a help menu for all the suggestions setup commands.", inline=True)
        # admin.add_field(name="-approve [sID] [response]",
        #                value="Approve a suggestion (use command in the suggestions channel)", inline=True)
        # admin.add_field(name="-reject",
        #                value="Approve a suggestion (use command in the suggestions channel)", inline=True)
#
        # essentials = discord.Embed(color=0x0a4d8b,
        #                           description="Commands for the essential commands of the bot")
        # essentials.set_author(name="Help For Essential Commands 1/4",
        #                      icon_url=ctx.message.author.avatar_url)
#
        # essentials.add_field(name="-ping",
        #                     value="Ping the bot.",
        #                     inline=True)
        # essentials.add_field(name="-version",
        #                     value="Check the current version of the bot.",
        #                     inline=True)
        # essentials.add_field(name="-say [message]",
        #                     value="Let the bot say things (only available if you can mention everyone).",
        #                     inline=True)
        # essentials.add_field(name="-members",
        #                     value="Get the amount of members in the server.",
        #                     inline=True)
        # essentials.add_field(name="-announce",
        #                     value="Get a help menu for all the announce commands (only available if you can mention everyone).",
        #                     inline=True)
        # essentials.add_field(name="-timer [minutes]",
        #                     value="Set a timer.",
        #                     inline=True)
        # essentials.add_field(name="-poll [message]",
        #                     value="Make a yes or no poll.",
        #                     inline=True)
        # essentials.add_field(name="-createpoll \"[message]\" \"[option1]\", \"[option2]\", ...",
        #                     value="Make a poll.",
        #                     inline=True)
        # essentials.add_field(name="-poll [message]",
        #                     value="Make a yes or no poll.",
        #                     inline=True)
#
        # essentials.set_footer(
        #    text="Arguments are surrounded in [].")
#
        # fun = discord.Embed(color=0x0a4d8b,
        #                    description="Help for the fun commands of the bot")
        # fun.set_author(name="Help For Fun Commands 3/4",
        #                    icon_url=ctx.message.author.avatar_url)
#
        # fun.add_field(name="-big",
        #              value="Get a big surprise.",
        #              inline=True)
        # fun.add_field(name="-hanz",
        #              value="Get hanz in the building.",
        #              inline=True)
        # fun.add_field(name="-pesten",
        #              value="Bully someone.",
        #              inline=True)
        # fun.add_field(name="-hit [member]",
        #              value="Hit someone.",
        #              inline=True)
        # fun.add_field(name="-shovel [user]",
        #              value="Smash someone with a shovel.",
        #              inline=True)
        # fun.add_field(name="-burn [user]",
        #              value="Burn someone.",
        #              inline=True)
        # fun.add_field(name="-8ball [question]",
        #              value="Get an answer to the hardest questions.",
        #              inline=True)
        # fun.add_field(name="-rus",
        #              value="Play Russian Roulette with someone else.",
        #              inline=True)
        # fun.add_field(name="-ruslonely",
        #              value="Play Russian Roulette on your own. ",
        #              inline=True)
        # fun.add_field(name="-circle",
        #              value="Play the drinking game \"circle of death\".",
        #              inline=True)
        # fun.add_field(name="-wyr",
        #              value="Play Would you rather.",
        #              inline=True)
        # fun.add_field(name="-coin",
        #              value="Flip a coin.",
        #              inline=True)
        # fun.add_field(name="-starwars",
        #              value="Get a random Star Wars quote.",
        #              inline=True)
        # fun.add_field(name="-doggo",
        #              value="Get a pretty doggo picture.",
        #              inline=True)
        # fun.add_field(name="-randomfact",
        #              value="Get a random fact (sometimes in Deutsch).",
        #              inline=True)
        # fun.add_field(name="-yoda [message]",
        #              value="Say something like Yoda.",
        #              inline=True)
        # fun.add_field(name="-roastme",
        #              value="Roast yourself.",
        #              inline=True)
        # fun.add_field(name="-lovecalc [user 1] [user 2]",
        #              value="Calculate the love chance between two people.",
        #              inline=True)
        # fun.set_footer(
        #    text="Arguments are surrounded in [].")
#
        # info = discord.Embed(color=0x0a4d8b,
        #                     description="Information commands of the bot")
        # info.set_author(name="Help For info Commands 2/4",
        #                icon_url=ctx.message.author.avatar_url)
#
        # info.add_field(name="-rank (optional: [user])",
        #               value="Get your rank or the rank of someone else.",
        #               inline=True)
        # info.add_field(name="-leaderboard",
        #               value="Get the server leveling leaderboard.",
        #               inline=True)
        # info.add_field(name="-website",
        #               value="Get the url from the Pineapple Bot website.",
        #               inline=True)
        # info.add_field(name="-invite",
        #               value="Get an invite to the Pineapple Discord server.",
        #               inline=True)
        # info.add_field(name="-artist [name]",
        #               value="Search for an artist on Deezer.",
        #               inline=True)
        # info.add_field(name="-fruit [name]",
        #               value="Get information about a fruit.",
        #               inline=True)
        # info.add_field(name="-movie [name]",
        #               value="Get the rating and information about a movie ",
        #               inline=True)
        # info.add_field(name="-steam [name]",
        #               value="Get information about a user on steam.",
        #               inline=True)
        # info.add_field(name="-coc [id]",
        #               value="Get information about a Clash of Clans player by entering his in game id.",
        #               inline=True)
        # info.add_field(name="-guildinfo",
        #               value="Get information about the guild you're in.",
        #               inline=True)
        # info.add_field(name="-userinfo (optional: [user])",
        #               value="Get information about a user.",
        #               inline=True)
        # info.add_field(name="-shorturl [url] [title]",
        #               value="Get your url shortened with a custom title.",
        #               inline=True)
        # info.add_field(name="-iplookup [ip]",
        #               value="Get information about a certain IP address.",
        #               inline=True)
        # info.add_field(name="-qr [url]",
        #               value="Make a QR-code for a certain url.",
        #               inline=True)
        # info.add_field(name="-screenshot [url]",
        #               value="Get a screenshot from a webpage without having to open it yourself.",
        #               inline=True)
#
        # info.set_footer(
        #    text="Arguments are surrounded in [].")
#
        # embeds = {1: menu,
        #          2: essentials,
        #          3: info,
        #          4: fun,
        #          5: admin}
#
        # message = await ctx.send(embed=essentials)
        # await message.add_reaction("⏪")
        # await message.add_reaction("◀️")
        # await message.add_reaction("⏹️")
        # await message.add_reaction("▶️")
        # await message.add_reaction("⏩")
        # await message.add_reaction("🔢")
        # await message.add_reaction("ℹ️")
        #page = 1
#
        # while True:
        #    try:
        #        reaction, user = await self.client.wait_for("reaction_add", timeout=90.0)
        #        if user == ctx.author and str(reaction) in ["⏪", "◀️", "▶️", "⏩", "⏹️", "🔢", "ℹ️"]:
        #            if str(reaction.emoji) == "⏪" and page != 2:
        #                page = 2
        #                await message.edit(embed=embeds[page])
#
        #            elif str(reaction.emoji) == "◀️" and page != 2:
        #                page -= 1
        #                await message.edit(embed=embeds[page])
#
        #            elif str(reaction.emoji) == "▶️" and page != 5:
        #                page += 1
        #                await message.edit(embed=embeds[page])
#
        #            elif str(reaction.emoji) == "⏩" and page != 5:
        #                page = 5
        #                await message.edit(embed=embeds[page])
#
        #            elif str(reaction.emoji) == "⏹️":
        #                await message.delete()
        #                return
#
        #            elif str(reaction.emoji) == "🔢":
        #                number = None
        #                question = await ctx.send("**Which page do you want to see?**")
        #                try:
        #                    while number is None:
        #                        response = await self.client.wait_for("message", timeout=60.0)
        #                        if response.author == ctx.author and response.content in ["1", "2", "3", "4"]:
        #                            try:
        #                                number = int(response.content)+1
        #                            except ValueError:
        #                                number = None
        #                                continue
        #                        else:
        #                            continue
        #                except asyncio.TimeoutError:
        #                    return
        #                await question.delete()
        #                await response.delete()
        #                page = number
        #                await message.edit(embed=embeds[page])
#
        #            elif str(reaction.emoji) == "ℹ️":
        #                page = 1
        #                await message.edit(embed=embeds[page])
#
        #            await message.remove_reaction(str(reaction.emoji), ctx.author)
        #        else:
        #            continue
#
        #    except asyncio.TimeoutError:
        #        return await message.delete()


def setup(client):
    client.add_cog(Help(client))
    print('Help loaded succesfully')
