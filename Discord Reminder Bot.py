import discord
from discord.ext import commands, tasks
from decouple import Config
import asyncio
import datetime

config = Config('botterfly.env')
BOT_TOKEN  = config.get('DISCORD_TOKEN')
BOT_CHANNEL = config.get('DISCORD_CHANNEL')
bot = commands.Bot(command_prefix='!')

# EVENTS
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# COMMANDS

# MAIN
@bot.command()
async def remindme(ctx, duration: int, unit: str, *, reminder: str):
    valid_units = ['seconds', 'minutes', 'hours', 'days']
    
    if unit not in valid_units:
        await ctx.send('Invalid time unit. Please use seconds, minutes, hours, or days.')
        return

    if duration <= 0:
        await ctx.send('Duration must be a positive number.')
        return

    if len(reminder) == 0:
        await ctx.send('Please provide a reminder message.')
        return

    multiplier = 1
    if unit == 'minutes':
        multiplier = 60
    elif unit == 'hours':
        multiplier = 3600
    elif unit == 'days':
        multiplier = 86400

    await ctx.send(f'I will remind you in {duration} {unit}.')

    await asyncio.sleep(duration * multiplier)
    await ctx.send(f'{ctx.author.mention}, here is your reminder: {reminder}')

@remindme.error
async def remindme_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please provide the duration, unit, and reminder message.')
# OTHERS
@bot.command()
async def ping(ctx):    
    message = await ctx.send("Pong!")
    await ctx.message.add_reaction("🏓")
@bot.command()
async def coinflip(ctx):
    result = random.choice(["heads", "tails"])
    await ctx.send(f"The coin landed on **{result}**!")
    coinflip.short_doc = "Flips a coin, landing on either heads or tails"

@bot.command()
async def roll(ctx, sides: float = 6.0):
    try:
        sides = int(sides)
    except ValueError:
        await ctx.send("The number of sides must be an integer.")
        return
    if sides < 2:
        await ctx.send("The dice must have at least 2 sides.")
        return
    result = random.randint(1, sides)
    await ctx.send(f"The dice rolled **{result}**!")
    roll.short_doc = "Roll a dice with the specified number of sides (default is 6)"

bot.run(BOT_TOKEN)
