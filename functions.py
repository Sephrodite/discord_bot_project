import os
import random
import json
import traceback
import math

from loader import (
    load_characters,
    save_characters,
    load_json,
    load_default,
    save_json,)

CHAR_FILE = os.getenv("CHAR_FILE", "characters.json")
DEFAULT = os.getenv("REFERENCE_FILE", "reference.json")
LANGUAGES = os.getenv("LANGUAGES", "languages.json")
SPORTS = os.getenv("SPORTS", "sports.json")
ARTS = os.getenv("ARTS", "arts.json")
    
# rolls dice and checks if it's in the checked skills array if the check is successfull and the skill isn't in the array yet.
def roll_default(char_skill, char_skill_name, characters, user_id, char_name):
    
    roll = (random.randint(1, 100))
    # comparse the roll to the skill
    if roll <= char_skill:
        roll= str(roll)
        char_skill = str(char_skill)
        if char_skill_name not in characters[user_id][char_name]["checked skills"]:
            (characters[user_id][char_name]["checked skills"]).append(char_skill_name)
            save_characters(characters)
        # returns a message that notifies the user that their check succeeded
        msg = char_name + " rolled a " +  roll + " against " + char_skill + "! Check successfull"
        return msg
    else:
        # returns a message that notifies the user on discord that their check failed. 
        roll= str(roll)
        char_skill = str(char_skill)
        msg =  char_name + " rolled a " +  roll + " against your skill level of " + char_skill + "! Check/action failed."
        return msg

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
        (characters[user_id][char_name])["checked skills"]=[]
        save_characters(characters)
                        
# rolls a skill check, and adds 1d10 to the skill if it failed, which is sent back to be saved
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
        if char_skill_name in characters[user_id][char_name]["skills"]:
            char_skill = int(characters[user_id][char_name]["skills"][char_skill_name])
            char_skill = char_skill + amount
            (characters[user_id][char_name]["skills"][char_skill_name])=char_skill
            points = points - amount
            (characters[user_id][char_name]["points"])=points
        elif char_skill_name in characters[user_id][char_name]["skills"]["magical"]:
            char_skill = int(characters[user_id][char_name]["skills"]["magical"][char_skill_name])
            char_skill = char_skill + amount
            (characters[user_id][char_name]["skills"]["magical"][char_skill_name])=char_skill
            points = points - amount
            (characters[user_id][char_name]["points"])=points
        elif char_skill_name in characters[user_id][char_name]["skills"]["combat"]:
            char_skill = int(characters[user_id][char_name]["skills"]["combat"][char_skill_name])
            char_skill = char_skill + amount
            (characters[user_id][char_name]["skills"]["combat"][char_skill_name])=char_skill
            points = points - amount
            (characters[user_id][char_name]["points"])=points
        elif char_skill_name in characters[user_id][char_name]["skills"]["sports"]:
            char_skill = int(characters[user_id][char_name]["skills"]["sports"][char_skill_name])
            char_skill = char_skill + amount
            (characters[user_id][char_name]["skills"]["sports"][char_skill_name])=char_skill
            points = points - amount
            (characters[user_id][char_name]["points"])=points
        elif char_skill_name in characters[user_id][char_name]["skills"]["arts and crafts"]:
            char_skill = int(characters[user_id][char_name]["skills"]["arts and crafts"][char_skill_name])
            char_skill = char_skill + amount
            (characters[user_id][char_name]["skills"]["arts and crafts"][char_skill_name])=char_skill
            points = points - amount
            (characters[user_id][char_name]["points"])=points
        elif char_skill_name in characters[user_id][char_name]["skills"]["language"]:
            char_skill = int(characters[user_id][char_name]["skills"]["language"][char_skill_name])
            char_skill = char_skill + amount
            (characters[user_id][char_name]["skills"]["language"][char_skill_name])=char_skill
            points = points - amount
            (characters[user_id][char_name]["points"])=points
        elif char_skill_name in characters[user_id][char_name]["skills"]["special"]:
            char_skill = int(characters[user_id][char_name]["skills"]["special"][char_skill_name])
            char_skill = char_skill + amount
            (characters[user_id][char_name]["skills"]["special"][char_skill_name])=char_skill
            points = points - amount
            (characters[user_id][char_name]["points"])=points
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
    
