import os
import json
import traceback

CHAR_FILE = os.getenv("CHAR_FILE", "characters.json")
DEFAULT = os.getenv("REFERENCE_FILE", "reference.json")
LANGUAGES = os.getenv("LANGUAGES", "languages.json")
SPORTS = os.getenv("SPORTS", "sports.json")
ARTS = os.getenv("ARTS", "arts.json")
SKILLS = os.getenv("SKILLS", "skill_list.json")

def load_characters(char_file=CHAR_FILE):
    try:
        with open(char_file, "r", encoding="utf-8") as file:
            characters = json.load(file)
            return characters
    except FileNotFoundError:
        return {}

def save_characters(characters, char_file=CHAR_FILE):
    with open(char_file, "w", encoding="utf-8") as file:
        json.dump(characters, file, indent=4)
    
# loads defeault statistics from an existing file
def load_default(DEFAULT):
    try:
        with open(DEFAULT, 'r') as file:
            default = json.load(file)
            return default
    except FileNotFoundError:
        print("file not found")
        return

#loads a default json file, used for loading languages, sports, arts, and skills (in theory)
def load_json(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("file not found")
        return

def save_json(data, file):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

#loads languages from an existing file, since the generic one isn't working for some reason.
def load_languages(languages_file=LANGUAGES):
    try:
        with open(languages_file, 'r', encoding="utf-8") as file:
            languages = json.load(file)
            return languages
    except FileNotFoundError:
        print("file not found")
        return

def save_languages(languages, lang_file=LANGUAGES):
    with open(lang_file, 'w', encoding='utf-8') as f:
        json.dump(languages, f, indent=4)

#loads skills from an existing file, since the generic one isn't working for some reason.
def load_skills(skills_file=SKILLS):
    try:
        with open(skills_file, 'r', encoding="utf-8") as file:
            skills = json.load(file)
            return skills
    except FileNotFoundError:
        print("file not found")
        return
    
def save_skills(skills, skills_file=SKILLS):
    with open(skills_file, 'w', encoding='utf-8') as f:
        json.dump(skills, f, indent=4)

#loads sports from an existing file, since the generic one isn't working for some reason.
def load_sports(sports_file=SPORTS):
    try:
        with open(sports_file, 'r', encoding="utf-8") as file:
            sports = json.load(file)
            return sports
    except FileNotFoundError:
        print("file not found")
        return
    
def save_sports(sports, sports_file=SPORTS):
    with open(sports_file, 'w', encoding='utf-8') as f:
        json.dump(sports, f, indent=4)

#loads arts from an existing file, since the generic one isn't working for some reason.
def load_arts(arts_file=ARTS):
    try:
        with open(arts_file, 'r', encoding="utf-8") as file:
            arts = json.load(file)
            return arts
    except FileNotFoundError:
        print("file not found")
        return

def save_arts(arts, arts_file=ARTS):
    with open(arts_file, 'w', encoding='utf-8') as f:
        json.dump(arts, f, indent=4)