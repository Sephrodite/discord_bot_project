from dotenv import load_dotenv
load_dotenv()

import os
import discord
from discord.ext import commands
from discord import app_commands
import random
import json

from functions import load_characters
from functions import save_characters
from functions import roll_default
from functions import level_up
from functions import add_default_skills
from functions import quick_assign
from functions import assign_skill
from examples import (
    get_example_list_a_values,
    get_example_list_b_values,
    filter_autocomplete_values,
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHAR_FILE = os.getenv("CHAR_FILE", "characters.json")

@bot.event
async def on_ready():
    await bot.tree.sync()
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
async def create(ctx, name: str):
    try:
        characters = load_characters(CHAR_FILE)
        user_id = str(ctx.author.id)
        char_name = name

        if user_id not in characters:
            characters[user_id] = {}
            save_characters(characters)

        if char_name not in characters[user_id]:
            add_default_skills(user_id, char_name)

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
async def skill(ctx, char_name:str, char_skill_name:str):
    characters = load_characters(CHAR_FILE)
    user_id = str(ctx.author.id)
    char_skill_name = char_skill_name.lower()

#Iterates over the entire skill array for a character and sets a message tied to the skill in question.
    if user_id in characters:
        if char_name in characters[user_id]:
            if char_skill_name in characters[user_id][char_name]["skills"]:
                char_skill = int(characters[user_id][char_name]["skills"][char_skill_name])
                msg = roll_default(char_skill, char_skill_name, characters, user_id, char_name)
            elif char_skill_name in characters[user_id][char_name]["skills"]["magical"]:
                char_skill = int(characters[user_id][char_name]["skills"]["magical"][char_skill_name])
                msg = roll_default(char_skill, char_skill_name, characters, user_id, char_name)
            elif char_skill_name in characters[user_id][char_name]["skills"]["combat"]:
                char_skill = int(characters[user_id][char_name]["skills"]["combat"][char_skill_name])
                msg = roll_default(char_skill, char_skill_name, characters, user_id, char_name)
            elif char_skill_name in characters[user_id][char_name]["skills"]["sports"]:
                char_skill = int(characters[user_id][char_name]["skills"]["sports"][char_skill_name])
                msg = roll_default(char_skill, char_skill_name, characters, user_id, char_name)
            elif char_skill_name in characters[user_id][char_name]["skills"]["arts and crafts"]:
                char_skill = int(characters[user_id][char_name]["skills"]["arts and crafts"][char_skill_name])
                msg = roll_default(char_skill, char_skill_name, characters, user_id, char_name)
            elif char_skill_name in characters[user_id][char_name]["skills"]["language"]:
                char_skill = int(characters[user_id][char_name]["skills"]["language"][char_skill_name])
                msg = roll_default(char_skill, char_skill_name, characters, user_id, char_name)
            elif char_skill_name in characters[user_id][char_name]["skills"]["special"]:
                char_skill = int(characters[user_id][char_name]["skills"]["special"][char_skill_name])
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
async def tester(ctx, name: str):
    user_id = str(ctx.author.id)
    char_name = name
    
@bot.command()
async def assign(ctx, char_name: str, char_skill_name: str, amount: int):
    user_id = str(ctx.author.id)

    if char_skill_name.lower() == "wyrdness":
        await ctx.send("You are not allowed to upgrade this skill.")
        return

    try:
        msg = assign_skill(user_id, char_name, char_skill_name, amount)
    except KeyError as error:
        msg = (
            f"Something was not found: `{error}`.\n"
            "Please check that the character name and skill name are spelled exactly as stored."
        )
    except TypeError as error:
        msg = (
            "Something had the wrong data type while assigning the skill.\n"
            f"Technical detail: `{error}`"
        )
    except Exception as error:
        msg = (
            "Something went wrong while assigning the skill.\n"
            f"Technical detail: `{type(error).__name__}: {error}`"
        )

    await ctx.send(msg)

@bot.command()
async def quickassign(ctx, char_name:str, *skills:str):
    user_id = str(ctx.author.id)
    print(skills)
    msg = quick_assign(user_id, char_name, skills)
    await ctx.send(f'{msg}')



@bot.tree.command(name="foo", description="Example slash command with choices and a number.")
@app_commands.describe(
    option="Pick one of the example options.",
    amount="Enter any number."
)
@app_commands.choices(option=[
    app_commands.Choice(name="Alpha", value="alpha"),
    app_commands.Choice(name="Beta", value="beta"),
    app_commands.Choice(name="Charlie", value="charlie"),
    app_commands.Choice(name="Delta", value="delta"),
])
async def foo(
    interaction: discord.Interaction,
    option: app_commands.Choice[str],
    amount: int
):
    await interaction.response.send_message(
        f"You selected option='{option.value}' and amount={amount}."
    )



@bot.tree.command(
    name="bar",
    description="Example command with dynamic autocomplete from two files."
)
@app_commands.describe(
    item_a="Start typing to pick a value from List A.",
    item_b="Start typing to pick a value from List B.",
)
async def bar(
    interaction: discord.Interaction,
    item_a: str,
    item_b: str,
):
    await interaction.response.send_message(
        f"You selected item_a='{item_a}' and item_b='{item_b}'."
    )


@bar.autocomplete("item_a")
async def bar_item_a_autocomplete(
    interaction: discord.Interaction,
    current: str,
):
    values = get_example_list_a_values()
    filtered_values = filter_autocomplete_values(values, current)

    return [
        app_commands.Choice(name=value, value=value)
        for value in filtered_values
    ]


@bar.autocomplete("item_b")
async def bar_item_b_autocomplete(
    interaction: discord.Interaction,
    current: str,
):
    values = get_example_list_b_values()
    filtered_values = filter_autocomplete_values(values, current)

    return [
        app_commands.Choice(name=value, value=value)
        for value in filtered_values
    ]

if TOKEN is None:
	print("ERROR: DISCORD_BOT_TOKEN not found in environment variables")
else:
    print(f"TOKEN value: {repr(TOKEN)}")
    bot.run(TOKEN)




