import discord
from discord.ext import commands
import random
import sys
import asyncio

description = '''An example bot to showcase the discord.ext.commands extension module.
There are a number of utility commands being showcased here.'''

bot = commands.Bot(command_prefix='?', description=description)

@bot.listen()
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.listen()
async def on_message(message):
    #we do not want the bot to reply to itself
    if message.author == bot.user:
        return

    if message.content.startswith('!Hello'):
        var = '{0.author.nick}'.format(message) if message.author.nick else '{0.author.name}'.format(message)
        msg = 'Hello {0}'.format(var)
        await bot.send_message(message.channel, msg)
"""
@bot.event
async def on_message2(message):
    if message.content.startswith('!editme'):
        msg = await bot.send_message(message.author, '10')
        await asyncio.sleep(3)
        await bot.edit_message(msg, '40')
"""
@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together"""
    await bot.say(left + right)

@bot.command()
async def repeat(times : int, content = 'repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)

@bot.command()
async def roll(dice : str):
    """Rolls dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command()
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

@bot.group(pass_context=True)
async def poll(ctx):
    """Poll function group"""
    global asker
    await bot.say('Poll goes here')
    if ctx.invoked_subcommand is close:
        print('Gonna close')
    elif ctx.invoked_subcommand is check:
        print('Gonna check')
    elif ctx.invoked_subcommand is start:
        print('Gonna open')
        asker = '{0.author.nick}'.format(ctx.message)
        #global asker = '{0.author.nick}'.format(ctx.message) if ctx.message.author.nick else '{0.author.name}'.format(ctx.message)
    else:
        print('Invalid subcommand')


@poll.command()
async def start(Title : str, *choices : str):
    await bot.say('Poll opened')
    #cntntr = '{0.content}'.format(ctx.message)
    #cmd = ctx.command.clean_params
    await bot.say(asker)
    #await bot.say(list(cmd.values()))

@poll.command()
async def check():
    await bot.say('Checking poll')
    await bot.say(asker)

@poll.command()
async def close():
    await bot.say('Closing poll')
    await bot.say(asker)




#    tst = 'When can people watch a movie?, Mon, Tue, Wed, Thr, Fri, Sat, Sun'
#    tst = list(map(lambda s: s.strip(" "), tst.split(",")))

#    for a in range(len(tst)):
#        print("{0} \t{1}".format(a, tst[a]))

#    print(tst[-1])
#    p = {}
#    p=p.fromkeys(tst[1:], 0)
#    p['Question']=tst[0]


    #await bot.say(ctx.message.)
    #asker = '{0.author.nick}'.format(message) if message.author.nick else '{0.author.name}'.format(message)
    #msg = 'Hey {}, {0.author.nick} has made a poll'.format(message)    
bot.run('MzI1NzE0OTQ2OTE2ODc2Mjg4.DCci9A.zZAe3yu8IxiboUtTAnYYq206XSg')
