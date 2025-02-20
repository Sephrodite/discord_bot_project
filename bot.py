from dotenv import load_dotenv
load_dotenv()

import os
import discord
from discord.ext import commands
import random
import json

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHAR_FILE = "characters.json"

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
    rolls = []
    total = 0
    for _ in range(dice_number):
        roll = (random.randint(1, dice_type))
        rolls.append(roll)
        total +=roll
    result = ' and a '.join([str(s) for s in rolls])
    await ctx.send(f'You rolled a total of {dice_number} dice, of which the individual rolls were {result}. The total is: {total}')

@bot.command()
async def create(ctx, name: str, group: str, archetype: str):
    try:
        # with open('characters.json', 'r') as file:
        #     characters = json.load(file)
        characters = load_characters(CHAR_FILE)
        user_id = str(ctx.author.id)

        if user_id not in characters:
            characters[user_id] = {}
            
        characters[user_id][name] = {"group": group, "archetype": archetype, "skills":{}}

        await ctx.send(f'Character creation attempted.')

        save_characters(characters)
    except FileNotFoundError:
         return




def load_characters(CHAR_FILE):
    try:
        with open('characters.json', 'r') as file:
            characters = json.load(file)
            return characters
    except FileNotFoundError:
         return {}

def save_characters(characters):
    try:
        with open('characters.json', 'w') as file:
            json.dump(characters, file, indent=4)
    except FileNotFoundError:
        return {}



@bot.command()
async def listchars(ctx):
    characters = load_characters(CHAR_FILE)
    user_id = str(ctx.author.id)

    if user_id in characters:
        for i in characters[user_id]:
            char_name = characters[user_id]
        msg = "### " + "Characters:\n" + "\n".join(char_name)

    await ctx.send(f'{msg}')

@bot.command()
async def charbase(ctx, char_name:str):
    characters = load_characters(CHAR_FILE)
    user_id = str(ctx.author.id)

    if user_id in characters:
        if char_name in characters[user_id]:
                char_group = characters[user_id][char_name]["group"]
                char_arch = characters[user_id][char_name]["archetype"]
        msg = "### " + char_name + "\n" + "Group: " + char_group + "\n" + "Archetype: " + char_arch
    await ctx.send(f'{msg}')

# You could add more commands for showchar, updatechar, delchar, etc.

if TOKEN is None:
	print("ERROR: DISCORD_BOT_TOKEN not found in environment variables")
else:
	bot.run(TOKEN)

