import os
import discord
from discord.ext import commands
import random
import json
import math

CHAR_FILE = "characters.json"
DEFAULT = "reference.json"

def load_characters(CHAR_FILE):
    try:
        with open('characters.json', 'r') as file:
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
        msg =  char_name + " rolled a " +  roll + " against " + char_skill + "! Check failed"
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

                elif char_skill_name in characters[user_id][char_name]["skills"]["job specialties"]:
                    char_skill = int(characters[user_id][char_name]["skills"]["job specialties"][char_skill_name])
                    char_skill = roll_up(char_skill)
                    (characters[user_id][char_name]["skills"]["job specialties"][char_skill_name])=char_skill

                elif char_skill_name in characters[user_id][char_name]["skills"]["combat"]:
                    char_skill = int(characters[user_id][char_name]["skills"]["combat"][char_skill_name])
                    char_skill = roll_up(char_skill)
                    (characters[user_id][char_name]["skills"]["combat"][char_skill_name])=char_skill

                elif char_skill_name in characters[user_id][char_name]["skills"]["classes"]:
                    char_skill = int(characters[user_id][char_name]["skills"]["classes"][char_skill_name])
                    char_skill = roll_up(char_skill)
                    (characters[user_id][char_name]["skills"]["classes"][char_skill_name])=char_skill

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

def add_default_skills(user_id, char_name, group, archetype):
    characters = load_characters(CHAR_FILE)
    group = str(group)
    archetype = str(archetype)
    default = load_default(DEFAULT)
    skills = default[group]["skills"]
    job_points = default[group]["job points"]
    characters[user_id][char_name] = {"group": group, "archetype": archetype,"job points": job_points,"personal interest": 120, "skills":skills, "checked skills":[]}
    save_characters(characters)

def add_archetype_skills(user_id, char_name, group, archetype):
    characters = load_characters(CHAR_FILE)
    group = str(group)
    archetype = str(archetype)
    default = load_default(DEFAULT)

    for key in default[archetype]:
        skill_name = key
        skill_points = int(default[archetype][key])
        print(skill_name , skill_points)

        if char_name in characters[user_id]:
            if skill_name in characters[user_id][char_name]["skills"]:
                char_skill = int(characters[user_id][char_name]["skills"][skill_name]) + skill_points
                (characters[user_id][char_name]["skills"][skill_name])=char_skill
                
            elif skill_name in characters[user_id][char_name]["skills"]["job specialties"]:
                char_skill = int(characters[user_id][char_name]["skills"]["job specialties"][skill_name]) + skill_points
                (characters[user_id][char_name]["skills"]["job specialties"][skill_name])=char_skill
                
            elif skill_name in characters[user_id][char_name]["skills"]["combat"]:
                char_skill = int(characters[user_id][char_name]["skills"]["combat"][skill_name]) + skill_points
                (characters[user_id][char_name]["skills"]["combat"][skill_name])=char_skill
                
            elif skill_name in characters[user_id][char_name]["skills"]["classes"]:
                char_skill = int(characters[user_id][char_name]["skills"]["classes"][skill_name]) + skill_points
                (characters[user_id][char_name]["skills"]["classes"][skill_name])=char_skill
                
            elif skill_name in characters[user_id][char_name]["skills"]["sports"]:
                char_skill = int(characters[user_id][char_name]["skills"]["sports"][skill_name]) + skill_points
                (characters[user_id][char_name]["skills"]["sports"][skill_name])=char_skill
                
            elif skill_name in characters[user_id][char_name]["skills"]["arts and crafts"]:
                char_skill = int(characters[user_id][char_name]["skills"]["arts and crafts"][skill_name]) + skill_points
                (characters[user_id][char_name]["skills"]["arts and crafts"][skill_name])=char_skill
                
            elif skill_name in characters[user_id][char_name]["skills"]["language"]:
                char_skill = int(characters[user_id][char_name]["skills"]["language"][skill_name]) + skill_points
                (characters[user_id][char_name]["skills"]["language"][skill_name])=char_skill
                
            elif skill_name in characters[user_id][char_name]["skills"]["special"]:
                char_skill = int(characters[user_id][char_name]["skills"]["special"][skill_name]) + skill_points
                (characters[user_id][char_name]["skills"]["special"][skill_name])=char_skill

            save_characters(characters)


def assign_skill():
    return




