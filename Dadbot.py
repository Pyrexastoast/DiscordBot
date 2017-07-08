import discord
from discord.ext import commands
from collections import deque
import random
import sys
import asyncio

   
description = '''A discord bot made and implemented (so far) by Alex Miranker. This bot was designed for use on very small servers and provides a few basic commands'''


auth_filename = 'auth_token_DadBot.tmp'

if auth_filename == 'auth_token_DadBot.tmp':
    pref = '!'
else:
    pref = '?'

#These lines are how the bot get its Auth token. For security 
#   reasons, the auth tokens aren't kept in this file and are 
#   not tracked on the git repo. Please substitute your own file 
#   or your own token. 
with open(auth_filename, 'r') as auth:
    try:
        token=auth.read().strip()
    except FileNotFoundError:
        print('auth_token file not found')
        raise

bot = commands.Bot(command_prefix=pref, description=description)

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
    r = random.randint(0,1785)
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

#Returns a random joke from the text file of jokes that I have
#   formatted. It splits the joke into lines with the last line
#   being the punchline so that the dadjoke command can handle
#   that line differently
def get_joke():
    r = random.randint(0,114)
    try:
        with open('DadBot_Humor.txt') as jokes:
            for i, line in enumerate(jokes):
                if i==r:
                    jok = list(line.strip().split('_'))
                    return jok
    except FileNotFoundError:
        print('No sense of humor detected')

#Executes this block when the bot is done preparing data recieved
#   from Discord. Usually after login is successful.
@bot.listen()
async def on_ready():
    
    #Prints some information to the command line
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True, hidden=True)
async def greet(ctx):
    await bot.delete_message(ctx.message)
    
    #This is the greeting that the bot says in chat when you log in
    greeting = 'Hello, World!\nPlease use the command \"{0}help\" if you want to know what I can do.\nDon\'t forget to put a \"{0}\" in front of any commands or I won\'t see them!'.format(bot.command_prefix) 

    await bot.say(greeting)

#Executes this block whenever anyone messages the chat.
@bot.listen()
async def on_message(message):
    #Prevents the bot from replying to itself
    if message.author == bot.user:
        return

    #Looks for posts that start with "I am" or "I'm" and flips them around
    #   For example:
    #   If user posts: "I'm hungry"
    #   Bot will post: "Nice to meet you Hungry, I'm Dadbot"
    trigger_Im_Dad = ['I am ', 'i am ', 'I\'m ', 'i\'m ', 'Im ', 'im ']
    for trig in trigger_Im_Dad:
        if message.content.startswith(trig):
            you = message.content.replace(trig, '', 1)
            if len(you.split(' '))<3:
                im_Dad = 'Nice to meet you, {0}. I\'m DadBot'.format(you.title())
                await bot.send_message(message.channel, im_Dad) 
    
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
    
    #Set a limit of 10 repetitions
    if times>10:
        times = 10
    
    #Perform the repetition
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

@bot.command()
async def dadjoke():
    """DadBot tells a joke!
    
    Tells a joke but waits for you to respond before saying the punchline.
    He will say the punchline if no one responds for 8 seconds.
    """
    
    #Gets the joke from the get_joke funtion and checks to see if it
    #   has a punchline. If it does, it separates the punchline from
    #   the main body of the joke.
    joke = get_joke()

    if len(joke)>1:
        punchline = joke.pop()
    msg = '\n'.join(joke)
    
    #Says the joke
    await bot.say(msg)
    
    #If there is a punchline, waits for one second to stop from reacting 
    #   to his own message, then looks for any reply in the discord 
    #   channel. When a reply is detected, or after 8 seconds, the 
    #   punchline gets messaged to the channel.
    if punchline:
        await asyncio.sleep(1)
        response = await bot.wait_for_message(timeout=8)
        if response:
            await bot.say(punchline)
        else:
            await bot.say(punchline)

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


bot.run(token)
