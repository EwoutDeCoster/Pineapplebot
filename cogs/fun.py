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
import praw

webs = str("Pineapplebot.ga")

reddit = praw.Reddit(client_id='v_NySebP-KOhMg',
                     client_secret='-BMX1V_cu3HKLoWaUdqTHr-VtJCIFQ',
                     user_agent='Pineapple',
                     check_for_async=False)


class Fun(commands.Cog, name='Fun'):

    def __init__(self, client):
        self.client = client
        self.discord = discord

    @commands.command(name='big')
    @commands.guild_only()
    async def big(self, ctx):
        await ctx.send("https://tenor.com/view/dick-penis-dildo-forest-running-gif-16272085")
        message = await ctx.send('SLONG!')
        await message.add_reaction("🍆")
        print(f'{ctx.author} used Big cmd')

    @commands.command(name='hanz')
    @commands.guild_only()
    async def hanz(self, ctx):
        msg = await ctx.send(
            'https://tenor.com/view/hanz-get-ze-flammenwerfer-flammenwerfer-excited-hans-flamethrower-gif-18658452')
        message = ctx.message
        await msg.add_reaction("🔥")
        await msg.add_reaction("💥")
        await msg.add_reaction("✨")
        print(f'{ctx.author} used Hanz cmd')

    @commands.command(name='pesten')
    @commands.guild_only()
    async def pesten(self, ctx, arg1):
        try:
            message = ctx.message
            await message.delete()
            await ctx.send('This might help you {} <:FeelsBadMan:785490392375754842>'.format(arg1))
            embed = discord.Embed(title="Move tegen pesten", url="https://www.youtube.com/watch?v=phO3GxlcmEk",
                                  description="Brahim en Charlotte Leysen", color=0xc73333)
            embed.set_author(
                name="Pineapple", icon_url=f"{ctx.author.avatar_url}")
            embed.set_thumbnail(
                url="https://i.ytimg.com/vi/phO3GxlcmEk/maxresdefault.jpg")
            embed.set_footer(text=f"{webs}")
            await ctx.send(embed=embed)
            print(f'{ctx.author} used pesten for {arg1}')
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(
                name="Usage:", value="`-pesten [person]`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(name='hit')
    @commands.guild_only()
    async def hit(self, ctx, person: discord.Member):
        try:
            message = ctx.message
            sender = ctx.author
            gifs = ["https://media.giphy.com/media/srD8JByP9u3zW/giphy.gif",
                    "https://media.giphy.com/media/UbzayP2FNPWbm/giphy.gif",
                    "https://media.giphy.com/media/vxvNnIYFcYqEE/giphy.gif",
                    "https://media.giphy.com/media/Hz3YLyGYc15Oo/giphy.gif",
                    "https://media.giphy.com/media/s5zXKfeXaa6ZO/giphy.gif",
                    "https://media.giphy.com/media/gSIz6gGLhguOY/giphy.gif",
                    "https://media.giphy.com/media/3XlEk2RxPS1m8/giphy.gif", "https://media1.tenor.com/images/cf8ff538999c1125532e98758e8835d9/tenor.gif?itemid=7249411",
                    "https://media1.tenor.com/images/70f6224ee654bb54bfb15a14c26a85c8/tenor.gif", "https://media1.tenor.com/images/3c161bd7d6c6fba17bb3e5c5ecc8493e/tenor.gif?itemid=5196956", "https://media1.tenor.com/images/6e609268c0405a53799224602fc0373d/tenor.gif?itemid=4938822",
                    "https://media1.tenor.com/images/49796f431821592cafbdd97092347a00/tenor.gif?itemid=3468779", "https://media.tenor.com/images/1594e57cb72611729621930ef83b14db/tenor.gif", "https://media1.tenor.com/images/1e9048e96d0b57b5a23bb068e6c104bb/tenor.gif?itemid=13097976"]
            await message.delete()
            embed = discord.Embed(
                description='{} **got hit by** {}'.format(person.mention, sender.mention), color=0xc73333)
            embed.set_image(url=f'{random.choice(gifs)}')
            await ctx.send(embed=embed)
            print(f'{ctx.author} hit {person}')
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(
                name="Usage:", value="`-hit [person]`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(name='shovel')
    @commands.guild_only()
    async def shovel(self, ctx, person: discord.Member):
        try:
            shovels = ["https://media.giphy.com/media/43bOrDOasXG6Y/giphy.gif",
                       "https://media.giphy.com/media/tBmxLR7JkYZoY/giphy.gif",
                       "https://media.giphy.com/media/lh4SrOe05v8Fq/giphy.gif"]
            message = ctx.message
            sender = ctx.author
            await message.delete()
            embed = discord.Embed(
                description='{} **got shoveled by** {}'.format(person.mention, sender.mention), color=0xc73333)
            embed.set_image(url=f'{random.choice(shovels)}')
            await ctx.send(embed=embed)
            print(f'{ctx.author} shoveled {person}')
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(
                name="Usage:", value="`-shovel [person]`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(name='8ball')
    @commands.guild_only()
    async def _8ball(self, ctx, *, question):
        responses = ["maybe", "nope", 'jep', 'nah',
                     'big chance', 'hell no', 'no doubt']
        await ctx.send(f'🎱 | **{random.choice(responses)}**')
        print(f'{ctx.author} used 8ball: {question}')

    @commands.command(name='rus')
    @commands.guild_only()
    async def rus(self, ctx):
        responses = ['Click', 'Click', 'Click', 'Click', 'Click', 'BANG! 💥']
        clickresponses = ["Lucky!", "You're lucky!",
                          "Still alive", "Easy, still alive"]
        dieresponses = ["You died!", "Rest in peace my friend",
                        "You're dead!", "You lose!", "Auwch...", "This is so sad...", "Insert sad noises"]
        clicks = random.choice(clickresponses)
        response = random.choice(responses)
        die = random.choice(dieresponses)
        if response == 'BANG! 💥':
            embed = discord.Embed(title="🔫 Russian Roulette", color=0xff9500)
            embed.set_thumbnail(
                url="https://emojis.slackmojis.com/emojis/images/1558097714/5705/rip.png?1558097714")
            embed.add_field(name="Bang 💥", value=f"{die}", inline=False)
            embed.set_footer(text=f"{webs}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="🔫 Russian Roulette", color=0xff9500)
            embed.set_thumbnail(
                url="https://cdn.emojidex.com/emoji/seal/relieved.png?1417136196")
            embed.add_field(name="Click", value=f"{clicks}", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(name='ruslonely')
    @commands.guild_only()
    async def ruslonely(self, ctx):
        responses = ["Click", "Click", 'Click', 'Click', 'Click', 'BANG! 💥']
        random.shuffle(responses)
        for noice in responses:
            if noice == "BANG! 💥":
                embed = discord.Embed(title="🔫 Russian Roulette",
                                      description=f'{noice}', color=0xff9500)
                embed.set_footer(
                    text=f"{webs} | It took you {1 + responses.index(noice)} tries")
                await ctx.send(embed=embed)
                return
            else:
                embed = discord.Embed(title="🔫 Russian Roulette",
                                      description=f'{noice}', color=0xff9500)
                embed.set_footer(text=f"{webs} | {ctx.author}")
                await ctx.send(embed=embed)
            await asyncio.sleep(1)

        print(f'{ctx.author} used rus command')

    @commands.command(name='burn')
    @commands.guild_only()
    async def burn(self, ctx, person: discord.Member):
        message = ctx.message
        await message.delete()
        embed = discord.Embed(
            description='{} **just got burned by {}!**'.format(person.mention, ctx.author.mention), color=0xc73333)
        embed.set_image(
            url='https://media1.tenor.com/images/2a8ff555dc5195ff495e4501f6055fb7/tenor.gif?itemid=14920648')
        await ctx.send(embed=embed)
        print(f'{ctx.author} burned {person}')

    @commands.command(name='circle')
    @commands.guild_only()
    async def circle(self, ctx):
        kaarten = ["One is for all", "Two is for you", "Three is for me", "Four for the hoes", "Russian Roulette",
                   "Six for the dicks", "Seven point to heaven",
                   "Eight make a date", "Nine make a rhyme", "Ten is category.", "Jack: Never have i ever",
                   "Question queen", "King: Make a rule", ]

        embed = discord.Embed(title="Circle of Death",
                              description="drinking game", color=0xff9500)
        embed.set_thumbnail(
            url="https://icons.veryicon.com/png/o/food--drinks/food-icon/beer-27.png")
        embed.add_field(
            name="Order:", value=f"{random.choice(kaarten)}", inline=True)
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)
        print(f'{ctx.author} used circle of death')

    @commands.command(name="wyr")
    @commands.guild_only()
    async def wyr(self, ctx):
        wyrlist = ["Would you rather go into the past and meet your ancestors or go into the future and meet your great-great grandchildren?",
                   "Would you rather have more time or more money?",
                   "Would you rather have a rewind button or a pause button on your life?",
                   "Would you rather be able to talk with the animals or speak all foreign languages?",
                   "Would you rather win the lottery or live twice as long?",
                   "Would you feel worse if no one showed up to your wedding or to your funeral?",
                   "Would you rather be without internet for a week, or without your phone?",
                   "Would you rather meet George Washington, or the current President?",
                   "Would you rather lose your vision or your hearing?",
                   "Would you rather work more hours per day, but fewer days or work fewer hours per day, but more days?",
                   "Would you rather listen to music from the 70’s or music from today?",
                   "Would you rather become someone else or just stay you?",
                   "Would you rather be Batman or Spiderman?",
                   "Would you rather be stuck on a broken ski lift or in a broken elevator?",
                   "For your birthday, would you rather receive cash or gifts?",
                   "Would you rather go to a movie or to dinner alone?",
                   "Would you rather always say everything on your mind or never speak again?",
                   "Would you rather make a phone call or send a text?",
                   "Would you rather read an awesome book or watch a good movie?",
                   "Would you rather be the most popular person at work or school or the smartest?",
                   "Would you rather put a stop to war or end world hunger?",
                   "Would you rather spend the night in a luxury hotel room or camping surrounded by beautiful scenery?",
                   "Would you rather explore space or the ocean?",
                   "Would you rather go deep sea diving or bungee jumping?",
                   "Would you rather be a kid your whole life or an adult your whole life?",
                   "Would you rather go on a cruise with friends or with your spouse?",
                   "Would you rather lose your keys or your cell phone?",
                   "Would you rather eat a meal of cow tongue or octopus?",
                   "Would you rather have x-ray vision or magnified hearing?",
                   "Would you rather work in a group or work alone?",
                   "Would you rather be stuck on an island alone or with someone who talks incessantly?",
                   "Would you rather be too hot or too cold?",
                   "When you’re old, would you rather die before or after your spouse?",
                   "Would you rather have a cook or a maid?",
                   "Would you rather be the youngest or the oldest sibling?",
                   "Would you rather get rich through hard work or through winning the lottery?",
                   "Would you rather have a 10-hour dinner with a headstrong politician from an opposing party, or attend a 10-hour concert for a music group you detest?",
                   "Would you rather be an Olympic gold medalist or a Nobel Peace Prize winner?",
                   "Would you rather have a desk job or an outdoor job?",
                   "Would you rather live at the top of a tall NYC apartment building or at the top of a mountain?",
                   "Would you rather have Rambo or The Terminator on your side?",
                   "Would you rather be proposed to in private or in front of family and friends?",
                   "Would you rather have to sew all your clothes or grow your own food?",
                   "Would you rather hear the good news or the bad news first?",
                   "Would you rather be your own boss or work for someone else?",
                   "Would you rather have nosy neighbors or noisy neighbors?",
                   "Would you rather be on a survival reality show or dating game show?",
                   "Would you rather be too busy or be bored?",
                   "Would you rather watch the big game at home or live at the stadium.", ]
        wouldyourather = random.choice(wyrlist)
        embed = discord.Embed(title="Would you rather",
                              description=f"{wouldyourather}", color=0x0a4d8b)
        embed.set_thumbnail(
            url="https://image.freepik.com/free-vector/two-possible-choices-design_1133-16.jpg")
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(name="coin")
    @commands.guild_only()
    async def coin(self, ctx):
        flip = random.choice(["Heads", "Tails"])
        if flip == "Tails":
            embed = discord.Embed(title="🪙 Flip a coin",
                                  description="Tails", color=0x0a4d8b)
            embed.set_thumbnail(
                url="https://www.nicepng.com/png/full/84-848244_1-euro-euro-coin-png.png")
            embed.set_footer(text=f"{webs}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="🪙 Flip a coin",
                                  description="Heads", color=0x0a4d8b)
            embed.set_thumbnail(
                url="https://touchcoins.moneymuseum.com/coins_media/Republic-of-Austria-1-Euro-2002/1367/obverse.png")
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(name="starwars")
    @commands.guild_only()
    async def starwars(self, ctx):
        try:
            starwarsquotes = ["Many Bothans died to bring us this information. \n-Mon Mothma",
                              "Charming to the last. You don't know how hard I found it, signing the order to terminate your life. \n-Governor Tarkin",
                              "It's a trap! \n-Admiral Ackbar",
                              "So this is how liberty dies…with thunderous applause. \n-Padmé Amidala",
                              "He's no good to me dead. \n-Boba Fett",
                              "I've got a bad feeling about this. \n-Various characters in Star Wars",
                              "May the force be with you. \n-Various characters in Star Wars",
                              "Young fool... Only now, at the end, do you understand... \n-The Emperor",
                              "Your feeble skills are no match for the power of the Dark Side. \n-The Emperor",
                              "Now, you will pay the price for your lack of vision! \n-The Emperor",
                              "I will make it legal. \n-Darth Sidious",
                              "I suggest a new strategy, R2: let the Wookiee win. \n-C-3PO",
                              "We seem to be made to suffer. It's our lot in life. \n-C-3PO",
                              "Sir, the possibility of successfully navigating an asteroid field is approximately 3,720 to 1. \n-C-3PO",
                              "Sir, it's quite possible this asteroid is not entirely stable. \n-C-3PO",
                              "Don’t call me a mindless philosopher, you overweight glob of grease! \n-C-3PO",
                              "Help me, Obi-Wan Kenobi. You're my only hope. \n-Princess Leia Organa",
                              "Aren't you a little short for a stormtrooper? \n-Princess Leia Organa",
                              "Someone has to save our skins. Into the garbage chute, fly boy. \n-Princess Leia Organa",
                              "Will someone get this big walking carpet out of my way? \n-Leia Organa",
                              "You needn't worry about your reward. If money is all that you love, then that's what you'll receive. \n-Leia Organa",
                              "Chewie...we're home. \n-Han Solo",
                              "Never tell me the odds. \n-Han Solo",
                              "Women always figure out the truth. Always. \n-Han Solo",
                              "Fast ship? You've never heard of the Millennium Falcon? It's the ship that made the Kessel Run in less than twelve parsecs. \n-Han Solo",
                              "Great shot, kid, that was one in a million! \n-Han Solo",
                              "Boring conversation anyway. LUKE, WE'RE GONNA HAVE COMPANY! \n-Han Solo",
                              "No reward is worth this. \n-Han Solo",
                              "Wonderful girl. Either I'm going to kill her or I'm beginning to like her. \n-Han Solo",
                              "Look, Your Worshipfulness, let's get one thing straight. I take orders from just one person: me. \n-Han Solo",
                              "I'll never turn to the Dark Side. You've failed, your highness. I am a Jedi, like my father before me. \n-Luke Skywalker",
                              "If there's a bright center to the universe, you're on the planet that it's farthest from. \n-Luke Skywalker",
                              "I'm Luke Skywalker. I'm here to rescue you. \n-Luke Skywalker",
                              "The Force is strong in my family. My father has it. I have it. My sister has it. You have that power, too. \n-Luke Skywalker",
                              "But I was going into Tosche Station to pick up some power converters! \n-Luke Skywalker",
                              "Do. Or do not. There is no try. \n-Yoda",
                              "You must unlearn what you have learned. \n-Yoda",
                              "When nine hundred years old you reach, look as good you will not. \n-Yoda",
                              "Truly wonderful, the mind of a child is. \n-Yoda",
                              "A Jedi uses the Force for knowledge and defense, never for attack. \n-Yoda",
                              "Adventure. Excitement. A Jedi craves not these things. \n-Yoda",
                              "Size matters not. Judge me by my size, do you? \n-Yoda",
                              "Fear is the path to the dark side…fear leads to anger…anger leads to hate…hate leads to suffering. \n-Yoda",
                              "Wars not make one great. \n-Yoda",
                              "Luminous beings are we…not this crude matter. \n-Yoda",
                              "Difficult to see. Always in motion is the future. \n-Yoda",
                              "Control, control, you must learn control! \n-Yoda",
                              "I find your lack of faith disturbing. \n-Darth Vader",
                              "The circle is now complete. When I left you, I was but the learner. Now I am the master. \n-Darth Vader",
                              "The Force is with you, young Skywalker, but you are not a Jedi yet. \n-Darth Vader",
                              "No. I am your father. \n-Darth Vader",
                              "Impressive. Most impressive. \n-Darth Vader",
                              "I am altering the deal. Pray I don't alter it any further. \n-Darth Vader",
                              "You underestimate the power of the Dark Side. If you will not fight, then you will meet your destiny. \n-Darth Vader",
                              "You have failed me for the last time, Admiral! \n-Darth Vader",
                              "The Force is strong with this one. \n-Darth Vader",
                              "The ability to destroy a planet is insignificant next to the power of the Force. \n-Darth Vader",
                              "You must do what you feel is right, of course. \n-Obi-Wan Kenobi",
                              "Mos Eisley Spaceport. You will never find a more wretched hive of scum and villainy. We must be cautious. \n-Obi-Wan Kenobi",
                              "Your eyes can deceive you. Don’t trust them. \n-Obi-Wan Kenobi",
                              "Remember... the Force will be with you, always. \n-Obi-Wan Kenobi",
                              "In my experience, there is no such thing as luck. \n-Obi-Wan Kenobi",
                              "These aren't the droids you're looking for. \n-Obi-Wan Kenobi",
                              "I felt a great disturbance in the Force, as if millions of voices suddenly cried out in terror and were suddenly silenced. \n-Obi-Wan Kenobi",
                              "Use the Force, Luke.\n-Obi-Wan Kenobi",
                              "You can't win, Darth. If you strike me down, I shall become more powerful than you could possibly imagine. \n-Obi-Wan Kenobi",
                              "That's no moon. It's a space station. \n-Obi-Wan Kenobi",
                              "Luke! Don't give in to hate. That leads to the Dark Side. \n-Obi-Wan Kenobi",
                              "Who's the more foolish, the fool or the fool who follows him? \n-Obi-Wan Kenobi",
                              "And these blast points, too accurate for Sandpeople. Only Imperial Stormtroopers are so precise. \n-Obi-Wan Kenobi",
                              ]
            quote = random.choice(starwarsquotes)
            embed = discord.Embed(
                title="⭐ Star Wars", description=f"{quote}", color=0xffc800)
            embed.set_thumbnail(
                url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Star_Wars_Logo.svg/694px-Star_Wars_Logo.svg.png")
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(name="Usage:", value="`-starwars`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(name='doggo')
    @commands.guild_only()
    async def doggo(self, ctx):
        r = requests.get('https://dog.ceo/api/breeds/image/random')
        d = r.json()
        short = d["message"]
        embed = discord.Embed(
            title="🐕 Doggo", color=0x006ec2)
        embed.set_image(
            url=f"{short}")
        embed.set_footer(text=f"{webs} | {ctx.author}")
        await ctx.send(embed=embed)
        print(f'{ctx.author} used doggo cmd')

    @commands.command(name='seal')
    @commands.guild_only()
    async def seal(self, ctx, top, bottom):
        await ctx.send(ctx.author.mention)
        await ctx.send(f'http://apimeme.com/meme?meme=Awkward-Moment-Sealion&top={top}&bottom={bottom}')
        msg = ctx.message
        await msg.delete()
        print(f'{ctx.author} used seal meme cmd. Top: {top} | Bottom: {bottom}')

    @commands.command(name='sanders')
    @commands.guild_only()
    async def sanders(self, ctx, top, bottom):
        await ctx.send(ctx.author.mention)
        await ctx.send(
            f'http://apimeme.com/meme?meme=Bernie-I-Am-Once-Again-Asking-For-Your-Support&top={top}&bottom={bottom}')
        msg = ctx.message
        await msg.delete()
        print(f'{ctx.author} used Sanders meme cmd. Top: {top} | Bottom: {bottom}')

    @commands.command(name='sponge')
    @commands.guild_only()
    async def sponge(self, ctx, top, bottom):
        await ctx.send(ctx.author.mention)
        await ctx.send(f'http://apimeme.com/meme?meme=Chicken-Bob&top={top}&bottom={bottom}')
        msg = ctx.message
        await msg.delete()
        print(f'{ctx.author} used sponge meme cmd. Top: {top} | Bottom: {bottom}')

    @commands.command(name='disaster')
    @commands.guild_only()
    async def disaster(self, ctx, top, bottom):
        await ctx.send(ctx.author.mention)
        await ctx.send(f'http://apimeme.com/meme?meme=Disaster-Girl&top={top}&bottom={bottom}')
        msg = ctx.message
        await msg.delete()
        print(f'{ctx.author} used disaster meme cmd. Top: {top} | Bottom: {bottom}')

    @commands.command(name='drunkbaby')
    @commands.guild_only()
    async def drunkbaby(self, ctx, top, bottom):
        await ctx.send(ctx.author.mention)
        await ctx.send(f'http://apimeme.com/meme?meme=Drunk-Baby&top={top}&bottom={bottom}')
        msg = ctx.message
        await msg.delete()
        print(f'{ctx.author} used drunk baby meme cmd. Top: {top} | Bottom: {bottom}')

    @commands.command(name='randomfact')
    @commands.guild_only()
    async def randomfact(self, ctx):
        r = requests.get('https://useless-facts.sameerkumar.website/api')
        d = r.json()
        short = d["data"]
        await ctx.send("🔎 | {}".format(short))
        print(f'{ctx.author} used randomfact cmd')

    @commands.command(name="yoda")
    @commands.guild_only()
    async def yoda(self, ctx, *, text):
        try:
            msg = text
            r = requests.get(
                f"https://api.funtranslations.com/translate/yoda.json?text={msg}")
            d = r.json()
            output = d["contents"]["translated"]
            embed = discord.Embed(
                title="Yoda:", description=f"{output}", color=0x0ecc00)
            embed.set_thumbnail(
                url="https://static0.cbrimages.com/wordpress/wp-content/uploads/2020/05/yoda-revenge-of-the-sith.jpg?q=50&fit=crop&w=960&h=500")
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(
                name="Usage:", value="`-yoda [message]`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)
            await ctx.message.delete()

    @commands.command(name="roastme")
    async def roastme(self, ctx):
        try:
            r = requests.get(
                f"https://evilinsult.com/generate_insult.php?lang=en&type=json")
            d = r.json()
            output = d["insult"]
            embed = discord.Embed(
                title="Roast me:", description=f"{output}", color=0xffee00)
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title="⚠ Command error", color=0xff4000)
            embed.add_field(name="Usage:", value="`-roastme`", inline=False)
            embed.set_footer(text=f"{webs} | {ctx.author}")
            await ctx.send(embed=embed)

    @commands.command(name='lovecalc')
    @commands.guild_only()
    async def lovecalc(self, ctx, pers1, pers2):
        url = "https://love-calculator.p.rapidapi.com/getPercentage"
        key = "56d547268amshd523bc34916b2eep15def3jsnfcd6610c4e3a"

        querystring = {"fname": "{}".format(
            pers1), "sname": "{}".format(pers2)}

        headers = {
            'x-rapidapi-key': f"{key}",
            'x-rapidapi-host': "love-calculator.p.rapidapi.com"
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        d = response.json()
        p1 = d["fname"]
        p2 = d["sname"]
        desc = d["result"]
        perc = d["percentage"]

        embed = discord.Embed(title=f"{p1} x {p2}", color=0xff4747)
        embed.set_author(name="Love Calculator")
        embed.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Heart_coraz%C3%B3n.svg/1200px-Heart_coraz%C3%B3n.svg.png")
        embed.add_field(name=f"{perc}%", value=f"{desc}", inline=True)
        embed.set_footer(text=f"{webs}")
        await ctx.send(embed=embed)
        print(f"{ctx.author} used lovecalc with {pers1} and {pers2} ({perc})")

    @commands.command(name="meme")
    @commands.guild_only()
    async def _meme(self, ctx, *, subreddit="memes"):
        top_submissions = []
        color = discord.Colour.random()
        loading = discord.Embed(color=color,
                                description=f"<a:loading:841639840785498173> Loading meme ")
        loadmes = await ctx.send(embed=loading)
        try:
            for submission in (reddit.subreddit(subreddit)).top(limit=100):
                top_submissions.append(submission)
        except:
            embed = discord.Embed(color=discord.Colour.red(),
                                  description="Invalid Subreddit!!")
            embed.set_author(name="Error",
                             icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
            return await ctx.send(embed=embed)
        choice = top_submissions[random.randint(1, 100)]
        embed = None
        tries = 0
        while embed is None and tries < 5:
            if not choice.is_self and choice.url.endswith(".jpg"):
                embed = discord.Embed(color=color,
                                      description=f"**Posted by:** u/{choice.author}\n**Posted at:** {datetime.datetime.utcfromtimestamp(int(choice.created_utc)).strftime(('%d/%m/%Y at %H:%M'))}")
                embed.set_author(name=f"{choice.title}",
                                 url=choice.url)
                embed.set_image(url=choice.url)
                embed.set_footer(
                    text=f"Upvote Percentage: {int(choice.upvote_ratio*100)}% ({choice.score} upvotes in total)")
                return await loadmes.edit(embed=embed)
            else:
                choice = random.choice(top_submissions)
                tries += 1
                continue
        embed = discord.Embed(color=discord.Colour.red(),
                              description="Could not find meme.")
        embed.set_author(name="Error",
                         icon_url="https://cdn.discordapp.com/emojis/802083299559473222.png")
        return await ctx.send(embed=embed)

    @commands.command(name="drugs")
    @commands.guild_only()
    async def drugs(self, ctx):
        await ctx.send("**N O**")


def setup(client):
    client.add_cog(Fun(client))
    print('Fun loaded succesfully')
