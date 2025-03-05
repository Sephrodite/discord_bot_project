
import random
import json


CHAR_FILE = "characters.json"
DEFAULT = "reference.json"

# loads characters from an existing file
def load_characters(CHAR_FILE):
    try:
        with open('characters.json', 'r') as file:
            characters = json.load(file)
            return characters
    except FileNotFoundError:
         return {}
    
# loads defeault statistics from an existing file
def load_default(DEFAULT):
    try:
        with open(DEFAULT, 'r') as file:
            default = json.load(file)
            return default
    except FileNotFoundError:
        print("file not found")
        return

# updates the characters file
def save_characters(characters):
    try:
        with open('characters.json', 'w') as file:
            json.dump(characters, file, indent=4)
    except FileNotFoundError:
        return {}
    
# rolls dice and checks if it's in the checked skills array if the check is successfull and the skill isn't in the array yet.
def roll_default(char_skill, char_skill_name, characters, user_id, char_name):
    
    roll = (random.randint(1, 100))
    # comparse the roll to the skill
    if roll <= char_skill:
        roll= str(roll)
        char_skill = str(char_skill)
        # checks if the skill is in the array, if not, it adds it and saves it.
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
        msg =  char_name + " rolled a " +  roll + " against " + char_skill + "! Check failed"
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
                
                # finds each checked skill in the array of checked skills and finds the matching skill with skill points
                # it performs a roll_up check and then saves the new skill points with the rolled skill
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

                elif char_skill_name in characters[user_id][char_name]["skills"]["social"]:
                    char_skill = int(characters[user_id][char_name]["skills"]["social"][char_skill_name])
                    char_skill = roll_up(char_skill)
                    (characters[user_id][char_name]["skills"]["social"][char_skill_name])=char_skill

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
                    
                # empties out the checked skills arrays for all characters and saves it.
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

# adds the default set of skills to newly created characters and assigns points for customisation
def add_default_skills(user_id, char_name, group, archetype):
    characters = load_characters(CHAR_FILE)
    group = str(group)
    archetype = str(archetype)
    default = load_default(DEFAULT)
    skills = default[group]["skills"]
    job_points = default[group]["job points"]
    characters[user_id][char_name] = {"group": group, "archetype": archetype,"job points": job_points,"personal interest": 120, "skills":skills, "checked skills":[]}
    save_characters(characters)

# adds points to the skills linked to an archetype upon character creation.
def add_archetype_skills(user_id, char_name, group, archetype):
    characters = load_characters(CHAR_FILE)
    group = str(group)
    archetype = str(archetype)
    default = load_default(DEFAULT)

    # checks all skills and their points for the specified archetype and adds them to the current skill points.
    for key in default[archetype]:
        skill_name = key
        skill_points = int(default[archetype][key])
        
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
            
            elif skill_name in characters[user_id][char_name]["skills"]["social"]:
                char_skill = int(characters[user_id][char_name]["skills"]["social"][skill_name]) + skill_points
                (characters[user_id][char_name]["skills"]["social"][skill_name])=char_skill
                
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

