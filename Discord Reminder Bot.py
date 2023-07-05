import discord
from discord.ext import commands, tasks
from config import TOKEN
import asyncio
import datetime

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

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

bot.run(TOKEN)
