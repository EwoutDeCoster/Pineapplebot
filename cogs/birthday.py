import discord
from discord.ext import commands
import datetime
import asyncio

vers = str("v2.0")
webs = str("Pineapplebot.ga")


class Birthday(commands.Cog, name='Birthday'):

    def __init__(self, client):
        self.client = client


async def check_for_birthday(self):
    await self.wait_until_ready()
    now = datetime.datetime.now()
    curmonth = now.month
    curday = now.day

    while not self.is_closed():
        with open('birthdays.json', 'r') as f:
            var = jason.load(f)
            for member in var:
                if member['month'] == curmonth:
                    if member['day'] == curday:
                        try:
                            await self.client.get_user(member).send("Happy birthday!")
                        except:
                            pass
                        success = False
                        index = 0
                        while not success:
                            try:
                                await guild.channels[index].send(f"Happy birthday to <@{member}>!")
                            except discord.Forbidden:
                                index += 1
                            except AttributeError:
                                index += 1
                            except IndexError:
                                # if the server has no channels, doesn't let the bot talk, or all vc/categories
                                pass
                            else:
                                success = True
        await asyncio.sleep(86400)  # task runs every day


@commands.command()
@commands.guild_only()
async def setbirthday(self, ctx):
    '''Set a birthday.'''
    member = ctx.message.author.id
    await ctx.send("What is your birthday? (MM/DD)")

    def check(user):
        return user == ctx.message.author and user == ctx.message.channel
    msg = await self.client.wait_for('message', check=check)
    try:
        list = msg.split("/")
        if list[0] > 13 or list[0] < 1:
            await ctx.send("Invalid date.")
            await ctx.send("Aborting...")
            return
        else:
            pass

        if list[0] in (1, 3, 5, 7, 8, 10, 12):
            if list[1] > 31 or list[1] < 1:
                await ctx.send("Invalid date.")
                await ctx.send("Aborting...")
                return
            else:
                pass
        elif list[0] in (4, 6, 9, 11):
            if list[1] > 30 or list[1] < 1:
                await ctx.send("Invalid date.")
                await ctx.send("Aborting...")
                return
            else:
                pass
        elif list[0] == 2:
            if list[1] > 29 or list[1] < 1:
                await ctx.send("Invalid date.")
                await ctx.send("Aborting...")
                return
            else:
                pass
        else:
            await ctx.send("Invalid date.")
            await ctx.send("Aborting...")
            return
    except:
        await ctx.send("Invalid date.")
        await ctx.send("Aborting...")
        return

    list = msg.split("/")
    month = list[0]
    day = list[1]

    with open('./birthdays.json', 'r+') as f:
        var = jason.load(f)
        var[member] = {'month': month, 'day': day}
        jason.dump(var, f, indent=4)


def setup(client):
    client.add_cog(Birthday(client))
    print('Birthday loaded succesfully')
