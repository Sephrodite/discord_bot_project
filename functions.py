import os
import discord
from discord.ext import commands
import random
import json
import math

CHAR_FILE = os.getenv("CHAR_FILE", "characters.json")
DEFAULT = os.getenv("REFERENCE_FILE", "reference.json")

def load_characters(char_file=CHAR_FILE):
    try:
        with open(char_file, "r", encoding="utf-8") as file:
            characters = json.load(file)
            return characters
    except FileNotFoundError:
        return {}
    
def load_default(DEFAULT):
    try:
        with open(DEFAULT, 'r') as file:
            default = json.load(file)
            return default
    except FileNotFoundError:
        print("file not found")
        return

def save_characters(characters, char_file=CHAR_FILE):
    with open(char_file, "w", encoding="utf-8") as file:
        json.dump(characters, file, indent=4)
    
def roll_default(char_skill, char_skill_name, characters, user_id, char_name):
    
    roll = (random.randint(1, 100))
    if roll <= char_skill:
        roll= str(roll)
        char_skill = str(char_skill)
        if char_skill_name not in characters[user_id][char_name]["checked skills"]:
            (characters[user_id][char_name]["checked skills"]).append(char_skill_name)
            save_characters(characters)
        msg = "You rolled a " +  roll + " against " + char_skill + "! Check successfull"
        return msg
    else:
        roll= str(roll)
        char_skill = str(char_skill)
        msg =  char_name + " rolled a " +  roll + " against your skill level of " + char_skill + "! Check/action failed."
        return msg

def level_up():
    characters = load_characters(CHAR_FILE)
    for a in characters:
        user_id = a
        for i in characters[user_id]:
            char_name = i
            for x in range(len(characters[user_id][char_name]["checked skills"])) :
                char_skill_name = characters[user_id][char_name]["checked skills"][x]
                print(char_skill_name)  

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
                    
                (characters[user_id][char_name])["checked skills"]=[]
                save_characters(characters)
                    
def roll_up(char_skill):
    char_skill = int(char_skill)
    roll = (random.randint(1, 100))
    if roll > char_skill:
        up_roll = (random.randint(1,10))
        char_skill = char_skill + up_roll
    return int(char_skill)

def add_default_skills(user_id, char_name):
    characters = load_characters(CHAR_FILE)
    default = load_default(DEFAULT)
    skills = default["skills"]
    characters[user_id][char_name] = {"points": 320, "skills":skills, "checked skills": []}
    save_characters(characters)

def assign_skill(user_id, char_name, char_skill_name, amount):
    characters = load_characters(CHAR_FILE)
    points = int(characters[user_id][char_name]["points"]) 
    
    if points >= amount:
        points = points - amount
        print(points)
        (characters[user_id][char_name]["points"])=points
        save_characters(characters)
        if char_skill_name in characters[user_id][char_name]["skills"]:
            char_skill = int(characters[user_id][char_name]["skills"][char_skill_name])
            char_skill = char_skill + amount
            (characters[user_id][char_name]["skills"][char_skill_name])=char_skill
        elif char_skill_name in characters[user_id][char_name]["skills"]["magical"]:
            char_skill = int(characters[user_id][char_name]["skills"]["magical"][char_skill_name])
            char_skill = char_skill + amount
            (characters[user_id][char_name]["skills"]["magical"][char_skill_name])=char_skill
        elif char_skill_name in characters[user_id][char_name]["skills"]["combat"]:
            char_skill = int(characters[user_id][char_name]["skills"]["combat"][char_skill_name])
            char_skill = char_skill + amount
            (characters[user_id][char_name]["skills"]["combat"][char_skill_name])=char_skill
        elif char_skill_name in characters[user_id][char_name]["skills"]["sports"]:
            char_skill = int(characters[user_id][char_name]["skills"]["sports"][char_skill_name])
            char_skill = char_skill + amount
            (characters[user_id][char_name]["skills"]["sports"][char_skill_name])=char_skill
        elif char_skill_name in characters[user_id][char_name]["skills"]["arts and crafts"]:
            char_skill = int(characters[user_id][char_name]["skills"]["arts and crafts"][char_skill_name])
            char_skill = char_skill + amount
            (characters[user_id][char_name]["skills"]["arts and crafts"][char_skill_name])=char_skill
        elif char_skill_name in characters[user_id][char_name]["skills"]["language"]:
            char_skill = int(characters[user_id][char_name]["skills"]["language"][char_skill_name])
            char_skill = char_skill + amount
            (characters[user_id][char_name]["skills"]["language"][char_skill_name])=char_skill
        elif char_skill_name in characters[user_id][char_name]["skills"]["special"]:
            char_skill = int(characters[user_id][char_name]["skills"]["special"][char_skill_name])
            char_skill = char_skill + amount
            (characters[user_id][char_name]["skills"]["special"][char_skill_name])=char_skill
        save_characters(characters)
        amount = str(amount)
        char_skill_name = str(char_skill_name)
        char_skill = str(char_skill)
        points = str(points)

        msg = "You've succesfully assigned " + amount + " points to " + char_skill_name + ". The total skill is now " + char_skill + " points. You have " + points + " points left to assign."
        return msg
    else:
        msg = "Not enough points left! Please enter fewer points to assign."
    return msg