# assigns 30 skill points from the skill point reserve of a character to a set of chosen skills
def quick_assign(user_id, char_name, skills):
    characters = load_characters(CHAR_FILE)
    point_job = int(characters[user_id][char_name]["job points"]) 
    point_pers = int(characters[user_id][char_name]["personal interest"])
    point_total = point_job + point_pers
    skill_amount = len(skills)*30
    
    # checks if there are enough available points to assign
    if point_total >= skill_amount:
        for x in range(len(skills)) :
            char_skill_name = str(skills[x])

            # removes the needed points from the point reserves
            if   point_job >= 30:
                point_job = point_job - 30
                (characters[user_id][char_name]["job points"])=point_job
                save_characters(characters)
            elif point_pers >= 30:
                point_pers = point_pers - 30
                (characters[user_id][char_name]["personal interest"])=point_pers
                save_characters(characters)

            # adds skills to the skill, if and elifs used to find the existing skill in the list
            if char_skill_name in characters[user_id][char_name]["skills"]:
                char_skill = int(characters[user_id][char_name]["skills"][char_skill_name])
                char_skill = char_skill + 30
                (characters[user_id][char_name]["skills"][char_skill_name])=char_skill

            elif char_skill_name in characters[user_id][char_name]["skills"]["job specialties"]:
                char_skill = int(characters[user_id][char_name]["skills"]["job specialties"][char_skill_name])
                char_skill = char_skill + 30
                (characters[user_id][char_name]["skills"]["job specialties"][char_skill_name])=char_skill

            elif char_skill_name in characters[user_id][char_name]["skills"]["combat"]:
                char_skill = int(characters[user_id][char_name]["skills"]["combat"][char_skill_name])
                char_skill = char_skill + 30
                (characters[user_id][char_name]["skills"]["combat"][char_skill_name])=char_skill

            elif char_skill_name in characters[user_id][char_name]["skills"]["social"]:
                char_skill = int(characters[user_id][char_name]["skills"]["social"][char_skill_name])
                char_skill = char_skill + 30
                (characters[user_id][char_name]["skills"]["social"][char_skill_name])=char_skill

            elif char_skill_name in characters[user_id][char_name]["skills"]["classes"]:
                char_skill = int(characters[user_id][char_name]["skills"]["classes"][char_skill_name])
                char_skill = char_skill + 30
                (characters[user_id][char_name]["skills"]["classes"][char_skill_name])=char_skill

            elif char_skill_name in characters[user_id][char_name]["skills"]["sports"]:
                char_skill = int(characters[user_id][char_name]["skills"]["sports"][char_skill_name])
                char_skill = char_skill + 30
                (characters[user_id][char_name]["skills"]["sports"][char_skill_name])=char_skill

            elif char_skill_name in characters[user_id][char_name]["skills"]["arts and crafts"]:
                char_skill = int(characters[user_id][char_name]["skills"]["arts and crafts"][char_skill_name])
                char_skill = char_skill + 30
                (characters[user_id][char_name]["skills"]["arts and crafts"][char_skill_name])=char_skill

            elif char_skill_name in characters[user_id][char_name]["skills"]["language"]:
                char_skill = int(characters[user_id][char_name]["skills"]["language"][char_skill_name])
                char_skill = char_skill + 30
                (characters[user_id][char_name]["skills"]["language"][char_skill_name])=char_skill

            elif char_skill_name in characters[user_id][char_name]["skills"]["special"]:
                char_skill = int(characters[user_id][char_name]["skills"]["special"][char_skill_name])
                char_skill = char_skill + 30
                (characters[user_id][char_name]["skills"]["special"][char_skill_name])=char_skill
        save_characters(characters)
        msg = "Skills for " + char_name + " successfully assigned!\nYou have " + str(point_job) + " left for your profession and " + str(point_pers) + " for personal interests."
        return msg
    else:
        msg = "Not enough points left! Please enter fewer skills to assign points to.\nYou have " + str(point_job) + " left for your profession and " + str(point_pers) + " for personal interests."
    return msg

