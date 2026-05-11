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
                characters[user_id][character_name]["points"]=(int(points) + int(characters[user_id][character_name]["points"]))
                save_characters(characters)
                points = str(characters[user_id][character_name]["points"])
                msg = "Points for " + char_name + " have been set to " + points + "."
                return msg

def addwyrd(char_name, points):
    # this function is used to fix the wyrdness of a character in case of bugs.
    characters = load_characters(CHAR_FILE)
    for a in characters:
        user_id = a
        for i in characters[user_id]:
            character_name = i
            if character_name == char_name:
                characters[user_id][character_name]["skills"]["wyrdness"]=(int(points) + int(characters[user_id][character_name]["skills"]["wyrdness"]))
                save_characters(characters)
                points = str(characters[user_id][character_name]["skills"]["wyrdness"])
                msg = "Wyrdness for " + char_name + " has been set to " + points + "."
                return msg

# rolls a skill check, and adds 1d10 to the skill if it failed, which is sent back to be saved
def roll_up(char_skill):
    char_skill = int(char_skill)
    roll = (random.randint(1, 100))
    if roll > char_skill:
        up_roll = (random.randint(1,10))
        char_skill = char_skill + up_roll
    return int(char_skill)
            
# function for levelling up all characters
def level_up():
    characters = load_characters(CHAR_FILE)
    # the various nested for statements check users, their characters, and the checked skills for their characters.
    for a in characters:
        user_id = a
        for i in characters[user_id]:
            char_name = i
            for x in range(len(characters[user_id][char_name]["checked skills"])) :
                char_skill_name = characters[user_id][char_name]["checked skills"][x]
                print(char_skill_name)  
                try:
                    if char_skill_name in characters[user_id][char_name]["skills"]:
                        char_skill = int(characters[user_id][char_name]["skills"][char_skill_name])
                        char_skill = roll_up(char_skill)
                        (characters[user_id][char_name]["skills"][char_skill_name])=char_skill

                    elif char_skill_name in characters[user_id][char_name]["skills"]["magical"]:
                        char_skill = int(characters[user_id][char_name]["skills"]["magical"][char_skill_name])
                        char_skill = roll_up(char_skill)
                        (characters[user_id][char_name]["skills"]["magical"][char_skill_name])=char_skill

                    elif char_skill_name in characters[user_id][char_name]["skills"]["combat"]:
                        char_skill = int(characters[user_id][char_name]["skills"]["combat"][char_skill_name])
                        char_skill = roll_up(char_skill)
                        (characters[user_id][char_name]["skills"]["combat"][char_skill_name])=char_skill

                    elif char_skill_name in characters[user_id][char_name]["skills"]["sports"]:
                        char_skill = int(characters[user_id][char_name]["skills"]["sports"][char_skill_name])
                        char_skill = roll_up(char_skill)
                        (characters[user_id][char_name]["skills"]["sports"][char_skill_name])=char_skill

                    elif char_skill_name in characters[user_id][char_name]["skills"]["arts and crafts"]:
                        char_skill = int(characters[user_id][char_name]["skills"]["arts and crafts"][char_skill_name])
                        char_skill = roll_up(char_skill)
                        (characters[user_id][char_name]["skills"]["arts and crafts"][char_skill_name])=char_skill

                    elif char_skill_name in characters[user_id][char_name]["skills"]["language"]:
                        char_skill = int(characters[user_id][char_name]["skills"]["language"][char_skill_name])
                        char_skill = roll_up(char_skill)
                        (characters[user_id][char_name]["skills"]["language"][char_skill_name])=char_skill

                    elif char_skill_name in characters[user_id][char_name]["skills"]["special"]:
                        char_skill = int(characters[user_id][char_name]["skills"]["special"][char_skill_name])
                        char_skill = roll_up(char_skill)
                        (characters[user_id][char_name]["skills"]["special"][char_skill_name])=char_skill
                    
                    
                except Exception as error:
                    traceback.print_exc()
                    msg = (
                        "Could not assign that skill.\n"
                        "Check that the character name, skill name, and amount are correct.\n"
                        f"Error: `{type(error).__name__}: {error}`"
                    )
                    return msg
        (characters[user_id][char_name])["checked skills"]=[]
        save_characters(characters)