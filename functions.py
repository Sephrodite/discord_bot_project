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

    for category_name, category_value in skills.items():

        if category_name in ["language", "arts and crafts", "sports"]:
            extra_skills = load_json(category_name)

            if isinstance(extra_skills, dict):
                skill_list.extend(str(skill_name) for skill_name in extra_skills.keys())
            elif isinstance(extra_skills, list):
                skill_list.extend(str(skill_name) for skill_name in extra_skills)

        elif isinstance(category_value, dict):
            skill_list.extend(str(skill_name) for skill_name in category_value.keys())

        elif isinstance(category_value, list):
            skill_list.extend(str(skill_name) for skill_name in category_value)

        else:
            skill_list.append(str(category_name))

    return skill_list


def make_skill_list_explained():
    # Load the main/default skills file.
    # This is probably reference.json or whatever DEFAULT points to.
    skills = load_default(DEFAULT)

    # This is the list we will fill and return at the end.
    skill_list = []

    # Loop through the main skills file.
    #
    # If skills looks like this:
    #
    # {
    #     "combat": {...},
    #     "magical": {...},
    #     "language": "language.json"
    # }
    #
    # then:
    # - category_name is "combat", then "magical", then "language"
    # - category_value is whatever is stored under that key
    #
    # This is the same idea as:
    #
    # for i in skills:
    #     category_name = i
    #     category_value = skills[i]
    #
    for category_name, category_value in skills.items():

        # These categories live in their own separate JSON files.
        #
        # So if category_name is "language", we do not use category_value
        # directly. Instead we load the language file with load_json("language").
        if category_name in ["language", "arts and crafts", "sports"]:

            # Load the extra JSON file for this category.
            #
            # Example:
            # - load_json("language")
            # - load_json("arts and crafts")
            # - load_json("sports")
            extra_skills = load_json(category_name)

            # If the extra file is a dictionary, loop through its keys.
            #
            # Example:
            # {
            #     "English": 0,
            #     "Dutch": 0,
            #     "French": 0
            # }
            #
            # In this case, the skill names are the keys:
            # English, Dutch, French
            if isinstance(extra_skills, dict):
                for skill_name in extra_skills:
                    skill_list.append(str(skill_name))

            # If the extra file is a list, loop through the list items.
            #
            # Example:
            # [
            #     "English",
            #     "Dutch",
            #     "French"
            # ]
            #
            # In this case, the skill names are the list items.
            elif isinstance(extra_skills, list):
                for skill_name in extra_skills:
                    skill_list.append(str(skill_name))

        # If this category is already a dictionary in the main file,
        # use the keys as skill names.
        #
        # Example:
        # "combat": {
        #     "brawling": 0,
        #     "dodge": 0
        # }
        #
        # The skill names are:
        # brawling, dodge
        elif isinstance(category_value, dict):
            for skill_name in category_value:
                skill_list.append(str(skill_name))

        # If this category is a list in the main file,
        # use the list items as skill names.
        #
        # Example:
        # "special": [
        #     "luck",
        #     "sixth sense"
        # ]
        elif isinstance(category_value, list):
            for skill_name in category_value:
                skill_list.append(str(skill_name))

        # Fallback:
        # If the category is not a dict or list, we add the category name itself.
        #
        # This prevents the function from crashing if the JSON structure
        # is slightly different than expected.
        else:
            skill_list.append(str(category_name))

    return skill_list