# adds specific languages to a characters sheet
def add_lang(user_id, char_name, skill_name):
    characters = load_characters(CHAR_FILE)
    # checks if they have the "other" skill still and replaces it's name for the language they wish to add and then refunds any points that were assigned to other. This is because the "other" skill is a placeholder for any language the user wishes to add, and it can be assigned points to be used for the language before it's added to the character sheet.
    if "other" in (characters[user_id][char_name]["skills"]["language"]):
        characters[user_id][char_name]["points"]=int(characters[user_id][char_name]["skills"]["language"]["other"])
        del characters[user_id][char_name]["skills"]["language"]["other"]
        save_characters(characters)
        msg = "Added " + skill_name + " to " + char_name + "\'s skill list! You can now assign points to it."
        return msg
    # otherwise it adds the language to the list with the standard amount of points. 
    else:
        characters[user_id][char_name]["skills"]["language"][skill_name]=int(1)
        save_characters(characters)
        msg = "Added " + skill_name + " to " + char_name + "\'s skill list! You can now assign points to it."
        return msg

# adds specific languages to a characters sheet
def add_art(user_id, char_name, skill_name):
    characters = load_characters(CHAR_FILE)
    # checks if they have the "any" skill still and replaces it's name for the art/craft they wish to add and then refunds any points that were assigned to other. This is because the "other" skill is a placeholder for any language the user wishes to add, and it can be assigned points to be used for the language before it's added to the character sheet.
    if "any" in (characters[user_id][char_name]["skills"]["arts and crafts"]):
        characters[user_id][char_name]["points"]=int(characters[user_id][char_name]["skills"]["arts and crafts"]["any"])
        del characters[user_id][char_name]["skills"]["arts and crafts"]["any"]
        save_characters(characters)
        msg = "Added " + skill_name + " to " + char_name + "\'s skill list! You can now assign points to it."
        return msg
    # otherwise it adds the language to the list with the standard amount of points. 
    else:
        characters[user_id][char_name]["skills"]["arts and crafts"][skill_name]=int(5)
        save_characters(characters)
        msg = "Added " + skill_name + " to " + char_name + "\'s skill list! You can now assign points to it."
        return msg
    
# adds specific languages to a characters sheet
def add_sport(user_id, char_name, skill_name):
    characters = load_characters(CHAR_FILE)
    #adds whatever sport the user wants to add to the character sheet with the standard amount of points.
    characters[user_id][char_name]["skills"]["sports"][skill_name]=int(10)
    save_characters(characters)
    msg = "Added " + skill_name + " to " + char_name + "\'s skill list! You can now assign points to it."
    return msg

def add_new(user_id, char_name, skill_name, skill_type):
    match(skill_type):
        case "language":
            languages = load_json(LANGUAGES)
            if skill_name in languages:
                pass
            else:
                languages.append(skill_name)
                save_json(languages, LANGUAGES)
            return add_lang(user_id, char_name, skill_name)
        case "arts and crafts":
            arts = load_json(ARTS)
            if skill_name in arts:
                pass
            else:
                arts.append(skill_name)
                save_json(arts, ARTS)
            return add_art(user_id, char_name, skill_name)
        case "sports":
            sports = load_json(SPORTS)
            if skill_name in sports:
                pass
            else:
                sports.append(skill_name)
                save_json(sports, SPORTS)
            return add_sport(user_id, char_name, skill_name)
        
def make_char_list(user_id):
    characters = load_characters(CHAR_FILE)
    char_list = []
    for char_name in characters[user_id]:
        char_list.append(char_name)
    return char_list

def make_skill_list():
    skills = load_default(DEFAULT)
    skill_list = []
    for i in skills:
        skill_name = skills[i]
        if i == "special" or i == "combat" or i == "magical":
            for x in skills[i]:
                skill_name = skills[i][x]
                skill_list.append(skill_name)
        elif i == "language" or i == "arts and crafts" or i == "sports":
            load_json(i)
            for x in load_json(i):
                skill_name = i[x]
                skill_list.append(skill_name)
        else:
            skill_list.append(skill_name)
    return skill_list