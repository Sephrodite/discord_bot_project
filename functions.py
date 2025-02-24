import os
import discord
from discord.ext import commands
import random
import json
import math

CHAR_FILE = "characters.json"

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

def roll_default(char_skill, char_skill_name, characters, user_id, char_name):
    roll = (random.randint(1, 100))
    if roll <= char_skill:
        roll= str(roll)
        char_skill = str(char_skill)
        if char_skill_name  not in characters[user_id][char_name]["checked skills"]:
            (characters[user_id][char_name]["checked skills"]).append(char_skill_name)
            save_characters(characters)
        msg = "You rolled a " +  roll + " against " + char_skill + "! Check successfull"
        return msg
    else:
        roll= str(roll)
        char_skill = str(char_skill)
        msg = "You rolled a " +  roll + " against " + char_skill + "! Check failed"
        return msg