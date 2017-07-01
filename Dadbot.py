import discord
from discord.ext import commands
from collections import deque
import random
import sys
import asyncio

DadBot_token = 'MzMwNTEzNjY3MjczNjU0Mjcy.DDiGew.hzz0ArO4yDqpHtqAGcFJj0Q2S-c'
testbot_token = 'MzI1NzE0OTQ2OTE2ODc2Mjg4.DCci9A.zZAe3yu8IxiboUtTAnYYq206XSg'

description = '''A discord bot made and implemented (so far) by Alex Miranker. This bot was designed for use on very small servers and provides a few basic commands'''

bot = commands.Bot(command_prefix='!', description=description)

#Only takes Message.author as argument. Will return
#   their nickname on that server if they have one.
#   If not, it will return their username.
def handle_nick(person):
    display_name = '{0}'.format(person.nick) if person.nick else '{0}'.format(person.name)
    return display_name

#Returns a random emoji that is guaranteed to be supported
#   across discords different apps and can be used as a reaction.
#   (probably)
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
    greeting = 'Hello, World!\nPlease use the command \"{0}help\" if you want to know what I can do.\nDon\'t forget to put a \"{0}\" in front of any commands or I won\'t see them!'.format(bot.command_prefix) 
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    for serv in bot.servers:
        print("Now messaging:\t", serv.name)
        await bot.send_message(serv.default_channel, greeting)

@bot.listen()
async def on_message(message):
    #Prevents the bot from replying to itself
    if message.author == bot.user:
        return
    
    #Looks for posts that start with "I am" or "I'm" and flips them around
    #   For example:
    #   If user posts: "I'm hungry"
    #   Bot will post: "Nice to meet you Hungry, I'm Dadbot"
    #   This needs neatening into one if statement.
    if message.content.startswith('I am ') or message.content.startswith('i am '):
        obj = message.content[5:]
        dadjk = 'Nice to meet you, {0}. I\'m DadBot'.format(obj.title())
        await bot.send_message(message.channel, dadjk)
    if message.content.startswith('I\'m ') or message.content.startswith('i\'m '):
        obj = message.content[4:]
        dadjk = 'Nice to meet you, {0}. I\'m DadBot'.format(obj.title())
        await bot.send_message(message.channel, dadjk)
    if message.content.startswith('Im ') or message.content.startswith('im '):
        obj = message.content[3:]
        dadjk = 'Nice to meet you, {0}. I\'m DadBot'.format(obj.title())
        await bot.send_message(message.channel, dadjk)
    
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
async def poll(ctx, *polargs : str):
    """Makes a poll in the current chat.

    Enter your question, followed by the different choices.
    Separate the question and all the options with commas.

    If you enter no choices, Dadbot will default to a scheduling
    poll and use pre-formatted days of the week.
    """
    
    #Uncommenting this line will tell the bot to delete the 
    #   message that invokes this command
    #await bot.delete_message(ctx.message)      
    
    #Creates 'asker' using handle_nick(). It is the author's nickname 
    #   if they have one. Otherwise, 'asker' is set to their name.
    asker = handle_nick(ctx.message.author)
    arg = deque(map(lambda s: s.strip(" "), ' '.join(polargs).split(",")))  #Separate the argument by commas
    title = arg.popleft()           #Parse the question from the options
    
    #This segment handles a default case if no options are given.
    #   in this scenario, week is set to True and the default
    #   days of the week are used as options for the poll
    week = False if arg else True    
    day = ctx.message.timestamp.strftime('%A')      #Get the day of the week from the message timestamp
    if week:        #Executes if no options are given. Uses default week day options 
        opts = deque(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        while day!=opts[-1]:    #Cycle the order until the current day is last
            opts.rotate(1)               
        opts[0] = 'Tomorrow'    #Change the first day to 'Tomorrow'
    else:           #Executes if options are given. Uses given options instead of defaults
        opts = deque(arg)
    
    #Create a list of random emojis for every options
    randemoj = []
    for a in opts:
        randemoj.append(random_emoji())
     
    #Creates the message that the bot will post to the channel. The header
    #   mentions everyone and then asks the given question. Then each option 
    #   is formatted and appended to the message after a new line. As a tool 
    #   for developing, the commented line will remove the @everyone mention 
    #   
    msg = 'Hey @everyone, {0} has made a new poll\n\n{1}'.format(asker, title)
    #msg = 'Hey , {0} has made a new poll\n\n{1}'.format(asker, title)
    for i,choice in enumerate(opts):
       msg = '\n'.join((msg, '{0}: {1}'.format(randemoj[i], choice)))
    
    #Sends the message to the chat. The bot.say() method returns the 
    #   message object that the bot published. Assigning it to a variable 
    #   here and referencing it in the line below prevents the bot from 
    #   adding a reaction to the wrong message.
    m = await bot.say(msg) 
    
    #Adds each of the random emojis chosen above as a reaction to the poll
    #   so that people don't have to find the specific emojis themselves
    for e in randemoj:
        await bot.add_reaction(m, e)
    
#bot.run(testbot_token)
bot.run(DadBot_token)
