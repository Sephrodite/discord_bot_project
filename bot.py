from dotenv import load_dotenv
load_dotenv()

import os
import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
	print(f'Logged in as {bot.user}')

@bot.command()
async def hello(ctx):
	await ctx.send(f'Hello, {ctx.author.display_name}!')
	
@bot.command()
async def roll(ctx, dice: str):
    try: 
        notation = dice.lower()
        parts = notation.split('d')
        dice_number = int(parts[0])
        dice_type = int(parts[1])
    except Exception as e:
        await ctx.send(f'please enter a valid number')
        return
    total = 0
    for _ in range(dice_number):
        roll = random.randint(1, dice_type)
        total += roll
    await ctx.send(f'You rolled a total of {dice_number} dice, the result per dice should be between 1 and {dice_type}. The total (if more than 1) is: {total}')

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if TOKEN is None:
	print("ERROR: DISCORD_BOT_TOKEN not found in environment variables")
else:
	bot.run(TOKEN)