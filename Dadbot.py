import discord
from discord.ext import commands
import random
import sys
import asyncio

description = '''A discord bot made and implemented (so far) by Alex Miranker. This bot was designed for use on very small servers and provides a few basic commands'''

bot = commands.Bot(command_prefix='!', description=description)

def random_emoji():
    r = random.randint(1,1786)
    try:
        with open('emojinumcodes') as f:
            for i, line in enumerate(f):
                if i==r:
                    hxcode = list(map(lambda x: chr(int(x, 16)), line.strip().split(',')))
                    hxcode = ''.join(hxcode)
                    break
    except FileNotFoundError:
        print('emojinumcodes file not found')
    return hxcode

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
        msg = 'Hello {0.author.mention}'.format(message)
        await bot.send_message(message.channel, msg)

@bot.command(pass_context=True, hidden=True)
async def clean(ctx):
    """Deletes the previous 100 bot messages
    
    To be used only during development
    """
    
    def is_me(m):
        return m.author == bot.user

    deleted = await bot.purge_from(ctx.message.channel, limit=100, check=is_me)
    await bot.say('Deleted {} message(s).'.format(len(deleted)))

@bot.command(pass_context=True, hidden=True)
async def firebomb(ctx):
    """Deletes the previous 100 messages
    
    To be used only during development
    """
    deleted = await bot.purge_from(ctx.message.channel, limit=100)
    await bot.say('Deleted {} message(s).'.format(len(deleted)))

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together"""
    await bot.say(left + right)

@bot.command()
async def repeat(times : int, content = 'repeating...'):
    """Repeats a message multiple times.
    
    Will only repeat up to 10 times
    """
    
    if times>10:
        times = 10

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

@bot.command(pass_context=True)
async def msginfo(ctx):
    m1=bot.messages[-1]
    m2=bot.messages[-2]
    m3=bot.messages[-3]
    print('bot.messages[-1] content: {0}'.format(m1.content))
    print('bot.messages[-2] content: {0}'.format(m2.content))
    print('bot.messages[-3] content: {0}'.format(m3.content))

@bot.command(pass_context=True)
async def echo(ctx, txt:str=''):
    a = chr(0x1F487)
    b = chr(0x0200D)
    c = chr(0x02642)
    d = chr(0x0FE0F)
     
    await bot.say(a)
    await bot.say(''.join((a,b)))
    await bot.say(''.join((a,b,c)))
    await bot.say(''.join((a,b,c,d)))

@bot.command(pass_context=True)
async def rreact(ctx):
    target = bot.messages[-2]
    await bot.delete_message(bot.messages[-1])
    await bot.add_reaction(target, random_emoji())
    await bot.add_reaction(target, random_emoji())

@bot.command(pass_context=True)
async def specreact(ctx, emoj:str):
    target = bot.messages[-2]
    await bot.delete_message(bot.messages[-1])
    await bot.add_reaction(target, emoj)

@bot.command()
async def remoji():
    rem = list()
    for i in range(5):
        rem.append(random_emoji())
    await bot.say(rem)

@bot.command(pass_context=True)
async def poll(ctx, *polargs : str):
    """Makes a poll in the current chat.

    Enter your question, followed by the different choices.
    Separate the question and all the options with commas.
    """
    asker = '{0.author.nick}'.format(ctx.message) if ctx.message.author.nick else '{0.author.name}'.format(ctx.message)
    tmp = ' '.join(polargs)
    arg = list(map(lambda s: s.strip(" "), tmp.split(",")))
    title = arg.pop(0)
    opts = list(arg[0:])
    randemoj = []
    for a in opts:
        randemoj.append(random_emoji())
    print(randemoj) 
    #msg = 'Hey , {0} has made a new poll\n\n{1}'.format(asker, title)
    msg = 'Hey @everyone, {0} has made a new poll\n\n{1}'.format(asker, title)
    print(opts)
    for i,choice in enumerate(opts):
       msg = '\n'.join((msg, '{0}: {1}'.format(randemoj[i], choice)))
    
    m = await bot.say(msg) 
    for e in randemoj:
        await bot.add_reaction(m, e)
    
bot.run('MzI1NzE0OTQ2OTE2ODc2Mjg4.DCci9A.zZAe3yu8IxiboUtTAnYYq206XSg')
