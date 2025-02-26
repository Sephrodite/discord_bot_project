from dotenv import load_dotenv
load_dotenv()

import os
import discord
from discord.ext import commands
import random
import json

from functions import load_characters
from functions import save_characters
from functions import roll_default
from functions import level_up
from info import info_arche
from functions import add_default_skills
from functions import add_archetype_skills

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
        characters = load_characters(CHAR_FILE)
        user_id = str(ctx.author.id)
        char_name = name

        if user_id not in characters:
            characters[user_id] = {}
            
            add_default_skills(user_id, char_name, group, archetype)
            add_archetype_skills(user_id, char_name, group, archetype)

            await ctx.send(f'Character {name} successfully added to {ctx.author.display_name}\'s character list!')
        else:
            await ctx.send(f'Characters {name} already exists!')

    except FileNotFoundError:
         return

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

@bot.command()
async def skill(ctx, char_name:str, char_skill:str):
    characters = load_characters(CHAR_FILE)
    user_id = str(ctx.author.id)
    char_skill_name = char_skill

    if user_id in characters:
        if char_name in characters[user_id]:
            if char_skill in characters[user_id][char_name]["skills"]:
                char_skill = int(characters[user_id][char_name]["skills"][char_skill])
                msg = roll_default(char_skill, char_skill_name, characters, user_id, char_name)
            elif char_skill in characters[user_id][char_name]["skills"]["job specialties"]:
                char_skill = int(characters[user_id][char_name]["skills"]["job specialties"][char_skill])
                msg = roll_default(char_skill, char_skill_name, characters, user_id, char_name)
            elif char_skill in characters[user_id][char_name]["skills"]["combat"]:
                char_skill = int(characters[user_id][char_name]["skills"]["combat"][char_skill])
                msg = roll_default(char_skill, char_skill_name, characters, user_id, char_name)
            elif char_skill in characters[user_id][char_name]["skills"]["classes"]:
                char_skill = int(characters[user_id][char_name]["skills"]["classes"][char_skill])
                msg = roll_default(char_skill, char_skill_name, characters, user_id, char_name)
            elif char_skill in characters[user_id][char_name]["skills"]["sports"]:
                char_skill = int(characters[user_id][char_name]["skills"]["sports"][char_skill])
                msg = roll_default(char_skill, char_skill_name, characters, user_id, char_name)
            elif char_skill in characters[user_id][char_name]["skills"]["arts and crafts"]:
                char_skill = int(characters[user_id][char_name]["skills"]["arts and crafts"][char_skill])
                msg = roll_default(char_skill, char_skill_name, characters, user_id, char_name)
            elif char_skill in characters[user_id][char_name]["skills"]["language"]:
                char_skill = int(characters[user_id][char_name]["skills"]["language"][char_skill])
                msg = roll_default(char_skill, char_skill_name, characters, user_id, char_name)
            elif char_skill in characters[user_id][char_name]["skills"]["special"]:
                char_skill = int(characters[user_id][char_name]["skills"]["special"][char_skill])
                msg = roll_default(char_skill, char_skill_name, characters, user_id, char_name)
            else:
                msg = "Your characters doesn't have this skill listed yet! Please use the [!add WIP] command to add the skill!"
        else:
            msg = "Please create this character to roll skills for them! You can check your character list with the !listchars command. Please check the spelling to make sure your character can be found by me!"
    else:
        msg= "Please create your first character to participate in skill checks!"
    await ctx.send(f'{msg}')
# You could add more commands for showchar, updatechar, delchar, etc.

@bot.command()
async def lvlup(ctx):
    author = (ctx.author.id)
    if author == 298490512128606223:
        level_up()
        await ctx.send(f'Level up successful!')
    else:
        await ctx.send(f'Unauthorised action. Seph will run a level up once a month!')
        
@bot.command()
async def infoarchetype(ctx, archetype:str):
    if archetype == "info":
        msg = "These are the various archetypes to choose from. They have 100 skill points divided between the associated skills. Some have more associated skills but they have less points per skill compared to those that are already more specialised.\n\nList of available archetypes: \n- adventurer \n- beefcake \n- bon vivant \n- cold blooded \n- dreamer \n- egghead \n- explorer \n- le fatale \n- grease monkey \n- hard boiled \n- harlequin \n- hunter \n- mystic \n- outsider \n- rogue \n- scholar \n- seeker \n- sidekick \n- steadfast \n- swashbuckler \n- thrill seeker \n- two fisted"
    else:
        msg = info_arche(archetype)
    await ctx.send(f'{msg}')

@bot.command()
async def tester(ctx, name: str, group: str, archetype: str):
    user_id = str(ctx.author.id)
    char_name = name
    
@bot.command()
async def assign(ctx):
     await ctx.send(f'in progress')



if TOKEN is None:
	print("ERROR: DISCORD_BOT_TOKEN not found in environment variables")
else:
	bot.run(TOKEN)

