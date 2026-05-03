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
    load_characters,
    save_characters,
    load_json,
    load_default,
    save_json,)
from functions import (
    assign_skill,
    make_skill_list,
    roll_default,
    level_up,
    add_default_skills,
    make_char_list,
    skill,
    )
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
        char_skill_name = char_skill_name.lower()
        msg = assign_skill(user_id, char_name, char_skill_name, amount)
    except Exception as error:
        traceback.print_exc()
        msg = (
            "Could not assign that skill.\n"
            "Check that the character name, skill name, and amount are correct.\n"
            f"Error: `{type(error).__name__}: {error}`"
        )

    await ctx.send(msg)



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



@bot.tree.command(
    name="checker",
    description="Example command with dynamic autocomplete from two files."
)
@app_commands.describe(
    char_name="choose your character",
    item_b="choose the applicable skill",
)
async def checker(
    interaction: discord.Interaction,
    char_name: str,
    skill_name: str,
):
    user_id = str(interaction.user.id)
    msg = skill(user_id, char_name, skill_name)
    await interaction.response.send_message(
        f'{msg}'
    )


@checker.autocomplete("char_name")
async def checker_item_a_autocomplete(
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


@checker.autocomplete("skill_name")
async def checker_item_b_autocomplete(
    interaction: discord.Interaction,
    current: str,
):
    values = make_skill_list()
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
