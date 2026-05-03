from dotenv import load_dotenv
load_dotenv()

import os
import discord
from discord.ext import commands
from discord import app_commands
import traceback
import random
import json

from loader import (
    ARTS,
    load_characters,
    save_characters,
    load_json,
    load_default,
    save_json,)
from functions import (
    add_new,
    make_skill_list,
    level_up,
    add_default_skills,
    make_char_list,
    skillz,
    assign_points,
    )
from examples import (
    filter_autocomplete_values,
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHAR_FILE = os.getenv("CHAR_FILE", "characters.json")

@bot.event
# prepares the bot
async def on_ready():
    dev_guild_id = os.getenv("DEV_GUILD_ID")

    if dev_guild_id:
        guild = discord.Object(id=int(dev_guild_id))
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)

        print(f"Synced {len(synced)} slash command(s) to guild {dev_guild_id}.")
    else:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} global slash command(s).")

    print(f"Logged in as {bot.user}")

@bot.command()
# says hello back to the user
async def hello(ctx):
	await ctx.send(f'Hello, {ctx.author.display_name}!')
     
@bot.command()
# rolls dice
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

        # adds the user to the file when creating their first characters.
        if user_id not in characters:
            characters[user_id] = {}
            save_characters(characters)

        # checks if the character to be created already exists.
        if char_name not in characters[user_id]:
            add_default_skills(user_id, char_name)

            await ctx.send(f'Character {name} successfully added to {ctx.author.display_name}\'s character list!')
        else:
            await ctx.send(f'Characters {name} already exists!')

    except FileNotFoundError:
         return

@bot.command()
# generates a list of characters assigned to the user
async def listchars(ctx):
    characters = load_characters(CHAR_FILE)
    user_id = str(ctx.author.id)

    if user_id in characters:
        for i in characters[user_id]:
            char_name = characters[user_id]
        msg = "### " + "Characters:\n" + "\n".join(char_name)

    await ctx.send(f'{msg}')

@bot.command()
# allows the creator of this bot to level up the characters.
async def lvlup(ctx):
    author = (ctx.author.id)
    if author == 298490512128606223:
        level_up()
        await ctx.send(f'Level up successful!')
    else:
        await ctx.send(f'Unauthorised action. Seph will run a level up once a month!')


# --------------------- SKILL ------------------------

@bot.tree.command(
    name="skill",
    description="Rolls a skill check for the chosen character."
)
@app_commands.describe(
    char_name="choose your character",
    skill_name="choose the applicable skill",
)
async def skill(
    interaction: discord.Interaction,
    char_name: str,
    skill_name: str,
):  
    skills = make_skill_list()
    user_id = str(interaction.user.id)
    msg = skillz(user_id, char_name, skill_name)
    await interaction.response.send_message(
        f'{msg}'
    )


@skill.autocomplete("char_name")
async def skill_char_name_autocomplete(
    interaction: discord.Interaction,
    current: str,
):
    user_id = str(interaction.user.id)
    values = make_char_list(user_id)
    filtered_values = filter_autocomplete_values(values, current)

    return [
        app_commands.Choice(name=value, value=value)
        for value in filtered_values
    ]


@skill.autocomplete("skill_name")
async def skill_skill_name_autocomplete(
    interaction: discord.Interaction,
    current: str,
):
    values = make_skill_list()
    filtered_values = filter_autocomplete_values(values, current)

    return [
        app_commands.Choice(name=value, value=value)
        for value in filtered_values
    ]

#------------------------------ ASSIGN POINTS -----------------------------------------

@bot.tree.command(
    name="assign",
    description="Used to assign points to a skill for a character."
)
@app_commands.describe(
    char_name="choose your character",
    skill_name="choose the applicable skill",
    amount="the amount of points to assign"
)
async def assign(
    interaction: discord.Interaction,
    char_name: str,
    skill_name: str,
    amount: int
):
    user_id = str(interaction.user.id)
    msg = assign_points(user_id, char_name, skill_name, amount)
    await interaction.response.send_message(
        f'{msg}'
    )


@assign.autocomplete("char_name")
async def assign_char_name_autocomplete(
    interaction: discord.Interaction,
    current: str,
):
    user_id = str(interaction.user.id)
    values = make_char_list(user_id)
    filtered_values = filter_autocomplete_values(values, current)

    return [
        app_commands.Choice(name=value, value=value)
        for value in filtered_values
    ]


@assign.autocomplete("skill_name")
async def assign_skill_name_autocomplete(
    interaction: discord.Interaction,
    current: str,
):
    values = make_skill_list()
    filtered_values = filter_autocomplete_values(values, current)

    return [
        app_commands.Choice(name=value, value=value)
        for value in filtered_values
    ]

#------------------------------ ADD SKILL -----------------------------------------

@bot.tree.command(
    name="add",
    description="Used to add a skill to a character."
)
@app_commands.describe(
    char_name="choose your character",
    skill_name="describe the applicable skill",
    skill_type="choose the type of skill (language, arts and crafts, or sports)"
)
@app_commands.choices(skill_type=[
    app_commands.Choice(name="Language", value="language"),
    app_commands.Choice(name="Arts and Crafts", value="arts and crafts"),
    app_commands.Choice(name="Sports", value="sports"),
])
async def add(
    interaction: discord.Interaction,
    char_name: str,
    skill_name: str,
    skill_type: str
):
    user_id = str(interaction.user.id)
    msg = add_new(user_id, char_name, skill_name, skill_type)
    await interaction.response.send_message(
        f'{msg}'
    )

@add.autocomplete("char_name")
async def add_new_char_name_autocomplete(
    interaction: discord.Interaction,
    current: str,
):
    user_id = str(interaction.user.id)
    values = make_char_list(user_id)
    filtered_values = filter_autocomplete_values(values, current)

    return [
        app_commands.Choice(name=value, value=value)
        for value in filtered_values
    ]


#------------------------------ RUN THE BOT -----------------------------------------


if TOKEN is None:
	print("ERROR: DISCORD_BOT_TOKEN not found in environment variables")
else:
    print(f"TOKEN value: {repr(TOKEN)}")
    bot.run(TOKEN)
