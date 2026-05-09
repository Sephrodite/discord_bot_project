import os
import discord
from discord.ext import commands
from discord import app_commands
import traceback
import random
import json

from loader import load_characters, save_characters

CHAR_FILE = os.getenv("CHAR_FILE", "characters.json")

def fixpoints(char_name, points):
    # this function is used to fix the points of a character in case of bugs.
    characters = load_characters(CHAR_FILE)
    for a in characters:
        user_id = a
        for i in characters[user_id]:
            character_name = i
            if character_name == char_name:
                characters[user_id][character_name]["points"]=int(points) + int(characters[user_id][character_name]["points"])
                save_characters(characters)
                points = str(points)
                msg = "Points for " + char_name + " have been set to " + points + "."
                return msg