# assigns a chosen number of skill points to a single skill of choice
def assign_skill(user_id, char_name, char_skill_name, skill_amount):
    characters = load_characters(CHAR_FILE)
    point_job = int(characters[user_id][char_name]["job points"]) 
    point_pers = int(characters[user_id][char_name]["personal interest"])
    point_total = point_job + point_pers
        
    # checks if the points to be added are available
    if point_total >= skill_amount:
        
        # if available, removes them from job points first, otherwise from the personal interest points.
        if   point_job >= skill_amount:
            point_job = point_job - skill_amount
            (characters[user_id][char_name]["job points"])=point_job
            save_characters(characters)
        elif point_pers >= skill_amount:
            point_pers = point_pers - skill_amount
            (characters[user_id][char_name]["personal interest"])=point_pers
            save_characters(characters)
        else: 
            msg = "Not enough points per catagory, please split the skill assign in two.\nYou have " + str(point_job) + " left for your profession and " + str(point_pers) + " for personal interests."

        # finds the appropriate skill in the characters sheet and adds the assigned points to it. 
        if char_skill_name in characters[user_id][char_name]["skills"]:
            char_skill = int(characters[user_id][char_name]["skills"][char_skill_name])
            char_skill = char_skill + skill_amount
            (characters[user_id][char_name]["skills"][char_skill_name])=char_skill

        elif char_skill_name in characters[user_id][char_name]["skills"]["job specialties"]:
            char_skill = int(characters[user_id][char_name]["skills"]["job specialties"][char_skill_name])
            char_skill = char_skill + skill_amount
            (characters[user_id][char_name]["skills"]["job specialties"][char_skill_name])=char_skill

        elif char_skill_name in characters[user_id][char_name]["skills"]["combat"]:
            char_skill = int(characters[user_id][char_name]["skills"]["combat"][char_skill_name])
            char_skill = char_skill + skill_amount
            (characters[user_id][char_name]["skills"]["combat"][char_skill_name])=char_skill

        elif char_skill_name in characters[user_id][char_name]["skills"]["social"]:
            char_skill = int(characters[user_id][char_name]["skills"]["social"][char_skill_name])
            char_skill = char_skill + skill_amount
            (characters[user_id][char_name]["skills"]["social"][char_skill_name])=char_skill

        elif char_skill_name in characters[user_id][char_name]["skills"]["classes"]:
            char_skill = int(characters[user_id][char_name]["skills"]["classes"][char_skill_name])
            char_skill = char_skill + skill_amount
            (characters[user_id][char_name]["skills"]["classes"][char_skill_name])=char_skill

        elif char_skill_name in characters[user_id][char_name]["skills"]["sports"]:
            char_skill = int(characters[user_id][char_name]["skills"]["sports"][char_skill_name])
            char_skill = char_skill + skill_amount
            (characters[user_id][char_name]["skills"]["sports"][char_skill_name])=char_skill

        elif char_skill_name in characters[user_id][char_name]["skills"]["arts and crafts"]:
            char_skill = int(characters[user_id][char_name]["skills"]["arts and crafts"][char_skill_name])
            char_skill = char_skill + skill_amount
            (characters[user_id][char_name]["skills"]["arts and crafts"][char_skill_name])=char_skill

        elif char_skill_name in characters[user_id][char_name]["skills"]["language"]:
            char_skill = int(characters[user_id][char_name]["skills"]["language"][char_skill_name])
            char_skill = char_skill + skill_amount
            (characters[user_id][char_name]["skills"]["language"][char_skill_name])=char_skill

        elif char_skill_name in characters[user_id][char_name]["skills"]["special"]:
            char_skill = int(characters[user_id][char_name]["skills"]["special"][char_skill_name])
            char_skill = char_skill + skill_amount
            (characters[user_id][char_name]["skills"]["special"][char_skill_name])=char_skill
        save_characters(characters)
        msg = "Points successfully assigned to " + char_skill_name + "! Total skill is now: " + str(char_skill) + "\nYou have " + str(point_job) + " left for your profession and " + str(point_pers) + " for personal interests."
        return msg
    else:
        msg = "Not enough points left! Please enter fewer skills to assign points to."
    return msg
    
# adds specific languages to a characters sheet
def add_lang(user_id, char_name, skill_name):
    characters = load_characters(CHAR_FILE)
    # checks if they have the "other" skill still and replaces it's name for the language they wish to add.
    if "other" in (characters[user_id][char_name]["skills"]["language"]):
        characters[user_id][char_name]["skills"]["language"][skill_name]=int(characters[user_id][char_name]["skills"]["language"]["other"])
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

# adds specific art/craft skills to a characters sheet
def add_craft(user_id, char_name, skill_name):
    characters = load_characters(CHAR_FILE)
    # checks if they have the "any" skill still and replaces it's name for the art/craft they wish to add.
    if "any" in (characters[user_id][char_name]["skills"]["arts and crafts"]):
        characters[user_id][char_name]["skills"]["arts and crafts"][skill_name]=int(characters[user_id][char_name]["skills"]["arts and crafts"]["any"])
        del characters[user_id][char_name]["skills"]["arts and crafts"]["any"]
        save_characters(characters)
        msg = "Added " + skill_name + " to " + char_name + "\'s skill list! You can now assign points to it."
        return msg
    # otherwise it adds the art/craft to the list with the standard amount of points.
    else:
        characters[user_id][char_name]["skills"]["arts and crafts"][skill_name]=int(5)
        save_characters(characters)
        msg = "Added " + skill_name + " to " + char_name + "\'s skill list! You can now assign points to it."
        return msg
