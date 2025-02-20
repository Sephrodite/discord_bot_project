from dotenv import load_dotenv
load_dotenv()

import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
	print(f'Logged in as {bot.user}')

@bot.command()
async def hello(ctx):
	await ctx.send(f'Hello, {ctx.author.display_name}!')

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if TOKEN is None:
	print("ERROR: DISCORD_BOT_TOKEN not found in environment variables")
else:
	bot.run(TOKEN)